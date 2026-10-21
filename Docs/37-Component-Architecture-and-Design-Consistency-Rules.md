# 37 — Component Architecture and Design-Consistency Rules

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-37 |
| Version | 1.0 |
| Status | **PROPOSED — not approved.** A build contract for code that does not exist yet. **No component, no `packages/ui`, no Storybook and no build is present in this workspace**; nothing here has been rendered in a browser. |
| Owner | Frontend Lead (web + Control Center) + Mobile Lead (Flutter), with Product Design Lead for the contract in §4 |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `12` §6.2/§6.3/§7, `14` §6 (`FE-01`…`FE-08`, `FL-01`…`FL-08`), `30` §3–§9/§11, `33` §5, `35` §6–§9, `36` §3/§4/§5, `13` §5.2, `21` §3/§7 |
| Blocks | `29` §4.8's consistency gate, `33` §5's gap closure, and every screen built from a component in §2 |

---

## 1. What this owns, and the one thing it may never do

| Question | Home |
|---|---|
| What a token is **worth** (hex, ratio, duration, easing, alpha, shadow) | `30` §3–§7 |
| Which **library** supplies a capability | `36` |
| Which **component exists**, by name | `12` §6.2 — the canonical list |
| Which component appears on which **screen**, in which states | `33` |
| **Where files go** | `35` |
| **How a component is built, composed, themed and reviewed** | **this document** |

**Rule CA-00 (the one that matters).** This document never adds a component name. `12` §6.2 is the
single place a component enters the system (`DEC-01`), and `33` §5 already lists eight components the
screens demand that `12` §6.2 does not yet name — ServiceCard, BookingSummary, a compact status
indicator, EstimateApproval, PaymentSummary, InvoiceView, ErrorState, PermissionDeniedState. Those eight
are **gaps awaiting an owner amendment**, not a licence to create them here. A component invented in
code and missing from `12` §6.2 will exist on one surface only, which is precisely the drift `12` §7
`XS-03`/`XS-04` forbid.

---

## 2. The four-layer model, and the only allowed import direction

| Layer | Contains | May import | Never contains |
|---|---|---|---|
| **1 · Tokens** | `packages/design-tokens` — names and values only (`35` `PS-12`) | nothing | markup, components, framework code |
| **2 · Primitives** | the `12` §6.2 foundation row: Button, IconButton, Input, Select, DatePicker, TimePicker, Checkbox, Radio, Switch, Slider, Stepper, Chip, Tag/Badge, Avatar, Tooltip, Toast, Snackbar | tokens, a11y primitives (`36` §4) | domain concepts, API types, i18n strings |
| **3 · Composites** | SearchField, FilterBar, StatusChip, MoneyField, DataTable wrapper, Sheet, ConfirmDialog, Skeleton, EmptyState | layers 1–2 | a screen's business rules |
| **4 · Domain patterns** | BookingStatusTimeline, PriceBreakdownSheet, TechnicianCard, SlotGrid, OTPInput, EvidenceUploader, CallPanel, SettlementTable, ScopeBadge (`12` §6.2's Domain row) | layers 1–3, the generated client (`ADR-012`, `ML-02`) | another screen's state, another surface's copy of itself |

```
1 Tokens  →  2 Primitives  →  3 Composites  →  4 Domain patterns  →  Screens
     ↑                                              ↑
     └────────── every layer may read tokens ───────┘
```

**Rule CA-01** — imports point one way. A primitive that renders a booking status, or a domain pattern
that reaches into a vendor kit, fails review (`36` `LB-07`).
**Rule CA-02** — anything two surfaces want is promoted to `packages/ui` **once**, with both call sites
updated in the same change (`35` `PS-21`). `XS-03`'s "identical status timeline on web, app and Control
Center" and `XS-04`'s fixed line order are enforced by this rule, not by good intentions.
**Rule CA-03** — a component's public surface is its folder's `index.ts` (`14` `TS-05`: barrels at
module roots only). Deep imports into another component's internals are refused.

---

## 3. File layout inside one component

```
packages/ui/src/status-chip/
├── status-chip.tsx           # the component; props typed, no `any` (14 FE-04, TS-02)
├── status-chip.variants.ts   # the variant map: tone × size × emphasis, all bound to token names
├── status-chip.css           # or the styled equivalent per OD-14-09; no hex, no literals (PS-07)
├── status-chip.test.tsx      # states asserted (§4), a11y asserted (12 §6.3)
├── status-chip.stories.tsx   # the workshop case per state, incl. forced-colors and reduced-motion
└── index.ts                  # the only public entry (CA-03)
```

| Rule | Detail |
|---|---|
| CA-04 | One component per folder, kebab-case file names, folder name = component name. This mirrors the discipline `32` §2 imposes on asset files: a name that can be validated is a name that stays true. |
| CA-05 | The variant file is the **only** place a visual state is declared. A `.tsx` that sets `background` imperatively has duplicated the design system. |
| CA-06 | Every component folder ships its workshop case and its test in the same commit as the component. A component without a visible state list is unreviewable while placeholders stand (`30` §5.3, `OD-DOC-36`). |

---

## 4. The component contract — what "done" means for every component

A component is finished when all ten rows below hold. This is the checklist `29` §4.8 and the design
review both read, and it is derived from existing rules rather than added to them.

| # | Requirement | Source |
|---|---|---|
| 1 | **Every visual state exists as code**: default, hover, pressed, focus-visible, disabled, loading, error — plus the four screen-level states `14` `FE-07` demands (loading skeleton, empty, error-with-retry, permission-denied) | `12` §6.2, `33` §5, `14` FE-07 |
| 2 | **Contrast verified, not assumed** at the token level: 4.5:1 body, 3:1 large text and non-text boundaries | `12` A11Y-1, `30` §3 (measured by `contrast.py`) |
| 3 | **Touch target** ≥ 48 × 48 dp on mobile, ≥ 44 × 44 px on web, even when the visual box is smaller | `12` A11Y-2 |
| 4 | **Labelled and associated**: programmatic label; error text linked via `aria-describedby`; a name for every non-text control | `12` A11Y-3, `14` FE-08 |
| 5 | **Never colour alone**: status carries text + icon + colour; `color.focus` ring is 2 px with 2 px offset on `:focus-visible` | `12` A11Y-4, `30` §3.5/§5 |
| 6 | **Motion honoured both ways**: `prefers-reduced-motion` removes translation and scale, keeps opacity ≤ 150 ms, and **never removes a state change** — the change must still be announced | `30` §7 prohibition 4, `12` A11Y-7 |
| 7 | **Money and rates are formatted by the shared formatter** (`₹1,119.82`, tabular numerals; bps for rates), never by a component-local `toFixed` | `12` XS-02, `14` `TS-08`, `35` `PS-04` |
| 8 | **Strings come from the i18n catalogue**; a lint rule fails the build on a hard-coded string, and no text lives inside an image | `14` `FE-05`, `12` §8 i18n-03, `30` §11 |
| 9 | **No literal colour, spacing, radius, duration or shadow** anywhere outside the token package; the token layer is the only permitted source of a value | `35` `PS-07`, `12` `DX-4`, `30` §3.6 |
| 10 | **Permission-denied reads as absent**, matching the `404`-not-`403` rule, and a component never presents an animation as proof of server processing | `03` §5 step 3, `13` §5.3, `30` §7 prohibition 1 |

**Rule CA-07** — a component that fails any row is not merged, and `33` §5's row for it stays
`UNDESIGNED`. The matrix is the definition of done, not a status report.

### 4.1 The variant API

Every component exposes state through a **declared variant map**, not through ad-hoc props:

| Axis | Permitted values | Notes |
|---|---|---|
| `intent` | `action` · `neutral` · `danger` · `success` · `warning` · `info` | maps to `color.action`/`success`/`warning`/`error`/`info` in `30` §3.5. `positive` is **not** an intent — it is decoration only |
| `emphasis` | `solid` · `outline` · `ghost` · `link` | `12` §6.2 names Button's four kinds |
| `size` | `sm` · `md` · `lg` (24/32/40 px control height on web; 40/48/56 dp on mobile) | the smallest size must still satisfy CA-04's touch target with padding, not with a bigger visual box |
| `state` | `default` · `hover` · `pressed` · `focus-visible` · `disabled` · `loading` · `error` | `disabled` and `loading` are separate: `12` §6.2's Button has both, and `30` §7 prohibition 2 requires the in-flight control to be disabled **and** show its in-flight state |
| `density` | `comfortable` · `compact` | `compact` exists for the Control Center's tables (`12` §9's < 100 ms interaction, `35` `PS-15`) — a documented axis, not a per-screen override |

**Rule CA-08** — a new value on any axis is a design-system change: it lands in `30` first (a token or a
measured ratio), then in this table, then in the component. A screen asking for "one more shade" is the
exact mechanism by which `30` §3.1's temperature split re-enters the product.

---

## 5. Custom colour in code

The values are `30` §3's; this is the delivery mechanism, and it is the difference between a palette
that survives four surfaces and one that drifts.

| Rule | Detail |
|---|---|
| CA-09 | One CSS custom-property layer, generated from `packages/design-tokens` (`35` `PS-11`), named for the **role** and never for the hue: `--amm-color-action`, `--amm-color-ink`, `--amm-color-body`, `--amm-color-muted`, `--amm-color-border`, `--amm-color-border-strong`, `--amm-color-canvas`, `--amm-color-surface`, `--amm-color-surface-sunk`, `--amm-brand-50…950`, `--amm-metal-tint/soft/decor/text`, `--amm-color-success/warning/error/info/positive/positive-text/focus`. A variable called `--teal-500` invites a second teal. |
| CA-10 | **Semantic pairs are consumed, never unwrapped.** `surface`/`ink`, `canvas`/`body`, `surface-sunk`/`body` are used as pairs (`30` §3.3, `12` §6.1's "semantic surface/ink pairs"). Picking a background from one pair and a text colour from another is how contrast fails after a token edit. |
| CA-11 | **The metal budget is a code rule, not advice.** `metal.decor` is decoration on ink only (it measures 2.42 on light — never text), `metal.text` is the only gold permitted to carry words, and metal stays ≤ 2 % of a screen's pixels (`30` §3.4). No gold button, no gold input border, no gold body text. |
| CA-12 | **`positive` may not carry text and may not sit under white text** — it measures 3.10 in both directions (`30` §3.5). Any use of `--amm-color-positive` with a foreground colour attached fails review; use `positive-text`. |
| CA-13 | **Shadows are tinted, never black**, and are consumed as `elevation.1/2/3/action/hero` (`30` §5.1). A card gets a 1 px border plus `elevation.1` at most; a component needing both a strong shadow and a border is a hierarchy error (`30` §5.1). |
| CA-14 | **Saturation budget**: chromatic fill ≤ 25 % of a screen; large areas use `brand.50`/`brand.100` tints (`30` §3.6). Gradient is confined to the brand ramp and to the marketing surface (`30` §3.6, `30` §5.2). |
| CA-15 | **One theme today.** `30` §10 proposes **light only** and registers the dark-mode question as `OD-DOC-31`; so the token layer must be pair-based enough to accept a second theme later (`35` `PS-13`) but must **not** ship a dark variant now — `32` §4 records that no dark exports exist precisely because the policy is undecided. |

```css
/* Generated from packages/design-tokens — the ONLY file in the front end with colour values in it.
   Values live in 30 §3; this block shows the shape, not the numbers. */
:root {
  --amm-color-action:        var(--amm-brand-500);
  --amm-color-action-hover:  var(--amm-brand-600);
  --amm-color-action-press:  var(--amm-brand-700);
  --amm-color-action-subtle: var(--amm-color-action-subtle-source);
  --amm-color-focus:         var(--amm-color-action);
  --amm-elevation-1: …;   /* 30 §5.1 */
  --amm-motion-fast: 150ms; --amm-motion-base: 250ms; --amm-motion-page: 400ms;  /* 12 §6.1 = 30 §7 */
  --amm-ease-standard: cubic-bezier(.2,0,.13,1);
  --amm-ease-entering: cubic-bezier(.16,1,.3,1);
  --amm-ease-exiting:  cubic-bezier(.4,0,1,1);
}
[data-pair="surface"] { background: var(--amm-color-surface); color: var(--amm-color-ink); }
[data-pair="canvas"]  { background: var(--amm-color-canvas);  color: var(--amm-color-body); }
```

**Enforcement** (`36` §4's visual-regression row, `14` `FE-05`'s precedent): a stylelint rule rejects
any hex, `rgb()`, `hsl()` or named colour outside the token layer; a second rule rejects `box-shadow`
built from black; a third rejects a `transition` duration that is not one of the three motion tokens.
The lint failure is the design-system rule — a rule nobody can check is a preference.

---

## 6. Custom animation in code

Durations and easings are `30` §7's (`motion.fast 150` / `base 250` / `page 400`, the three curves,
an 8 px slide, ≤ 4 px scale, a 6-item stagger cap). What follows is how each **named recipe** is built,
and the surface it is permitted on per `30` §5.2.

| Recipe | Built from | Allowed on | Implementation rule |
|---|---|---|---|
| `press` | `motion.fast` + `ease.exiting` | everywhere | scale ≤ 4 px or a tone step; **no movement in Control Center tables** (`30` §5.2) |
| `sheet-in` | `motion.base` + `ease.entering`, 8 px slide + opacity | web, customer, partner | enter uses `ease.entering` (the machined settle); **exit uses `ease.exiting`** — never the enter curve in reverse (`30` §7) |
| `route` | `motion.page` | apps only | the Control Center uses `motion.fast` because its budget is 100 ms perceived interaction (`12` §9, `30` §7) |
| `list-stagger` | `motion.fast`, 30–40 ms per sibling | web, apps | **max 6 items, first paint immediate**; beyond 6 the stagger is a wait (`30` §7) |
| `shimmer` | 1.2–1.8 s cycle, `surface-sunk → surface` | all four surfaces | **stops when data lands** — it is bound to request-in-flight state, never to a timer (`30` §7 prohibition 3) |
| `kpi-cross-fade` | opacity only, `motion.base` | Control Center KPI tiles | permitted where `count-up` is not; **prohibited in Finance/Reports tables** (`30` §5.2) |
| `count-up` | — | **marketing web home only, once, in view** | prohibited on money everywhere else: an animating figure invites a misread of an amount (`12` XS-02, `30` §5.2) |
| `focus-ring` | 2 px ring, 2 px offset, `color.focus` | everywhere | appears on `:focus-visible` only; never colour-only (`30` §3.5, `12` A11Y-4) |
| `motion-graphic` | Lottie/Rive payload | marketing web, customer app | ≤ 1 payload, ≤ 40 KB, budgeted like an image (`32` §4); prohibited in the partner checklist flow and unused in the Control Center (`30` §5.2) |

```tsx
// The contract is a token reference, not a number. Reduced motion is the default path, not a patch.
const sheetVariants = {
  initial: { opacity: 0, y: 8 },
  animate: { opacity: 1, y: 0, transition: { duration: 'var(--amm-motion-base)', ease: 'var(--amm-ease-entering)' } },
  exit:    { opacity: 0, y: 8, transition: { duration: 'var(--amm-motion-fast)',  ease: 'var(--amm-ease-exiting)'  } },
};
// prefers-reduced-motion: strip y, keep opacity ≤ 150ms, and still announce the change (30 §7 p.4, A11Y-7)
```

```dart
// Flutter mirror: the same three durations from the generated token map (35 PS-11), never a literal.
Duration get motionBase => reduceMotion ? const Duration(milliseconds: 150) : tokens.motionBase;
```

| Rule | Detail |
|---|---|
| CA-16 | **Compositor-only.** `transform` and `opacity` — never `width/height/top/left/filter` animation on a scrolling surface (`30` §7's low-end-Android constraint, `12` §9's cold start and APK ceilings). |
| CA-17 | **State truth.** A transition may follow a backend status (`23` §2.3) or a socket/poll freshness signal (`12` §3.3); it may never *create* one. The success animation is not the receipt (`30` §7 prohibition 1). |
| CA-18 | **No looping decoration** and no motion that implies progress a payment or a job has not made (`23` §11.2/§12, `30` §7 prohibition 3). |
| CA-19 | **In-flight means disabled.** Every mutating control disables while pending and shows its in-flight state, because `23` §3.2 idempotency exists for double-taps (`30` §7 prohibition 2). |

---

## 7. Effects in code

`30` §5.2 decides **whether** an effect is permitted per surface; this decides **how** it is written so
that four surfaces cannot four different ways.

| Effect | Implementation | Guard |
|---|---|---|
| **Scrim over imagery** | the two-stop gradient from `30` §5.2, α **.65 → .85**, as a token `--amm-scrim-hero`, applied to the container — never as a text shadow | no white body copy in a band lighter than .65; where the photo is mostly sky or white tile, **move the text beside the image** (`30` §5.2). Text drop-shadow is prohibited on every surface |
| **Blur** | `backdrop-filter` on **one** layer, marketing hero nav only, with a solid `--amm-color-surface` fallback when `@supports not` or when reduced motion is set | prohibited in app scrolling lists, prohibited in the Control Center (`30` §5.2) — the prohibition is enforced by the same lint rule that bans off-token durations |
| **Gradient** | `brand.900 → brand.950`, two stops, one hue family, with the `elevation.hero` metal hairline closing the band | marketing surface only (`30` §3.6/§5.2). Gradient text is prohibited outright |
| **Elevation** | the five `elevation.*` tokens (`30` §5.1), border-first | a component may not compose its own shadow |
| **Hover lift** | `translateY(-2px)` at `motion.fast`, cards only, web | n/a on touch (`30` §5.2) |
| **Skeleton** | the `shimmer` recipe on `surface-sunk`, at the **final component's dimensions** | the skeleton must reserve the real content's box so CLS < 0.1 holds (`13` §2.2), and must stop on data arrival |
| **Z layers** | `base 0 · sticky 10 · overlay 20 · dialog 30 · toast 40 · sheet 50` from `30` §5 | declared once in tokens; an unscoped `z-index` is refused (`30` §5) |

### 7.1 Placeholder slot — the component that carries this phase's decision

`30` §5.3 (owner-directed, `[CONFIRMED — direction]`) and `32` §5/§6 make the reserved container a
first-class component, and it is the single most important consistency device in the design phase:

| Prop | Contract | Source |
|---|---|---|
| `ratio` | one of `4:3` (category tile, job photo), `16:9` (hero), `1:1` (avatar), `1.91:1` (OG) | `30` §5.3, `32` §3 |
| `assetClass` | names the slot so the fallback glyph is **one glyph per class** | `30` §5.3, `31` §3 |
| `label` | `"Service image — pending"`: describes the slot, never a picture that is absent | `30` §5.3 (an `alt` that invents content is a false statement to a screen-reader user) |
| `state` | `placeholder` · `loading` · `error` · `served` | `14` FE-07's quartet applied to media |
| `radius` | inherited from the owning component | `30` §5.3 |

**Rule CA-20** — no component may render a grey checkerboard, baked-in "IMAGE HERE" text, or a 1×1
transparent stretch (`30` §5.3's explicit prohibitions), and **no slot may point at a generated image
that is not in `32` §3's manifest with a `GENERATED` status and a provenance record**. The upload/serve
path itself is `OD-DOC-34` `[BLOCKER]`, so `served` is not reachable today in any environment.
**Rule CA-21** — a screen assembled from placeholder slots is an approved **layout**, not an approved
**screen** (`30` §5.3, `OD-DOC-36`). `33` records the distinction per row; §11 below keeps the review
from blurring it, which matters because `26` §4.1's second ₹1,00,000 instalment hangs on UI approval.

---

## 8. Data-visualisation and status components

| Rule | Detail |
|---|---|
| CA-22 | Charts draw only `30` §8's seven measured series colours, in luminance order, ≤ 6 series without legend interaction; `color.error`/`warning` never appear as category colours; every chart ships **with its table alternative** (`12` §6.2's DataTable already exists for this purpose) |
| CA-23 | Money axes use `XS-02` formatting; commission and margin axes are **bps-labelled**, because `07` carries basis points and a "15 %" axis hiding a 1500 bps value invites a rounding story (`30` §8) |
| CA-24 | Coverage and serviceability boards render the documented RED/AMBER/GREEN set from `23` §5 (`ADR-004`) **with a text label always attached** (`12` A11Y-4, `30` §8, `33` §4.2 `SCR-CC-05`) |
| CA-25 | Status chips take their tone from the `30` §6 status→colour binding to `23` §2.3/§2.4, keyed off the **shared enum** (`XS-06`, `35` `PS-03`). A component with its own status map is the drift `XS-06` exists to stop |
| CA-26 | Markers are the `30` §9 spec (32 × 40 px SVG, tip anchor, selected state adds a ring not a size jump); a cluster shows a count and is never drawn as a technician; any demo or marketing map imagery uses **synthetic coordinates** (`09` §8 `PERSONAL`) |

---

## 9. Flutter mirror of the same contract

The contract in §4 is platform-neutral; only the mechanism differs.

| Web / CC mechanism | Flutter mechanism |
|---|---|
| CSS custom properties (`CA-09`) | a generated `ThemeExtension` from the same token source (`35` `PS-11`, `OD-14-06`) |
| Variant map file (`CA-05`) | a `WidgetStateProperty` set — pressed/hover/focus/disabled resolved by the framework, not by an `if` |
| `data-pair` semantic pairs (`CA-10`) | `Theme` colour roles set in pairs; no widget composes a `Color` literal (`30` §3.6's "nothing hard-codes a hex in a screen") |
| `prefers-reduced-motion` (`CA-06`/`30` §7) | `MediaQuery.disableAnimations`, and `accessibilityFeatures.boldText` honoured on the money path |
| Focus ring token | a `FocusTraversalGroup` + visible focus indicator of the same 2 px/2 px geometry (`12` A11Y-2/4) |
| Touch target | 48 × 48 dp minimum, enforced in widget tests on the smallest size variant |
| `shimmer` stops on data | the same rule in a `StreamBuilder`/provider bound to request state, never to a timer (`30` §7 p.3) |
| Placeholder slot (§7.1) | a widget with the same five props and the same glyph-per-class rule; `FL-06`'s golden tests are its evidence |

**Rule CA-27** — the two Flutter apps share tokens, the generated client and the widget-state contract
(`12` `DX-4`, `ML-02`, `35` §8). A partner-app-only visual choice is a bug report waiting for the
customer app to make the same one differently.

---

## 10. Where the "advanced" look is allowed to come from

The owner's brief asks for something that reads as premium and modern. Stated as engineering rules, so
the answer is not a mood board:

| Look for | Via | Never via |
|---|---|---|
| Depth | border-first + tinted `elevation.1/2/3`, `surface-sunk` wells, an inset hairline in the hero | black shadows, heavy blur stacks, neumorphism |
| Craft | a 4 px spacing rhythm used without exception, tabular money, an 8 px slide, a decelerating settle | mixed spacing systems per screen, animating counters on amounts |
| Brand confidence | one temperature across neutrals and controls (`30` §3.1), teal as action, gold as a 2 % metal budget | a second accent invented screen-by-screen; gold buttons |
| Density that still reads | `density=compact` as a declared axis, sticky tinted table headers, 43-icon nav at one stroke weight (`30` §11's 1.5 px at 24 px) | shrinking type below the `30` §4.3 floor; a themed Ant Design look (`OD-14-07`) |
| Motion with intent | three durations, three curves, enter/exit asymmetry, stagger capped at 6 | parallax, scroll-jacking, looping decoration, WebGL |
| Empty and error states as design | `31` §3/§5's per-screen empty states + `34`'s illustration direction (line in `color.body`, one fill in `brand.50`, one accent, **no text in the image**) | grey boxes, lorem text baked into components, mascot art (`30` §11's rejected list) |

**Rule CA-28** — if an effect cannot be traced to a token in `30` and a surface in `30` §5.2's table, it
does not ship. This single rule is what stops "premium" from meaning "whatever each screen's author
liked", across four surfaces and 68 screens.

---

## 11. The consistency gate — how this is checked, and how a rule gets updated

### 11.1 Review checklist (feeds `29` §4.8; every item is a yes/no, none is a matter of taste)

| # | Check | Fails when |
|---|---|---|
| 1 | Component is named in `12` §6.2 | a new name appeared first in code (`CA-00`) |
| 2 | Screen is in `33` with its states | an undocumented screen was built (`35` `PS-06`) |
| 3 | Layer order respected (`packages/ui` not imported by a primitive; no vendor kit in domain patterns) | CA-01/`36` LB-07 |
| 4 | Zero literals: no hex, no ms, no px shadow, no ad-hoc radius outside tokens | `35` `PS-07`, CA-09/16 |
| 5 | All ten §4 contract rows hold, including the four screen-level states | CA-07 |
| 6 | Contrast evidence exists for every new foreground/background pair (measured by `contrast.py`, not asserted) | `30` §3's basis for the AA claims |
| 7 | Motion recipe is one of §6's rows **and is permitted on this surface** | `30` §5.2's per-surface budget |
| 8 | Reduced-motion and forced-colors cases exist in the workshop | `30` §7 p.4; `12` A11Y-4/7 |
| 9 | Money and rates use the shared formatter; no `toFixed` in a component | `XS-02`, `35` `PS-04` |
| 10 | Strings come from the catalogue; no text inside an asset | `14` FE-05, `12` §8, `30` §11 |
| 11 | Every image slot is a §7.1 placeholder or a manifest-registered `GENERATED` asset | `CA-20`, `32` §3/§4 |
| 12 | Permission-denied reads as absent; nothing animates a state the server has not confirmed | `03` §5, `30` §7 p.1 |
| 13 | Nothing in the diff adds a third-party origin to CSP assumptions (`36` §3) | `13` §5.2 |
| 14 | Documents updated in the same change: `12` §6.2, `33`, `30` if a token or a state changed | `DC-04`; a code-only design change is how `08` §9 / `14` §2 / `27` §6 drifted apart in the first place |

### 11.2 Automatic enforcement (`36` §4's last row, made concrete)

| Check | Mechanism | Blocks |
|---|---|---|
| token purity | stylelint + a custom rule | any literal colour/size/duration outside the token layer |
| tinted-shadow rule | stylelint | `rgba(0,0,0,…)`, `black`, `#000` in a shadow |
| motion allowlist | ESLint rule | an off-token duration or an easing not in the three curves |
| a11y | `eslint-plugin-jsx-a11y` + `axe-core` in tests | `A11Y-1`…`A11Y-7` regressions |
| hard-coded strings | `14` `FE-05`'s existing lint rule | a UI string outside the catalogue |
| state coverage | workshop case exists per declared state (test asserts one case per §4 row) | an unrendered state |
| asset integrity | `validate_assets.py` (`32` §4) | a file with no inventory ID, wrong bytes, wrong pixels, missing alt treatment |
| architecture | `15` `TST-04`, `08` `ML-01`/`ML-02` | a boundary violation in the API or a hand-written client |
| CSP smoke | a build-time check that no remote origin is referenced | a `13` §5.2 violation found in production |

### 11.3 How a design rule gets updated — the procedure the owner asked for

A design rule changes through **documents first, code second**, in this order:

1. **Register it.** If the change conflicts with an existing rule, it goes into `21` as an `OD-*` row
   with a severity and a named owner — `DEC-06`. Two sides stay on file until it is decided; nobody
   edits one side into the other (`DEC-07`).
2. **Decide.** The named owner decides (`DEC-03`: approval is an owner act, never silence, never a
   document, never this pass). Anything that alters a rule, boundary, formula, model, permission or
   control needs an ADR first (`README` §14 step 4, `22` §5). A new token value needs measured contrast
   evidence attached (`30` §3's method: `contrast.py`).
3. **Edit the owning document, once.** Token value → `30`. Component name → `12` §6.2. Screen or state →
   `33`. Library choice → `36`. File placement → `35`. Build contract or recipe → this document. Nothing
   is copied into a second home (`DEC-01`).
4. **Propagate.** Every affected document in the same change (`DC-04`), with a Revision History row each
   (`DC-02`), and a version bump per `DC-03` — a rule change is **major**, an addition is **minor**, an
   editorial fix is **patch**.
5. **Trace and gate.** `28` gets or updates its row (`DC-05`); `29` §4.8's checklist and §11.2's
   automatic checks change to match, or the rule is unenforced and will drift.
6. **Then code.** Tokens, then the component, then the call sites — in that order, in one change
   (`CA-08`, `PS-21`).

---

## 12. What remains blocked while these are open

| Open decision | What it stops in this document |
|---|---|
| `OD-DOC-30` | whether §5's colour layer is the brand at all — `12` §6.1 still says blue and orange, and `30` §3's values are unapproved |
| `OD-DOC-31` | whether a second theme is ever required; today `CA-15` ships light only |
| `OD-DOC-32` | the self-hosted font pipeline, so §4's typography contract has no deliverable family |
| `OD-DOC-34` `[BLOCKER]` | the `served` state in §7.1 — no CDN origin is in `13` §5.2, and no object is publicly readable per `24` §11 |
| `OD-DOC-36` | whether a placeholder-based review can ever satisfy the UI-approval trigger in `26` §4.1 |
| `OD-DOC-37` | the super-admin storage-configuration surface, which needs §8's domain pattern and a screen, route and token that do not exist |
| `OD-10-06` / `OD-DOC-29` `[BLOCKER]` | the permission and API columns `33` leaves empty, so a domain component's access states cannot be completed |
| `OD-14-07` / `OD-14-09` / `OD-14-10` / `OD-14-11` / `OD-14-13` | the mechanism of §5–§7: styling engine, variant implementation, animation runtime, chart and grid renderers, token build tool |
| `OD-DOC-38` `[BLOCKER]` | nothing in §2–§10, and everything in §12's dependency on the generated enum contract (`PS-03`) if the backend language changes the artefact's shape |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.0 | 2026-10-21 | Frontend Lead + Mobile Lead + Product Design Lead (design-consistency pass) | First issue, at the owner's direction to document the design rules and the component-based structure every surface must follow, including custom colour, animation and effect usage. Four-layer model with a one-way import rule (CA-01/CA-02), the per-component file layout (CA-04…CA-06), a ten-row contract that makes `12` §6.2's state list, `33` §5's matrix, `14` FE-05/FE-07 and `12` §6.3's A11Y list a single definition of done, and a five-axis variant API (intent/emphasis/size/state/density) with CA-08 requiring any new value to land in `30` first. §5 expresses Scheme A in code — role-named custom properties, consumed semantic pairs, the ≤ 2 % metal budget, the `positive` text ban, tinted shadows, the 25 % saturation budget and light-only — with the values cited to `30` rather than restated, and three lint rules named as the enforcement. §6 turns `30` §7 into nine recipes with a permitted-surface column and four prohibitions; §7 does the same for `30` §5.2's effects, adds the measured scrim as a token and specifies the placeholder-slot props exactly as `30` §5.3 defines them. §8 binds charts, coverage boards, status chips and markers to `30` §6/§8/§9 and `23`; §9 mirrors the whole contract in Flutter terms. §11 is the operational part: a 14-item review checklist feeding `29` §4.8, nine automatic checks, and the six-step rule-update procedure the owner asked for (register → decide → edit the owning document once → propagate → trace → then code). **Adds no component name** (`12` §6.2 remains the only home, `CA-00`); the eight `33` §5 gaps stay gaps. Nothing is rendered, built or measured on a device; no version, cost or library availability is asserted. | All |
