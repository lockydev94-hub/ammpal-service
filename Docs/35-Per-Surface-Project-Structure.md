# 35 — Per-Surface Project Structure

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-35 |
| Version | 1.3 |
| Status | **PROPOSED — not approved.** A scaffold target, not a description of anything that exists. **No directory named in this document has been created**; the workspace holds `Docs/`, `design-assets/` (registers only), `visualize-image-of-project/` (4 reference PNGs) and eight root Python scripts. |
| Owner | Frontend Lead (web + Control Center + Flutter) + Engineering Lead (API) |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-22 |
| Depends On | `14` §1/§2/§2.1/§6, `08` §2/§9, `27` §6, `12` §2–§6, `30` §3–§7/§11, `33` §5, `22` ADR-011/ADR-012, `13` §5.2, `16` §5.2, `21` §2/§3/§7 |
| Blocks | the front-end scaffold, the API scaffold, `36` §5 (a token package needs a home), `37` §3, and `29` §4.8's consistency gate |

---

## 1. What this owns, and the tree it will not draw a fourth time

The **top-level monorepo tree already exists in three documents** — `14` §2 (canonical), `08` §9
(`Rule ML-01`/`ML-02`), and `27` §6 ("Where the Code Goes", the agent-facing copy). `35` does **not**
restate it, because a fourth copy is how a tree drifts into three different truths. What no document
currently holds is the **interior** of each surface — where a screen file, a component, a token import
and a state hook go — which is exactly what a designer-engineer needs in order to produce consistent
work across four surfaces and 68 screens (`33`).

| Question | Canonical home | This document's relationship to it |
|---|---|---|
| Top-level repo layout (`apps/`, `packages/`, `infra/`) | `14` §2, mirrored by `08` §9 and `27` §6 | referenced, never redrawn |
| Backend module list (16 modules) and module interior (`domain/`, `application/`, …) | `README` §3, `08` §2, `14` §2.1 (`ES-01`) | §4 adds only the design-relevant contract files |
| Shared packages (`contracts`, `design-tokens`, `api-client`, `config`, `testing`) | `08` §9 `ML-01`/`ML-02` | §5–§8 say which package each front-end file may import from |
| Component **names** | `12` §6.2 | §7–§9 use those names; they never add one |
| Screens, states, permissions | `33` | §5–§8 organise them into directories |
| Token **values**, effect policy, motion tokens | `30` §3–§7 | §6 places them in code; `37` §5–§7 implements them |
| Which **library** fills each capability | `36` | this document stays library-neutral |
| Asset file naming and storage | `32` §2, `31` §6 | §10 states the one rule that touches code: assets are imported, never fetched |

**Rule PS-01** — the top-level tree is `14` §2. A change to it is a change to `14` §2, `08` §9 **and**
`27` §6 in the same edit (`DC-04`), and nothing else may re-issue it.
**Rule PS-02** — the three copies disagree about **one** thing today, and it is registered: worker
placement. `14` §2 puts BullMQ processors at `apps/api/src/workers/`; `08` §9 lists a top-level
`apps/worker/`. See `OD-DOC-39`.
**Status, 2026-10-21** — the trees in this document stopped being hypothetical on the owner's direction
("scaffold as base on docs"). §3 / §5 / §6 / §7 / §8 plus `14` §2 exist on disk as **221 empty
directories**, 164 of them leaves; §4's FastAPI alternative does **not**, because `ADR-011` is the only Accepted backend
decision. `.gitkeep` is the only file in any leaf, and the emptiness is the finding, not an oversight: an
empty `apps/api/src/modules/booking/domain/` satisfies no rule in `37`, ships no screen, and fails
`17` `P0-03`, which asks for something that **builds**. Every blocker in §10 below is still open.

**Status, superseded 2026-10-22 for the front end only.** The sentence "`.gitkeep` is the only file in any
leaf" no longer holds for four workspaces: `apps/web`, `packages/ui`, `packages/contracts` and
`packages/design-tokens` carry **87 source and config files** between them — `package.json`, lockfile,
`tsconfig`, the token build, the primitives, the fixtures and Home's eight sections. The rest of the finding
stands unchanged, and is the reason this paragraph was written rather than the block above edited: **162
`.gitkeep` leaves are still empty**, nothing was placed at the repository root (the owner's constraint when
approving the install, keeping `OD-14-04` genuinely open rather than silently answered), `P0-03` still asks
for `apps/*` **and** `packages/*` building under CI and there is no workflow YAML and no backend, and every
blocker in §10 is still open. The application code is also **uncommitted by owner direction** — `14` §2
records what the public remote carries.

---

## 2. The FastAPI instruction, stated as what it is

On 2026-10-21 the owner asked this pass to document **"backend Fast API folder and files structure"**
(`[REPORTED]` — a direction given in conversation, not a decision record). The suite's backend row is
**NestJS + TypeScript**, and it is not a stray sentence: it is inside an **Accepted** ADR and it is
copied into three documents.

| Side | What it says | Where |
|---|---|---|
| **A — as decided** | `ADR-011` **Accepted** 2026-10-21, deciders Founder + Engineering Lead: "NestJS + TypeScript (backend); PostgreSQL 16 + PostGIS; Redis 7 + BullMQ"; `ADR-012` Accepted: the OpenAPI document is the contract and every client is generated from it; `14` §1 pins Nest 11, BullMQ 5, Socket.IO, Zod + class-validator, Prisma-or-Kysely; `14` §1.1 argues the choice on one-language + shared-contract grounds | `22` ADR-011/ADR-012, `14` §1/§1.1/§2.1, `08` §9, `27` §6, `README` §3 |
| **B — as instructed** | the backend should be **FastAPI**, and its folder and file structure should be documented so design and engineering follow one reference | owner direction, this pass, `[REPORTED]` |

Neither side has been edited into the other (`DEC-07`). The conflict is **`OD-DOC-38` `[BLOCKER]`** in
`21` §7, with the owner named as the decider and the deadline "before any repository scaffold exists".

### 2.1 What actually changes if B wins

This is not a swap of a framework name. The backend language is load-bearing in eight places:

| Coupled item | Under A (NestJS/TS) | Under B (FastAPI/Python) |
|---|---|---|
| Shared validation (`ML-01`) | `packages/contracts` holds zod schemas consumed by API and both React surfaces | zod cannot run in Python; contracts become **Pydantic models + a generated OpenAPI document only**, and the TS side must generate types from that document |
| End-to-end type safety (`14` §1.1) | one schema breaks the compiler everywhere at once | lost between the API and the two React surfaces; drift is caught by contract tests instead (`15` `TST-05`) |
| Client generation (`ADR-012`) | Nest decorators → `/openapi.json` → generated TS + Dart clients | FastAPI emits OpenAPI natively; **`ADR-012` survives this change**, and the Dart clients are unaffected — Flutter already cannot share TypeScript types (`ADR-011`'s own acknowledged limitation) |
| Queues and jobs | BullMQ on Redis 7 (`14` §1, `08`, `16`) | a different library and a different operational shape (arq / Celery / Dramatiq) — **which one is not decided here**; it is part of `OD-DOC-38`'s consequence, not a row in this document |
| Realtime | Socket.IO with a Redis adapter, rooms per booking (`14` §1, `10`) | Starlette/WebSockets; the room model and reconnect contract in `10` must be re-expressed, not re-assumed |
| Data layer | Prisma or Kysely — `OD-14-01`, itself an open **blocker** | neither is available; SQLAlchemy 2 + Alembic (or equivalent) would replace it, which reopens `OD-14-01` and every migration rule in `16` |
| Guards, interceptors, RBAC alignment | the reason given for Nest in `14` §1 maps onto `03`'s 92 permission tokens | FastAPI dependencies + middleware can express the same guards, but every `common/` file in `14` §2.1's shape becomes Python |
| Tests, CI, deploy | Jest + Supertest + Playwright, `pnpm` workspaces + Turborepo, `16` pipeline | pytest + httpx, a Python package manager, and a rewrite of `16` §5 and `14` §9's pipeline steps; `15` `TST-04`'s architecture test needs a Python boundary checker |

**Cost of the change, honestly bounded:** the two React surfaces lose their shared schema layer, the API
loses its ORM decision, and `14`/`08`/`16`/`15`/`27` each need a matching edit — while **the Flutter apps
notice nothing**, because they already talk only to the generated OpenAPI client. That asymmetry is the
argument to have in `22` §5, in one ADR, before a scaffold exists. It is also the reason for **`R-48`**
in `19`: an agent instructed in chat to build "the FastAPI backend" while three documents scaffold
NestJS will produce two half-finished backends, and no CI in `16` can run either.

### 2.2 What design work does *not* wait for this decision

Nothing in §5–§9 depends on the backend language. Front-end structure, the token package's consumer
side (`37` §5), component architecture (`37`), the library capability baseline (`36`) and every screen in
`33` are unaffected by A-vs-B, because in both cases the clients consume a **generated** contract
(`ADR-012`). Design and documentation may proceed at full speed while `OD-DOC-38` is open — which is the
right sequencing given `26` §4.1's UI-approval instalment.

---

## 3. Backend structure as specified today (side A), design-relevant view

`14` §2 and §2.1 own the tree and the module interior. This section adds only what a front-end or a
design review needs to know exists, so that neither goes hunting for it:

```
apps/api/
├── src/modules/<the 16 modules in README §3>/    # interior shape is 14 §2.1, unchanged
├── src/common/                                   # guards, filters, interceptors, pipes, decorators
├── src/config/                                   # typed config, validated at boot (14 ENV-03, 16 §5.6)
└── <the contract surface>                        # the only three things a UI engineer may depend on
    ├── openapi.json            # generated; the single bridge to every client (ADR-012)
    ├── error-code catalogue    # the machine-readable codes behind 10 §5's error envelope
    └── enum exports            # status and role enums — the same values 30 §6 binds colour to, XS-06
```

**Rule PS-03** — a front-end never hand-copies an enum, an error code or a DTO field name. It imports
the generated artefact (`packages/api-client`, `ML-02`) or fails review. This is the engineering form of
`12` §7 XS-06 ("one shared enum → one i18n file → no per-surface drift") and of `30` §6's status→colour
binding: three documents, one mechanism.
**Rule PS-04** — money never crosses the boundary as a display string. `07` and `09` carry integer paise
and basis points; `14` `TS-08` brands the types; `12` XS-02 fixes the rendering (`₹1,119.82`, tabular
numerals). A component that formats a number it received pre-formatted is a defect, not a style choice.
**Rule PS-05** — the API never learns about surfaces. No `if (client == "control-center")` branch exists
in `apps/api`; per-role shape is expressed by scope and permission (`03`), not by the caller's skin.

---

## 4. Backend structure if `OD-DOC-38` resolves to FastAPI

`[PROPOSED — CONTINGENT]` This tree is **not** a recommendation and is **not** the scaffold target while
`ADR-011` stands. It exists so that, if the owner supersedes `ADR-011` with a new ADR (`22` §5), the
16-module boundary model, the purity rule (`ES-01`) and the contract surface survive the move rather
than being quietly dropped.

```
apps/api/                                    # FastAPI, if OD-DOC-38 resolves to side B
├── app/
│   ├── main.py                              # app factory; mounts every module router
│   ├── deps.py                              # auth/scope/pagination dependencies (replaces guards)
│   ├── core/                                # config, logging (pino's structural equivalent), security
│   ├── db/                                  # engine, session, Alembic migrations, seeds
│   └── modules/<module>/                    # the same 16 boundaries, one package each
│       ├── router.py                        # HTTP surface only — no business logic
│       ├── schemas.py                       # Pydantic request/response models → OpenAPI
│       ├── service.py                       # use-case orchestration
│       ├── domain/                          # PURE: no framework import, mirrors 14 ES-01
│       ├── repository.py                    # data access; the only place SQL lives
│       ├── events.py                        # transactional outbox (README §3)
│       └── module.py                        # declares owned tables + dependencies (MB-03)
├── workers/                                 # queue consumers; placement still OD-DOC-39
└── tests/                                   # mirrors module boundaries (15 TST-01…TST-05)
```

Two constraints carry over unchanged, and they are the point of drawing the tree:
`pricing` and `commission` stay **pure** (`08` §2, `14` §2.1) with no I/O and no framework import, and
module boundaries stay **enforced by an architecture test** (`15` `TST-04`) — in Python that means
writing the checker, not inheriting one. A boundary nobody can test is a suggestion.

---

## 5. Website — Next.js interior (`12` §2's route set)

`14` §1 fixes the stack (Next 15 / React 19 / TS 5, App Router, static export for the marketing
surface). The directory shape below maps one-to-one onto the routes in `12` §2 and the 9 page types in
`12` §2.1, so a designer opening the repository finds the screen they were shown.

```
apps/web/
├── app/
│   ├── (marketing)/              # home, /partner, /toll-free, /offers, /pricing, /support
│   ├── (catalogue)/services/…    # /services, /services/{categorySlug}, …/{slug}
│   ├── (technicians)/…           # /technicians, /technicians/{id}
│   ├── (booking)/book/…          # the 7-step flow: address → service → slot → technician → price → payment → confirm
│   ├── (account)/bookings/…      # history + detail/tracking  (auth required)
│   └── (legal)/                  # terms · privacy · refund-policy — text from ONE source (XS-05)
├── components/
│   ├── marketing/                # surface-specific composites; anything shared moves to packages/ui
│   └── forms/                    # booking-flow forms; schema-first, one zod schema per form (FE-06)
├── features/                     # per-domain hooks, mappers, query keys — not components
├── lib/                          # formatters (XS-02), locale, map loader, api client wiring (FE-02)
├── styles/                       # ONLY the import of packages/design-tokens + CSS entry; no hex
└── public/                       # same-origin static bundle (16 §5.2, 13 §5.2 img-src 'self')
```

| Rule | Detail |
|---|---|
| PS-06 | A route segment exists only for a route in `12` §2. A designer or agent wanting a new page **adds it to `12` §2 first**, then to this tree, then to `33` §3 — not the other way round. |
| PS-07 | `styles/` and every component file contain **zero colour literals**. The only hex permitted anywhere in the front end is inside `packages/design-tokens` (`30` §3, `DX-4`, enforced by lint per `37` §5). |
| PS-08 | Fonts and imagery are self-hosted from the same origin. `13` §5.2 sets `font-src 'self'` and `img-src 'self' … maps.googleapis.com …`, so a CDN font or an off-origin image is not a style preference but a CSP violation — which is precisely why `OD-DOC-32` (who owns the subsetting pipeline) and `OD-DOC-34` (media storage, `[BLOCKER]`) are gate items for this surface, not for `30` alone. |
| PS-09 | Anything drawn over a photograph uses the scrim token from `30` §5.2 (α .65 floor, .85 where the headline sits), never a drop-shadow on text — prohibited in `30` §5.2 on every surface. |
| PS-10 | Store screenshots and marketing imagery are **not** invented. `30` §11 and `34` §2 forbid generated artwork standing in for real screens; the marketing surface ships placeholder slots (`30` §5.3) until the upload/asset question closes. |

---

## 6. Shared design layer — the one package four surfaces import

`packages/design-tokens` is named in `14` §2, `08` §9, `12` §7 `DX-4` and `OD-14-06`. Its consumer
contract matters to design consistency more than its contents (`30` holds the values):

```
packages/design-tokens/
├── tokens/          # source of truth: the token names in 30 §3/§4/§5/§7 — colour, type, space, radius, elevation, motion, scrim, series
├── build/           # emits CSS custom properties (web + Control Center) and a Dart ThemeExtension map (Flutter)
└── index.ts         # the only public entry (14 TS-05: barrels at module roots only)
```

| Rule | Detail |
|---|---|
| PS-11 | One source, two outputs. A value added for the Control Center is available to both Flutter apps in the same commit, or the package is not doing `DX-4`'s job. |
| PS-12 | The package holds **names and values only** — no component, no framework import, no runtime dependency. `ML-01`'s discipline applied to design. |
| PS-13 | Semantic pairs (`surface`/`ink`, `canvas`/`body`) are exported as pairs, never as loose colours, because `30` §10's dark-mode proposal (`OD-DOC-31`) can only be adopted cheaply if the pairing already exists in code. |

---

## 7. Control Center — React + Vite interior (`12` §5)

The densest surface: `12` §5.1's 43 navigation destinations, 12 key screens in `12` §5.2 (all 12 catalogued as
`SCR-CC-01`…`12` in `33` §4.2), per-role KPI sets in `12` §5.3, and `12` §9's budget — FCP < 1.5 s,
table interactions < 100 ms perceived.

```
apps/control-center/
├── src/
│   ├── routes/                 # one folder per 12 §5.1 destination, grouped by role family (03 §2)
│   ├── nav/
│   │   └── nav.config.ts       # the 43 destinations, each with icon (30 §11 / 31 nav-icon set)
│   │                           #   and permissionToken: the value from 03 §4 — see PS-14, currently UNRESOLVED
│   ├── components/
│   │   ├── data/               # DataTable wrappers: sort, filter, paginate, export (12 §6.2)
│   │   ├── charts/             # only 30 §8's series palette; ≤ 6 series; table alternative always present
│   │   └── status/             # the compact indicator 33 §5 names as a gap — must not be invented here
│   ├── features/               # approvals, settlement, coverage, price book, commissions, tickets, audit
│   ├── realtime/               # socket rooms per booking (10), freshness rules from 12 §3.3
│   └── lib/                    # query layer (FE-01), money and bps formatters (XS-02, PS-04)
└── ...
```

**Rule PS-14 (the important one)** — `nav.config.ts` cannot be completed today. `10` §4 lists 117 route
rows and `03` §4 declares 92 permission tokens, and **nothing joins a screen to a route or a token** —
`OD-10-06` `[BLOCKER]` and `OD-DOC-29`. So the field is declared, typed and explicitly empty, and the
role filter is *not* simulated with a placeholder token. `33`'s API and permission columns are empty for
the same reason, on purpose; the code mirrors that honesty rather than papering over it. A fabricated
token is worse than an empty one, because it will be shipped.

| Rule | Detail |
|---|---|
| PS-15 | The Control Center is **not** a second design system. It consumes `30`'s tokens like every surface; a role-pressing need for density is expressed as a documented variant in `37` §4, never as a local palette. This is the live tension inside `OD-14-07` (Ant Design themed vs custom on tokens), which is `[IMPORTANT]` and unresolved. |
| PS-16 | No motion in tables and no blur anywhere in this surface (`30` §5.2: row highlight in `brand.50` with no movement; Control Center budget is 100 ms perceived interaction with a 43-item nav). |
| PS-17 | Every screen folder implements the four-state quartet `14` FE-07 demands — skeleton, empty, error-with-retry, permission-denied — as files, not as an afterthought. `ErrorState` and `PermissionDeniedState` are recorded gaps in `33` §5, so their component home is a `12` §6.2 amendment (`DEC-01`), not a folder-local invention. |

---

## 8. The two Flutter apps — feature-first interior (`14` §6.2 `FL-01`)

One skeleton, two apps. `14` `FL-01` fixes the shape (`lib/features/<x>/{data,domain,presentation}`);
what it does not fix is the shared layer, which `OD-14-06` (`[NICE]`) and `OD-14-02` (state management,
**`[BLOCKER]`**) still hold open.

```
apps/customer-app/lib/          (partner-app shares this shape; the two additions are marked)
├── app/                    # router, theme assembly, bootstrap, error handler
├── core/
│   ├── tokens/             # generated from packages/design-tokens (PS-11) — never a literals file
│   ├── api/                # THE GENERATED CLIENT (ADR-012, ML-02, FL-03). Hand-written = review fail.
│   ├── formatters/         # money (XS-02), bps, dates, distance
│   ├── l10n/               # ARB catalogues; status labels from the shared enum (XS-06); 30 % expansion tolerance (12 §8)
│   └── widgets/            # the 12 §6.2 foundation components, themed once
├── features/
│   ├── auth/  catalogue/  booking/  tracking/  payment/  support/  rating/
│   │   ├── data/           # repositories, DTO mappers, local cache
│   │   ├── domain/         # entities and rules — framework-free, the Flutter face of ES-01
│   │   └── presentation/   # screens + widgets + state controller, one folder per SCR-* in 33 §4 / §4.1
│   ├── sync/               # PARTNER ONLY — offline queue, idempotent sync (FL-05, 23 §3.2 idempotency)
│   └── evidence/           # PARTNER ONLY — checklist + photo upload gate; blocked by OD-DOC-34 for its storage path
└── l10n/
```

| Rule | Detail |
|---|---|
| PS-18 | A screen folder is named after its `33` ID (`scr_cc_*`, customer/partner `SCR-*` rows) in its README header comment, so a screen, its states and its asset demand are traceable from code without a spreadsheet. |
| PS-19 | The partner app's offline queue is a **feature**, not a core service, because the customer app has no offline requirement in `12` §3; a shared `core/sync` would make the customer APK pay for a capability it does not use against `12` §9's ≤ 25 MB budget. |
| PS-20 | Neither app renders a status from colour alone (`A11Y-4`, `30` §6), and neither treats an animation as proof of a server state (`30` §7 prohibition 1). In file terms: state comes from the repository/socket layer, and the widget reads it. |

---

## 9. Where a new file goes — the four-question test

| Question | If yes | If no |
|---|---|---|
| Used by two or more surfaces? | `packages/` (`ui`, `design-tokens`, `contracts`, `api-client`, `testing`) | it stays inside the app that owns it |
| A visual state or a token? | `packages/design-tokens` (`30` values) + the component's own state file (`37` §4) | it is a one-off and must be justified in review |
| A screen? | the owning app's `features/…/presentation/`, named for its `33` ID | — a screen not in `33` is not in the product; amend `12` §2–§5 first (`PS-06`) |
| An asset? | `design-assets/` per `31` §6, imported by path, registered in `32` §3 | it is invented UI — refused (`32` §4, `31` §1: a row without a `doc_ref` is an invention) |
| Mode or lifecycle logic from `38` — the guard, the transition service, the step-up? | the owning backend module's `domain/` + `application/`, with the guard as **cross-cutting** middleware, and its database half as a migration under whichever path `OD-DOC-43` chooses. `38` owns the rules; this document only places the files | anywhere a client can set it. A mode read from a header, a store, a config file or an environment variable is a defect (`38` `PM-02`, `14` `ENV-07`), so there is **no legitimate home for it in a front-end package** |
| The mode indicator (`38` `PM-16`)? | `packages/ui`, promoted once under `PS-21` — four surfaces show it, and forking it is exactly the drift `PS-21` names. Where it sits inside the Control Center shell is still open (`OD-DOC-44`), and no component is named here (`37` `CA-00`) | a per-app banner |

**Rule PS-21** — a component that two surfaces want is promoted **once**, into `packages/ui` (the home
`36` §3 defines and `37` §3 lays out), with both call sites updated in the same change. Forking it
because promotion is slower is how `XS-03` ("the status timeline is identical across web, app and
Control Center") becomes three timelines.

---

## 10. What must close before any of this is scaffolded

> **Read this table as what-it-stops, not whether-the-folders-exist.** The directories were created on
> 2026-10-21 by owner direction (§1's status note), so none of these rows is gated by a `mkdir` any more —
> each decides something the **first file** in those folders has to get right, and choosing wrong is a
> rewrite rather than a rename. `OD-14-04` decided `apps/` vs separate repos, which the skeleton assumed;
> if separate repos win, this is not a move but a split of history and CI. That assumption is why the
> scaffold carried no `package.json`: a folder can be renamed, a published dependency cannot. **That is no
> longer true of the front end** — four workspaces now have one each (`14` §2's 2026-10-22 note), so the
> assumption has been *spent*, not tested: if `OD-14-04` decides separate repositories, `apps/web` splits with
> its own lockfile and the three `packages/*` imports `PS-11` relies on become published dependencies. Nothing
> was placed at the repository root, which is why the decision is still open rather than pre-empted.

| Blocker | Why it decides a directory, not a detail |
|---|---|
| `OD-14-04` `[BLOCKER]` | monorepo or separate repos decides whether `apps/` and `packages/` exist at all. §5–§8 assume `14` §2's monorepo shape; if B wins for repos, every cross-package import in `PS-11`/`PS-21` becomes a published dependency. |
| `OD-14-03` `[BLOCKER]` | Turborepo vs Nx decides the root task files and the `packages/config` shape. |
| `OD-14-01` `[BLOCKER]` | Prisma vs Kysely/Drizzle decides `apps/api/src/database/` and every migration path in `16`. |
| `OD-14-02` `[BLOCKER]` | Riverpod vs Bloc decides the shape of `presentation/` in §8 — it is a folder-structure decision wearing a library label. |
| `OD-DOC-38` `[BLOCKER]` | A-vs-B: NestJS vs FastAPI decides §3 vs §4 and forces the `14`/`08`/`16`/`15`/`27` re-edit described in §2.1. |
| `OD-DOC-39` | worker placement: `apps/api/src/workers/` (`14` §2) vs `apps/worker/` (`08` §9) — it decides the deployable unit in `16` §5 and the scaling step in `08` §6.3. |
| `OD-DOC-34` `[BLOCKER]` | media storage and serving decides §5's `public/` story, `PS-08`, and where `features/evidence/` (partner) uploads to. |
| `OD-DOC-43` | where the `38` guard is enforced decides **how many connection configurations exist**: L3 needs a separate database role per purpose (guarded app / purge / migration), which is a directory decision in `16` §5's deployables and in whatever path holds role-grant migrations, not a detail inside one module. `OD-DOC-40`/`41` `[BLOCKER]` gate the same file set from the rules side (`38` §6/§8.3) — a delete path and an invoice-series path cannot be written until both close. |
| `OD-10-06` / `OD-DOC-29` `[BLOCKER]` | no screen → route → permission join exists, so `PS-14`'s empty field stays empty and `33` cannot be completed. |
| `OD-DOC-30` … `OD-DOC-37` | the visual system itself (`30` §12's twelve decisions). Structure can be built against unapproved tokens; **assets cannot be exported and the design gate cannot be certified** (`26` §4.1). |

**What this document unblocks now, with none of the above closed:** the file-placement rules, the
import discipline, the token-package contract (`PS-11`…`PS-13`) and the four-state requirement are all
decidable today, and following them is what makes the design consistent across surfaces — which is the
owner's stated reason for asking for these documents.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.3 | 2026-10-22 | Frontend Lead (first front-end files written) | **Two status sentences corrected against the tree, both kept visible rather than rewritten.** §1's 2026-10-21 block is untouched and a dated block follows it: its "**`.gitkeep` is the only file in any leaf**" is now true of **162** leaves, not all of them — `apps/web`, `packages/ui`, `packages/contracts` and `packages/design-tokens` hold **87 source/config files**, while the rest of the finding stands exactly as written (`P0-03` unmet, every §10 blocker open, nothing at the repository root). §10's blockquote gained the consequence: the monorepo assumption the scaffold made has been **spent, not tested** — four lockfiles and three workspace-local imports exist on it, so an `OD-14-04` answer of "separate repos" is now a split of history and CI rather than a folder move, and it is still the reason `apps/web` sits where §5 puts it. `OD-DOC-38` is unaffected: no backend directory was created and the FastAPI alternative remains unbuilt. **No rule (`PS-01`…`PS-23`), no directory in any §3–§9 tree, no import direction and no blocker row changed.** | §1, §10, Revision History, header |
| 1.2 | 2026-10-21 | Eng Lead (scaffold and git-baseline pass) | §1 gained a **Status, 2026-10-21** paragraph: the trees in this document stopped being only drawings — the directories of `14` §2/§2.1 and here were created as an empty skeleton (221 directories, `.gitkeep` in the 164 leaves only) — and the paragraph states what that does **not** buy: an empty `apps/api/src/modules/booking/domain/` satisfies no rule, ships no screen, fails `P0-03`, and every `[BLOCKER]` in §10 is still open. §10 gained a lead-in that re-reads its table as **what-it-stops** rather than whether-the-folders-exist, and names the asymmetry the scaffold makes visible: **a folder can be renamed, a published dependency cannot**. **No tree, path, package or `PS-*` rule was renamed, added or removed**, and no file was written into any created directory. | §1, §10 |
| 1.1 | 2026-10-21 | Eng Lead (platform-mode pass) | §9's four-question placement test gained **two mode questions**, and they are the only pair in the table whose 'no' branch is a defect rather than a refactor: mode or lifecycle logic goes in the owning backend module with the guard as cross-cutting middleware and its database half as a migration — and **there is no legitimate home for the mode in a front-end package**, because reading it from a header, a store, a config file or an environment variable is `38` `PM-02` / `14` `ENV-07` territory. The indicator itself is promoted **once** into `packages/ui` under `PS-21` rather than forked per surface; its Control Center placement stays open (`OD-DOC-44`) and no component is named (`CA-00`). §10 gained **`OD-DOC-43`** as a structural blocker — where the guard is enforced decides **how many connection configurations and deployables exist**, which is a directory question, not a detail inside one module. **No tree, path, package or rule was renamed or removed.** | §9, §10 |
| 1.0 | 2026-10-21 | Frontend Lead + Engineering Lead (design-engineering structure pass) | First issue, at the owner's direction to document the folder and file structure of every surface plus the backend. Deliberately does **not** restate the top-level tree, which `14` §2 already owns and `08` §9 and `27` §6 mirror — instead `PS-01` names `14` §2 canonical and `DC-04` requires all three to move together. Adds the interiors no document held: website route folders mapped to `12` §2/§2.1, Control Center routes and the `nav.config.ts` permission gap, the two Flutter feature-first skeletons with the partner-only `sync/` and `evidence/`, the shared token package's consumer contract, and a four-question file-placement test. **Records the owner's "FastAPI" instruction as a conflict rather than a change**: `ADR-011` (Accepted, NestJS + TypeScript) and `ADR-012` stand untouched, `14` §1/§2/§2.1 and `08` §9 are unedited, and the collision is registered as `OD-DOC-38` `[BLOCKER]` with an eight-row consequence table and a contingent Python tree in §4 tagged as contingent. Also registers `OD-DOC-39` for the worker-placement disagreement between `14` §2 and `08` §9 that this pass discovered. No package version, licence cost, repository URL or capability was invented; nothing here is scaffolded and no directory named in this document exists. | All |
