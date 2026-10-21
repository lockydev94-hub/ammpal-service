# 36 — Design Engineering Toolchain and Library Baseline

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-36 |
| Version | 1.0 |
| Status | **PROPOSED — not approved.** Every library named here is a **candidate** for an owner decision, not an installed dependency. **No package exists in this workspace**: there is no `package.json`, no `pubspec.yaml`, no lockfile and no build. Nothing here was installed, evaluated hands-on or priced. |
| Owner | Frontend Lead + Mobile Lead, with Engineering Lead for anything crossing `packages/` |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `14` §1/§1.3/§6 (the framework rows are `[CONFIRMED]` and are not re-opened here), `13` §5.2 (CSP), `12` §6.2/§6.3/§9, `30` §3–§8/§11, `35` §6–§8, `15` §2, `16` §5, `21` §2/§3/§7, `22` ADR-011/ADR-012 |
| Blocks | `37` §3 (a component file layout presumes a styling engine), the scaffold, and any bundle-size claim in `13` §2.2 |

---

## 1. What this owns

| Question | Home |
|---|---|
| **Which framework** each surface is built on (Next/React, Vite/React, Flutter, NestJS-or-not) | `14` §1 — `[CONFIRMED]`, mirrored in `ADR-011`. **Not re-opened here**, except where `OD-DOC-38` already flags the backend-language conflict registered in `35` §2 |
| **Where** files live, per surface | `35` |
| **What** the tokens are worth, and which effects are permitted at all | `30` §3–§7 |
| **How** a component is built and composed | `37` |
| **Which library** fills each capability, and under what constraint | **this document** |

A framework is a decision; a library is a choice inside it. This document only makes choices inside
decisions that have already been made.

---

## 2. Selection principles

| ID | Principle | Where the requirement comes from |
|---|---|---|
| LB-01 | **A library may not own the visual language.** Anything that ships its own palette, type scale or elevation set is either themed completely from `30`'s tokens or rejected. A component kit left in its default look is the clearest possible tell of an unbuilt design system. | `30` §3, `12` §6.1, `DX-4` |
| LB-02 | **It must survive the CSP as written.** `13` §5.2 sets `script-src 'self' 'nonce-<random>'`, `style-src 'self' 'nonce-<random>'`, `img-src 'self' data: blob: <maps origins>`, `font-src 'self'`, `connect-src 'self' <api origins> https://*.googleapis.com https://fcm.googleapis.com`, `frame-src https://api.razorpay.com`. Any dependency that injects a remote script, a remote stylesheet, a remote font or an off-list `connect-src` endpoint is a production breakage, not a development convenience. §3 checks every candidate against it. | `13` §5.2 |
| LB-03 | **It must fit a budget that has never been measured.** `12` §9 caps APK at 25 MB (customer) / 30 MB (partner) with cold start < 2.5 s, and `13` §2.2 sets LCP < 2.5 s / INP < 200 ms / CLS < 0.1 — which `13` §2.2 itself annotates as **never measured on a real device**, and `32` §4 repeats for the raster ceilings. Runtime cost, tree-shakeability and whether the library can be loaded per-route are the whole question. | `12` §9, `13` §2.2, `32` §4 |
| LB-04 | **Accessibility is not a follow-up module.** If the accessible implementation of a control (focus order, `aria-describedby`, roving tabindex, screen-reader announce) has to be hand-written on top of a library, the library has saved nothing. `12` §6.3 A11Y-1…A11Y-7 and `14` `FE-08` make this a review item. | `12` §6.3, `14` FE-08 |
| LB-05 | **Compositor-only motion, or no motion.** `30` §7 requires transform/opacity only, `prefers-reduced-motion` honoured, no animation as evidence of a server state, Lottie payloads budgeted like images. A runtime that animates `top/left/width/height`, or that cannot be paused, is out. | `30` §5.2/§7, `12` §6.1 |
| LB-06 | **Permissive licence, no runtime seat, no vendor lock at the data layer.** MIT/Apache/BSD-class. No capability that only works when a paid SaaS is reachable. **No cost figure is asserted anywhere in this document** — the standing rule that third-party pricing needs current evidence (`README` §12; `OD-COM-07` is open on what third-party consumption is even inside the fee). | `26` §4, `OD-COM-07` |
| LB-07 | **Replaceable behind our own API.** Every third-party component is wrapped once, in `packages/ui` (`37` §3), and no screen imports a vendor primitive directly. This is what makes a mid-phase swap possible at all, and `OD-14-07` is explicitly a live example of why the wrapper matters. | `35` `PS-21`, `37` §2 |
| LB-08 | **Upgraded on `14` §1.3's cadence, not on a whim.** No version is pinned here; pinning is a scaffold act, and `14` §1.3 owns the cadence, the batching and the four sensitive categories that never auto-merge. | `14` §1.3, `OD-14-08` |

---

## 3. The CSP gate, applied

`13` §5.2 is the strictest thing in the front end, and it is a `[CONFIRMED]` control. Read as a filter:

| Pattern a library relies on | Verdict under `13` §5.2 as written | Consequence |
|---|---|---|
| Remote font service (any "just add a `<link>`" fonts CDN) | **Blocked** — `font-src 'self'` | self-hosted, subset files; the pipeline nobody owns is `OD-DOC-32` |
| CDN-loaded script or widget (chat bubble, analytics beacon, video player embed) | **Blocked** — `script-src 'self' 'nonce-…'` | must be bundled locally **and** its endpoint added to `connect-src`, which is a `13` §5 change and therefore an ADR (`22` §5) |
| Runtime CSS injection without a nonce (classic CSS-in-JS) | **Blocked** — `style-src 'self' 'nonce-…'` | prefer a build-time stylesheet, or a nonce-aware setup verified in CI before adoption |
| Remote imagery from a media CDN | **Blocked today** — `img-src` names no origin of ours | this is `OD-DOC-34` `[BLOCKER]`, and `35` `PS-08`; nothing image-led may be promised until it closes |
| Google Maps JS SDK + tiles | **Allowed by name** — `maps.googleapis.com`, `maps.gstatic.com`, `*.googleusercontent.com` in `img-src`, `*.googleapis.com` in `connect-src` | the launch map layer is Google Maps, exactly as `30` §9 states; a self-hosted or third-party tile source is not CSP-compatible without an amendment |
| Razorpay hosted checkout frame | **Partly allowed** — `frame-src` names `api.razorpay.com` only | confirm during contract testing which origin the checkout frame actually loads from (`24` §5 records no origin list); discovering this in production is a payment outage |
| `data:`/`blob:` inline SVG and canvas exports | Allowed — both are in `img-src` | the icon pipeline in §4 uses this |

---

## 4. Web and Control Center, by capability

React 19 / Next 15 / Vite 6 / TypeScript 5 are `14` §1 and are **not** candidates here. `[PROPOSED]`
below means "recommended, awaiting the owner decision named in the row".

| Capability | Candidates | Proposed | Why, from the documents | Status |
|---|---|---|---|---|
| **Styling engine** | Tailwind (utility, build-time CSS) · CSS Modules · vanilla-extract (zero-runtime, typed) | **Tailwind for the marketing web; CSS Modules or vanilla-extract for the Control Center, decided once and shared** | Build-time CSS is the only pattern that satisfies `13` §5.2's `style-src` without nonce plumbing; `30` §3's tokens arrive as CSS custom properties either way (`35` `PS-11`). The split is real: a marketing page and a 200-row table have different ergonomics, and `30` §3.3's neutrals deliberately replaced off-the-shelf slate | `OD-14-09` |
| **Component primitives (a11y behaviour only)** | Radix UI · React Aria · hand-rolled | **Unstyled primitives, wrapped once in `packages/ui`** | `LB-01` + `LB-04`. `12` §6.2 already names the components; the visual treatment is `30`'s job, and `A11Y-2/3/6/7` are behaviour, not styling | `OD-14-09` |
| **Variant composition** | class-variance-authority + tailwind-merge · compiled props | **CVA-style variant maps** as the contract in `37` §4 | `12` §6.2 gives Button seven states and four kinds; a variant API is how those stop being if-chains | `OD-14-09` |
| **Control Center component kit** | Ant Design (themed) · MUI · custom on tokens | **custom on `30`'s tokens, with a dense table layer from §4 "tables" below** | `OD-14-07` currently recommends Ant Design themed. The tension is `LB-01`: a themed kit still carries its own spacing rhythm, focus rings and density, which is exactly what makes a product look assembled rather than designed. Kept as an owner decision, not reversed by this document | `OD-14-07` **stays open**; `35` `PS-15` |
| **Tables + virtualisation** | TanStack Table + TanStack Virtual · AG Grid · vendor-kit table | **TanStack Table + Virtual** | `12` §6.2 requires sort/filter/paginate/export; `33` §5 requires overflow behaviour at 390 px; `12` §9 demands < 100 ms perceived interaction with a 43-item nav; export goes through `SCR-CC-12`'s CSV/XLSX path | `OD-14-11` |
| **Charts** | Recharts · visx · Chart.js (canvas) · Apache ECharts | **SVG-rendered, theme-driven library (Recharts-class) with the series palette injected from `30` §8** | `30` §8 fixes seven measured series colours, ≤ 6 series, **a table alternative for every chart**, `XS-02` money axes and bps-labelled rate axes. Canvas-only libraries make the accessible table alternative and the text-label rule harder to honour | `OD-14-11` |
| **Forms** | react-hook-form + the schema resolver · TanStack Form · controlled-by-hand | **react-hook-form, one schema per form** | `14` `FE-06` states schema-first ("one zod schema per form, shared with the API contract where possible") and `13` §5.2's `form-action 'self'` makes client validation the first line of defence. Note the coupling: `zod` presumes the TypeScript backend — `OD-DOC-38` decides whether the schema is genuinely *shared* or only *mirrored* | `14` FE-06 (confirmed); shared-source depends on `OD-DOC-38` |
| **Server/client state** | TanStack Query · SWR · hand-rolled | **TanStack Query for the Control Center; server components + route handlers for Next.js** | `14` `FE-01` already names this split; `FE-02` forbids a stray `fetch` outside the query layer | `[CONFIRMED]` in `14` §6.1 |
| **Animation (web)** | Motion (Framer Motion) · GSAP · CSS keyframes only | **CSS for state-level motion; one declarative runtime for enter/exit and layout, used sparingly** | `30` §7 fixes three durations, three easings, an 8 px slide, a ≤ 4 px scale, a 6-item stagger cap and compositor-only. A runtime that animates layout properties fails `LB-05`; a runtime that cannot respect `prefers-reduced-motion` fails `A11Y` | `OD-14-10` |
| **Motion graphics (web + app)** | Lottie-web · dotLottie · Rive | **at most one brand loader per surface, ≤ 40 KB, budgeted like an image** | `30` §5.2 permits Lottie only on marketing web and the customer app, prohibits it in the partner checklist flow (one-handed, offline, `12` §4.3) and does not use it in the Control Center; `32` §4 is the weight gate | `OD-14-10` |
| **Icon pipeline** | SVGR · vite-plugin-svgr · a sprite build | **SVG imported as components, plus a sprite for the nav set; no icon font** | `30` §11's SVG-first rule and `32` §4's 4 KB icon ceiling; `31` plans 43 nav icons at 24 px (`33` §6). `13` §5.2 permits `data:`/`blob:` so inlining is legal | `[CONFIRMED]` direction (`30` §11); build tool not decided |
| **Fonts** | self-hosted subsets (any) | **self-hosted, subset, one `<link>` strategy per surface** — `font-src 'self'` leaves no alternative | `30` §4.2's families (Inter UI, a display face on marketing only, Noto for Odia/Hindi), `13` §5.2, and the trap `30` §4.2 flags: the `Noto Sans Oriya` vs `Odia` family-name question is `[UNVERIFIED]` and must be tested by rendering, not by reading a font page | `OD-DOC-32` |
| **Overlays, toasts, menus** | primitives from the a11y row above | same wrapper rule | `12` §6.2 names Dialog/Sheet/Snackbar/Toast/Drawer; `30` §5.1's border-first elevation defines how they separate from the page | covered by `OD-14-09` |
| **Date / time / number formatting** | `Intl` + date-fns · day.js · Moment (not proposed) | **`Intl` for locale, a small immutable helper for timezone conversion; no mutable date library** | `README` §14.2 fixes ISO-8601 UTC at the boundary; `XS-02` fixes `₹1,119.82` with tabular numerals; `12` §8 requires the three locales. Money is never a float (`14` `TS-08`, `35` `PS-04`) | `[CONFIRMED]` at the rule level |
| **i18n runtime** | next-intl / react-i18next / FormatJS | **one catalogue format shared with Flutter's ARB files, decided together** | `12` §8 (i18n-03, the 30 % expansion tolerance, XS-06 one-enum-one-catalogue) and the owner's English-first-at-design-time direction, which defers translation but not the layout tolerance (`OD-DOC-35`) | depends on `OD-DOC-35` |
| **Realtime client** | the Socket.IO client already implied by `14` §1 | bundled locally, `wss://api.ammpalservice.com` per `connect-src` | `10`'s WebSocket contract; `12` §3.3's freshness rules; `30` §7 prohibition 1 means the socket is the truth and the animation is decoration | `[CONFIRMED]` (`14` §1) |
| **Component workshop** | Storybook · Ladle · a route in each app | **a workshop is required, the host is not decided** | this is the only artifact that can show `33` §5's state matrix — default/hover/pressed/focus/disabled/loading/error × L/E/F/P/A — **without any production imagery**, which is what the placeholder-first direction (`30` §5.3, `OD-DOC-36`) leaves the design gate with | `OD-14-12` |
| **Visual regression + a11y in CI** | Playwright screenshots · axe-core · eslint-plugin-jsx-a11y · stylelint | **lint for token purity, axe for the A11Y list, screenshot diff for the 5 golden screens** | `14` `FE-05` already shows the pattern (a lint rule that fails CI on hard-coded strings); `15` `TST-06` puts Playwright in the stack; `FL-06` demands golden tests for 5 screens on mobile | `[PROPOSED]`, extends `15` §2 |
| **Design-token build** | a small TS build emitting CSS custom properties + a typed object + a Dart map · Style Dictionary | **the smallest build that emits three outputs from one source** | `35` `PS-11`/`PS-12`; `12` `DX-4`; `OD-14-06` (shared Flutter token package, `[NICE]` — but it is `[NICE]` *after* the web build exists, not instead of it) | `OD-14-13` |

**Design-tool note, unchanged:** `OD-12-01 / OD-UX-01` (design tool of record) is still open in `21`, and
it decides whether tokens are authored in a design file and exported, or authored in code and mirrored.
Nothing in this document assumes an answer.

---

## 5. Flutter (Customer App and Partner App), by capability

Both apps are Flutter 3.x / Dart 3 (`14` §1, `ADR-011`). The two open blockers in the table are not
cosmetic: they decide the folder shape `35` §8 drew.

| Capability | Candidates | Proposed | Note from the documents | Status |
|---|---|---|---|---|
| **State management** | Riverpod · Bloc | **not decided by this document** | `OD-14-02` `[BLOCKER]`, recommendation Riverpod. `35` `PS-19` and §8's `presentation/` shape are written framework-neutral on purpose | `OD-14-02` |
| **Routing** | go_router · auto_route · Navigator 2.0 by hand | **declarative router with deep-link support** | `12` §6.2 lists a "Deep-link router" as a component, and `12` §3.1's 5-tab + stack-flow model needs one route table, not per-screen pushes | `[PROPOSED]` |
| **Generated API client** | openapi-generator Dart client · a hand-thin wrapper | **generated, committed, never hand-written** | `ADR-012`, `ML-02`, `14` `FL-03` — this is a `[CONFIRMED]` rule, not a choice | `[CONFIRMED]` |
| **Local persistence / offline queue** | Drift (SQLite) · Isar-class | **Drift, per `FL-05`'s own wording** | partner app is offline-first with idempotent sync (`23` §3.2); `35` `PS-19` keeps it a feature, not a core service | `[CONFIRMED]` direction |
| **DI / configuration** | get_it · Riverpod providers · compile-time | follows `OD-14-02` | a state-management decision always drags DI with it; decided together to avoid two frameworks in one app | depends on `OD-14-02` |
| **Charts (partner earnings, KPI tiles)** | fl_chart · chartist | **whatever honours `30` §8**, incl. the table alternative | `SCR-*` earning screens in `33` §4.1; money axes stay `XS-02`, rates stay bps | `OD-14-11` |
| **Animation** | flutter_animate-class (implicit/explicit) · Rive · lottie | **implicit/explicit animations bound to `30` §7 durations; motion graphics capped as in §4** | `12` §9's cold-start and APK figures are the ceiling; `30` §7 requires `MediaQuery.disableAnimations` handling and prohibits animation as proof of a state | `OD-14-10` |
| **Maps** | the Google Maps Flutter plugin | allowed, and the only CSP-compatible provider in the current policy (`30` §9) | markers are 32 × 40 px SVG overlays per `30` §9 and `31`; demo/marketing map imagery **must use synthetic coordinates** (`09` §8 `PERSONAL` class) | `[CONFIRMED]` provider (`14` §1) |
| **Images / cache** | any cache layer | **deferred**: placeholder containers render until `OD-DOC-34` decides where imagery is served from (`35` `PS-08`, `37` §9) | a caching library presumes a network source that today's CSP does not name | `OD-DOC-34` `[BLOCKER]` |
| **Crash reporting** | Firebase Crashlytics (named in `FL-08`) | as specified, **with PII scrubbing enabled** | `FL-08` is a rule, not a suggestion; `13` §5/§7 DPDP obligations are why scrubbing is mandatory | `[CONFIRMED]` |
| **Localisation** | `flutter_localizations` + ARB | one ARB pipeline shared with web (`12` §8, XS-06) | Odia needs Noto **at runtime**, `FR-CAT-08`, and the expansion tolerance is non-deferrable (`OD-DOC-35`) | `[PROPOSED]` mechanism |
| **Secure storage** | platform secure storage | tokens never in plain shared preferences | `13` §5, `14` §11, `ENV-03` (server-side analogue) | `[CONFIRMED]` requirement |
| **Testing** | widget tests, golden tests | `FL-06`: widget test for every stateful widget with logic, goldens for the 5 key screens | goldens are also the only design evidence available while placeholders stand (`OD-DOC-36`) | `[CONFIRMED]` |

---

## 6. What actually makes this look premium

The owner's brief asks for "premium, professional, attractive, animated, effects". Measured against the
documents, the premium feel is **not** produced by a library. Six causes, in order of effect:

| Cause | Where it is already specified | Library involvement |
|---|---|---|
| **One colour temperature across every surface** — brand-tinted neutrals rather than blue-grey slate beside teal controls | `30` §3.1 (measured), `30` §3.3 | none; token discipline only |
| **Every state designed**, so nothing degrades into a browser default | `33` §5's matrix, `14` `FE-07` | workshop + primitives |
| **Restrained, consistent motion** — three durations, no overshoot in apps, enter-settle curve | `30` §7 | one runtime, used lazily |
| **Type hierarchy with tabular money** and a display face only where it earns its keep (marketing hero) | `30` §4, `XS-02` | fonts self-hosted per `13` §5.2 |
| **Real media behaviour**: scrims at the measured α floor, no text drop-shadows, border-first elevation | `30` §5.1/§5.2 | none |
| **Density done on purpose** in the Control Center rather than inherited from a kit | `12` §9, `35` `PS-15`/`PS-16` | table layer |

Everything else that usually gets called "premium" — glassmorphism everywhere, animated counters on
money, gradient text, parallax, looping shimmer — is **prohibited** in `30` §5.2, on the record and with
a reason (`12` XS-02's misread-an-amount risk, the AA contrast rule, the 100 ms perceived-interaction
budget).

---

## 7. Not adopted, with the reason on file

| Rejected | Why |
|---|---|
| A styled UI kit as the design system (MUI/Chakra/Ant left in default appearance) | `LB-01`; `30` §3 exists precisely because off-the-shelf values failed contrast or read as a template |
| Runtime CSS-in-JS that injects un-nonce'd style tags | `13` §5.2 `style-src`; breaks in production while passing locally |
| Remote font CDNs, remote widget beacons, third-party chat bubbles | `13` §5.2 `font-src`/`script-src`/`connect-src`; every one is an amendment to a `[CONFIRMED]` control and therefore an ADR |
| Icon fonts | `30` §11 SVG-first; an icon font costs a font download and breaks the 4 KB icon ceiling in `32` §4 |
| A general-purpose date library that mutates | `README` §14.2's ISO-8601 UTC rule; mutable dates in a booking system with an 8-year retention window is a defect generator |
| WebGL / three.js / heavy hero animation | `12` §9's cold start and APK ceilings on mid-range Android; `30` §5.2 prohibits parallax outright |
| Canvas-only charting as the default | `30` §8's table-alternative and text-label rules; a11y becomes a re-implementation |
| Any self-hosted or third-party map tile service | not in `img-src` today; `30` §9 names PostGIS as the geometry store, not the imagery source |
| Paid template or stock artwork bundles | `31` §2's IP position and `OD-COM-12` are open, and `34` §2 refuses invented screenshots, fake reviews, fake badges and real-looking credentials outright |
| A micro-frontend or module-federation layer | `08` §2's extraction gates are the seams that matter; four surfaces do not need a fifth abstraction, and `OD-14-04` (repo topology) is still a blocker |

---

## 8. Cost, licence and evidence posture

- **No cost, no pricing and no quota figure appears in this document.** `OD-COM-07` (what third-party
  consumption sits inside the fee) and `OD-COM-04` (what the annual service includes) are open, and
  `README` §12 forbids asserting third-party costs without current evidence.
- Every candidate is expected to be MIT/Apache/BSD-class (`LB-06`). A dependency needing a paid seat for
  core behaviour is not a technical objection — it is an unpriced commercial decision that belongs in
  `26`, and `OD-COM-07` is where it must be raised.
- **Nothing here was installed or run.** There is no lockfile, no `node_modules`, no `.dart_tool` and no
  build in this workspace; every "fits the budget" claim in §2/§4/§5 is a *criterion to measure at
  scaffold*, not a measurement. If a bundle or APK number is needed, it has to come from a real build
  (`13` §2.2's own annotation says as much).

---

## 9. What the owner must decide for the toolchain

Five rows are registered in `21` §3 by this pass, and the two pre-existing rows they touch are **not**
folded up or replaced:

| New row | Severity | One-line question |
|---|---|---|
| `OD-14-09` | `[IMPORTANT]` | Styling engine + component-primitive approach for the two React surfaces (§4 rows 1–3) |
| `OD-14-10` | `[IMPORTANT]` | Animation runtime on web and in Flutter, and Lottie-vs-Rive for motion graphics under `30` §5.2's 40 KB cap |
| `OD-14-11` | `[IMPORTANT]` | Charting and data-grid library pair that can render `30` §8's rules with a table alternative |
| `OD-14-12` | `[NICE]` | Component workshop and visual-regression tool — the artifact that lets the design gate be reviewed while placeholders stand |
| `OD-14-13` | `[IMPORTANT]` | Design-token build tool producing CSS custom properties, a typed TS object and a Dart map from one source (`35` `PS-11`) |

Pre-existing and still governing: `OD-14-01` (data layer), `OD-14-02` (Flutter state), `OD-14-03`
(task runner), `OD-14-04` (repo topology), `OD-14-06` (shared token package), **`OD-14-07`** (Ant Design
themed vs custom — the row this document argues against without reversing), `OD-14-08` (update
mechanism), `OD-12-01/OD-UX-01` (design tool of record), `OD-DOC-32` (font pipeline), `OD-DOC-34`
(media storage, `[BLOCKER]`), `OD-DOC-38` (backend language, `[BLOCKER]`).

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.0 | 2026-10-21 | Frontend Lead + Mobile Lead + Engineering Lead (design-engineering toolchain pass) | First issue, at the owner's direction to name "which library is needed for modern design" and to specify custom colour, animation and effect usage. Eight selection principles derived from existing rules rather than from taste (`LB-01`…`LB-08`), with the CSP in `13` §5.2 used as an actual filter (§3) — which is what disqualifies remote fonts, un-nonce'd runtime CSS injection, CDN widgets and any off-list `connect-src` endpoint, and what confirms Google Maps as the only CSP-compatible map source while leaving `OD-DOC-34` unresolved for imagery. Capability tables for the two React surfaces (§4, 19 rows) and Flutter (§5, 13 rows), each with its candidates, its proposal, the document that creates the requirement and the decision status; `14` §1's framework rows are cited, never re-opened. §6 states plainly that the premium feel comes from token discipline, complete states, restrained motion, measured scrims and deliberate density — and that the effects normally called premium are prohibited in `30` §5.2. §7 lists the rejections with reasons, §8 refuses to assert any cost, version pin or bundle measurement, and §9 registers five new owner decisions (`OD-14-09`…`13`) while leaving `OD-14-07` and every other pre-existing row open. **No dependency was installed, evaluated hands-on or priced; no version is pinned.** | All |
