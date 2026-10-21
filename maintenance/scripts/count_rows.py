import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else '21-Open-Decisions-and-Questions.md'
src = open(path, encoding='utf-8').read()
sev = {'BLOCKER': 0, 'IMPORTANT': 0, 'NICE': 0}
rows = []
for ln in src.split('\n'):
    s = ln.strip()
    if not s.startswith('|'):
        continue
    cells = [c.strip() for c in s.strip('|').split('|')]
    first = cells[0].strip('`').strip()
    m = re.fullmatch(r'((?:OD|ORG)-[A-Za-z0-9\-]+)(?:\s*/\s*(?:OD|ORG)-[A-Za-z0-9\-]+)?', first)
    if not m:
        continue
    last = cells[-1]
    tag = next((t for t in sev if '[' + t + ']' in last), None)
    if tag is None:
        continue
    rows.append(m.group(1))
    sev[tag] += 1

single = [r for r in rows if '/' not in [c.strip() for c in ln.strip('|').split('|')][0]]
print('rows', len(rows), sev, 'sum', sum(sev.values()))
print('OD-only first cells', sum(1 for r in rows if r.startswith('OD-')))
print('ORG-led', sum(1 for r in rows if r.startswith('ORG-')), [r for r in rows if r.startswith('ORG-')])
print('dupes', [r for r in set(rows) if rows.count(r) > 1])
