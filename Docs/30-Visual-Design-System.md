# 30 — Visual Design System

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-30 |
| Version | 1.3 |
| Status | **PROPOSED — not approved.** Nothing in this document is a requirement until the named owner decides it (`DEC-03`). |
| Owner | Product Design Lead + Frontend Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `12`, `13`, `14`, `23`, `09`, `03`, `06`, `24`, `26`, `29`, `31`, `32`, `34`, `35`, `36`, `37` |
| Blocks | `31`, `32`, `33`; the second instalment, which `26` makes payable **on UI design approval** |

---

## 1. Ownership — why this document exists next to `12`

`12` is the source of truth for information architecture, screens, component *names*, accessibility
rules and performance budgets. It is **not** amended here and is not superseded. This document owns
the things `12` §6.1 deliberately leaves as a list of token *groups* rather than values.

| Concern | Canonical home | Why |
|---|---|---|
| Surface list, navigation trees, screen inventories, component names, A11Y-1…7, performance budgets | `12` §1–§5, §6.2, §6.3, §9 | Unchanged. `33` indexes them; it does not restate them. |
| Token **values** (hex, px, ms, z-index), contrast evidence, state→colour mapping, motion curves | **this document** | `12` §6.1 names groups ("Primary (brand blue)…"); a designer cannot ship a group. |
| Machine-readable tokens | `packages/design-tokens` (`14` §2, `08` rule ML-01) | The typed JSON/TS is the build input. It does not exist yet — there is no source tree in this workspace. |
| Asset IDs, sizes, formats, approvals | `31`, `32` | Production concern, not design language. |
| Screen-level state and asset requirements | `33` | Per-screen view of `12` plus what `12` does not record. |

`OD-12-01 / OD-UX-01` recommends Figma as the design tool with **the token file as source of truth and
Figma variables generated from it**. That row is `[IMPORTANT]` and **undecided**, so the tables below
are the only record of these values today; if the owner reverses it, this document becomes the
generated artefact and `12`/`30` swap roles.

---

## 2. Brand direction and what the workspace actually evidences

**There is no existing brand palette in this workspace.** The four files in
`visualize-image-of-project/` are the only visual artefacts present. Measured dominant colours
(80-px-wide resample, top 7 buckets) are `#FFFFFF`, `#FEFEFE`, `#E6F5FE`, `#F0F9FE`, `#FEE7EF` — pale
infographic renders, ~1.9–2.1 MB each at 1536 × 1024. They evidence a *documentation* style, not a
product identity, and none of their colours is used below as a brand claim. Their provenance record
(tool recorded, prompt/licence/creation-date **not recorded**) is in
`design-assets/manifests/asset-manifest.json`.

Confirmed naming, from the documents rather than from the images:

| Item | Value | Source |
|---|---|---|
| Brand | AmmPal Service | `00` §1 Executive Summary; `20` §8 |
| Customer app | AmmPal Service | `12` §1; `20` §8 |
| Provider app | **AmmPal Partner** | `20` §8 ("AmmPal Partner (app)"); `01` §1 P2 Channels |
| Admin surface | AmmPal Control Center | `12` §1; `16` §5.2 (`admin.ammpalservice.com`) |
| Domain | `ammpalservice.com` | `00` §12 DP-8; `10` §2 base URL; `16` §5.2 |
| Launch region | Odisha; `or` is the default script for Odisha branches | `00` §1; `06` §7 LOC-01 |

Personality as proposed — trustworthy, modern, helpful, local, efficient, accessible — is a
`[PROPOSED]` sentence, not an approved brief. The palette in §3 was `[PROPOSED]` and conflicted with
`12` §6.1, which still says **"Primary (brand blue), Secondary (accent orange)"**. On 2026-10-21 the
owner chose **Scheme A — Deep Teal + Gold** (§3.2–§3.5) as the direction to develop. That is a direction
chosen, **not** a palette approved: `OD-DOC-30` stays open until the sign-off is recorded in `21`,
neither side has been edited into the other (`DEC-07`), and no designer should open Figma before it
closes.

---

## 3. Colour tokens, with measured contrast

Ratios below are computed from sRGB relative luminance (WCAG 2.1 definition) by `contrast.py` — now at
**`maintenance/scripts/contrast.py`**; it took no path arguments, so the move does not affect it — and
re-running it reproduces every figure in this section. They are **not** estimated. `12` §6.3 A11Y-1
requires WCAG 2.1 AA, so the bar is **4.5:1 for body text, 3:1 for large text and for non-text UI
boundaries**.

### 3.1 Why the supplied set was re-based

The palette supplied with the design brief is not wrong — four of its values were measured AA failures
and are corrected below — but the reason it reads as a component-library default rather than as a brand
is a **temperature split**, and it is measurable:

| Group | Hue in the supplied set | Consequence |
|---|---|---|
| Neutrals `#102A43`, `#334155`, `#64748B` | H 209 · 215 · 215 (blue-grey) | the page is tinted **blue** |
| Brand action `#087F8C`, accent `#20A675`, success `#15803D` | H 186 · 158 · 142 (teal → green) | the controls are tinted **teal/green** |

Two temperatures on one screen is what makes a layout feel assembled instead of designed. Every
premium system tints the neutrals **toward the brand hue**, so one temperature runs from the page
background to the button. Scheme A below does exactly that: neutrals sit at H 197–203, the brand hue at
H 185, and the greens at H 158/142 stay confined to *status only*. The supplied set also carried three
near-neighbour greens (`#20A675` H 158, `#15803D` H 142, and the chart `#157A55`), which is how "green"
ends up meaning three unrelated things; here green appears once, as `positive`.

**Scheme A — Deep Teal + Gold** is the proposal the owner was shown and chose on 2026-10-21. Choosing
the direction is not the approval of the design gate; `OD-DOC-30` stays open until `21` says otherwise
(`DEC-03`).

### 3.2 Brand ramp — teal, one hue, eleven steps

`white-on` is the ratio when the swatch is used as a **fill** with white type; `on card` / `on page` is
the ratio when it is used as **type**; `on ink` is its readability on the dark hero surface `#0E2731`.

| Token | Hex | white-on | on card | on page | on ink | Role |
|---|---|---|---|---|---|---|
| `brand.50` | `#E9F3F4` | 1.13 | 1.13 | 1.06 | 13.74 | selected-row ground, hero gradient start |
| `brand.100` | `#CFE6E8` | 1.30 | 1.30 | 1.22 | 11.92 | chip ground, hover ground |
| `brand.200` | `#A6D0D4` | 1.67 | 1.67 | 1.56 | 9.31 | illustration mid-tone, dark-surface secondary text |
| `brand.300` | `#74B6BC` | 2.29 | 2.29 | 2.14 | **6.77** | illustration highlight, **text on ink** ✓ |
| `brand.400` | `#3F97A0` | 3.42 | 3.42 | 3.20 | 4.54 | focus glow, chart series 2 — large type / graphics only |
| **`color.action` = `brand.500`** | **`#0A6E77`** | **5.98** | **5.98** | **5.60** | 2.59 | primary button, active nav, links — **the whole point of the re-base: 5.98 against the old 4.75** |
| `brand.600` | `#086570` | 6.76 | 6.76 | 6.32 | 2.30 | hover |
| `brand.700` | `#075A62` | **7.93** | 7.93 | 7.42 | 1.96 | pressed; also AAA as text |
| `brand.800` | `#064751` | 10.36 | 10.36 | 9.69 | 1.50 | dark footer ground |
| `brand.900` | `#053842` | 12.72 | 12.72 | 11.90 | 1.22 | hero gradient end |
| `brand.950` | `#032A32` | 15.21 | 15.21 | 14.22 | 1.02 | deepest surface in the set |

Every step is monotonic in luminance, so a greyscale print, a low-brightness phone and a colour-blind
reader all still see the same hierarchy.

### 3.3 Neutrals — tinted toward the brand hue, not Tailwind slate

| Token | Hex | on card | on page | ink-on-it | Role |
|---|---|---|---|---|---|
| `color.ink` | `#0E2731` | **15.52** AAA | 14.51 | — | headings, hero text on light, **dark hero surface** (white on it = 15.52 AAA) |
| `color.body` | `#2C4551` | **10.11** AAA | 9.46 | 1.53 | paragraph text on every surface |
| `color.muted` | `#5C7280` | 5.03 AA | **4.71** AA | 3.08 | captions, metadata. Replaces `#64748B`, which measured **4.46 FAIL** on the page background |
| `color.border-strong` | `#5F7484` | 4.86 | 4.55 | 3.19 | **new.** The input boundary. 4.86 also clears the 3:1 non-text rule with margin |
| `color.border` | `#DBE4E8` | 1.29 | 1.21 | 12.03 | decorative dividers only — never the only cue for a control |
| `color.action-subtle` | `#E3F1F2` | 1.16 | 1.08 | **13.40** | selected rows, soft chips. Legality comes from the **ink on it** (13.40), not from itself |
| `color.canvas` | `#F4F8F9` | 1.07 | — | 14.51 | page background. Replaces `#F5F8FA`; H 190, one degree of teal in it |
| `color.surface` | `#FFFFFF` | — | — | 15.52 | cards, sheets, dialog |
| `color.surface-sunk` | `#EAF0F2` | 1.15 | 1.08 | 13.48 | table headers, inset wells |

### 3.4 Metal — the premium lever, and the most misused one

| Token | Hex | on card | on page | on ink | Role |
|---|---|---|---|---|---|
| `metal.tint` | `#F2E3BC` | 1.27 | 1.19 | 12.19 | verified-badge ground, premium-plan card wash |
| `metal.soft` | `#E3CB84` | 1.60 | 1.49 | 9.71 | illustration gold mid-tone |
| `metal.decor` | `#C9A227` | **2.42 — never text on light** | 2.26 | **6.41 ✓** | hairline rules, hero ornament, award marks **on ink only** |
| `metal.text` | `#8A5B0B` | **5.86** AA | 5.48 AA | 2.65 | the *only* gold permitted to carry words, and only on light |

**Budget: metal occupies ≤ 2 % of any screen's pixels.** Gold is what makes the teal look deliberate,
and it stops doing that the moment it becomes a second accent. One hairline in a hero, one rule under a
section title, one badge ground. No gold buttons, no gold body text, no gold borders on inputs.

### 3.5 Semantic colour — one hue per meaning

| Token | Hex | white-on | on card | Role |
|---|---|---|---|---|
| `color.success` | `#15803D` | 5.02 AA | 5.02 | completed money, verified |
| `color.warning` | `#B45309` | 5.02 AA | 5.02 | outstanding balance, pending SLA |
| `color.error` | `#B91C1C` | 6.47 AA | 6.47 | breach, dispute, destructive |
| `color.info` | `#1D4ED8` | 6.70 AA | 6.70 | requested, rescheduled, neutral system notice |
| `color.positive` | `#20A675` | 3.10 | 3.10 | **decoration, icon fill, large type only.** Fails AA as text in both directions — measured, not opinion |
| `color.positive-text` | `#157A55` | 5.32 AA | 5.32 | the green that carries words (savings, rating, "on time") |
| `color.focus` | `#0A6E77` | — | 5.98 (≥3:1 ✓) | 2 px ring, 2 px offset, never colour-only (`12` A11Y-4 logic) |

**Four corrections carried over from the supplied set, and one new ban:** muted → `#5C7280`;
`border-strong` added at `#5F7484`; green split into decorative `positive` and text-safe
`positive-text`; white-on-`#20A675` **prohibited anywhere** (3.10:1 is a fail in both directions, so
there is no legal combination). None of these is cosmetic — each closes a measured AA failure.

### 3.6 Rules that follow from the documents rather than from taste

- **Surfaces are tinted, shadows are tinted.** Shadow colour is `rgba(14, 39, 49, α)` — the ink hue,
  never `#000000`. A pure-black shadow on a blue-tinted page is the single cheapest-looking mistake in
  the set, and it is the one every generated mockup makes.
- **Gradient only inside the brand ramp, only on the marketing surface.** `brand.900 → brand.950` with
  a `metal.decor` hairline is the hero treatment. `brand.500 → #7C3AED` is not: violet does not exist in
  this system except as chart series 6.
- **Saturation budget.** Chromatic fill ≤ 25 % of a screen; large areas use `50`/`100` tints only. A
  full-teal page is not premium, it is a warning.
- **Money is never hue-only.** `12` XS-02 fixes money as `₹1,119.82` in tabular numerals; colour may
  reinforce a sign, never replace it.
- **Out-of-scope data reads as absent.** A permission-denied state must not say "you cannot see this",
  because `03` §5 step 3 returns `404` rather than `403` precisely so existence is not leaked.
- Chart, marker and status palettes are defined in §6, §8 and §9; nothing hard-codes a hex in a
  screen (`12` XS-06: one enum → one i18n file → no per-surface drift).
- `12` §6.1 still reads **"Primary (brand blue), Secondary (accent orange)"**, which is not this scheme.
  That conflict is registered as `OD-DOC-30` and **neither side has been edited into the other**
  (`DEC-07`); Scheme A is what the owner has now chosen to evaluate, and `12` §6.1 is amended in one
  edit the moment `OD-DOC-30` closes.

---

## 4. Typography

### 4.1 What the owner decided about language sequencing (2026-10-21)

Recorded as `[REPORTED]` — the owner stated this; it has not been verified against a build, and it does
not by itself relax `12`:

> "Default language is English, but translate other language if user switch language like Odia and
> Hindi. Currently design time focus in English; after design and programming then make multi-language
> supported. Yes, location-based service and category visible in website or app."

Two consequences, and they point in opposite directions, which is why both are written down:

1. **Design-time assets are English-only.** No per-locale export of a hero, no text baked into an
   illustration, no three-width variants of a category card. This *shrinks* the asset matrix in `31` and
   is why `30` §11's "no text in images" rule costs nothing today.
2. **The layout tolerance is NOT deferred.** `12` §8 i18n-03 requires `or` and `hi` at 100 % coverage and
   a layout that tolerates **30 % string expansion**. Deferring *translation* is a scheduling decision
   the owner is entitled to make; deferring the *expansion tolerance* means every fixed-width label,
   button and chip drawn now gets re-fitted later — and Odia glyphs are taller than Latin ones, so a
   fixed-height label silently clips them. **Rule for this phase: no fixed-height text containers, no
   width-fitted labels, line-height ≥ 1.4 on any string that will ever be localised.** The requirement
   itself stays open as `OD-DOC-35`, because "later" carries no date and `DEC-03` does not let a document
   retire a stated requirement by silence.

The location-based catalogue visibility the owner confirms is already specified (`06` §7 LOC-01,
`12` §3.1/§3.2); that answer invents nothing new here.

### 4.2 Families

| Role | Proposal | Coverage | Self-host consequence |
|---|---|---|---|
| UI everywhere — web, both apps, Control Center | **Inter** 400 / 500 / 600 / 700 | Latin, Greek, Cyrillic. **No Odia, no Devanagari**: an Indic string set in Inter falls through to the next family in the stack | `font-src 'self'` (`13` §5.2) means vendored WOFF2 subsets. A Google Fonts `<link>` or `@import` is **blocked in production**, and a build that works in dev while silently dropping the font in prod is the failure mode this rule exists to prevent |
| Display, **marketing website only** | **Fraunces** 600 with its optical-size axis, tracking `-0.02em` | Latin only | One variable file in the web bundle. **Never inside the Flutter apps** — a second family would be bought into the APK against `12` §9's ≤ 25 MB, and the apps have no hero to spend it on |
| Odia (`or`) | **Noto Sans Oriya** — read the name warning below | Oriya block U+0B00–0B7F | Required by `12` §8 i18n-03 and `FR-CAT-08` |
| Hindi (`hi`) | **Noto Sans Devanagari** (a `… Devanagari UI` variant also exists) | Devanagari block U+0900–097F | Same |

**Name warning, `[UNVERIFIED]`.** The evidence found by search names the Odia family **`Noto Sans
Oriya`** — the `@expo-google-fonts/noto-sans-oriya` package is the concrete instance — while the
language is officially *Odia* (the Unicode block kept the older name). So `font-family: 'Noto Sans Odia'`
risks a string that matches nothing, and under `font-src 'self'` that does not error: it renders in the
system font and nobody notices until a customer screenshots it. `Noto Sans Devanagari` surfaced with 954
glyphs at Google Fonts and a separate UI variant with 922. **The exact `font-family` strings, the weight
axis actually shipped, and the licence text must be confirmed at build time by reading the downloaded
file's name table — not by reading this row.** The font pages themselves could not be fetched in this
session (the fetch was refused with a rate-limit error), so this is a pointer, not a verification. Noto
is SIL OFL 1.1 per the search results; Inter's and Fraunces' licence text is **not verified in this
workspace** and stays routed at `OD-DOC-32`.

### 4.3 Scale

| Style | Desktop | Mobile | Weight | Line height | Notes |
|---|---|---|---|---|---|
| Display / hero | 48–56 px | 32–36 px | 700 | 1.1 | **Fraunces on the web hero, Inter 700 in the apps** — the apps get their hierarchy from size and weight, not from a second voice |
| Section title | 28–34 px | 22–26 px | 600 | 1.15 | A `metal.decor` hairline sits under it on the marketing surface only: one per page, not one per card |
| H1 | 32–40 px | 24–28 px | 700 | 1.15 | One per screen (`12` A11Y-6) |
| H2 | 24–30 px | 20 px | 600 | 1.2 | Section heads in detail pages |
| H3 | 18–20 px | 16–18 px | 600 | 1.25 | Card titles |
| Body | 16 px | 16 px | 400 | **1.55** | **16 px is the floor for input text**; never 14 px for a paragraph. Raised from 1.5 so the same paragraph clears Odia ascenders when `or` is switched on |
| Secondary | 14 px | 14 px | 400 | 1.45 | Captions under a control |
| Caption / metadata | 12 px | 12 px | 400–500 | 1.4 | Minimum size; `color.muted` only |
| Button / nav label | 14–16 px | 14–16 px | 600 | 1.2 | ≥ 44 × 44 px / 48 × 48 dp target (`12` A11Y-2) |
| Money / table numeric | inherit | inherit | 400–600 | 1.3 | `font-variant-numeric: tabular-nums` (`12` XS-02); right-aligned; never justified |
| Dense dashboard table | 13 px | — | 400 | 1.35 | **Exception, scoped**: Finance/Reports DataTables only, on `#FFFFFF`, `color.body` ink, with a 44 px row height so the target stays legal |

Tracking: `-0.02em` above 24 px, `0` from 16–24 px, `+0.01em` on 12 px captions and all-caps labels.
Never letterspace a numeric column — it breaks the tabular alignment money depends on.

### 4.4 Loading and fallback

Subset WOFF2 per locale (Latin subset for `en`/`hi`, Oriya subset for `or`), `font-display: swap`, and a
**metrics-matched** fallback (`system-ui`) so the swap does not move layout — CLS < 0.1 is a stated
budget in `12` §9 and in `13` §2.2, and a font swap is a classic CLS source. Because the design phase is
English-only (§4.1), the Indic subsets are **not** needed to draw a screen; they are needed before `or`
or `hi` can be switched on, which makes it a `29` release item rather than a design item. Stack order
matters: `Inter, 'Noto Sans Oriya', system-ui, sans-serif` — the Indic family sits *after* Inter and is
never named in a `font-family` used for Latin text, or Latin glyphs get substituted as well.

---

## 5. Layout, spacing and elevation

| Group | Tokens | Source |
|---|---|---|
| Spacing | 4 px base: `4 8 12 16 24 32 48 64` | `12` §6.1 — accepted unchanged |
| Radius | `4 / 8 / 12 / 16 / 999` | `12` §6.1 — accepted unchanged |
| Elevation | 3 shadow levels, border-first | `12` §6.1 — accepted; a card that needs a shadow *and* a border is a signal the surface hierarchy is wrong |
| z-index layers | `base 0 · sticky 10 · overlay 20 · dialog 30 · toast 40 · sheet 50` | Proposed here; **must be declared once** in tokens. Unscoped `z-index: 9999` is how Control Center modals end up under toolbars. |
| Touch targets | 48 × 48 dp mobile; 44 × 44 px web | `12` A11Y-2 |
| Icon viewports | 20 / 24 px, one outline set | `12` §6.1 |
| Focus ring | 2 px `color.focus`, 2 px offset, visible on `:focus-visible` | Proposed; required by WCAG keyboard operability |
| Working frames | web desktop 1440 px, web mobile 390 px, apps 390 × 844, CC 1440 × 1000, partner dashboard 1366–1440 **if approved** | Frames, not supported-size claims. The supported-device matrix is a `29` release question, not a design decision. |
| Breakpoints | 390 / 600 / 904 / 1280 / 1440 | Proposed; CC sidebar collapses below 1280 |
| Grids | web 12-col / 24 px gutter; tablet 8-col; CC 12-col with a 240–280 px fixed sidebar | Proposed |

Responsive behaviour that the documents already require and that layout must therefore honour:
table overflow on mobile (`12` §6.2 DataTable) needs an alternative view, not horizontal scroll,
because the same data must be readable on a 390 px screen; the partner app's checklist screen is
one-handed and offline-first (`12` §4.3), so no bottom sheet may cover the capture control.

### 5.1 Elevation — tinted, three levels, border-first

Shadow colour is derived from `color.ink`, never from black. `12` §6.1's "border-first" rule stands: a
surface earns a shadow when it lifts (dialog, sheet, sticky bar), and a card on the canvas gets a
**1 px border plus level 1 at most** — a card that needs both a strong shadow and a border is a signal
the hierarchy is wrong.

| Token | Value | Use |
|---|---|---|
| `elevation.1` | `0 1px 2px rgba(14,39,49,.06), 0 2px 4px rgba(14,39,49,.04)` | Cards, tiles, sticky table header |
| `elevation.2` | `0 4px 12px rgba(14,39,49,.10), 0 1px 3px rgba(14,39,49,.06)` | Dropdown, popover, bottom sheet at rest |
| `elevation.3` | `0 12px 32px rgba(14,39,49,.16), 0 2px 6px rgba(14,39,49,.08)` | Modal, command palette, toast stack |
| `elevation.action` | `0 2px 6px rgba(10,110,119,.24)` | Primary button at rest — a **brand-hued** glow, not a grey shadow. This is what makes a teal button look manufactured rather than pasted on |
| `elevation.hero` | `inset 0 -1px 0 rgba(201,162,39,.55)` | The `metal.decor` hairline that closes the dark hero band |

Two alpha layers per level (a tight one for the edge, a wide one for the fall-off) is what reads as
depth; a single blurred layer at 20 % reads as a smudge.

### 5.2 Effects — what "premium" is allowed to cost

The brief asks for an attractive, animated, effect-led feel. `13` §2.2 sets LCP < 2.5 s, CLS < 0.1 and
INP < 200 ms and **has never been measured on a real device** (`13` §2.2 note), and `12` §9 caps the APK
at 25 MB. So effects are permitted where they are cheap and prohibited where they are not, per surface:

| Effect | Marketing web | Customer app | Partner app | Control Center |
|---|---|---|---|---|
| Gradient | `brand.900 → brand.950` hero band, **two stops max, one hue family** | Header tint only | Not used (offline list performance) | Not used |
| `backdrop-filter: blur` | Allowed, **one layer**, hero nav only | **Prohibited in scrolling lists** — blur cost is per-pixel per-frame on a mid-range Android | Prohibited | Prohibited: the CC budget is 100 ms perceived interaction (`12` §9) with a 43-item nav |
| Parallax / scroll-jacking | Prohibited | Prohibited | Prohibited | Prohibited |
| Count-up on numbers | Allowed on the web home once, in view | Prohibited on money — a figure that animates to its value invites a misread of an amount (`12` XS-02) | Prohibited | Prohibited in Finance/Reports tables; KPI tiles may cross-fade |
| Lottie | One brand loader | ≤ 1 payload, ≤ 40 KB, budgeted like an image (`32` §4) | Prohibited in the checklist flow — it is one-handed and offline (`12` §4.3) | Not used |
| Skeleton shimmer | `color.surface-sunk → surface` sweep, ≤ 1.8 s cycle | Same | Same | Same; **stops when data lands** (§7 prohibition 3) |
| Hover lift / scale | `translateY(-2px)`, 150 ms, on cards only | n/a (touch) | n/a | Row highlight in `brand.50`, no movement — 43 icons and 200-row tables do not move |
| Gradient text | **Prohibited.** It is the tell of a template | — | — | — |
| Text drop-shadow | **Prohibited.** It destroys AA contrast on photographs | — | — | — |

Anything drawn over imagery (a hero headline, a chip on a category photo) carries a **scrim**, not a
shadow: `linear-gradient(180deg, rgba(14,39,49,.65), rgba(14,39,49,.85))` under the text block. The
alpha values are measured, not guessed, against the **worst case a photograph can present** — a
near-white region, where the composite is brightest and white text is weakest:

| Scrim α over a pure-white photo region | Composite | White text | Verdict |
|---|---|---|---|
| .45 | `#939EA2` | 2.74 | **FAIL** — the usual "look, it's dark enough" value |
| .55 | `#7A888E` | 3.66 | large / bold text only (≥ 24 px or 18.5 px bold) |
| **.65** | `#627379` | **4.94** | **the floor** — the first α at which body-size white text is legal |
| .75 | `#4A5D64` | 6.91 | comfortable; where the headline actually sits |

So the gradient starts at .65 and deepens to .85: no white body copy may sit in a lighter band than
.65, and a photograph that is mostly sky or white tile is handled by moving the text **beside** the
image, not on it. There is no α that makes white-on-photograph safe in principle, because the
photograph is not a token.

### 5.3 Placeholder-first delivery — decided 2026-10-21

The owner directed that design work proceed with **SVG or blank containers**, with real imagery arriving
when the upload/storage system is implemented. `[CONFIRMED — direction]` for this phase; the storage
decision itself is open as `OD-DOC-34`.

Every image slot in every screen drawn from now is a **reserved container**, not an `<img>`:

| Property | Value | Why it is this and not something prettier |
|---|---|---|
| Aspect ratio | Fixed per asset class: category tile `4:3`, hero `16:9`, avatar `1:1`, job photo `4:3`, OG image `1.91:1` (`32` §3) | The container, not the picture, holds the layout. This is what keeps CLS < 0.1 honest when a real image finally lands |
| Ground | `color.surface-sunk` `#EAF0F2` with a 1 px `color.border` `#DBE4E8` | Reads as "intentionally empty", not as a broken render |
| Radius | Inherited from the owning component's token | A placeholder that looks like a different component gets mistaken for finished work |
| Fallback glyph | Inline **SVG** at 24–48 px, stroke `color.muted` `#5C7280`, one icon per asset class | Vector, ~1 KB, no network request, crisp at every density. A broken-image icon is a defect; a glyph is a decision |
| Accessible name | `aria-label` describing the **slot** ("Service image — pending"), never a description of a picture that is not there | An `alt` that invents content is a false statement to a screen-reader user and to `29` §4.8's a11y item |
| Never | Grey checkerboard, "IMAGE HERE" lorem text baked into a component, a 1×1 transparent stretched to 16:9 | All three ship into screenshots and then into the store listing |

Consequence for the design gate: **a screen reviewed with placeholder containers is not an approved
screen.** It is an approved *layout*. `33` records that distinction per row, and `29` §4.8 already
refuses a release whose shipped screens reference unapproved assets — the mirror image of that rule is
that no amount of placeholder work can be presented as delivered brand imagery.
---

## 6. Status colour — bound to the documented state machines

Colours are assigned to the **canonical codes in `23` §2.3 and the phases in §2.4**, not to invented
labels. Per `12` A11Y-4 every one of these renders as **text + icon + colour**, never colour alone.

| Canonical status (`23` §2.3) | Token | Hue family |
|---|---|---|
| `REQUESTED` | `color.info` | blue |
| `ACCEPTED`, `EN_ROUTE` | `color.action` | teal (in-motion, platform-confirmed) |
| `STARTED`, `COMPLETED` | `color.warning` | amber (work outstanding: balance, invoice) |
| `CLOSED`, `REFUNDED` | `color.success` | green (`REFUNDED` is a completed money movement, not an error) |
| `CANCELLED_BY_CUSTOMER`, `CANCELLED_BY_TECHNICIAN`, `REJECTED`, `EXPIRED` | `color.muted` | neutral (a cancellation is not an incident) |
| `NO_SHOW`, `DISPUTED` | `color.error` | red |
| `RESCHEDULED` | `color.info` + reschedule glyph | blue |
| `REFUND_PENDING` | `color.warning` + refund glyph | amber |

Phase overlays (`AWAITING_PARTNER`, `AWAITING_CUSTOMER_APPROVAL`, `SUSPENDED`, `REASSIGNING` …) render
as a **neutral chip with the phase word**, because a phase is an elapsed-time claim (`23` §2.4 carries
the SLA minutes) and a saturated colour would read as a breach that has not been declared.
`SUSPENDED` is the one phase permitted to use `color.error`, matching its operator-held meaning.

**The SLA relationship is a rule, not a colour choice:** an item turns red only when `23` §2.4's SLA
has actually elapsed, never when the UI guesses. The tracking screen already commits to telling the
truth about freshness ("updated 30 s ago", `12` §3.3).

---

## 7. Motion

`12` §6.1 already fixes three durations: 150 ms micro, 250 ms transition, 400 ms page. The bands
proposed for this phase (100–160 / 180–240 / 250–400) **overlap but are not identical**: 250 ms falls
outside the proposed "standard" band's ceiling of 240 ms. Resolution taken here, recorded rather than
silently chosen: **`12`'s values win** as the token set — `motion.fast 150`, `motion.base 250`,
`motion.page 400` — and the bands become the acceptable tolerance around them (fast 100–160, base
220–280, page 350–400). Nothing is re-invented, and `12` is not edited.

| Token | Value | Use |
|---|---|---|
| `motion.fast` | 150 ms (100–160 allowed) | Press states, chip toggles, tooltips |
| `motion.base` | 250 ms (220–280) | Sheets, drawers, accordions, tab cross-fade |
| `motion.page` | 400 ms (350–400) | Route transitions; app only — CC routes use `fast` because its budget is 100 ms perceived interaction (`12` §9) |
| `motion.shimmer` | 1.2–1.8 s cycle | Skeletons **only while a request is in flight** |
| `ease.standard` | cubic-bezier(.2,0,.13,1) | Enters and settles without overshoot |
| `ease.exiting` | cubic-bezier(.4,0,1,1) | Leave fast |
| `ease.entering` | cubic-bezier(.16,1,.3,1) | **Added for Scheme A.** A long, decelerating settle is what makes a sheet feel machined rather than dropped; use for enter only, never for exit, and never with overshoot in the apps |
| distance | 8 px slide, ≤ 4 px scale | No parallax, no scroll hijacking |
| stagger | 30–40 ms per sibling, **max 6 items**, first paint immediate | List and KPI-tile entry. Beyond 6 items a stagger is a wait, and `12` §9's 100 ms perceived-interaction budget for the Control Center is spent on the first row, not the last |

Hard prohibitions, each traceable to a documented rule:

1. **An animation is never evidence of a state.** The source of truth is the backend status (`23` §2.3)
   and the socket/poll freshness (`12` §3.3). A booking that "succeeds" visually while the POST failed
   is a defect with financial consequences, not a polish problem.
2. **No repeat submission.** While an action is in flight the control is disabled *and* shows the
   in-flight state; `23` §3.2 idempotency exists because double-taps happen.
3. **No looping decoration.** Shimmer stops when data lands; nothing animates to imply progress a
   payment or a job has not made (`23` §11.2, §12).
4. **`prefers-reduced-motion`** (`12` §6.1) removes all translation and scale, keeps opacity ≤ 150 ms,
   and never removes a state *change* — the change must still be announced (`12` A11Y-7).
5. **Low-end Android is the constraint**, not the desktop browser: `12` §9 sets cold start < 2.5 s and
   APK ≤ 25 MB, so motion must be compositor-only (transform/opacity), and Lottie payloads are
   budgeted like images.

---

## 8. Data visualisation

Reporting screens and per-role KPIs are defined in `12` §5.2 and §5.3; this section only fixes how they
may be drawn.

- One series palette, **ordered by descending measured luminance on white** so a greyscale print still
  reads, and every member clears AA as a label or a legend swatch on both card and canvas:
  `#0E2731` 15.52 · `#1D4ED8` 6.70 · `#0A6E77` 5.98 · `#8A5B0B` 5.86 · `#7C3AED` 5.70 · `#157A55` 5.32 ·
  `#5C7280` 5.03. Never more than 6 series without a legend interaction. `color.error` and
  `color.warning` stay out of the series list entirely.
- `color.error` is reserved for breaches and disputes; it is not a category colour.
- Every chart encodes its value in a label or a table alternative — a `DataTable` with export already
  exists in `12` §6.2, and a chart that cannot be read is that table's reason to exist.
- Money axes use `12` XS-02 formatting; commission and margin axes use **bps-labelled** values, since
  `07` carries rates as basis points and a "15 %" axis that is really 1500 bps invites a rounding story.
- Coverage boards (`12` §5.2) use the documented RED/AMBER/GREEN serviceability states from
  `23` §5 (ADR-004) and must pair each with a text label (A11Y-4).

---

## 9. Maps and markers

`13` §5.2's CSP allows `img-src 'self' … https://maps.googleapis.com https://maps.gstatic.com
https://*.googleusercontent.com` — **so the launch map layer is Google Maps, not a self-hosted PostGIS
tile server.** PostGIS (`09`) is the geometry store, not the imagery source, and the marker assets in
`31` are Google-Maps overlays, to be validated against the SDK actually chosen
(`OD-08-01`/`OD-08-05`/`OD-10-06` remain open; `OD-DOC-29` blocks endpoint/permission joins).

- Markers 32 × 40 px SVG; anchor at the tip; selected state adds a ring, not a size jump (a size jump
  shifts the point the marker is claiming to be at).
- Clustering shows a count; a cluster is never drawn as a technician, because a customer reads it as
  "a person is here now".
- **Demo, screenshot and marketing map imagery must use synthetic coordinates.** A real job site is
  `PERSONAL` data (`09` §8 — "job photos can contain a person and their home"); an export of a live
  coverage board is a privacy incident wearing a design-asset costume.
- The live-tracking marker obeys the same freshness honesty as `12` §3.3.

---

## 10. Dark mode

**No document in `00`–`29` states a dark-mode requirement** (checked across `12`, `13`, `01`, `17`).
Proposed policy for the launch: **light only.** Rationale is cost and risk, not preference — every
token above would need a second measured contrast pass, the CSP self-hosted font subsets and map
imagery both behave differently on dark surfaces, and `12` §9's budgets are already tight on a
mid-range Android.

Consequences of choosing light-only, which must be accepted explicitly:
`prefers-color-scheme: dark` may not invert the page (force `color-scheme: light`), Google Play's
dark-theme rendering of any system dialogs is out of our control, and the decision is a
`[PROPOSED]` one, registered as `OD-DOC-31` for the owner.

One thing Scheme A buys for free: §3.2's `on ink` column is already the first contrast pass for a dark
theme (`brand.800/900/950` as surfaces, `brand.200/300` and `metal.decor` as the legal text hues on
them, all measured ≥ 6.4:1). If `OD-DOC-31` is ever reversed, the ramp does not need re-deriving — but
the light-theme tables would still need the full second pass, which is the cost this proposal defers.

---

## 11. Iconography, illustration and the SVG-first rule

**Decided 2026-10-21 by the owner, and it is the correct call:** at design time the product uses
**SVG or a blank container**, and real imagery arrives when the upload system is implemented
(§5.3, and the storage decision `OD-DOC-34`). That settles the medium question that `31` and `32` had
left open, and it has one consequence nobody should discover late — **an image-generation model is the
wrong tool for most of this inventory.**

| Asset class | Rows in `32`/`31` | Correct source | Why a raster model is wrong here |
|---|---|---|---|
| Nav + action icons | 43 (CC nav) + ~6 | **Vendored open-licensed SVG set** (Lucide or Tabler class), retuned to one stroke weight | A 1024 px PNG flattened to 24 px is mush; per-icon files generated separately never share a stroke weight, a corner radius or an optical size, so a 43-icon nav looks like 43 opinions |
| Logo, mark, app icon, favicon, `og-image` base | ~7 | **Vector artwork with a declared construction** (grid, geometry, one SVG source, export sizes derived from it) | A mark must be reproducible, must survive 16 px, and must be *claimable* — `OD-COM-12` asks whether generated design assets can be brand-owned at all, and "the model drew it" is not an assignment chain |
| Category / service icons | per category | Same vendored SVG set, one glyph per family | Same drift argument, plus these are inside the disputed launch-category count (`OD-DOC-27`/`28`) |
| Store screenshots | 1 row, `screenshot-set`, `BLOCKED` | **A real build** | A generated mockup of an app that does not exist is the prohibited artefact, not a placeholder for one |
| Illustrations, empty/success/error states, hero art, patterns, photo placeholders | ~50 | **This is the class an image model is actually for**, run from `34`'s prompt pack when the owner pulls the trigger | — |

So the placeholder-first decision does not defer the artwork problem; it defers *spending on* the
artwork, and it makes the vector work the thing that has to be right now.

- **One outline set**, 20 / 24 px, one stroke weight (`12` §6.1). Proposal: **1.5 px at 24 px**, which
  is 6.25 % of the box — the value that keeps a 20 px rendering from closing its own counters. Vendored
  into the build, not fetched from a CDN: `13` §5.2's CSP is `'self'`-first, and an icon font or remote
  SVG is a third-party dependency disguised as a stylesheet.
- **Illustration direction** for empty / success / serviceability states: single scene, one-point
  perspective, **line in `color.body` `#2C4551`, one fill in `brand.50` `#E9F3F4`, one accent in
  `color.action`**, `metal` permitted only as a badge or a star. No faces, **no text in the image**
  (text in images breaks `12` §8 i18n-03 expansion and forces a per-locale export — and §4.1 makes the
  design phase English-only today, which is a reason to keep the rule, not to drop it).
- **Photography direction, when it is possible to serve it**: real appliances, real Odisha homes,
  uniform in brand teal, natural light, no stock-smile staging, and the §5.2 scrim under any text
  drawn on it. **No photograph may be presented as an actual registered partner** — the technician card
  shows `technicians.photo_url` from `09` §4.4 and a placeholder is labelled as one. Generating a
  "technician at a customer's home" is also the case where a synthetic face most easily reads as a real
  person, so it needs the `32` provenance record and a visible non-real label if it ever ships.
- **Rejected direction, stated so nobody re-proposes it:** mascot characters, 3D isometric "tech" art,
  gradient meshes on status chips, gradient text, AI-generated "app screenshots", and any purple/blue
  neon SaaS hero — none of which is in this system's hue range.

---

## 12. What the owner must actually decide

| # | Decision | Registered as | Effect of not deciding |
|---|---|---|---|
| 1 | **Sign off Scheme A as the brand palette**, or correct it — including the four measured AA fixes and the `metal` budget in §3 | `OD-DOC-30` (still conflicts with `12` §6.1 "brand blue / accent orange"; choosing a direction is **not** this approval) | Nothing downstream can be exported; `26`'s UI-approval instalment cannot be certified; `12` §6.1 cannot be amended |
| 2 | Design tool of record | `OD-12-01 / OD-UX-01` | Tokens have no build home; §1's swap risk stays live |
| 3 | Does the catalogue carry photography at all, or icons only? | `OD-DOC-25` — **eased** by the placeholder-first direction: nothing ships either way until `OD-DOC-34` closes | ~18 category/detail exports are undefined work |
| 4 | Where catalogue media is stored and served | `OD-DOC-26` (`09` has no media column on `categories`/`services`/`service_variants`) — now carries the owner's `[REPORTED]` answer, see row 9 | Approved assets have nowhere to be referenced from |
| 5 | Dark mode for launch | `OD-DOC-31` | §10 stays a proposal; second theme may arrive as an emergency |
| 6 | IP and licence position on generated design assets | `OD-COM-12` (open; `26` records design-asset IP as "not yet documented") | No generated mark can be claimed as brand-owned |
| 7 | Font licensing, subsetting and who owns that pipeline; **and the exact `font-family` strings for the Indic families** (§4.2 name warning) | `OD-DOC-32` | A `font-src 'self'` CSP with no self-hosted subset = silent fallback typography in production |
| 8 | Launch category set | `OD-RM-04`, plus `OD-DOC-27` (3 vs 4 vs 6) and `OD-DOC-28` (salon/beauty in `06` §4 but `17` §6) | The category asset count cannot be fixed |
| 9 | **Media storage: Cloudinary as primary with a pluggable second provider, configured by a super admin.** This is not compatible with `13` §5.2's `img-src 'self'` as written, nor with `24` §11's "no bucket, prefix or object is publicly readable", and job photos are `PERSONAL` data (`09` §8) leaving the platform's own storage boundary | `OD-DOC-34` `[BLOCKER]` | CSP blocks every production image; the storage abstraction has no schema, no endpoint and no permission token; the DPDP/processor question is unasked |
| 10 | **Multi-language is deferred until after design and programming** — confirm, and give it a phase, because `12` §8 i18n-03 currently states it as a launch requirement | `OD-DOC-35` `[IMPORTANT]` | Screens are drawn at Latin width and re-fitted later; `29`'s release gate and `28`'s traceability both still cite 100 % `or`/`hi` |
| 11 | **Placeholder-first as the delivery method** — that a layout review is not an image review, and that no screen with a blank container can be called designed | `OD-DOC-36` `[IMPORTANT]` | The design gate gets certified against an empty page; `33`'s `UNDESIGNED` counts stop meaning anything |
| 12 | **A super-admin storage-provider configuration surface** — which Control Center screen, which route, which permission token | `OD-DOC-37` `[IMPORTANT]`, and it **cannot be answered before `OD-10-06` / `OD-DOC-29`** (no screen→route→token join exists) | The one new admin capability this pass asks for has no screen, no endpoint and no guard |

Rows 1–8 are unchanged from the first issue except where a 2026-10-21 owner answer moved them; rows
9–12 are new, and they are the reason this document did not simply get on with generating artwork.
**Nothing in §3, §4, §5 or §11 is approved** — the owner picked a direction, which is the input to
decision 1, not its output (`DEC-03`). Each row has a named owner in `21`.

**There is no row 13, and that is deliberate.** The decisions the design-engineering pass opened on
2026-10-21 — `OD-DOC-38` (which backend framework), `OD-DOC-39` (where the workers live) and
`OD-14-09`…`13` (styling engine, animation runtime, charting and grid, workshop and visual regression,
token build) — are decisions about **construction**, not about appearance. They belong to `35` §2 and
`36` §9, are registered in `21`, and are not restated here (`DEC-01`). The one that changes what this
section lists is `OD-14-13`: until the token build is decided, the values in §3–§7 exist only as text
in this document, and `PS-11` already forbids copying them by hand into a component.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.3 | 2026-10-21 | Product Design Lead (tooling and backup relocation) | §3's measurement citation was wrong and is corrected: it named `_ramp.py` **and** `contrast.py` 'in the project root', and **`_ramp.py` exists nowhere in this workspace** — a reference to a scratch file that was never kept, which would have left every contrast figure in this document citing a tool a reader cannot find. The section now names `maintenance/scripts/contrast.py` and states that re-running it reproduces the figures; it was re-run for this edit and returned the same ratios. **No token value, measured ratio, rule or recommendation changed** — the numbers already on file are the numbers the script prints. The palette remains `PROPOSED` and `OD-DOC-30` remains open. | §3 |
| 1.2 | 2026-10-21 | Product Design Lead (design-engineering structure pass) | Depends On gained `35`, `36`, `37`. §12 gained a paragraph explaining **why there is no row 13**: the decisions the design-engineering pass opened — `OD-DOC-38`, `OD-DOC-39`, `OD-14-09`…`13` — are about **construction**, not appearance, so they live in `35` §2 and `36` §9 and are registered in `21`, and restating them here would be the second copy `DEC-01` forbids. One consequence is named rather than left to be discovered: until **`OD-14-13`** (the token build) closes, the values in §3–§7 exist only as text in this document, while `PS-11` already forbids copying them by hand into a component. **No token value, measured contrast pair, ramp step, motion curve, metal budget, scrim alpha or effect budget was altered**, and nothing in §3, §4, §5 or §11 became approved by this edit — the owner’s Deep Teal + Gold choice is still the input to `OD-DOC-30`, not its output. | §12, Depends On, Revision History, header |
| 1.1 | 2026-10-21 | Product Design Lead + Frontend Lead (palette, type and effects pass) | Owner chose **Scheme A — Deep Teal + Gold**; §3 rebuilt as measured 11-step brand ramp + hue-tinted neutrals + `metal` scale + semantic set, with the temperature split that made the supplied palette read as a template measured (neutrals H 209-215 vs brand H 186-142) and the action's contrast raised from 4.75 to 5.98 on card; §3.6 bans pure-black shadows and off-ramp gradients; §4 rewritten for the owner's `[REPORTED]` English-first-at-design-time answer, adds Fraunces display on the marketing surface only, flags the `Noto Sans Oriya` vs `Odia` family-name trap as `[UNVERIFIED]` (the font pages could not be fetched this session), and holds the 30 % expansion tolerance as non-deferrable; §5 gains tinted elevation levels, a per-surface effects budget with the blur prohibition, and the measured image scrim table (.65 is the floor for body-size white text); §5.3 states the **placeholder-first** rule; §7 adds `ease.entering` and a stagger limit; §8 series palette re-measured; §10 notes the ramp already supplies the dark-theme first pass; §11 becomes the SVG-first rule with a per-class table of what an image model must not be used for; §12 gains decisions 9-12 (`OD-DOC-34`…`37`). **No hex, ratio, alpha or easing value was estimated — all were computed; nothing is approved.** | §2, §3, §4, §5, §7, §8, §10, §11, §12 |
| 1.0 | 2026-10-21 | Product Design Lead + Engineering Lead (documentation pass) | First issue. Token values proposed with measured WCAG contrast (`contrast.py`), four AA failures corrected against the supplied palette; ownership split with `12` stated; status colours bound to `23` §2.3/§2.4; motion reconciled with `12` §6.1 rather than redefined; dark mode, catalogue photography, IP and font pipeline registered as open (`OD-DOC-25`…`32`, `OD-COM-12`) rather than assumed. Brand palette marked PROPOSED because the workspace contains no brand asset and the four reference PNGs measure as near-white infographics. | All |
