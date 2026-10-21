# 32 — Asset Manifest and Export Specification

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-32 |
| Version | 1.4 |
| Status | **PROPOSED — not approved.** The register format is usable now; nothing inside it is approved artwork. |
| Owner | Product Design Lead + Frontend Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `30`, `31`, `34`, `12`, `13`, `16`, `24`, `09`, `35` §6 (the storage-layout half of §6), `37` §7.1 (what a consumer does with a missing asset) |
| Artifacts | `design-assets/manifests/asset-inventory.csv`, `design-assets/manifests/asset-manifest.json`, `gen_asset_inventory.py`, `validate_assets.py` |

---

## 1. Two registers, deliberately separate

| File | Holds | Written by | Read by |
|---|---|---|---|
| `asset-inventory.csv` | **intent** — 93 planned/registered rows, one per asset the documents ask for | `gen_asset_inventory.py` (regenerate, never hand-edit) | `validate_assets.py`, `33`, designers |
| `asset-manifest.json` | **fact** — one record per file that exists on disk, with measured size, measured pixels and a SHA-256 prefix | designer at export time, then verified | `validate_assets.py`, build pipeline |

The split exists because a plan and an inventory drift the moment they share a file: an approved
asset changes state, it does not change intent. **Regenerating the CSV from the script is the only
supported way to change counts** — the same discipline `21` §1 now applies to the decision registry
after three separate mis-counts. `validate_assets.py` prints the row count and status split so a
stale figure cannot survive a single run.

---

## 2. Naming rule

Grammar (enforced by `NAME_RE` in `validate_assets.py`, applied to inventory stems **and** to every
file that lands in `design-assets/`):

```
AMM-<SURFACE>-<ASSET-TYPE>-<SUBJECT>[-<W>x<H> | -<DIM>][-v<NN>].<ext>
```

| Part | Values | Rule |
|---|---|---|
| `SURFACE` | `BRAND · SERVICE · WEB · CUSTOMER · PARTNER · CONTROL · STORE · REFERENCE` | one segment, uppercase |
| `ASSET-TYPE` | `logo · mark · app-icon · favicon · og-image · pattern · hero · category-icon · category-image · illustration · empty-state · success-state · error-state · photo-placeholder · nav-icon · action-icon · map-marker · store-icon · feature-graphic · pwa-icon · screenshot-set · infographic` | uppercase in the filename (`EMPTY-STATE`), kebab inside a segment is legal |
| `SUBJECT` | one or more uppercase kebab segments — `APPLIANCE-REPAIR`, `JOB-FEED`, `HOMEPAGE` | **ASCII only.** Catalogue codes keep their `UPPER_SNAKE` form in the database (`06` §2 `code`), but a filename is a filesystem string that passes through CDNs, shells and Windows paths — `_` vs `-` in `AC_REPAIR` is how two names for one asset start. The inventory maps `APPLIANCE_REPAIR` → `APPLIANCE-REPAIR`. |
| size | `-1600x1000` for two-dimensional rasters, `-24` / `-512` for single-dimension icons | optional; when present it must equal the measured pixels (§4) |
| version | `-v01`, `-v02`, … | **never overwritten.** A new file gets a new version and the manifest gains a record with `supersedes` |
| ext | `svg · png · webp · avif · jpg · json` | lowercase |

Two exemptions, recorded rather than silently allowed: `screenshot-set` is not one file, and the four
`AMM-REF-*` references keep their original `visualize-image-of-project/` names because the brief
forbids renaming or deleting existing references.

Examples, matching the brief's own samples:

| Inventory `filename_stem` | Production file |
|---|---|
| `AMM-BRAND-LOGO-HORIZONTAL` | `AMM-BRAND-LOGO-HORIZONTAL-v01.svg` |
| `AMM-WEB-HERO-HOMEPAGE-1600` | `AMM-WEB-HERO-HOMEPAGE-1600-v01.webp` |
| `AMM-SERVICE-APPLIANCE-REPAIR-CATEGORY-800` | `AMM-SERVICE-APPLIANCE-REPAIR-CATEGORY-800-v01.webp` |
| `AMM-CUSTOMER-EMPTY-BOOKINGS-600` | `AMM-CUSTOMER-EMPTY-BOOKINGS-600-v01.svg` |
| `AMM-CONTROL-ICON-JOB-FEED-24` | `AMM-CONTROL-ICON-JOB-FEED-24-v01.svg` |

---

## 3. Manifest record schema

Every field is required; `null` is legal only where marked. Values not in the enumerated sets are
validation errors, not warnings.

| Field | Type | Rule |
|---|---|---|
| `asset_id` | string | `AMM-…`, unique, immutable for the life of the asset |
| `file` | path | repo-relative; must exist for `REGISTERED`/`GENERATED`/`APPROVED` |
| `format` | enum | `svg png webp avif jpg json` — must equal the file extension |
| `width_px`, `height_px` | int | **measured**, never asserted; `0` for scalable/vector records where the design size is nominal |
| `bytes` | int | measured; guards against a re-export that quietly doubles the weight |
| `sha256_16` | hex | first 16 hex chars of SHA-256. This was the substitute for version control — the workspace was **not a git repository** when the registers were built, so a silent overwrite was otherwise invisible. It became one on 2026-10-21 (`README` §16), and the field is **kept**: git records that a file changed, this records that the file on disk is the export the row describes (`31` §6) |
| `status` | enum | `REGISTERED · PLANNED · GENERATED · APPROVED · REJECTED · SUPERSEDED · BLOCKED`. `BLOCKED` means a *registered `OD-*` decision* must close; work that is merely not startable stays `PLANNED` with a note |
| `approval_status` | enum | `NOT_APPROVED · APPROVED · NOT_FOR_PRODUCTION · REJECTED`. A `GENERATED` file is never `APPROVED` in the same edit |
| `version` | `vNN` | matches the filename |
| `supersedes` | `asset_id` \| null | set when a later version replaces an earlier one |
| `source` + `provenance` | object | `tool`, `prompt`, `licence`, `creation_date`, `human_authored`. **All five required for anything AI-generated**; "NOT RECORDED" is a legal value and is what makes the gap visible — the four reference images carry it today, which is why `OD-COM-12` matters |
| `used_by` | array | screen IDs from `33` or route paths — never "various" |
| `alt_text` | string \| null | present iff `a11y_treatment == ALT_REQUIRED` (§5) |
| `a11y_treatment` | enum | §5 |
| `dependencies` | array | `sha256:…`, token names, or other asset IDs. The 9 brand/store derivatives depend on `AMM-BRAND-APPICON-MASTER`, so a master change must invalidate them |
| `notes` | string | why a row is blocked, deferred or refused |

Inventory CSV columns are the same contract minus the measured fields, plus `surface`,
`asset_type`, `subject`, `filename_stem`, `variants`, `intended_screens`, `source_class`,
`doc_ref` and `version`.

---

## 4. Export, optimisation and verification

| Rule | Value | Why, from the documents |
|---|---|---|
| Masters are never shipped | `master/` holds SVG/PSD/1024 PNG; `exports/` holds the delivered format | an optimised file cannot be re-optimised losslessly |
| Vector first | icons, empty states, markers, patterns ship as **SVG** | `12` §6.1 icon set; a 24 px raster at 3 dpr is 2× the weight for worse edges |
| Raster formats | **AVIF → WebP → JPEG/PNG fallback** via `<picture>`/`srcset` | `12` §9 LCP < 2.5 s on mid-range Android over 4G |
| Weight ceilings | hero mobile ≤ **150 KB**; category/detail ≤ **80 KB**; OG ≤ **200 KB**; icon SVG ≤ **4 KB**; illustration SVG ≤ **12 KB**; any store PNG ≤ **512 KB** | Derived from the `12` §9 budgets (LCP 2.5 s, CLS < 0.1) as a share of the budget, **not measured against a real device**. They are proposals to be re-confirmed against a mid-range Android once the site exists |
| Dimensions | recorded value must equal measured pixels | a `-800` file that is 1200 px wide is an unoptimised export |
| Transparency | declared, and verified where the format supports it | `12` §6.1 elevation/border-first surfaces break on unexpected alpha |
| Light/dark | only where `30` §10's dark-mode decision says yes — currently **none** | producing dark variants now doubles the register against an undecided policy (`OD-DOC-31`) |
| Locale variants | **only when text is inside the artwork, and text inside artwork is refused** (`31` §8) | `12` §8 i18n-03 (30 % expansion); `20` §11 GLO-01 defers Odia wording to the content owner |
| Serving | files go to the front-end static bundle (`16` §5.2), **not** the object store | `13` §5.2 `img-src 'self' …`; `24` §11 "no bucket, prefix or object is publicly readable" — see `OD-DOC-26` and `OD-DOC-34` `[BLOCKER]`, which asks whether this row survives at all: the owner has requested Cloudinary-primary delivery with a super-admin-selectable provider, and both cited rules forbid it as written. **Nothing in `validate_assets.py` checks a serving origin** — it validates IDs, grammar, statuses, alt-text treatment, `doc_ref` targets and bytes-on-disk, not where a file will be fetched from — so a CDN decision cannot be caught by the existing gate and this row is the only place the constraint is written down |
| Upload path | production *user* media uses presigned uploads with MIME/size validation and AV scan (`10` §11, `13` §5.1, `24` §11.4); **brand and product assets never traverse it** | they ship with the build, so `INF-07`'s 1 MB body cap does not apply to them. If `OD-DOC-34` is decided in favour of a managed media service, an admin-upload path for catalogue imagery becomes a *new* surface that no route, token or screen exists for yet — that is `OD-DOC-37`, and it must be designed before it is built |
| Request cap reminder | 1 MB request bodies (`16` INF-07) | a design that assumed uploads through the API would have hit this |

Verification, run from the project root — this is the gate, and it is intentionally boring. The scripts
live in `maintenance/scripts/` (moved out of the root on 2026-10-21; the **caller's** directory still has
to be the root, because both resolve their inputs relative to the working directory — `README` §12.5):

```
python3 maintenance/scripts/gen_asset_inventory.py   # regenerate intent (prints rows + status split)
python3 maintenance/scripts/validate_assets.py       # exit 0 or a list of refusals
```

It refuses: unknown statuses, `BLOCKED` rows citing no `OD-*`, `doc_ref` pointers to documents that do
not exist, duplicate `asset_id`s, alt text present where `a11y_treatment` forbids it or missing where
required, filenames outside the grammar, manifest records whose file is missing or whose bytes, hash,
format or measured pixels no longer match disk, and **any file in `design-assets/` that has no
inventory ID**. Manifest/CSV records are re-checked against the `Docs/` set on every run, so an asset
cannot quietly keep citing a section that has been renumbered.

---

## 5. Accessibility treatment

Declared per row in the inventory — never inferred from a file extension, because that inference is
exactly how decorative images end up with alt text and content images end up with none.

| `a11y_treatment` | Meaning | Alt rule | Rows |
|---|---|---|---|
| `ALT_REQUIRED` | the image carries the message | non-empty `alt_text_en`; `or`/`hi` wording owed by the content owner (`20` §11 GLO-01) | **24** — hero, illustrations, empty/success/error states, category-image, photo-placeholder, logo |
| `LABELLED_BY_ADJACENT_TEXT` | visible text already names it (`12` §3 screen 4: "icons, **names** (localised)") | ship `alt=""`, `aria-hidden` on the graphic only | **49** — 6 category icons + 43 Control Center nav icons |
| `DECORATIVE_EMPTY_ALT` | chrome — app icon, favicon, PWA icon, pattern, store icon, mark | `alt=""` or not present in the DOM | **12** — app/store/PWA/favicon/pattern/mark |
| `SOCIAL_META_IMAGE` | referenced by `og:image`, no DOM alt | none; must still avoid baked text | **3** — 2 OG rows + the Play feature graphic |
| `NOT_SHIPPED` | internal reference or blocked capture set | n/a | **5** — 4 registered references + the screenshot set |

The five treatments partition all **93** rows (24 / 49 / 12 / 3 / 5); `validate_assets.py` recomputes them, so this table cannot silently go
stale. `12` §6.3 A11Y-1…A11Y-7 remain the normative accessibility rules — this section is the asset
view of them, not a second statement of them.

---

## 6. Lifecycle

```
PLANNED → GENERATED → APPROVED → (SUPERSEDED | REJECTED)
   ↑          |
BLOCKED ──────┘   (a BLOCKED row cannot enter GENERATED, and a GENERATED row cannot be shipped in a build)
```

- **`GENERATED` is not `APPROVED`.** The brief's own rule; recorded here so a batch of AI output cannot
  reach a build by renaming a folder. The route a row takes to `GENERATED` — which prompts, which style
  lock, what to check at intake — is in `34` §4 and `34` §6, and nowhere else (`DEC-01`).
- **A placeholder container is not a register row, and does not move a status.** Under the owner's
  placeholder-first direction (`30` §5.3) a UI slot renders as an inline SVG or a blank ground-and-border
  container in code. That is presentation, not an asset: no inventory row becomes `GENERATED` because a
  container was drawn, and none may be deleted or renumbered because one was. The only `photo-placeholder`
  row in the register is `AMM-WEB-PLACEHOLDER-PARTNER-512` (`01` FR-CAT-05 and `09` §4.4's technician
  `photo_url`), it is authored rather than generated, it carries `Must never depict an identifiable person
  as a registered partner`, and it is still `PLANNED` / `NOT_APPROVED`.
- **`REJECTED` records are kept.** A refusal with a reason is cheaper than a re-generation, and the
  brief asks for rejected assets to be recorded.
- **Approval is an owner act, not a document act** (`DEC-03`). Nothing in `30`–`37` can move a record
  to `APPROVED`; only the named owner's decision, logged in `21`, can.
- **Version increments never delete.** With no git history, a deleted master is gone permanently.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.4 | 2026-10-21 | Product Design Lead (scaffold and git-baseline pass) | §3’s `sha256_16` row is now past tense about the missing version control — the workspace became a git repository on 2026-10-21 (`main`, baseline commit `0cc6910`) — and **the field is kept, not dropped**, because the hash plus byte-length is what §4’s verification proves and git history does not carry it. For the same reason `.gitattributes` was written with `* -text` before the first commit: EOL normalisation would silently rewrite byte lengths and invalidate the recorded hashes. §4’s verification block now calls `maintenance/scripts/gen_asset_inventory.py` and `validate_assets.py` at their relocated paths; re-run after the edit, the inventory is unchanged and the validator still reports **0 errors** against the 4 manifest records. **No grammar, treatment, export figure or lifecycle rule changed**, and no asset was generated or moved. | §3, §4 |
| 1.3 | 2026-10-21 | Product Design Lead (tooling and backup relocation) | §4's verification block now calls the two scripts at `maintenance/scripts/` and records that the caller's directory still has to be the project root. Both were re-run after the move: `gen_asset_inventory.py` regenerates the same **93 rows** and the same status split (83 PLANNED / 6 BLOCKED / 4 REGISTERED), and `validate_assets.py` still reports **0 errors** against the 4 manifest records. **No grammar, treatment, export figure or lifecycle rule changed**, and no asset was generated, approved or moved. | §4 |
| 1.2 | 2026-10-21 | Product Design Lead + Engineering Lead (design-engineering structure pass) | Depends On now points at **`35` §6** (the storage-layout half of §6 is the token package’s and asset directories’ problem, not this document’s) and **`37` §7.1** (what a consumer does when the asset is absent, which is the other half of every `approval_status` value here). **The naming grammar, the two register formats, the export ceilings, the alt-text treatments and §4’s byte-and-hash fields are unchanged**, and the measured state on disk is unchanged too: `design-assets/` holds 11 top-level directories (25 counting sub-folders), **two register files and no artwork**, and `asset-manifest.json` still records four files, all `NOT_FOR_PRODUCTION`. Nothing was renamed, moved or deleted. | Depends On, Revision History, header |
| 1.1 | 2026-10-21 | Product Design Lead + Frontend Lead (palette, storage and prompt-pack pass) | §4's **Serving** row now names `OD-DOC-34` (`[BLOCKER]`) beside `OD-DOC-26`: the requested Cloudinary-primary, super-admin-selectable delivery contradicts `13` §5.2's `img-src 'self'` and `24` §11's no-public-read rule, so the static-bundle row remains the serving design until that closes — and the row states plainly that **`validate_assets.py` checks no serving origin at all** (IDs, grammar, statuses, alt-text treatment, `doc_ref` targets, bytes-on-disk), which is why a CDN decision cannot be caught by the existing gate. The **Upload path** row notes that an admin-upload route would be a new surface with no route, token or screen behind it (`OD-DOC-37`). §6 gained the rule that **a placeholder container is not a register row** — under `30` §5.3 the container is presentation, so it cannot move a row to `GENERATED` nor license deleting one, and `AMM-WEB-PLACEHOLDER-PARTNER-512` (authored, `Must never depict an identifiable person as a registered partner`) is still `PLANNED`/`NOT_APPROVED`; and the `GENERATED → APPROVED` separation now points at `34` §4/§6 as the only home for prompt wording (`DEC-01`). `30`–`33` widened to `30`–`34` in the approval bullet. **No status enum, column, naming rule, ceiling or validator behaviour was changed.** | §4, §6, header, Revision History |
| 1.0 | 2026-10-21 | Product Design Lead + Frontend Lead (documentation pass) | First issue. Intent (`asset-inventory.csv`) separated from fact (`asset-manifest.json`); naming grammar formalised with the `_`→`-` catalogue-code mapping and two recorded exemptions; export rules bound to the `12` §9 budgets, the `13` §5.2 CSP and `24` §11's non-public bucket; hash/size/pixel verification defined as the integrity gate because the workspace is not a git repository; five-value `a11y_treatment` replacing any extension-based inference. Weight ceilings are derived proposals, not device measurements. | All |
