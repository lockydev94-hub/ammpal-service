"""Validates the asset register against the filesystem and against Docs/.

Run from the project root:  python3 maintenance/scripts/validate_assets.py
Exit code 0 = clean. This is the integrity gate the registers needed before the workspace was a git
repository, and it is still the gate now that it is one (git init, 2026-10-21): git records that a file
changed, this records that the bytes on disk are the export the inventory row describes.
"""
import csv, glob, hashlib, json, os, re, sys

MANIFEST = 'design-assets/manifests/asset-manifest.json'
INVENTORY = 'design-assets/manifests/asset-inventory.csv'
NAME_RE = re.compile(r'^AMM-[A-Z]+(-[A-Z]+)*-[A-Z]+(-[A-Z]+)*-[A-Za-z0-9]+(-\d{2,4}x\d{2,4})?(-\d{2,4})?-v\d{2}\.(svg|png|webp|avif|jpg|json)$')
STATUSES = {'REGISTERED', 'PLANNED', 'GENERATED', 'APPROVED', 'REJECTED', 'SUPERSEDED', 'BLOCKED'}
# Only ALT_REQUIRED rows may carry alt text; the treatment is declared per row, never inferred.
TREATMENTS = {'ALT_REQUIRED', 'DECORATIVE_EMPTY_ALT', 'LABELLED_BY_ADJACENT_TEXT',
              'SOCIAL_META_IMAGE', 'NOT_SHIPPED'}
# Pre-existing reference files live outside design-assets/ and are never renamed or deleted;
# they are governed by their manifest records, not by the naming rule.

errors = []


def err(msg):
    errors.append(msg)


docs_files = {os.path.basename(p): p for p in glob.glob('Docs/*.md')}


def check_doc_ref(ref, where):
    for token in re.findall(r'(\b\d{2}\b|README)(?= sec)', ref):
        if token == 'README':
            if 'README.md' not in docs_files:
                err('%s: cites README which does not exist' % where)
            continue
        hits = [f for f in docs_files if f.startswith(token + '-')]
        if not hits:
            err('%s: doc_ref cites Docs/%s which does not exist' % (where, token))


man = json.load(open(MANIFEST, encoding='utf-8'))
missing_vocab = STATUSES - set(man['status_vocabulary'])
if missing_vocab:
    err('manifest status_vocabulary is missing %s' % ', '.join(sorted(missing_vocab)))

ids_in_inventory = set()
with open(INVENTORY, encoding='utf-8') as fh:
    inv = list(csv.DictReader(fh))
for r in inv:
    ids_in_inventory.add(r['asset_id'])
    if r['generation_status'] not in STATUSES:
        err('inventory %s: unknown status %r' % (r['asset_id'], r['generation_status']))
    if r['generation_status'] == 'BLOCKED' and not re.search(r'OD-[A-Z]+-\d+|OD-\d', r['notes'] + r['doc_ref']):
        err('inventory %s: BLOCKED with no registered OD-* decision cited' % r['asset_id'])
    if r['doc_ref']:
        check_doc_ref(r['doc_ref'], 'inventory %s' % r['asset_id'])
    if r['asset_type'] not in ('screenshot-set', 'infographic'):
        if not NAME_RE.match(r['filename_stem'] + '-v01.svg'):
            err('inventory %s: filename_stem %r does not satisfy the naming rule (uppercase kebab '
                'segments, optional size, version, extension)' % (r['asset_id'], r['filename_stem']))
    treat = r['a11y_treatment']
    if treat not in TREATMENTS:
        err('inventory %s: a11y_treatment %r is not one of the five legal values' % (r['asset_id'], treat))
    if treat == 'ALT_REQUIRED' and not r['alt_text_en']:
        err('inventory %s: declared ALT_REQUIRED but carries no alt text' % r['asset_id'])
    if treat != 'ALT_REQUIRED' and r['alt_text_en']:
        err('inventory %s: declared %s but carries alt text - ship it with an empty alt or '
            'reclassify' % (r['asset_id'], treat))

dupes = {r['asset_id'] for r in inv if [x['asset_id'] for x in inv].count(r['asset_id']) > 1}
for d in dupes:
    err('inventory: duplicate asset_id %s' % d)

seen = set()
for rec in man['records']:
    rid = rec['asset_id']
    seen.add(rid)
    if rid not in ids_in_inventory:
        err('manifest %s: not present in the inventory' % rid)
    if rec['status'] not in STATUSES:
        err('manifest %s: unknown status %r' % (rid, rec['status']))
    path = rec['file']
    if rec['status'] in ('REGISTERED', 'GENERATED', 'APPROVED'):
        if not os.path.exists(path):
            err('manifest %s: file missing on disk: %s' % (rid, path))
            continue
        size = os.path.getsize(path)
        if size != rec['bytes']:
            err('manifest %s: bytes %d recorded, %d on disk' % (rid, rec['bytes'], size))
        digest = hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16]
        if digest != rec['sha256_16']:
            err('manifest %s: sha256 mismatch (%s recorded, %s on disk) - file changed without a new version'
                % (rid, rec['sha256_16'], digest))
        try:
            from PIL import Image
            w, h = Image.open(path).size
            if (w, h) != (rec['width_px'], rec['height_px']):
                err('manifest %s: %dx%d recorded, %dx%d on disk' % (rid, rec['width_px'], rec['height_px'], w, h))
        except ImportError:
            err('manifest %s: PIL unavailable, dimensions NOT verified' % rid)
        ext = os.path.splitext(path)[1].lstrip('.').lower()
        if ext != rec['format']:
            err('manifest %s: format %r but extension .%s' % (rid, rec['format'], ext))

for path in glob.glob('design-assets/**/*', recursive=True):
    if not os.path.isfile(path):
        continue
    if path.startswith('design-assets/manifests/'):
        continue
    base = os.path.basename(path)
    if base.endswith(('.csv', '.json')) and 'manifest' in path:
        continue
    if not NAME_RE.match(base):
        err('file %s does not match the naming rule' % path)
    if base.split('-v')[0] not in ids_in_inventory:
        err('file %s has no asset_id in the inventory (unregistered asset)' % path)

counts = {}
for r in inv:
    counts[r['generation_status']] = counts.get(r['generation_status'], 0) + 1

print('INVENTORY ROWS: %d  %s' % (len(inv), counts))
print('MANIFEST RECORDS: %d' % len(man['records']))
print('ERRORS: %d' % len(errors))
for e in errors:
    print('  - ' + e)
sys.exit(1 if errors else 0)
