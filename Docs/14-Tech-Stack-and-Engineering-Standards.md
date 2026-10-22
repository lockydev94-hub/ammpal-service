# 14 — Tech Stack & Engineering Standards

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-14 |
| Version | 1.8 |
| Status | Approved for Design & Development |
| Owner | Engineering Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-22 |
| Depends On | `08`, `10`, `21`, `26`, `29` |

---

## 1. Stack

| Layer | Technology | Version | Rationale |
|---|---|---|---|
| **Website** | Next.js + React + TypeScript | Next 15 · React 19 · TS 5.x | SSR/SEO for public pages; App Router; static export for the marketing surface |
| **Customer App** | Flutter | 3.x (Dart 3) | One codebase → Android + iOS; strong UI consistency; excellent on low-end Android |
| **Partner App** | Flutter | 3.x | Shares patterns, tokens and the generated API client with the customer app |
| **Control Center** | React + Vite + TypeScript | React 19 · Vite 6 | A dense, authenticated SPA — no SSR requirement; fast HMR; small bundle |
| **Partner web dashboard** | *not yet in the stack* | — | **`[OPEN]` — `OD-DOC-03`/`OD-COM-08`.** `12`, `07` §3.1 and `README` describe a branch-facing dashboard, but `26` does not include one in the paid scope. If it is built it is a **third surface on this stack** (most likely a route set inside the Control Center bundle, reusing its auth, tokens and generated client), and it changes the front-end estimate in `17` and the team shape in `18`. Until `OD-COM-08` is answered this row stays empty on purpose — do not assume it exists |
| **Backend API** | NestJS + TypeScript | Nest 11 | DI + module boundaries + guards/interceptors align exactly with the RBAC model |
| **Main database** | PostgreSQL | 16 | ACID, mature tooling, JSONB, enums, partitioning |
| **Geographic queries** | PostGIS | 3.4 | Point-in-polygon and distance queries in the database |
| **Cache & job queues** | Redis + BullMQ | Redis 7 · BullMQ 5 | Cache, rate limiting, distributed locks, durable queues, delayed/repeatable jobs |
| **Object storage** | S3-compatible | — | Photos, documents, invoices, recordings |
| **Maps** | Google Maps Platform | — | Geocoding, Places, Distance Matrix, Directions |
| **Payments** | Razorpay | — | UPI-first, reliable webhooks, good developer experience |
| **Push** | Firebase Cloud Messaging | — | Free tier, cross-platform, reliable |
| **Realtime** | WebSockets (Socket.IO) | — | Rooms per booking, Redis adapter for horizontal scale, auto-reconnect |
| **IVR & toll-free** | Indian cloud-telephony provider | TBD | DND-compliant commercial voice, IVR, recording (see `OD-INT-01`) |
| **WhatsApp** | Official WhatsApp Business Platform | — | Template messaging, 24-hour window |
| **SMS / Email** | Indian SMS provider / transactional email provider | TBD | OTP-critical SMS; transactional email |
| **Hosting** | Linux VPS | 4 vCPU / 16 GB (Phase 1–2) | Fits the modular monolith; scale-up path in `08` §6.3 |
| **API documentation** | OpenAPI / Swagger | 3.1 | Generated from NestJS decorators; published at `/openapi.json` |
| **Monorepo tooling** | pnpm workspaces + Turborepo | — | Fast, incremental builds; consistent task orchestration |
| **ORM / query layer** | Prisma (or Kysely) | — | Decision in `OD-14-01` |
| **Validation** | Zod + class-validator | — | Zod for shared contracts in `packages/contracts`; class-validator inside NestJS |
| **Testing** | Jest (unit) · Supertest (API) · Playwright (E2E) · Vitest (web) | — | See `15` |
| **Observability** | OpenTelemetry · Prometheus · Grafana · Loki · pino | — | See `16` |

### 1.1 Why TypeScript Everywhere

| Benefit | Detail |
|---|---|
| One language | Front end, back end, contracts and scripts. A Flutter engineer and a backend engineer can read each other's code. |
| Shared contracts | `packages/contracts` is the single source of truth for DTOs and validation, consumed by NestJS, Next.js, the Control Center and the Flutter clients (via OpenAPI codegen). |
| End-to-end refactors | A schema change breaks the compiler in every surface at once, not at runtime in production. |
| Runtime efficiency | Node 22 + a well-tuned NestJS core comfortably meets the Phase 3 targets on 4 vCPU. |

### 1.2 Why Flutter for the Two Apps

| Benefit | Detail |
|---|---|
| One codebase, two stores | Android + iOS from one team. |
| Low-end Android performance | Flutter's rendering is consistent on the ₹8,000–₹15,000 Android devices that dominate the Odisha market. |
| Offline-first maturity | Local database + sync queue is straightforward. |
| UI consistency | Both apps share components and design tokens, so the technician and customer experiences feel like one product. |

### 1.3 Dependency Update and Vulnerability Cadence `[PROPOSED]`

Nothing in this repository is executed today — there is no pipeline and no lockfile in version
control. This section is the policy the scaffold must implement, not a description of a running
process. It exists because `29` already refuses a release when a critical/high CVE is open
without a written acceptance and an expiry date, and `17` lists "dependency patching" as a
standing ops activity, while no document said how often anything gets updated. The gate had no
input feeding it.

6. **A front-end dependency is chosen from `36` §4/§5, not from habit.** `36` states the eight
   admission rules (`LB-01`…`LB-08`), the `13` §5.2 CSP gate that rejects anything loading a remote
   font, script or un-nonce'd style, and the ten libraries this suite has already decided not to use.
   A capability with no admitted library goes to `21` as a new `OD-14-*` row before it goes into
   `package.json` — and there is no `package.json` yet, so this rule is currently a rule for the
   scaffold, not a description of one.

| Class | Trigger | Cadence | Who | Note |
|---|---|---|---|---|
| **Security patch** (fixes a known CVE) | Advisory published against a direct dependency | Same working day for critical, **≤ 7 days** for high, **≤ 30 days** for medium | Eng Lead triages; the owning surface lead applies | A critical that cannot be applied within the day is an incident per `25` §3, not a backlog item |
| **Patch/minor release** (no CVE) | Upstream release | Monthly batch, one PR per package group | Rotating engineer | Batched so a regression has one small blast radius and a clean revert |
| **Major upgrade** (breaking) | Upstream major | Quarterly review; scheduled into the next available phase in `17`, never mid-phase | Eng Lead + Founder where it touches a vendor SDK | The four high-churn items are **NestJS, Next.js/React, Flutter, Prisma-or-not** (`OD-14-01` must land before Prisma majors are tracked) |
| **Runtime / base image / Postgres / Redis** | Vendor EOL date | Tracked against EOL, not against a release cycle | Eng Lead | Postgres 16 and Redis 7 are the versions pinned in §1. An EOL falling inside the six-month target in `26` §4.1 or the annual-service horizon in `26` §4.5 is a decision that needs the Founder, not an ops task |

**Commercial caveat** — `26` §4.5 item 1 lists "patching, security updates" among the annual-service
terms that are **not yet defined**. Every row above is therefore currently unbilled, unbounded work:
the cadence is specified, but nobody has agreed who pays for it or how much of it sits inside the
₹60,000 single-city figure. That is `OD-COM-04` (what the annual service includes) and `OD-COM-07`
(what third-party consumption is inside the fee) — this document does not decide them. Writing the
policy is not the same as committing to it.

**Mechanical rules**

1. Automated PRs are opened by the bot; **a human merges**. Auto-merge is disabled for any change that touches authentication, payment, telephony or the ORM, because those four are where a silent upgrade becomes a financial or compliance defect.
2. A dependency PR is only green when `pnpm install --frozen-lockfile` succeeds in CI and the suite in `15` passes; the lockfile is committed, and `--frozen-lockfile` is the check that a manifest and a lockfile have not drifted.
3. Vendor SDKs (Razorpay, WhatsApp, SMS, telephony, Maps) are **not** upgraded on cadence. They are upgraded when the integration contract in `24` changes, because the breaking surface is the provider's API, not the package.
4. Flutter packages are upgraded in the app that consumes them, not in the shared token package (`OD-14-06`) first, so a store build failure cannot block the API.
5. An accepted-but-unfixed advisory goes in a dated register that the release checklist in `29` reads. "Accepted" without an expiry date is not acceptance.

The tooling choice (Renovate vs Dependabot vs a scheduled audit job) and the exact day of the
monthly batch are **not decided here** — see `OD-14-08` in `21`.

---

## 2. Repository Layout

```
ammpal-service/
├── apps/
│   ├── api/                       # NestJS modular monolith
│   │   ├── src/
│   │   │   ├── main.ts
│   │   │   ├── app.module.ts
│   │   │   ├── common/            # guards, filters, interceptors, decorators, pipes
│   │   │   ├── config/            # typed configuration + validation
│   │   │   ├── database/          # Prisma/Kysely client, migrations, seeding
│   │   │   ├── modules/
│   │   │   │   ├── identity/
│   │   │   │   ├── rbac/
│   │   │   │   ├── organization/
│   │   │   │   ├── catalog/
│   │   │   │   ├── workflow/
│   │   │   │   ├── partner/
│   │   │   │   ├── booking/
│   │   │   │   ├── pricing/       # PURE domain module — no I/O
│   │   │   │   ├── billing/
│   │   │   │   ├── commission/    # PURE domain module — no I/O
│   │   │   │   ├── support/
│   │   │   │   ├── notification/
│   │   │   │   ├── realtime/
│   │   │   │   ├── reporting/
│   │   │   │   ├── audit/
│   │   │   │   └── integration/
│   │   │   └── workers/           # BullMQ processors (same app, separate entry)
│   │   └── test/
│   ├── web/                       # Next.js (website)
│   ├── control-center/            # React + Vite
│   ├── customer-app/              # Flutter
│   └── partner-app/               # Flutter
├── packages/
│   ├── contracts/                 # zod schemas, DTO types, error codes, enums
│   ├── design-tokens/             # colour, spacing, typography, elevation
│   ├── api-client/                # generated OpenAPI clients (web + apps)
│   ├── config/                    # eslint, tsconfig, prettier, editorconfig
│   └── testing/                   # factories, fixtures, builders, mocks
├── docs/                          # ← this directory — it exists as `Docs/` (capital D). One directory, not two.
├── infra/
│   ├── docker/                    # Dockerfiles, compose
│   ├── ansible/                   # VPS provisioning
│   ├── nginx/                     # reverse proxy + TLS
│   └── monitoring/                # prometheus, grafana, loki, alert rules
├── scripts/                       # codegen, db ops, seed — NOT the documentation checkers,
│                                  #   which live in `maintenance/scripts/` (`README` §12.5, §16)
└── .github/workflows/
```

> **Scaffold status, 2026-10-21.** At the owner's direction ("scaffold as base on docs") this tree and the
> `35` §5–§8 interiors were created as **221 empty directories**, `.gitkeep` in each of the 164 leaves, and committed on top
> of a documentation-only baseline. **Nothing in them is code**: no `package.json`, `tsconfig`, lockfile,
> source file, migration, Dockerfile or workflow YAML exists, so `17` `P0-03` ("`apps/*` and `packages/*`
> build; CI runs green") is **not** met and `ADR-025` still bars the `[IMPLEMENTED]` tag from every path
> below. The layout follows side A because `ADR-011` is the only **Accepted** backend decision on file;
> `OD-DOC-38` remains open and `35` §4's FastAPI alternative was not created. `08` §9 and `27` §6 mirror
> this tree and disagree about worker placement (`OD-DOC-39`) — `35` `PS-01` names §2 above as canonical.
>
> **Superseded 2026-10-22 for `apps/` and `packages/`, and the sentence it is superseded on is the one above:
> "no `package.json`, `tsconfig`, lockfile, source file … exists".** Four workspaces now carry real code —
> `apps/web` (Next 15 App Router, Home's eight sections), `packages/ui`, `packages/contracts` and
> `packages/design-tokens`: **87 source/config files** between them (counted by `find` over those four paths,
> excluding `.gitkeep`, `node_modules/`, `.next/`, `dist/`, `*.tsbuildinfo` and `next-env.d.ts` — build output
> is not source), the remaining **162 `.gitkeep` leaves**
> still empty. Each workspace owns its own `package.json`, lockfile, `node_modules` and `tsconfig`; **nothing
> was placed at the repository root**, which is the constraint the owner set when approving the install, so
> `OD-14-04` stays open and `apps/web/` records the monorepo answer as an assumption made visible (`39` §5).
> What that does *not* buy: `P0-03` is **still not met**, because it asks that `apps/*` **and** `packages/*`
> build with CI green — there is no workflow YAML and no backend to build; the four workspaces that exist are
> verified locally (`tsc --noEmit` clean across all four, `next build` clean, ESLint 0 errors). `ADR-025`
> still bars `[IMPLEMENTED]` from every path below, and the application code is **uncommitted by owner
> direction** (2026-10-22): the public remote carries the documents, the registers and the `.gitignore` that
> keeps generated artwork out of it, not the build.

> **This tree is the target for the application repository; it is not the current workspace, and only four of
> its paths hold anything.** The workspace today holds `Docs/` (capitalised — this suite),
> `visualize-image-of-project/` (4 reference infographics, `NOT_FOR_PRODUCTION`), `maintenance/` (the checkers,
> the prompt pack and the intake scripts), `design-assets/`
> (asset folders, two registers and 19 generated raster masters with 58 exports — **none approved**) and,
> since 2026-10-22, the four front-end workspaces named above —
> `design-assets/` deliberately does **not** appear
> above, because `31` §6 places approved asset masters at workspace root alongside their manifests, and
> because **three of this document's own `[BLOCKER]` rows are open**: `OD-14-04` (one monorepo or
> separate repos per app — the decision that determines whether §2's shape is even correct), `OD-14-03`
> (Turborepo or Nx — it decides the root workspace files) and `OD-14-01` (the data layer, which §2's
> `database/` directory presumes). There is no `source-code/` directory anywhere in this workspace;
> `31` §6 records why.
>
> **§2 is the top level only.** The interior of every surface — what sits inside `apps/web/src`, inside
> each Flutter `lib/`, inside the Control Center, inside the token package, and where the queue workers
> go — is `35`, whose rule `PS-01` names **this section canonical** and forbids a fourth copy of the
> tree. Two rows in `21` now hang on the shape above: **`OD-DOC-38` `[BLOCKER]`**, because the owner has
> asked for a FastAPI backend while `ADR-011` (Accepted) names NestJS, which is the framework in every
> row of §1 and the language `packages/contracts` is written in; and **`OD-DOC-39` `[IMPORTANT]`**,
> because `08` §9 places the workers at a top-level `apps/worker/` where §2 places them at
> `apps/api/src/workers/`. Both sides of each conflict stay on file (`DEC-07`); `35` §4 documents the
> contingent Python layout so that a superseding ADR does not silently lose the module boundaries, the
> `ES-01` purity rule or `ADR-012`.

### 2.1 Module Internal Structure

> The **NestJS** interior. If `OD-DOC-38` resolves to a Python backend, the equivalent interior — the
> router / schema / service / repository / domain split, and the test tree that must mirror it — is
> `35` §4, and `ES-01`'s purity requirement survives the change of language unchanged.

```
apps/api/src/modules/booking/
├── booking.module.ts          # NestJS module — declares providers, exports, imports
├── domain/                    # pure business logic, no NestJS decorators
│   ├── booking-state-machine.ts
│   ├── booking-policy.ts
│   ├── booking.service.ts
│   └── booking.errors.ts
├── application/               # use cases orchestrating domain + repositories + events
│   ├── create-booking.usecase.ts
│   ├── accept-offer.usecase.ts
│   └── complete-booking.usecase.ts
├── infrastructure/            # repository implementations, event publishers
│   ├── booking.repository.ts
│   └── booking.events.ts
├── interfaces/                # HTTP controllers, DTOs, mappers
│   ├── booking.controller.ts
│   └── booking.dto.ts
├── booking.manifest.ts        # declares owned tables + dependencies (MB-03)
└── index.ts                   # public contract barrel (everything else is private)
```

**Rule ES-01** — `domain/` contains **no NestJS imports**. It is plain TypeScript with injected interfaces. This makes the business logic testable without a Nest testing module and is what allows the `pricing` and `commission` modules to be pure.

---

## 3. Code Standards

### 3.1 TypeScript

| Rule | Detail |
|---|---|
| TS-01 | `strict: true`, plus `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `noFallthroughCasesInSwitch`. |
| TS-02 | `noImplicitAny` is on; `any` is banned. Use `unknown` + narrowing. |
| TS-03 | Explicit return types on exported functions. |
| TS-04 | `import type` for type-only imports. |
| TS-05 | Barrel files only at module roots (`index.ts`), never deep in the tree. |
| TS-06 | No default exports — **with one carve-out, because the framework requires it**: a Next.js App Router file whose *role* is a default export (`page`, `layout`, `not-found`, `route`, `loading`, `error`, `template`, `default`, and the `generateMetadata`/`generateStaticParams` companions those files already export as named) exports default. The rule still binds everything else in those files: components, helpers, fixtures and tokens are named exports, and the default in a route file is the framework's entry point, not a style choice. **Enforcement is not in place yet** — `apps/web/eslint.config.mjs` does not switch `import/no-default-export` on, so nothing fails today. Adding it needs a `files` override for `app/**` *and* for the toolchain's own config files, which default-export by contract (`next.config.ts`, `postcss.config.mjs`); naming those two is what makes the exception a line a reviewer can read rather than a suppressed warning. |
| TS-07 | Domain errors are typed unions or a typed `DomainError` class — never string codes inline. |
| TS-08 | Money is `number` of paise with a branded type `type Paise = number & { __brand: 'paise' }`. Rates are `type Bps = number & { __brand: 'bps' }`. Branded types prevent mixing units. |

### 3.2 Formatting & Linting

| Tool | Config |
|---|---|
| Prettier | 100-column print width, single quotes, trailing commas, semicolons |
| ESLint | `typescript-eslint` strict + `eslint-plugin-import` (no cycles across modules) + `eslint-plugin-security` + `eslint-plugin-boundaries` (enforces module isolation) |
| EditorConfig | 2-space indent, LF, final newline |
| Commit format | Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`) |
| Pre-commit | Lint-staged: format + lint on changed files |
| Pre-push | Type-check + affected unit tests |

### 3.3 Naming

| Thing | Convention | Example |
|---|---|---|
| Files | kebab-case | `create-booking.usecase.ts` |
| Classes | PascalCase | `CreateBookingUsecase` |
| Functions/variables | camelCase | `computeEligibleLabour` |
| Constants | UPPER_SNAKE | `MAX_ACCEPTANCE_WINDOW_MINUTES` |
| Types/interfaces | PascalCase, no `I` prefix | `BookingSnapshot` |
| Enum values | UPPER_SNAKE | `BookingStatus.REQUESTED` |
| DB columns | snake_case | `eligible_labour_paise` |
| API JSON | camelCase | `eligibleLabourPaise` |
| API paths | kebab-case, plural nouns | `/booking-offers` |
| Env vars | UPPER_SNAKE, prefixed | `DATABASE_URL`, `RAZORPAY_WEBHOOK_SECRET` |

### 3.4 Error Handling

```ts
// Domain errors are typed and carry a stable machine code.
export class DomainError extends Error {
  constructor(
    readonly code: ErrorCode,
    message: string,
    readonly details?: Record<string, unknown>,
  ) {
    super(message);
    this.name = 'DomainError';
  }
}

// Domain modules throw. The API layer maps them to HTTP.
```

| Rule | Detail |
|---|---|
| ERR-03 | Domain code throws `DomainError`; the HTTP layer maps `code` → status (`10` §6.1). |
| ERR-04 | The error envelope is produced by a single global exception filter. |
| ERR-05 | Unexpected errors are logged with a stack trace and returned as a generic `INTERNAL_ERROR` with a `requestId`. |
| ERR-06 | Never swallow an error. If it is ignored, log it at `warn` with context. |

---

## 4. Database & Data Access

| Rule | Detail |
|---|---|
| DB-01 | All queries are parameterised. No string concatenation of user input into SQL. |
| DB-02 | Migrations live with their owning module and are applied in order by a single migration runner. |
| DB-03 | Migrations are forward-only in production; a rollback is a new compensating migration. |
| DB-04 | Every migration that touches a large table must be non-blocking (`CONCURRENTLY`, `NOT NULL` with a default, or a separate backfill step). |
| DB-05 | Destructive schema changes require two releases of deprecation first. |
| DB-06 | Indexes are created with `CONCURRENTLY` in production. |
| DB-07 | No query may run unbounded. All list endpoints are paginated and use the cursor where possible. |
| DB-08 | N+1 access is forbidden. Use joins, `IN` queries or batched reads. |
| DB-09 | Long-running analytics queries run against a read replica or a materialised read model — never the primary. |
| DB-10 | Transactions are short (< 100 ms) and never contain an external network call. |
| DB-11 | Money columns are `BIGINT` paise; rates are `INT` bps. Checked by a migration lint. |
| DB-12 | Every table with `branch_id` is indexed on `branch_id`. |

---

## 5. API Engineering

| Rule | Detail |
|---|---|
| AE-01 | Controllers are thin. They validate, delegate to a use case, and map the response. |
| AE-02 | Use cases own transactions. Repositories do not open transactions. |
| AE-03 | Guards: `JwtAuthGuard` → `PermissionsGuard` → `ScopeGuard`. Registered in a fixed global order. |
| AE-04 | All `POST` create endpoints accept `Idempotency-Key` and implement the idempotency store. |
| AE-05 | DTOs are validated with a whitelist; unknown fields are rejected. |
| AE-06 | Versioned resources get a `version` column; updates require `If-Match`. |
| AE-07 | Every endpoint declares its rate limit. |
| AE-08 | OpenAPI is generated from decorators; `@ApiResponse` is mandatory on every handler. |
| AE-09 | Controllers never contain business logic. A review checklist enforces this. |
| AE-10 | Long-running work returns `202 Accepted` with a job id; it never holds an HTTP connection open. |

---

## 6. Frontend Standards

### 6.1 Web & Control Center

> **Which library may fill which capability: `36` §4. How a component is built, varianted, styled
> and reviewed: `37`. This section holds the engineering rules (`FE-*`) and nothing else** — a fourth
> copy of either would be the drift `OD-DOC-39` is an example of (`DEC-01`).

| Rule | Detail |
|---|---|
| FE-01 | Data fetching uses a typed query layer (TanStack Query for the Control Center; server components + route handlers for Next.js). |
| FE-02 | No direct `fetch` to the API outside the query layer. |
| FE-03 | All money rendering uses a shared formatter with locale-aware currency. |
| FE-04 | No `any` in component props. |
| FE-05 | Every user-facing string comes from the i18n catalogue. A lint rule fails CI on hard-coded strings. |
| FE-06 | Forms use a schema-first approach: one zod schema per form, shared with the API contract where possible. |
| FE-07 | Error states are designed: loading (skeleton), empty, error-with-retry, and permission-denied are distinct. |
| FE-08 | Accessibility is checked in review (`12` §6.3). |

### 6.2 Flutter

> Package-by-package selection for both apps is `36` §5; the Flutter mirror of the component contract
> is `37` §9 (`CA-27`). `FL-*` rules below are the engineering constraints, not a catalog.

| Rule | Detail |
|---|---|
| FL-01 | Feature-first folder structure: `lib/features/booking/{data,domain,presentation}`. |
| FL-02 | State management: Riverpod (or Bloc) — decision in `OD-14-02`. |
| FL-03 | The API client is **generated** from OpenAPI and committed; it is never hand-written. |
| FL-04 | All money uses an integer-paise value object with a formatted display extension. |
| FL-05 | Offline-first for the Partner App: a local queue (Drift/SQLite) with idempotent sync. |
| FL-06 | Widget tests for every stateful widget with business logic; golden tests for the 5 most important screens. |
| FL-07 | No `print()` in release; use structured logging. |
| FL-08 | Crash reporting (Crashlytics) with PII scrubbing enabled. |

---

## 7. Testing Standards

| Rule | Detail |
|---|---|
| TST-01 | Every domain module has unit tests at the **use-case** level, mocking only repositories and vendor adapters. |
| TST-02 | `pricing` and `commission` require **≥ 95%** line coverage and a full **golden-master** suite (`15` §5.3). |
| TST-03 | Every API endpoint has an integration test against a real Postgres (Testcontainers or a CI service container). |
| TST-04 | Architecture tests enforce module boundaries on every push. |
| TST-05 | Contract tests validate generated clients against the OpenAPI document. |
| TST-06 | Critical journeys have Playwright E2E coverage. |
| TST-07 | No test may depend on another test's state; each is isolated. |
| TST-08 | Flaky tests are quarantined and fixed within 48 h, not re-run into green. |
| TST-09 | Test data factories live in `packages/testing` and are reused. |

---

## 8. Git & Branching

| Rule | Detail |
|---|---|
| GIT-01 | `main` is always deployable and protected. |
| GIT-02 | Branch naming: `feat/<ticket>-<slug>`, `fix/<ticket>-<slug>`, `chore/<slug>`, `docs/<slug>`. |
| GIT-03 | Trunk-based with short-lived branches (< 3 days). |
| GIT-04 | Pull requests require: ≥ 1 approval, passing CI, a linked ticket, and no unresolved review comments. |
| GIT-05 | Squash-merge with a Conventional Commit message. |
| GIT-06 | Feature flags gate incomplete work; flags are removed within 2 releases. |
| GIT-07 | Migrations must be backward-compatible with the currently deployed version (expand → migrate → contract). |
| GIT-08 | Database changes and code changes deploy independently and safely in any order. |

---

## 9. CI/CD Pipeline

```
┌─ On push / PR ────────────────────────────────────────────────────────┐
│ 1. Install (pnpm, frozen lockfile)                                    │
│ 2. Lint + format check                                                │
│ 3. Typecheck (api, web, control-center)                               │
│ 4. Architecture tests (module boundaries)                              │
│ 5. Unit tests (coverage gate)                                         │
│ 6. Golden-master tests (pricing + commission)                         │
│ 7. Integration tests (Testcontainers Postgres + PostGIS)              │
│ 8. OpenAPI generation + drift check                                   │
│ 9. Build (api, web, control-center) + Flutter analyze/test           │
│ 10. Dependency scan + secret scan + SAST                              │
│ 11. Docker image build + push to the registry                         │
└────────────────────────────────────────────────────────────────────────┘
┌─ On merge to main ────────────────────────────────────────────────────┐
│ 12. Deploy to dev  → smoke tests                                      │
│ 13. Deploy to staging → E2E (Playwright) + migration rehearsal       │
│ 14. Manual approval → deploy to prod (canary 10% → 50% → 100%)        │
│ 15. Post-deploy smoke + automated rollback if the health gate fails  │
└────────────────────────────────────────────────────────────────────────┘
```

**Rule CI-01** — The pipeline never deploys from a local machine.
**Rule CI-02** — Production deploys require a manual approval from a non-author of the change.
**Rule CI-03** — A failed smoke test after a production deploy triggers an automatic rollback.

---

## 10. Logging

| Rule | Detail |
|---|---|
| LOG-01 | Structured JSON via pino. No string concatenation. |
| LOG-02 | Every log line carries `requestId`, `traceId`, `userId` (when authenticated), `role`, `branchId` (when scoped). |
| LOG-03 | Levels: `error` (needs action), `warn` (needs attention), `info` (business events), `debug` (dev only, off in prod), `trace` (diagnostics, sampled). |
| LOG-04 | Redacted fields: `otp`, `password`, `token`, `refreshToken`, `cardNumber`, `cvv`, `bankAccount`, `documentNumber`, `authorization`. |
| LOG-05 | Business events are emitted as structured events, not free-text logs — they feed the analytics pipeline. |
| LOG-06 | Log volume is controlled by sampling debug/trace in production. |

---

## 11. Environment & Secrets

| Rule | Detail |
|---|---|
| ENV-01 | `.env.example` per app documents every variable with a description and default. |
| ENV-02 | No secret is ever committed. Pre-commit secret scanning is enabled. |
| ENV-03 | Production secrets live in the server's secret store (systemd credentials / a `.env` file with `0600` owned by the deploy user, or a vault). |
| ENV-04 | Configuration is validated at boot — the app refuses to start with invalid config (`12-factor`, fail-fast). |
| ENV-05 | `NODE_ENV=production` enables strict mode: no stack traces, no verbose logs, no dev routes. |
| ENV-06 | Secrets are rotated; the rotation procedure is documented in `16`. |
| ENV-07 | The platform mode (`38`) is **database state, not configuration**. A variable may seed `platform.platform_mode` once on an empty database and never overrides it afterwards; boot reads the row and, on production infrastructure, refuses to serve staff mutations in `TESTING` without a recorded bootstrap exception (`16` §5). An `APP_MODE`-style flag that silently disagrees with the row is a defect, not a fallback. |

---

## 12. Code Review Checklist

- [ ] Does this belong to the right module? (`08` §2.3)
- [ ] Is business logic in `domain/`, not in a controller or a repository?
- [ ] Are money values integer paise with a branded type?
- [ ] Is the query parameterised and paginated?
- [ ] Are permissions and scope enforced?
- [ ] Is the operation idempotent or protected against duplication?
- [ ] Does a state change emit a domain event?
- [ ] Are tests present at the appropriate level, and do they cover the failure path?
- [ ] Are new user-facing strings localised?
- [ ] Is the migration backward-compatible with the deployed version?
- [ ] Does the OpenAPI document need updating?
- [ ] Is anything sensitive being logged?

---

## 13. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| OD-14-01 | **Prisma vs Kysely/Drizzle**: Prisma gives a great DX and migrations but a weaker story for raw SQL (needed for PostGIS and complex reporting). Drizzle is SQL-first. Recommend Prisma for the app + raw SQL via `$queryRaw` for PostGIS/reporting, or Kysely throughout. | Engineering | Phase 0 |
| OD-14-02 | Flutter state management — Riverpod or Bloc? Recommend Riverpod (less boilerplate, better testability). | Mobile Lead | Phase 0 |
| OD-14-03 | Monorepo task runner — Turborepo or Nx? Recommend Turborepo (simpler, less opinionated). | Engineering | Phase 0 |
| OD-14-04 | Do we use a monorepo at all, or separate repos per app? Recommend one monorepo for contract consistency. | Engineering | Phase 0 |
| OD-14-05 | Which SMS provider and transactional email provider? | Engineering | Phase 0 |
| OD-14-06 | Do we adopt a shared design-system package for Flutter (`flutter_design_tokens`) or duplicate? | Design + Mobile | Phase 1 |
| OD-14-07 | Should the Control Center use a component library (Ant Design / MUI) or custom components on the design tokens? | Design + Frontend | Phase 1 |
| OD-14-08 | Dependency-update **tooling** — Renovate, Dependabot, or a scheduled audit job? §1.3 sets the cadence; the mechanism is undecided and needs the pipeline (§9) to exist first. | Engineering | Before the first production release |
| OD-14-09 | **Styling engine and component primitives for the web and the Control Center** — the `FE-*` rules assume a typed token pipeline and a headless-primitive layer, and `OD-14-07` already asks the component-library half of this question for the Control Center. Candidates and the constraints each must satisfy: `36` §4. | Frontend Lead + Design | Before the front-end scaffold |
| OD-14-10 | **Animation runtime** — declarative compositor-driven motion versus an imperative timeline library versus Flutter's own `AnimatedTheme`. `36` §4/§5 name the candidates, `37` §6 fixes the nine recipes the chosen one must be able to express, and `12` §9's budget is the limit. | Frontend Lead + Mobile Lead | Before Phase 1 |
| OD-14-11 | **Charting and data-grid** for the Control Center — `12` §6.2 names a `DataTable` with sort/filter/paginate/export and the operations screens need charts; neither has an admitted implementation. `36` §4. | Control Center Lead | Before Phase 1 |
| OD-14-12 | **Component workshop and visual-regression tooling** — `37` §11.2 lists nine checks that are meant to run automatically, and none of them can until a workshop and a screenshot diff exist. `15` §2 and `16` §9 assume the artefacts, not the tool. | Design + QA | Before the design-gate review |
| OD-14-13 | **Design-token build tooling** — `30` holds the values, `35` §6 defines the token package's layout, `37` `CA-09`…`CA-15` define what consumes them, and no document says what compiles one into the other (CSS custom properties, Dart, and any native surface). `PS-11` forbids a hand-copied value, so this is a build question, not a preference. | Design + Frontend | Before the first component is written |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.8 | 2026-10-22 | Frontend Lead + Eng Lead (first code merged into the tree) | **Two stale statements corrected, measured rather than reworded.** `TS-06` gains the carve-out the framework forces: an App Router file whose *role* is a default export (`page`, `layout`, `not-found`, `route`, `loading`, `error`, …) may have one, everything else in the repository still may not — and the row now says plainly that **enforcement is not in place**, because `apps/web/eslint.config.mjs` does not enable `import/no-default-export` and switching it on needs overrides for `app/**` plus `next.config.ts` and `postcss.config.mjs`, which default-export by contract. §2's 2026-10-21 scaffold block is **kept as written and annotated beneath it**: "no `package.json`, `tsconfig`, lockfile, source file … exists" is no longer true of the front end (`apps/web`, `packages/ui`, `packages/contracts`, `packages/design-tokens` hold **87 source/config files**; **162 `.gitkeep` leaves remain empty**, nothing is at the repository root), and the block that claimed "no directory in it has been created" now lists what the workspace actually holds, `maintenance/` and the four workspaces included. `P0-03` is restated as **still not met** — no workflow YAML, no backend, verification is local only — and `ADR-025`'s `[IMPLEMENTED]` bar is unchanged, alongside the owner's 2026-10-22 scope decision that the application code stays **uncommitted** while documents, registers and the artwork `.gitignore` are pushed. **No stack row (§1), module boundary, `[BLOCKER]` or standard other than `TS-06` changed**; `OD-14-04`, `OD-14-03`, `OD-14-01`, `OD-DOC-38` and `OD-DOC-39` all stay open exactly as §2 records them. | §2, §TS-06, Revision History, header |
| 1.7 | 2026-10-22 | Eng Lead (website-design pass) | §2's workspace-state annotation was **re-measured, not reworded from memory**: `design-assets/` no longer holds "two registers, no artwork". It now holds those two registers plus **19 raster masters and 58 exports** in six sections (`01-brand`, `02-website`, `03-customer-app`, `04-partner-app`, `05-control-center`, `08-store`), all `GENERATED` and **none approved**, with the six generated-but-`BLOCKED` category PNGs held outside the tree in `maintenance/holding-blocked/`. The counts were printed by `validate_assets.py` (93 rows: 65 `PLANNED`, 18 `GENERATED`, 6 `BLOCKED`, 4 `REGISTERED`; 22 manifest records; 0 errors) and the file totals by a filesystem glob, not taken from the intake script's own output. **No stack row, standard, module boundary or `[BLOCKER]` in this document changed**; `OD-14-04`/`09` remain open and nothing was installed, so `apps/` and `packages/` remain 221 empty directories. | §2, Revision History, header |
| 1.6 | 2026-10-21 | Eng Lead (scaffold and git-baseline pass) | §2’s canonical tree was **annotated, not redrawn** (`DEC-07`): the `docs/` line now records that it exists as `Docs/` (capital D), and the `scripts/` line records that it is **not** the documentation checkers, which live at `maintenance/scripts/`. A new **"Scaffold status, 2026-10-21"** blockquote states what a tree diagram cannot: 221 directories (164 leaves) were created empty from this section and `35` §3/§5–§8, `.gitkeep` marks only the leaves, and no `package.json`, dependency, source file, migration or CI configuration exists in any of them, so `P0-03` ("`apps/*` and `packages/*` build; CI runs green on an empty app") is **not met**. Side A of the `OD-DOC-38` conflict — this section’s NestJS line, the only **Accepted** decision on the record — is the one built, and the note says that is a choice of evidence, not a resolution; `08` §9 and `27` §6 mirror the same tree and disagree with it via `OD-DOC-39`. **No standard, version, dependency or `ES-*` rule was changed.** | §2, §2.1 |
| 1.5 | 2026-10-21 | Eng Lead (platform-mode pass) | **`ENV-07`** added in §11: the platform mode is database state, not configuration. An environment variable may **seed the row once, at first boot, and never override it afterwards**; any code path that reads the mode from config, a feature flag, a request header or a client store is a defect, and the standard is stated here so a reviewer can reject it by rule number. This is the engineering-standards half of `38` `PM-02`/`PM-04` and it exists because the failure mode is invisible — a correctly-built screen can be pointed at a `TESTING` database and show the wrong thing convincingly. | §11 |
| 1.4 | 2026-10-21 | Engineering Lead + Frontend Lead (design-engineering structure pass) | The document this pass had to annotate rather than rewrite, because its §2 tree is the suite’s **canonical** one (`35` `PS-01`). §2’s lead blockquote now names both open questions sitting on that tree — `OD-DOC-38` `[BLOCKER]` (FastAPI as instructed versus Accepted `ADR-011`’s NestJS) and `OD-DOC-39` `[IMPORTANT]` (worker placement, where `08` §9 diverges) — and says why the interiors live in `35` instead of being drawn a fourth time here. §2.1 is now labelled the **NestJS** interior, with `35` §4 named as the contingent Python one and `ES-01`’s purity requirement explicitly surviving a change of language. §1.3 gained rule **6**: a front-end dependency is chosen from `36` §4/§5, and a capability with no admitted library goes to `21` before it goes into `package.json`. §6.1 and §6.2 gained one-line pointers to `36` and `37`, so the `FE-*`/`FL-*` rules stay rules rather than catalogues. **§13 gained `OD-14-09`…`13`** (styling engine, animation runtime, charting and data-grid, workshop and visual regression, token build) in the register’s own order and wording. No stack row, version, cadence rule or `ES-*`/`FE-*`/`FL-*`/`CI-*` rule was altered. | §1.3, §2, §2.1, §6.1, §6.2, §13, Revision History, header |
| 1.3 | 2026-10-21 | Engineering Lead (design-system and asset pass) | One blockquote added under §2, changing no stack choice, module path or rule. It states that the tree in §2 is the **target application repository** and that none of its directories exists yet; that the current workspace holds `Docs/`, `visualize-image-of-project/` and `design-assets/`; that `design-assets/` is intentionally absent from the tree because `31` §6 places asset masters at workspace root beside their two registers; and that **no `source-code/` directory exists**, because `OD-14-01`/`OD-14-03`/`OD-14-04` are open and §2/`08` §9 already fix the layout. Added to help an agent that reads §2 and concludes the scaffold has been agreed. | §2, header, Revision History |
| 1.2 | 2026-10-21 | Engineering Lead (documentation audit pass 3) | Added §1.3, the dependency-update and vulnerability cadence, marked `[PROPOSED]` because nothing in §1.3 is executed today — the repository has no pipeline and no committed lockfile. The section exists to feed the CVE release gate in `29` and the "dependency patching" ops activity in `17`, neither of which had a defined input. Commercial boundary flagged against `26` §4.5 item 1. Added the conditional **Partner web dashboard** row to §1 (per `OD-DOC-03`/`OD-COM-08`) rather than leaving the stack table silent about a surface other documents describe. Added `OD-14-08` to §13. Header `Depends On` extended. The prior 1.1 entry was found to describe cross-references that do not exist in this document — corrected below. | §1, §1.3, §13, header, Revision History |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | *(entry corrected 2026-10-21 — the original text is preserved, not deleted)* Documentation audit and consolidation. Cross-referenced the audit additions (the `legal_entities` table, the new entities, the idempotency store) and the ADR-002 two-layer model in the data-access rules. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |

> **On the 1.1 entry.** That summary describes changes that are **not present in this document**:
> `legal_entities` does not appear anywhere in §1–§13, `ADR-002` is not referenced, and the data-access
> rules in §4 (DB-01…DB-12) contain no two-layer booking-model or idempotency-store cross-reference —
> the only idempotency mention is API rule AE-04, which predates it. Either the 1.1 edits were made to a
> different document and copied here, or they were lost. The actual v1.1 change set cannot be recovered
> from this repository, so the entry is marked unreliable rather than rewritten. Future audits should not
> treat "v1.1 audited this document" as evidence that anything in it was verified.
