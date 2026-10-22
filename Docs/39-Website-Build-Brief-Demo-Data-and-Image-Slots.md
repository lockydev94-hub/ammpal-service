# 39 — Website Build Brief, Image Slots and Demo Data

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-39 |
| Version | 1.2 |
| Status | **PROPOSED — not approved.** It is a build brief, not an approval of the visual system. |
| Owner | Product Design Lead (sections and slots) + Frontend Lead (demo data and scaffold) |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-22 |
| Depends On | `12` §2/§2.1 (routes and page elements), `30` §3–§5/§7/§11 (tokens, layout, effects, SVG-first), `33` §3 (SCR-WEB-01…09), `35` §5 (`apps/web/` interior, PS-06…PS-10), `36` §4/§6 (library baseline, the six premium causes), `37` §4/§7 (variant contract, missing-asset behaviour), `32` §3/§4 (asset records and ceilings), `34` §4 (prompt wording), `38` (TESTING vs PRODUCTION data), `21` (the open decisions named below) |
| Artifacts | `maintenance/prompts/` (9 files in all — `00-START-HERE.md` plus one run sheet per landing folder, the website having two: `02-website.md` and `10-website-sections.md`), `maintenance/scripts/intake_asset.py`, `maintenance/scripts/record_assets.py`, `design-assets/manifests/`. From §8 steps 2–4: `packages/design-tokens/`, `packages/ui/`, `packages/contracts/`, `apps/web/` — **in the working tree, deliberately uncommitted** (owner scope 2026-10-22: the public remote carries the documents and the registers, not the application), and the generated artwork under `design-assets/` is `.gitignore`d for the same reason. |

---

## 1. What this owns, and what it deliberately does not

`12` §2 owns the routes. `30` owns the visual values. `33` owns the screen index. `35` owns the folder
tree. `36` owns the library baseline. This document owns the one thing none of them states: **for each
website page, which sections appear, in what order, and what image box each section reserves** — plus
the demo-data contract that lets those sections be drawn before a backend exists.

| Question | Where it is answered |
|---|---|
| What routes exist | `12` §2 — a new page is added there first, never here (`35` PS-06) |
| What a section looks like | `30` §3–§5 (colour, type, spacing, elevation, effects) |
| What components a section is built from | `12` §6.2 and `37` §3/§4 |
| What file goes where | `35` §5 |
| What may be installed | `36` §4, and §5 below, which is the same answer with the icon question made concrete |
| What image goes in what box | **§3 here** — nowhere else |
| What data fills it before the API exists | **§4 here** — nowhere else |

---

## 2. Page and section map

Nine page types in `12` §2.1, mapped onto `35` §5's six route groups. Home's sections are measured from
the "Key Elements" column of `12` §2.1 — five of the eight sections below are that column item by item,
and the three that are not are marked as such in the element column.

### 2.1 Home (`SCR-WEB-01`) — 8 sections

| # | Section | `12` §2.1 element | Image slot | Notes |
|---|---|---|---|---|
| H1 | Utility bar: city picker, language, toll-free | city picker | none | City picker is the location entry point (`02` §3); it writes the zone cookie, it does not guess from IP alone |
| H2 | Search-first hero | service search, "book now" CTA | `AMM-WEB-HERO-HOMEPAGE-1600` | **Search-first, not marketing-first** (`12` §2.1). Headline sits in the reserved empty half of the artwork, never baked into it |
| H3 | Appliance rail — what we fix | category tiles | 5 × `AMM-WEB-ILLU-*-REPAIR-800` | For the business being designed now this is an **appliance** rail (AC, refrigerator, washing machine, microwave, purifier), not the 6-family catalogue rail. The families are `OD-DOC-27`'s unresolved question; the appliances are `06` §4.1's existing service list |
| H4 | How it works — 3 steps | *not in the column* — earned by `12` §7's "Home → Book ≤ 3 minutes" target | 3 × `AMM-WEB-ILLU-STEP-*-800` | Three, not five: `04` §2's nine stages are the *system* lifecycle, the customer sees three choices |
| H5 | Price transparency and trust | trust signals | `AMM-WEB-ILLU-PRICING-TRANSPARENT-800`, `AMM-WEB-ILLU-TRUST-VERIFIED-800` | Links to `/pricing`. Shows a band, never a single number, until a location is chosen (`07` §3). Trust copy is a field with a source, never a decoration count (DD-06) |
| H6 | Offer strip | active offer strip | `AMM-BRAND-PATTERN-BACKGROUND` at 6 % | Coupon copy is server data (`07` §5); the strip renders empty when no campaign is live — it does not show a placeholder deal |
| H7 | Coverage / serviceability check | *not in the column* — restates H1's city picker as a verdict (`23` §5, ADR-004) | `AMM-WEB-ILLU-SERVICEABILITY-800` | The negative result is the design: "not yet in your area" |
| H8 | Partner + support footer band | *not in the column* — the footer in `12` §2's tree | `AMM-WEB-ILLU-SUPPORT-HELPLINE-800` | Legal links come from `(legal)` with one source of truth (`12` XS-05) |

**8 sections, 14 image slots, 14 distinct files on Home** — 3 already in the register and generated
(`AMM-WEB-HERO-HOMEPAGE-1600`, `AMM-BRAND-PATTERN-BACKGROUND`, `AMM-WEB-ILLU-SERVICEABILITY-800`) and 11
of the 12 website-section rows (they are **register rows now** — the owner said go on 2026-10-22, so the
CSV went 93 → 105 and `34` §4.7 carries their prompts; none has been generated yet).
`AMM-WEB-HERO-PARTNER-1600` is the twelfth and belongs to `/partner`, not
here. Two of the fourteen reappear on other screens — the pattern as a section ground, the serviceability
illustration as the `/services` empty state — so §3's table reserves 18 slots that consume 18 distinct
files. Nothing above the fold is a carousel, and there is no auto-advancing anything: `30` §7's
motion budget and `12` §9's LCP < 2.5 s on mid-range Android over 4G both die under hero sliders.

### 2.2 The other eight page types

| Page | Sections | Image slot |
|---|---|---|
| `/services` (`SCR-WEB-02`) | filter bar, service cards, empty state | `AMM-WEB-ILLU-SERVICEABILITY-800` when a filter returns nothing |
| `/services/{cat}` (`SCR-WEB-02`) | category header, service cards with "from ₹X", availability badge | `AMM-WEB-ILLU-*-REPAIR-800` per card |
| `/services/{cat}/{slug}` (`SCR-WEB-03`) | variant picker, price range, inclusions/exclusions, process steps, warranty, reviews, FAQ | header `AMM-SERVICE-*-CATEGORY-800` — **BLOCKED**, see §6.2 |
| `/technicians`, `/technicians/{id}` (`SCR-WEB-04/05`) | filter, cards, profile with rating breakdown | `AMM-WEB-PLACEHOLDER-PARTNER-512` (authored monogram, §3.3) |
| `/book/…` (`SCR-WEB-06`) | 7-step stepper: address → service → slot → technician → price → payment → confirm | none — a form screen earns its quality from `30` §4/§5, not from artwork |
| `/bookings`, `/bookings/{code}` (`SCR-WEB-07`) | history list, status timeline, technician card, live map, price breakdown, invoice | `AMM-CUSTOMER-SUCCESS-BOOKING-600` on the confirmed state only; marker set on the map |
| `/partner`, `/partner/register`, `/partner/login` (`SCR-WEB-08`) | partner hero, earnings model, requirements, multi-step registration | `AMM-WEB-HERO-PARTNER-1600`, `AMM-WEB-OG-PARTNER-1200` (meta only) |
| `/support`, `/toll-free` (`SCR-WEB-09`) | FAQ search, category cards, click-to-call, ticket form | `AMM-WEB-ILLU-SUPPORT-HELPLINE-800` |
| `/pricing`, `/offers`, legal | transparency bands, coupon list, text | `AMM-WEB-ILLU-PRICING-TRANSPARENT-800` |

Empty, loading, error and permission states for every one of these come from `33` §5's state matrix, and
the empty states are already drawn: the 10 `empty-state` assets and `AMM-CONTROL-DENIED-600` generated
on 2026-10-22.

---

## 3. Image slots — the box, not the picture

`30` §5.3's placeholder-first rule stands: **the container holds the layout, not the image.** Every slot
below is a reserved box with a fixed ratio; an `<img>` appears only when a file with a register row and
a manifest record exists to fill it.

| Slot id | Asset | Box at 1440 | Box at 390 | Ratio | `srcset` | Ceiling (`32` §4) |
|---|---|---|---|---|---|---|
| `web-hero-home` | `AMM-WEB-HERO-HOMEPAGE-1600` | 1200 × 750 | 358 × 224 | 16:10 | 780w, 1600w | 150 KB (mobile) |
| `web-tile-appliance` ×5 | `AMM-WEB-ILLU-*-REPAIR-800` | 282 × 212 | 358 × 268 | 4:3 | 564w, 800w | 12 KB |
| `web-step` ×3 | `AMM-WEB-ILLU-STEP-*-800` | 282 × 212 | 358 × 268 | 4:3 | 564w, 800w | 12 KB |
| `web-trust` | `AMM-WEB-ILLU-TRUST-VERIFIED-800` | 588 × 441 | 358 × 268 | 4:3 | 716w, 1200w | 12 KB |
| `web-pricing` | `AMM-WEB-ILLU-PRICING-TRANSPARENT-800` | 588 × 441 | 358 × 268 | 4:3 | 716w, 1200w | 12 KB |
| `web-serviceability` | `AMM-WEB-ILLU-SERVICEABILITY-800` | 474 × 356 | 358 × 268 | 4:3 | 716w, 800w | 12 KB |
| `web-support` | `AMM-WEB-ILLU-SUPPORT-HELPLINE-800` | 474 × 356 | 358 × 268 | 4:3 | 716w, 800w | 12 KB |
| `web-hero-partner` | `AMM-WEB-HERO-PARTNER-1600` | 1200 × 750 | 358 × 224 | 16:10 | 780w, 1600w | 150 KB |
| `web-offer-strip-bg` | `AMM-BRAND-PATTERN-BACKGROUND` | 1440 × 240 tile | 390 × 200 tile | 1:1 tile | 800w, 1600w | 12 KB |
| `web-avatar-partner` | `AMM-WEB-PLACEHOLDER-PARTNER-512` | 96 × 96 | 64 × 64 | 1:1 | 128w, 512w | 80 KB |
| `og-*` | `AMM-BRAND-OG-HOMEPAGE`, `AMM-WEB-OG-PARTNER-1200` | not in the DOM | — | 1.91:1 | single | 200 KB |

**3.1 Rules that make this look designed rather than assembled** (`36` §6, applied to these slots):

- The box is reserved with `aspect-ratio` and a `background: var(--amm-color-surface-sunk)` ground, so a
  missing file costs nothing to the layout and CLS stays < 0.1 (`12` §9). The name is the one the token
  build emits: `30` §3.4 calls the same value `surface.sunk`, and `--amm-surface-muted` was this section's
  earlier shorthand for it — there is no `muted` surface token and a component that asked for one would
  render a transparent ground.
- Every raster is served through `<picture>` with AVIF → WebP → JPEG in that order (`32` §4). The
  exports already on disk are in that order; the intake script produces all three.
- **No text over these images.** The hero artwork leaves its headline half empty; the headline is DOM
  text (`30` §11). Where a scrim is genuinely needed it is the `30` §5.2 token at α ≥ .65 (.85 under a
  headline), never a drop-shadow on the type (PS-09).
- Zero colour literals in components (`35` PS-07). The only hex in the front end lives in
  `packages/design-tokens`.
- `loading="lazy"` and an explicit `width`/`height` on every non-LCP image; the hero alone is
  `fetchpriority="high"` and unsized-by-lazy — it is the LCP element and the whole 2.5 s budget is spent
  on it.

**3.2 When the asset is absent**, `37` §7.1 governs: the slot renders its reserved container with the
label beside it, and the screen is still reviewable. A missing image is never a grey rectangle and never
a stock placeholder.

**3.3 The avatar is authored, not generated.** `AMM-WEB-PLACEHOLDER-PARTNER-512` carries the register note
*"Must never depict an identifiable person as a registered partner"*. Its design is a monogram: the
initial letterform on `brand.50`, a `color.border` hairline (`--amm-color-border`), radius 999, at 512 px — one authored SVG, and a
real `photo_url` replaces it when a partner supplies one (`09` §4.4).

---

## 4. Demo data contract

The owner's mission is **design every surface against demo data, then build the backend**. That is only
safe if the demo data has the same shape as the real contract, so a screen drawn today cannot be shipped
by rewriting its data path tomorrow.

| # | Rule | Why it is not a shortcut |
|---|---|---|
| DD-01 | Money is **integer paise** in the fixture, formatted at the edge as `₹1,119.82` with tabular numerals (`12` XS-02, `00` FR-03) | A fixture holding `1119.82` as a float trains every component to accept a float, and the first real bug is a rounding bug in a settlement |
| DD-02 | Rates are **basis points** (`1500` = 15 %), never `0.15` | `07` §2's commission model and `13` §2's correctness rules are stated in bps |
| DD-03 | Timestamps are **ISO-8601 UTC**, rendered in `Asia/Kolkata` at the edge (`README` §14.2) | A booking SLA timer drawn against local-time strings cannot be trusted when the real timer arrives |
| DD-04 | Every fixture row carries the `TEST` origin marker of `38` §5, and the demo set is loaded only in `TESTING` mode | `38`'s whole point: test data must never be mistaken for production data, and `OD-DOC-40`/`41` are unresolved |
| DD-05 | One fixture module per domain (`catalog`, `booking`, `pricing`, `partner`, `support`), typed with the same zod schema the form uses (`14` FE-06) | When the API lands, the mapper changes and the component does not |
| DD-06 | **No invented commercial claims**: no review counts, ratings, install counts, "trusted by", awards or partner counts that no record produced (`34` §7, `29` §4.8) | Ratings in the demo set are shown as *fields with a source* ("from verified completed bookings", `13` §5.3), never as decoration |
| DD-07 | Prices are **bands** (`min`/`default`/`max`) resolved through the location hierarchy, not single numbers (`00` BR-03, `07` §3) | A hard-coded "₹499" on a card is the price-transparency promise broken at design time |
| DD-08 | Location fixture: **State Odisha → City Bhubaneswar (HQ), Cuttack, Puri → Zone → Service area → Branch**, with one service area deliberately *outside* coverage | `02` §3's hierarchy and `23` §5's negative case are both drawable from the same file; the negative case is the section H7 design |
| DD-09 | Names in the demo set are obviously fictional and marked as such in the fixture header | A technician name that reads real invites a real person's photo into the slot next to it |
| DD-10 | Layout is drawn to the **30 % expansion tolerance** (`12` i18n-03) even though design proceeds English-first (`30` §4.1) | Odia and Hindi copy arrives later; a section that only fits English is a rebuild, not a translation |

**What demo data does not need:** the API, a database, a payment gateway, or any of the `[BLOCKER]`
decisions in §7. It does need `10` §4's shapes to be stable enough to mirror — and `OD-10-06`/`OD-DOC-29`
say no screen→route→permission join exists yet, so **the fixture is the contract's mirror, not its
source**, and every mapper file says so in one line.

---

## 5. Icons and the provisional library set

`36` §4 already decides the *shape* of the answer: SVG imported as components, a sprite for the nav set,
**no icon font**, 4 KB per icon (`32` §4), one outline set at 20/24 px (`30` §5/§11). The package question
is `OD-14-09`'s, and this is the recommendation to close it:

| Need | Proposed | Why this one |
|---|---|---|
| 43 Control Center nav icons, 6 category icons, action icons | **`lucide-react`** as the provisional source | MIT, tree-shaken per-icon (an unused icon costs nothing in the bundle), a single 24 px grid with a 2 px stroke that matches `30` §5's icon viewport, and no runtime CSS |
| A11y behaviour primitives (dialog, menu, tabs, popover, toast) | **Radix UI unstyled primitives**, wrapped once in `packages/ui` | `36` §4's `LB-01`/`LB-04` rule: behaviour from the library, appearance from `30`'s tokens |
| Styling | **Tailwind** for the marketing web | build-time CSS is the only pattern that satisfies `13` §5.2 `style-src` without nonce plumbing |
| Variants | **class-variance-authority + tailwind-merge** | `37` §4's five-axis variant contract, so states stop being if-chains |
| Forms | **react-hook-form + zod** | `14` FE-06's schema-first rule, one zod schema per form |
| Client state | **TanStack Query**; server components for Next reads | `14` FE-01/FE-02 — no stray `fetch` outside the query layer |
| Charts (later, Control Center) | SVG-rendered, series palette from `30` §8 | canvas-only breaks the table-alternative rule |

**Two conditions on any of that.** First, installing it means writing `apps/web/package.json` and
committing `node_modules`-adjacent tooling — the first build artefact in a repository that has none, on
the assumption `OD-14-04` (monorepo vs separate repos) has not decided. The `apps/web/` tree already
presumes the monorepo answer, so the file goes there and nowhere else, and the assumption becomes
visible instead of implied. Second, **provisional is not authored**: `lucide` covers the drawing phase,
and the 49 icon rows in the register still owe authored SVGs before `29` §4.8 can certify the design
gate. Replacing a library icon with a drawn one is a rename in one file; replacing 43 of them across a
shipped UI is not.

**Accepted 2026-10-22, as asked.** The owner chose this set over a self-authored icon package, so the
first condition is now a fact rather than a risk: `apps/web/package.json`, `packages/ui/package.json`,
`packages/contracts/package.json` and `packages/design-tokens/package.json` exist, one `node_modules`
sits under each workspace root, and nothing was placed at the repository root. The installed versions are
`next@15.5.28`, `react@19.3.1`, `typescript@5.9.3`, `tailwindcss@3.4.19`, `class-variance-authority@0.7.1` +
`tailwind-merge@3.7.0`, `react-hook-form@7.90.0` + `@hookform/resolvers@5.2.2`, `zod@4.6.7`,
`lucide-react@1.61.0`, `@tanstack/react-query@5.104.5` and the Radix primitives (`@radix-ui/react-dialog`
is the version pinned). The `apps/web` install also carries **11 reported npm-audit advisories (8 high, 3 moderate)** — none is in
a runtime path a demo build exposes, and they are recorded here rather than left for the deployment phase to
discover, because `29` §4 will ask. The second condition is **unchanged and still owed**:
every glyph a screen draws today is a library drawing, and `29` §4.8 cannot certify the icon rows until the
49 authored SVGs replace them.

---

## 6. Conflicts this brief found, stated on both sides

`DEC-07`: a conflict is recorded, not edited into agreement.

**6.1 `30` §5.3's ratios versus the register's dimensions.** `30` §5.3 fixes category tile **4:3**, hero
**16:9**, OG **1.91:1**. The register's `category-image` rows are `800 × 800` (1:1) and the hero row is
`1600 × 1000` (16:10). Both statements are in force. New slots in §3 use 4:3 and 16:10 — the hero's
existing asset is 16:10 and re-cropping it to 16:9 loses the empty headline half's proportion. **The
owner decides which side moves**; `32` §3's dimensions and `30` §5.3's table are both one-line edits.

**6.2 Service-level imagery asserts `OD-DOC-33`.** The five appliance tiles in §2.1-H3 bind artwork to a
*service* (AC repair), while the six `category-image` rows bind to a *family* (appliance repair). If
`OD-DOC-33` decides family-level binding, the five tiles become unnecessary; if it decides service
level, the six blocked family rows are the wrong unit. The tiles are proposed because the website being
designed sells appliance repair specifically — that is a design fact, not a catalogue decision, and it is
why the rows are new rather than a re-purpose.

**6.3 `OD-DOC-25` is now a live question, not a parked one.** The register's blocked rows cite it: does
the catalogue carry photography at all, and is a "tile" an icon or an image (`12` §2.1 and §3.2 name both,
twice in one document). §2.1-H3 answers it for the marketing surface only: **an image with a name beside
it**. The catalogue pages keep the question open.

**6.4 PS-10 versus "start the website using these images".** `35` PS-10 says marketing imagery ships as
placeholder slots until the upload/asset question (`OD-DOC-34`) closes, and `30` §5.3 makes
placeholder-first the delivery method. The owner's 2026-10-22 direction is to build the site **with**
these generated images and demo data. This brief follows the owner and records the tension: the images
are `GENERATED`, none is `APPROVED` (`DEC-03`), `OD-COM-12` leaves their IP position undocumented, and
`OD-DOC-34` still decides where a file may be *served from* — `validate_assets.py` checks no serving
origin at all, so intake succeeds today and a CDN decision would land on the build, not on the gate.

**6.5 The 12 KB illustration ceiling is a vector budget.** All 18 intaken rasters were compressed against
it and 17 of them fit in every shipped format. One did not: `AMM-WEB-ILLU-SERVICEABILITY-800`'s JPEG
fallback measures 15,009 B against the 12,288 B ceiling, while its AVIF (11,810 B) and WebP (12,138 B)
both fit — the intake script deliberately leaves an over-ceiling PNG out of the export set so JPEG never
becomes the delivered file. Fitting a vector budget as raster proves the number is reachable, but it is
not the same artefact: the traced SVGs are still owed for the 15 rows declared `format=svg`, and until
then `32` §4's vector-first rule is unmet on those rows. The deviation is recorded in each manifest
`notes` field by `record_assets.py`, not hidden.

**6.6 The build invented route strings, because no document publishes them.** `apps/web/lib/routes.ts`
holds every marketing path in one file — `/services`, `/offers`, `/support`, `/legal/{terms,privacy,refund,gst}`
and the rest — while `OD-10-06` / `OD-DOC-29` still own the screen→route→permission join. This is recorded as
a conflict, not a solved problem: the alternative was a screen with no navigation, and a section map that
cannot be clicked through is not reviewable. What a later pass owes is stated by the file's own header —
replace the strings with the ones `10` §2 and `29` publish, and every call site moves with it because they
all read `routes.*`. The category segment (`/services/{code}` with the code lowercased and hyphenated) is
this file's convention, not a published pattern.

**6.7 The hero export is an upscale, and `34` asks for it to be labelled one.** The register row and the
manifest both say `1600 × 1000`, and the shipped exports do measure that. The **masters on disk measure
1586 × 992** — the model's own grid, about 1 % short — so intake resized instead of cropping, and the ratio
moved a hair (1.599 : 1 → 1.6 : 1). `34`'s size-limit row instructs the opposite: generate the largest the
tool reaches and mark the row `GENERATED - UPSCALE REQUIRED` "rather than shipping an upscaled blur". A 0.9 %
upscale is not a visible blur, so the file is defensible on its merits, but the flag the document asked for
is absent from the row's notes. Either the row gains it or `34` drops the instruction; `DEC-07` leaves that
to the owner, and this pass changed neither — the register is generated and hand-editing it is prohibited.

**6.8 `37` §7.1's "served is not reachable today in any environment" is now locally false.** That sentence
holds because the serving path is `OD-DOC-34`'s. `apps/web/app/assets/[...path]/route.ts` reads
`design-assets/` and serves the manifest's `GENERATED` records same-origin, and `lib/assets.ts` exposes a slot
only when the manifest carries it — so `served` *is* reachable, on one machine, in one developer's browser,
behind no CDN and with no CSP (`13` §5.2's `img-src` still undecided). Both statements stay: §3.1's
reserved/serve behaviour is testable today because of the local route, and `37` §7.1's sentence remains true
of every environment anyone else can reach. Closing `OD-DOC-34` is what reconciles them.

---

## 7. What must close before the website is scaffolded, and what does not

| Gate | Stops | Can proceed anyway |
|---|---|---|
| `OD-14-04` `[BLOCKER]` monorepo vs repos | where `package.json` lives | §2/§3/§4 — a section map and slot table are topology-independent |
| `OD-14-09`/`10`/`11`/`12`/`13` | styling engine, motion runtime, workshop, token build | the fixture contract DD-01…DD-10 |
| `OD-DOC-34` `[BLOCKER]` media storage and serving | `public/` story, PS-08, any CDN URL | local files in `design-assets/` and a same-origin build |
| `OD-DOC-30` palette approval | re-running every prompt | building against the measured tokens as they stand |
| `OD-DOC-27`/`28`/`33` | the six family category images | the five appliance tiles, which is what this site sells |
| `OD-10-06`/`OD-DOC-29` `[BLOCKER]` screen→route→permission join | auth-aware states on `/bookings`, `/partner/*` | the whole marketing surface, which has no permission states |
| `OD-COM-12` design-asset IP | presenting any generated file as brand property, and a store submission | internal review and the demo build |

**Nothing in §2, §3 or §4 waits.** The website can be built today against demo data with the 18 intaken
assets plus the 12 registered-and-unrun ones — the twelve rows are in the register, so a reserved container
for each of them is legal, a file for one of them is not yet. The four `[BLOCKER]`s above decide the
*deployment* of that work, not its design.

---

## 8. Build order

| Step | Deliverable | Depends on |
|---|---|---|
| 1 | ~~12 rows added to `gen_asset_inventory.py` and CSV regenerated~~ — **done 2026-10-22** (93 → 105, gate clean). Remaining: prompts run, files intaken | owner's credits |
| 2 | ~~`packages/design-tokens` emitting CSS custom properties from `30` §3/§4/§5 (`35` PS-11)~~ — **done 2026-10-22**; see §8.1 | nothing |
| 3 | ~~`packages/ui`: Button, Card, Field, Badge, Sheet, DataTable shell with `37` §4's five variant axes and `33` §5's seven states~~ — **done 2026-10-22**; the review against `37` §4's ten rows is still open | step 2 |
| 4 | Home's 8 sections, `/pricing`, `/support`, `/toll-free`, `/offers` — **Home is drawn against the fixtures** (see §8.2); the four named pages are not | steps 2–3 + DD fixtures |
| 5 | `(catalogue)` + `(technicians)` with the serviceability negative state drawn first | step 4 |
| 6 | `(booking)` 7-step stepper against fixtures, address first | step 5 |
| 7 | `(account)` `/bookings` + detail/timeline against fixtures, `TEST`-marked | steps 4–6, and it is the first screen that wants an auth model |
| 8 | Legal text from one source (`12` XS-05) | nothing |
| 9 | Design gate review: `33`'s `UNDESIGNED` → drawn, per screen, with `29` §4.8's asset checks | steps 1–8 |

**8.1 What the token build emits, as built.** `packages/design-tokens/build/to-css.ts` writes
`packages/design-tokens/dist/tokens.css` — **217 lines, 156 `:root` custom properties**, regenerated by
`npm run tokens` and never hand-edited (the file had drifted from its generator before this pass, because
`to-css.ts` itself contained two syntax errors and the script had therefore never run: both are fixed and the
build is clean). Three deltas a reviewer should know:

- `--amm-scrim-overlay-alpha: 0.65` was **recovered** — `30` §5.2's dialog/drawer scrim floor had a consumer
  in `packages/ui`'s Sheet and no token, so the component read `opacity-[var(…)]` against a variable that did
  not exist. It is now `opacity-scrim` in Tailwind's scale.
- `--amm-pattern-alpha: 0.06` is **new**, and it is `39` §2.1-H6's own figure for the brand pattern as a
  section ground. It is a token rather than `opacity-[0.06]` because a Tailwind `/opacity` modifier cannot
  compose with a `var()` colour, so an alpha a screen needs belongs where the alphas live.
- `--amm-control-pad-web-*` were **removed**: they had no consumer anywhere in the repository (grep proved
  it), and `37` §4 row 3's rule is that the control grows its hit area in CSS, not through a token a
  component has to remember to apply.

**8.2 What Home renders today.** Eight sections, in the order §2.1 sets, in one server-rendered page
(`/`), with two client islands (the coverage form and the hero search) plus the city picker. Home carries
**fourteen image elements: 2 served and 11 reserved containers, plus the offer strip's pattern ground**, and
the served pair is `AMM-WEB-HERO-HOMEPAGE-1600` (v02, the owner's pick) and `AMM-WEB-ILLU-SERVICEABILITY-800`.
The other eleven are reserved because their artwork has not been generated: they are exactly the twelve rows
§8 step 1 registered, minus `AMM-WEB-ILLU-SERVICEABILITY-800`, which has since been intaken — the twelve are
the five appliance tiles, the three step illustrations, the two trust illustrations, serviceability and the
support helpline. The third file the page paints is `web-offer-strip-bg`, the brand pattern, drawn as a ground
rather than through `ImageSlot` (`39` §2.1-H6). Every number and every trust claim on the page is
read from a fixture field (`demoAcRepairBand`, `demoResolvedPrice`, `demoSplitBand`, `demoQuote`,
`demoAcRepair.warrantyDays`, `demoTechnicians[].rating.average`) rather than typed at the call site, which is
what keeps DD-06 honest: a rating row says "not yet rated" because the fixture's `average` is `null`.

Verification is at markup and CSS level, and its limit should be read as plainly as the result: a production
build (`next build`) was compiled, served and fetched, and the served HTML carries 13 `ImageSlot` boxes with
their `data-slot-state`/`data-asset-id` attributes, the compiled stylesheet carries both alpha tokens and the
`max-w-content` scale, the three asset routes return `200 image/avif`, `tsc --noEmit` is clean across
`apps/web`, `packages/ui` and `packages/contracts`, and ESLint reports 0 errors. **No browser or pixel tool
was available, so nothing here is a visual review** — spacing, weight and whether the artwork reads as
designed are the owner's `29` §4.8 pass, and §2's layout is an approved *layout*, not an approved *screen*
(`37` CA-21).

One defect that pass found: `packages/ui`'s `Card` destructured only `className` and passed everything else —
`children` included — to `cardVariants()`, which ignores unknown keys. Every card on the site therefore
rendered as an empty `<div data-card>` and eleven image slots looked absent from the page source. It was not
a layout bug and no amount of reading the section components would have found it; the fix is in `Card`, and
the reason it is recorded here is the lesson for `37` §4's still-open review — a primitive that accepts DOM
attributes must forward them, and a build that "compiles clean" cannot see a swallowed `children`.

Then the same sequence for the Customer app, and only then the backend — which is the order the owner
set, with the caveat that `OD-DOC-38` still decides what that backend is.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.2 | 2026-10-22 | Product Design Lead + Frontend Lead (Home built against the fixtures) | Steps 2, 3 and the Home half of step 4 are **done**: `packages/design-tokens` emits CSS, `packages/ui` has the primitives, and Home's eight sections render on demo data. §5 records that the owner **accepted the library set**, with the installed versions measured from the four workspace `package.json` files and **11 open npm-audit advisories (8 high, 3 moderate)** stated rather than deferred. §3.1 and §3.3 were corrected against what the build actually emits — `--amm-surface-muted` and `line.200` named tokens that do not exist (`--amm-color-surface-sunk` and `--amm-color-border` do). §6 gains **three conflicts** (§§6.6–6.8): the route strings `lib/routes.ts` had to invent while `OD-10-06`/`OD-DOC-29` are open, the hero's 1586 × 992 master shipped as a 1600 × 1000 export without the `UPSCALE REQUIRED` flag `34` asks for, and `37` §7.1's "served is not reachable in any environment" now being false locally. §8 adds **§8.1** (what the token build emits, including the two recovered/new alphas and the three removed pad tokens) and **§8.2** (what Home renders: 14 image elements, 2 served slots + 1 served pattern ground + 11 reserved, every claim read from a fixture, and the verification's limit — no browser tool was available, so this is an approved *layout*, not an approved *screen*). **No slot size, ratio, byte ceiling, `[BLOCKER]`, demo-data rule or §6.1/6.2/6.3/6.4/6.5 position changed**; the artwork itself remains `GENERATED`/`NOT_APPROVED` and untracked by owner direction. | §3.1, §3.3, §5, §6, §8, Revision History |
| 1.1 | 2026-10-22 | Product Design Lead + Frontend Lead (website design pass, registration step) | The owner answered the question §8 step 1 posed: **go**. The twelve section rows were added to `gen_asset_inventory.py` with the `12` §2.1 element that makes each necessary, the CSV regenerated **93 → 105** and `validate_assets.py` re-run clean (105 rows, 22 manifest records, 0 errors), so a file for any of them can now be intaken rather than refused as unregistered. §3's count paragraph no longer calls them "proposed", §7 says what placeholder-first means once they are rows — a reserved container is legal, a file is not yet — and step 1 is struck through with the half that remains (run the prompts, intake the output). The artifacts row was corrected on measurement: `maintenance/prompts/` holds **9 files**, not 10, because the website's run sheet is two of them. **No slot size, ratio, ceiling, demo-data rule, `[BLOCKER]` or build-order step changed**, and §6.1's unresolved `30` §5.3-versus-register ratio conflict is left open as recorded. | §header, §3, §7, §8, Revision History |
| 1.0 | 2026-10-22 | Product Design Lead + Frontend Lead (website design pass) | First issue, at the owner's direction to design the website with demo data and correct-size imagery. Sections are **measured from `12` §2.1's Key Elements column**, not invented; slot boxes are computed from `30` §5's 12-col/24 px grid at the 1440 and 390 working frames; the demo-data contract restates `XS-02`, `FR-03`, `DD-*` rules from `07`, `13`, `38` and `README` §14.2 rather than introducing new ones; §5 answers the icon-library question inside `36` §4's existing constraints and states the two conditions on installing anything. §6 records **five conflicts on both sides** (`DEC-07`), including the `30` §5.3-versus-register ratio disagreement this pass discovered. **Nothing was scaffolded, installed or approved**; the 12 proposed assets have no register row until the owner says go, and the six blocked category images stay in `maintenance/holding-blocked/` because `32` §6 says a BLOCKED row cannot enter GENERATED. | All |
