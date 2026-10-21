# 29 — Release & Deployment Checklist

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-29 |
| Version | 1.5 |
| Status | Approved for Design & Development |
| Owner | Engineering Lead + QA Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `15`, `16`, `17`, `12`, `13`, `30`, `32`, `34` |

> **Implementation status — read this first.**
>
> **Nothing described in this document has been built, run, rehearsed or executed.** This repository contains
> documentation and four PNG diagrams only — no application source code, no CI configuration and no deployed
> environment exist. Every checklist, gate, threshold, query, command and template below is a **designed control**
> with **no execution history**. A ticked box in a future run of this document must mean "evidence was produced and
> attached", never "we believe it works".

---

## 1. Purpose and how to use this document

**Purpose.** This is the release-governance reference for the **AmmPal Service** platform (label `AMMPAL-SERVICE-PROJECT-MASTER`, domain `https://ammpalservice.com/`). It defines who may approve, execute and verify a release (`§2`); what kinds of release exist (`§3`); the readiness, staging, migration, deployment, verification, rollback, feature-flag, city-activation and first-day checklists (`§4`–`§15`); and the artefacts every release must leave behind (`§13`, `§16`, `§18`). It is the single reference for "may we ship this?", written to be mechanical enough that a tired engineer at 02:00 during a P0 does not have to remember ten documents.

| Rule | Detail |
|---|---|
| **Copy, don't admire** | Copy the relevant checklist into the release ticket / PR description before starting. A checklist that lives only in a document is not being used. |
| **One checklist per release** | The release record names exactly which checklists were attached, and when. |
| **Evidence over assertion** | Every checked box needs a link to evidence: CI run URL, test report, query output, dashboard screenshot, signed record. "It passed" is not evidence. |
| **No checklist is a substitute for judgement** | A checklist proves a step was *performed*. It does not prove the step was *performed well*, that the change is correct, or that the release is safe. The person executing the release remains accountable for the outcome. A green checklist plus a bad design is still a bad release. |
| **Designed control, no execution history** | Every item here is a *designed* control. Until a real release produces evidence, this document records intent, not practice. Never cite it as proof that any process has run. |
| **Stop the release** | Any unchecked **Blocking** item stops the release. No "just this once" workaround. Exceptions need a written deviation signed by the Engineering Lead *and* the QA Lead, recorded in `§17.2`. |
| **Partial completion is a failure mode** | A checklist that is 90% complete is a failed checklist, not a nearly-passed one. |

**Status taxonomy.** `[CONFIRMED]` agreed, binding on implementers · `[PROPOSED]` suggested, open to change before build
· `[OPEN]` not decided, a decision is required · `[DEPENDENT]` cannot be finalised until another decision or artefact
lands. The status "implemented" is **never** used as a tag — no item here qualifies.

**Scope.** In scope: Public Website (Next.js + React + TS, static bundle); Customer App (Flutter, Android + iOS);
Partner App (Flutter); Control Center (React + Vite + TS); backend (NestJS + TS modular monolith; systemd units
`ammpal-api`, `ammpal-worker`, `ammpal-realtime`); PostgreSQL 16 + PostGIS, Redis 7 + BullMQ, S3-compatible storage;
infrastructure, DNS, TLS and vendors. The Partner web dashboard is **conditional** — out of scope until that scope is
confirmed `[OPEN]`. Out of scope: business-process design (`01`, `04`, `07`), test design (`15`), CI/CD implementation
detail (`16`). This document *consumes* `15` and `16`; it does not restate them.

---

## 2. Roles and release authority

| Role | Responsibilities during a release | Signs off on | May approve production? |
|---|---|---|---|
| **Engineering Lead** | Owns the release plan, change set, risk assessment, go/no-go call. | Technical readiness, architecture impact, rollback plan | **Yes** — Hotfix, Patch, Minor |
| **QA Lead** | Owns evidence that the `15` §7 quality gates were met on the exact artefact. | Test completeness, golden paths, defect triage | **Yes** — mandatory for every production release; unconditional veto |
| **Release Manager / Deployer** | Executes the pipeline, migration step, canary steps, observation windows; records the timeline. | Execution log, observation windows | **No** — may not approve a release they execute alone |
| **Database / Backend Owner** | Owns migrations, backfill batches, lock-risk assessment, replication-lag watch. | Migration plan, compensating actions | **No** — must be present for any release with a migration |
| **Mobile Lead** | Owns Flutter builds, store metadata, build numbers, staged rollout. | App artefact readiness | **No** |
| **Infrastructure / SRE Owner** | Owns the host, systemd units, reverse proxy, TLS, backups, monitoring. | Host readiness, capacity, observability | **Yes** — infrastructure-affecting changes |
| **Security Owner** | Owns SAST/DAST/dependency findings and the vulnerability gate. | Security gate, penetration-test status | **Veto** — 0 critical/high, non-negotiable |
| **Product Owner** | Owns scope, customer-visible change, feature-flag targeting. | Scope completeness, flag targeting, customer impact | **Yes** |
| **Finance Owner** | Owns pricing, commission (15% on eligible labour only), invoice/tax configuration, settlement. | Money-path correctness, statement/refund impact | **Veto** on money-path releases |
| **Operations Lead** | Owns technician roster, city readiness, support staffing, customer communications. | Operational readiness, roster, support coverage | **Yes** — required for city activation (`§14`, `§15`) |
| **Founder / Sponsor** | Approves major releases, new-city activation, risk acceptance above threshold. | Major releases, city activation, written deviations | **Yes** |

**Separation of duties — mandatory rules.**

| # | Rule | Detail |
|---|---|---|
| **SOD-1** | **The person who built it does not release it alone.** | The author of the change may not be the only approver, nor the only executor of the production deploy. |
| **SOD-2** | **Deployer ≠ approver.** | The Release Manager running the pipeline cannot also be the approver. Two distinct humans, both named in `§16`. |
| **SOD-3** | **Two signatures minimum for every production release.** | Engineering Lead + QA Lead, plus role-specific signatures in `§16`. |
| **SOD-4** | **No self-review of one's own PR.** | At least one approving reviewer who is not the author (`16` §3.1). |
| **SOD-5** | **Migration author ≠ migration executor.** | The person who wrote the migration does not run it against production alone. |
| **SOD-6** | **Money-path changes require Finance.** | Any change to pricing, commission, billing, settlement, refund or tax configuration requires the Finance Owner signature before deploy. |
| **SOD-7** | **Written deviation required.** | Waiving any Blocking item needs a dated written deviation signed by the Engineering Lead and the QA Lead, recorded in `§17.2`. Verbal waivers are invalid. |
| **SOD-8** | **Solo deploys prohibited.** | A production deploy is never performed by one person alone; a second engineer must be on call and reachable throughout. |

**Approval matrix by release type** — ✔ required, — not required, "if …" means only when that area is touched.

| Release type | Eng Lead | QA Lead | Infra/SRE | Finance | Security | Product | Ops | Founder |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Hotfix | ✔ | ✔ | ✔ (if infra) | — | ✔ | — | — | — |
| Patch | ✔ | ✔ | ✔ | ✔ (if money) | ✔ | ✔ | — | — |
| Minor | ✔ | ✔ | ✔ | ✔ (if money) | ✔ | ✔ | ✔ (if customer-visible) | — |
| Major | ✔ | ✔ | ✔ | ✔ (if money) | ✔ | ✔ | ✔ | ✔ |
| Feature-flagged | ✔ | ✔ | ✔ | ✔ (if money) | ✔ | ✔ | ✔ | — |
| Database-only | ✔ | ✔ | ✔ | ✔ (if money) | — | — | — | — |
| New city activation | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

---

## 3. Release types

| Type | Contents | Required approvals | Deploy window | Rollback expectation | Migration rehearsal required? |
|---|---|---|---|---|---|
| **Hotfix** | Single P0/P1 defect fix; smallest possible diff; no refactors; no dependency upgrades unless the upgrade *is* the fix; no schema change unless unavoidable. | Eng Lead + QA Lead + Infra; Security if security-related | Any time, incl. Friday and holidays | **Immediate** — under 15 minutes, single command, no data change | Only if a migration is unavoidable; otherwise a **compensating** action must be designed *before* the hotfix ships |
| **Patch** | Bug fixes only; no new behaviour, no API contract change, no schema change. | Eng Lead + QA Lead + Infra; Product if customer-visible | Tue–Thu 10:00–16:00 IST | Same-window rollback, under 30 minutes | No — but the rollback path must still be rehearsed |
| **Minor** | New features, additive API fields, new non-breaking endpoints, mobile feature releases. | Full matrix per `§2` for affected areas | Tue–Thu 10:00–16:00 IST | Same-window rollback; any feature may be switched off by flag instead | Mandatory if migrations are included |
| **Major** | Breaking API contract change, schema redesign, irreversible data transformation, pricing/tax model change, removal of a flag or deprecated field. | Full matrix + Founder | Tue–Thu 10:00–16:00 IST; extra change-freeze on surrounding days | **Not always possible** — breaking changes may be forward-only; a compensating migration must be pre-designed and pre-tested | **Mandatory**, including rehearsal of the compensating path |
| **Feature-flagged** | Code shipped dark (flag off in production), enabled selectively afterwards. | Eng Lead + QA Lead + Product Owner + named flag owner | Code deploy: Tue–Thu window. Flag enablement: any time, subject to `§10` | **Roll forward** by switching the flag off — no code rollback needed; this is the point of the pattern | No (any included migration still needs rehearsal) |
| **Database-only** | Migrations and/or backfills only, no application code change. Runs as a **pipeline step before** the app deploy, never in app startup. | Eng Lead + QA Lead + Database Owner + Finance (if money-path) + Infra | Tue–Thu 10:00–16:00 IST | Code rollback is irrelevant — the migration is forward-only unless a compensating migration exists (`§6.5`, `§9.4`) | **Mandatory** — rehearsal against a production-like snapshot is the only meaningful evidence |

---

## 4. Pre-release readiness checklist

> **Owner:** Release Manager · **Approvers:** Engineering Lead + QA Lead · every item Blocking unless stated.

**4.1 Branch, PR and ticket hygiene**

- [ ] Branch is `feature/<slug>` / `fix/<slug>` / `hotfix/<slug>` / `chore/<slug>` — never directly on `main`; branch is current with `main`.
- [ ] PR is open against `main`, uses a Conventional Commit title, and states **what**, **why**, **how it was tested** and **how it is rolled back**; ≥ 1 approving review from a non-author (SOD-4), no unresolved review threads, squash-merge only with a conventional-commit message.
- [ ] PR links at least one ticket with acceptance criteria; the ticket records the release type (`§3`), the target version (`§12`) and the risk assessment — blast radius, affected surfaces, affected booking statuses, affected money paths.
- [ ] Diff reviewed for debug statements, `console.log`, commented-out code, hard-coded values, TODOs without a ticket, unused imports, and any `TODO`/`FIXME` in a money path; no secrets, keys, tokens, certificates or real phone numbers in the diff (secret scan plus manual check).
- [ ] If booking status transitions change, the transition table in `04` is updated in the same PR; if pricing, commission, settlement, refund or tax changes, the Finance Owner is a required PR reviewer; customer- or partner-visible changes have a communication template selected (`§13`).

**4.2 CI green — every stage**

| Stage | Requirement | Blocking |
|---|---|:--:|
| Install (pnpm frozen lockfile) | Succeeds; lockfile unchanged; no `--no-frozen-lockfile` | ✔ |
| Lint + format + typecheck | Zero lint errors; Prettier check passes; `tsc --noEmit` clean for api, web, control-center; `flutter analyze` clean | ✔ |
| Architecture tests | Module-boundary tests pass (modular-monolith boundary enforced) | ✔ |
| Unit + property tests | 100% pass; coverage ≥ 80% overall, **≥ 95% on `pricing`, `commission`, `billing`** | ✔ |
| Golden-master tests | 0 unexpected diffs; any changed fixture is a reviewed, deliberate change | ✔ |
| Integration tests | 100% pass against Postgres+PostGIS and Redis | ✔ |
| Mode-guard tests (`15` `TE-06`) | The guard is asserted at **both** L2 and L3; the boot assertion refuses staff mutations on production infrastructure resolving `TESTING`; soft delete (`03` §3.2) and the code-defined purge (`09` §6) are proven **still working**; `TEST`-origin rows are proven invisible to reports, accrual and settlement (`38`, `ADR-026` `[PROPOSED]`) | ✔ once `ADR-026` is accepted — `[PROPOSED]` while it is not |
| OpenAPI drift check | 0 drift; 0 breaking changes without a major version bump (`§12.4`) | ✔ |
| Build web + control-center + Docker push | Builds clean, bundle size delta reviewed; image built, tagged with release version + commit SHA, pushed to the registry | ✔ |
| Flutter analyze + test | Analyze clean; widget/unit tests pass | ✔ |
| SAST + dependency scan | 0 critical/high from both | ✔ |
| Secret scan | 0 findings | ✔ |
| Deploy dev + smoke | Smoke suite passes on dev | ✔ |
| Deploy staging + Playwright E2E + perf smoke | E2E green; perf smoke within `13` targets | ✔ |

**4.3 Quality gates (from `15` §7) — all green**

- [ ] Unit + property coverage thresholds met (≥ 80% general, ≥ 95% pricing/commission/billing) and 100% of tests passing; integration suite 100% passing.
- [ ] Contract tests show 0 drift and 0 breaking changes; all four golden paths green on staging (GP-1 … GP-4 — `§5.1`).
- [ ] Security shows 0 critical/high; performance targets from `13` met on a production-like dataset; accessibility shows 0 serious/critical (WCAG 2.1 AA).
- [ ] Migration rehearsal performed and reviewed (`§5.4`) — or explicitly confirmed "no migration in this release"; rollback rehearsal performed and reviewed (`§9.6`) — or explicitly confirmed "forward-only release, compensating action documented".
- [ ] Documentation updated: `Docs/` changed in the same PR where behaviour changed; API reference regenerated.
- [ ] QA Lead sign-off recorded in the release ticket; all feature flags for this release are **default-off in production** (`§10`).

**4.4 Dependency, security and licence review**

- [ ] New dependency reviewed: licence compatible, maintained, bundle/runtime cost acceptable, supply-chain provenance checked; every new dependency has a test that fails if it misbehaves.
- [ ] Vulnerability scan re-run against the **release artefact**, not only the source tree; container image scanned (Trivy); base image pinned to a digest, not a floating tag.
- [ ] No critical/high CVE is "accepted under a ticket" without a written Security Owner acceptance and an expiry date.

**4.5 Feature flags and configuration**

- [ ] Every new behaviour that is not fully ready sits behind a flag, **default off in production**, with a named owner, an expiry date and a nominated removal release (`§10`); targeting rules tested in staging against at least one non-matching and one matching cohort; no flag is used to hide an unfinished *migration* — flags gate behaviour, not schema.
- [ ] Release environment variables staged in `/opt/ammpal/shared/env/*.env` (mode `0600`); secret values are never pasted into a ticket, PR or document — **placeholders only here**.

**4.6 Database readiness**

- [ ] Migrations written and reviewed by the Database Owner; **backward-compatible with the currently deployed version** (old code runs against the new schema).
- [ ] Migrations run as a **pipeline step before the app deploy**, never from application startup; no unreleased migration is left in the repository — every migration file is either part of this release or already applied.
- [ ] Backfill plan exists with batch size ≤ 1,000 rows, estimated row count and estimated duration (`§6.4`); lock-risk assessment complete (`§6.3`); compensating action designed for any non-reversible step (`§6.5`).

**4.7 Operational readiness**

- [ ] On-call roster published for the deploy window and the following 24 hours; support team informed of the change and briefed on likely customer questions (`§13`).
- [ ] Runbooks exist for every new alert introduced by the release; dashboards exist for every new metric.
- [ ] Capacity headroom confirmed on the VPS (4 vCPU, 16 GB RAM, 200 GB NVMe, 16 TB bandwidth — **planning target, not a guarantee**) for the expected load delta.
- [ ] Production database backup verified **and a restore rehearsed** within the last 30 days.

**4.8 Visual, asset, structure and component gate** `[PROPOSED]` — added with `30`–`33`, extended at v1.2 for `34` and `OD-DOC-34`, and at v1.3 for `35`–`37`; **no release has passed through any of it, because no release, and no scaffold, exists.**

- [ ] `python3 maintenance/scripts/validate_assets.py` exits `0` — run **from the workspace root**, which is where its relative `design-assets/` and `Docs/` paths resolve (`README` §12.5) — filename grammar, alt-text treatment, one inventory ID per file under `design-assets/`, and the manifest agreeing with each registered file on **bytes, hash, format and measured pixels** (`32` §4).
- [ ] No screen references an asset whose `approval_status` is not `APPROVED`. As written this means **no shipped screen may reference any asset**: the 93 inventory rows are 83 `PLANNED`, 6 `BLOCKED`, 4 `REGISTERED`, **0 `APPROVED`** (`32` §6). This item cannot be ticked by approving a file yourself — approval is the owner's act.
- [ ] The four `visualize-image-of-project/` infographics are absent from every bundle; they are registered as `NOT_FOR_PRODUCTION` (`31` §8).
- [ ] Colour, type, spacing, radius, elevation, z-index and motion come from the tokens in `30` §3–§7, not from literals in a component; every new text-on-background pair is measured at WCAG 2.1 AA, per `12` §6.3 `A11Y-1` and `30` §3.
- [ ] Every new image row in the inventory carries an `a11y_treatment`, and a `ALT_REQUIRED` row carries non-empty alt text — the validator refuses the mismatch in both directions (`32` §5).
- [ ] **No animation, skeleton or optimistic UI is treated as evidence that the server accepted anything**; the state comes from the API response or the socket event (`30` §7, `13` §2.2).
- [ ] Any newly added imagery or font is re-checked against the budgets in `13` §2.2 (LCP, CLS, APK size) — those ceilings are what `32` §4's weight limits are derived from, and neither has been measured on a real device.
- [ ] Store and marketing screenshots, if any are part of this release, were captured from an **actual approved build** — never generated, never mocked (`31` §8).
- [ ] **Every image origin in the build is named in `13` §5.2's `img-src`.** As written that list is `'self' data: blob:` plus the Google Maps and `googleusercontent` hosts, so an `<img>` pointing at any other CDN is a production-time render failure that passes in development; `validate_assets.py` checks no serving origin (`32` §4), so nothing in this workspace catches it automatically. `OD-DOC-34` `[BLOCKER]` is the open question about it.
- [ ] A screen whose media slots are placeholder containers (`30` §5.3) is **not** presented in this release's notes, or to anyone, as an approved design — an empty container satisfies layout, not the gate, and `OD-DOC-36` has not defined the gate's evidence yet. If such a screen ships, the release notes must say the artwork is outstanding.
- [ ] Any asset whose inventory status is `GENERATED` is blocked from the bundle by name: `GENERATED` is not `APPROVED` (`32` §6), and a `34` §4 run does not confer approval on the files it produces.
- [ ] **Every file this release adds sits in a directory `35` names** (`PS-01`: `14` §2 is the canonical tree, `35` holds the interiors). A new top-level directory, a new module, or a file that fails `35` §9's placement test needs a `21` row before it needs a review.
- [ ] **No dependency was added that `36` §4/§5 does not admit** (`LB-01`…`LB-08`). A library outside those tables is not a style preference — it is an unregistered decision, and the CSP items below are how it fails in production rather than in review.
- [ ] **Nothing this release ships loads a remote font, a CDN script, an icon font or an un-nonce'd injected stylesheet.** Each of those passes `13` §5.2's directives check and fails the gate `36` §3 documents.
- [ ] **Every new component passes `37` §11.1's fourteen-item checklist**, and the four items no reviewer can grade by eye — contrast measured, not judged; budget within `12` §9; reduced-motion honoured; state from the server, never from the animation — carry their evidence, not a tick.
- [ ] **No hex literal, no raw duration and no undeclared `z-index` appears outside the token package** (`PS-11`, `CA-09`…`CA-15`). The values are `30` §3–§7; a component that restates one has created a second source of truth, which is the failure `DEC-01` exists to prevent.
- [ ] **No component name was added anywhere except `12` §6.2** (`CA-00`), and no motion outside `37` §6's nine recipes shipped (`CA-16`). `37` may gain a rule in a release; it may not gain a name or a nameless animation.
- [ ] **No navigation item shipped with an empty `permissionToken`** (`PS-14`). Until `OD-10-06`/ `OD-DOC-29` close, the Control Center ships the item hidden, not unguarded — a route with no token is not a route with no permission.
- [ ] **`OD-DOC-38` is closed before anything is scaffolded, and before `git init`** (`19` `R-48`). A release that introduces a repository layout is a release that adopts one of the two trees `35` documents, and neither adoption is authorised by this checklist.

---

## 5. Staging verification checklist

> **Owner:** QA Lead · **Approvers:** QA Lead + Engineering Lead · Environment: `staging` — synthetic data at production-like volume, vendor sandboxes, never real customer data.

**5.1 Golden paths — all four green**

| Path | Flow | E2E suite | Assertions specific to a release | Result |
|---|---|---|---|---|
| **GP-1** | Book → Serve → Pay → Review | `e2e/gp-1-book-serve-pay-review` | Price snapshot matches golden-master; commission = 15% on eligible labour only; money stored as integer paise; review recorded; invoice issued | ☐ PASS |
| **GP-2** | Book → Accept → Settle | `e2e/gp-2-book-accept-settle` | Status transitions follow `REQUESTED(1) → ACCEPTED(2) → EN_ROUTE(3) → STARTED(4) → COMPLETED(5) → CLOSED(6)`; Mon–Sun accrual appears on the following Monday's statement; payment due within 7 calendar days; 5-business-day dispute window open | ☐ PASS |
| **GP-3** | Call → Book → Track | `e2e/gp-3-call-book-track` | Call logged against the toll-free number (`1800-XXX-XXXX` — **placeholder, not a real number**); IVR recording retained; call converts to a booking; technician GPS tracking visible to customer and Control Center | ☐ PASS |
| **GP-4** | Complaint → Rework → Refund | `e2e/gp-4-complaint-rework-refund` | Complaint raised; rework assigned; refund initiated via the payment provider; status reaches `REFUND_PENDING(13)` then `REFUNDED(14)`; `DISPUTED(15)` where applicable; refund equals captured amount less eligible commission | ☐ PASS |

- [ ] GP-1, GP-2, GP-3 and GP-4 each green on staging against the release artefact; each run twice consecutively — a flaky pass is a fail; golden-master fixtures unchanged, or each change reviewed and approved by the Finance Owner (money-path fixtures).

**5.2 Performance suite**

- [ ] k6 suite executed on staging with a production-like dataset (synthetic, production-shaped); all targets in `13` §2 met, with any unmet target documented as a deviation carrying an expiry.
- [ ] p95 latency measured per critical route (booking, pricing quote, availability, tracking, settlement) and compared to the recorded pre-deploy baseline.
- [ ] Load applied at expected peak plus headroom; no memory leak or unbounded queue growth; queue depth returns to baseline afterwards; worker and realtime throughput measured under load; result attached to the release ticket as evidence.

**5.3 Accessibility**

- [ ] Automated axe-core scan of the Public Website and Control Center: **0 serious, 0 critical**; manual TalkBack/VoiceOver pass on the Customer App and Partner App for changed screens.
- [ ] Keyboard-only pass on changed web screens — focus order and visible focus verified; pre-existing issues triaged and recorded separately so they do not silently become "accepted".

**5.4 Migration rehearsal against a production-like snapshot**

- [ ] A production-like snapshot is loaded into a **separate rehearsal database**, never the staging database used for E2E; all migrations for this release execute in order against it with total runtime recorded; pre-deploy and post-deploy query results for `§6.6` captured.
- [ ] Lock behaviour observed (long transactions, `AccessExclusiveLock` waits, replication lag) and recorded; backfill executed against the snapshot — batch size, batch count and per-batch duration recorded; the **rollback / compensating path** is executed against the snapshot and its outcome recorded (`§9.4`).
- [ ] Snapshot destroyed after rehearsal; no production-identical data persists.

**5.5 Rollback rehearsal**

- [ ] Symlink-swap rollback executed in the rehearsal environment: `/opt/ammpal/apps/<app>/current` repointed to the previous version, services restarted, health verified; `ammpal-api`, `ammpal-worker` and `ammpal-realtime` all restart cleanly on the previous version.
- [ ] Observed rollback time recorded and compared to the release type's expectation (`§3`); confirmed that the rollback path does **not** require a schema change to succeed (`§9.4`); timings attached to the release ticket.

**5.6 Vendor sandbox sanity**

| Vendor / integration | Sandbox check | Result |
|---|---|:--:|
| Razorpay | Test payment captured, refund initiated, webhook signature validated, idempotency honoured | ☐ |
| WhatsApp Business Platform (official) | Template message accepted, session window respected, delivery receipt received | ☐ |
| Firebase Cloud Messaging | Push delivered to a test device, deep link opens the correct booking | ☐ |
| Google Maps Platform | Address geocoding, service-area polygons, distance matrix within quota | ☐ |
| Indian cloud-telephony provider | Toll-free IVR reachable, recording retrievable, call disposition webhooks received — **placeholder** number `1800-XXX-XXXX` in test configuration only | ☐ |
| Indian SMS provider + transactional email | OTP delivered to a test number, DLT template registered, delivery receipts received; email template rendered, deliverable, links unspoofed | ☐ |
| S3-compatible object storage | Upload/read/delete of an object, presigned URL expiry enforced | ☐ |
| Redis 7 + BullMQ | Job enqueue → consume → retry → dead-letter path exercised | ☐ |

- [ ] No vendor sandbox points at production credentials; vendor quotas, rate limits and cost ceilings reviewed for expected production volume.

**5.7 Smoke checks per surface**

| Surface | Smoke check | Entry point | Result |
|---|---|---|:--:|
| Public Website + versioned API | Home, category list, service detail, booking form renders and submits, static assets 200; API reachable behind the proxy | `https://www.ammpalservice.com/` · `https://api.ammpalservice.com/v1/*` | ☐ |
| Customer App | Install, cold start, login/OTP, category browse, booking creation, live tracking | Android + iOS test build | ☐ |
| Partner App | Install, cold start, login, job feed, accept, start, complete | Android test build | ☐ |
| Control Center | Login, dashboard, booking list, technician roster, settlement report | `https://admin.ammpalservice.com/` | ☐ |
| Realtime | WebSocket connects, subscribes to a booking channel, receives a status event | `/ws` | ☐ |
| Backend health | Liveness, readiness and deep readiness all green | `/health/live`, `/health/ready`, `/health/ready?deep=1` | ☐ |
| Partner web dashboard | **Conditional** — only if that surface is in scope | `—` | ☐ N/A |

- [ ] Reverse proxy routes confirmed: `api.ammpalservice.com/v1/*`, `/ws`, `www.ammpalservice.com`, `admin.ammpalservice.com`; TLS certificate valid with complete chain and renewal automation confirmed per hostname.
- [ ] Health endpoints respond within their defined timeouts and expose no internals in the response body.

---

## 6. Database migration checklist

> **Owner:** Database Owner · **Approvers:** Engineering Lead + QA Lead (+ Finance Owner if money-path).
> **Doctrine:** **Expand → Migrate → Contract.** Migrations are code artefacts, run by the pipeline **before** the app
> deploy, never in app startup, and backward-compatible with the currently deployed version.

**6.1 Expand → Migrate → Contract**

| Phase | What happens | Release rule |
|---|---|---|
| **Expand** | Additive schema only: new tables, new nullable columns, new indexes (built `CONCURRENTLY` in production), widened column types. Old code keeps working. | Shipped and deployed **before** any code that reads or writes the new structure; never in the same release as the contract step. |
| **Migrate** | Data movement: backfills in batches ≤ 1,000 rows; dual-write or read-both where needed; new code path enabled behind a flag. | Backfill runs as a controlled batch job with progress reporting and a kill switch. |
| **Contract** | Removal: drop old columns/tables, enforce `NOT NULL`, remove the compatibility path. | Shipped **at least one full release** after the code stops reading the old structure; enforced by a compatibility lint rule. |

- [ ] Every migration is classified Expand, Migrate or Contract, stated in the migration file header; contract steps sit in a **separate release** from the matching expand step and no release contains both against the same structure.

> **`[OPEN]` — the mode guard and the contract step collide, and nobody has decided who wins (`OD-DOC-43`, scored as `19` `R-50`).**
> A `DROP COLUMN`, `DROP TABLE` or `TRUNCATE` is data-destructive DDL, which is **class A** under `38` §6 and therefore
> refused in `PRODUCTION` if `PM-05` is read literally. This doctrine's own contract phase is made of exactly those
> statements, and it runs on production infrastructure by design. Three readings exist and none is approved: (a) the guard
> scopes to **operator-initiated** deletes from a dashboard or admin API and never to a **reviewed, pipeline-run migration**,
> in which case `38` must say so in `PM-05` and `15` `TE-06` must assert the migration path is not blocked; (b) the guard is
> absolute, in which case schema contraction becomes impossible in production and `09`'s expand–contract model needs a new
> owner-approved mechanism; or (c) contract steps require a mode-aware exception recorded in the migration header. **This
> suite does not pick one** (`DEC-03`); the pipeline cannot be written until `OD-DOC-43` closes, and a release ticket that
> contains a contract step inherits the blockage. Note that reading (a) is what `38` §6 currently implies by naming class A
> "operator-initiated", but no rule text enforces the distinction yet — an implication is not a decision.

**6.2 Pre-migration gate**

- [ ] Migration files ordered and named `<YYYYMMDDHHMMSS>_<slug>.sql` with a unique timestamp; order is deterministic (`§12.6`); migration is idempotent where safely possible — re-running is a no-op — and idempotent on pipeline retry.
- [ ] Migration executed against a production-like snapshot in rehearsal (`§5.4`) with runtime recorded; it does not run from application startup, from a health probe, or from an ad-hoc manual session.
- [ ] Migration is present in the pipeline as an explicit, named, retryable step, sequenced **before** the app deploy step; the app deploy is blocked until the migration step exits `0`.
- [ ] `lock_timeout` and `statement_timeout` are bounded, never unlimited; the step fails fast rather than queueing behind a long transaction; lock-time and replication-lag budgets agreed with the Database Owner and Infra Owner.
- [ ] Migration covered by the verification query set (`§6.6`); migration logs (row counts, timings, lock waits) captured in the release record.

**6.3 Lock-risk assessment**

| Risk | Assessment question | Required answer before deploy |
|---|---|---|
| Table lock on `ALTER TABLE` | Does any statement take `AccessExclusiveLock` on a hot table? | If yes → rewrite as expand + contract, or schedule in a low-traffic sub-window |
| Non-concurrent index | Is every production index created with `CREATE INDEX CONCURRENTLY`? | Yes, always — otherwise Blocking |
| Foreign key add | Does FK validation scan the full child table? | Add `NOT VALID`, then `VALIDATE CONSTRAINT` in a later step |
| Column type change | Does the change rewrite the table (`varchar` → `text`, `int` → `bigint`)? | Rewrite avoided — dual-column + backfill + swap |
| Default value / `NOT NULL` on a large table | Does the statement scan or rewrite the table on PG16? | Use a non-rewriting path: `ADD COLUMN` without a volatile default, `CHECK ... NOT VALID` → `VALIDATE` → `SET NOT NULL` |
| Trigger creation | Does the trigger fire during backfill and amplify write load? | Measured in rehearsal; mitigated by batching |
| Long transaction | Does a long-running transaction hold a conflicting lock? | Identified and cleared before the migration starts |

**6.4 Backfill plan and replication-lag watch**

| Item | Required value |
|---|---|
| Target rows (estimated) / batch size | `<ROW_COUNT>` — **≤ 1,000 rows per batch, hard rule** |
| Batch delay / estimated total duration | `<MS>` between batches, to keep replication lag low — `<DURATION>` total |
| Resume support / kill switch | Idempotent and resumable from a persisted cursor — pausable without corrupting state |
| Concurrency / monitoring | Single batch worker unless the plan states otherwise and is reviewed — progress %, rows/sec, batch duration and errors all observable |

- [ ] Backfill uses `LIMIT`-bounded batches and commits per batch; it never runs inside one long transaction; it runs as a job, not as a foreground migration step, and its progress is on a dashboard before the production run.
- [ ] Replication lag is on a dashboard with an alerting threshold set **before** the migration starts; a named engineer watches lag live for the entire migration and backfill.
- [ ] **Pause** threshold defined (e.g. pause the backfill above `<LAG_THRESHOLD>`) and **abort** threshold defined, with the abort procedure written down before the run; expected lag recorded in the release ticket.

**6.5 Rollback and compensating plan**

- [ ] Each migration step is explicitly classified **reversible**, **irreversible**, or **irreversible with compensating migration**.
- [ ] Irreversible steps have a **compensating migration** written and rehearsed *before* deploy — not afterwards; it is idempotent and independently testable, and the release record links both the forward migration and the compensating migration.
- [ ] Where compensation requires a data fix rather than a schema revert, the Finance Owner signs it.

**6.6 Post-migration verification queries**

> Run immediately after the migration step and again after the app deploy; capture output in the release ticket.
> Table and column names are illustrative placeholders — replace with the real names.

- [ ] Row-count parity for touched tables, before vs after, per affected table; null-count on newly added columns matches expected backfill coverage.
- [ ] No orphan rows — every child row still resolves to a parent row; no duplicates introduced — `GROUP BY <key> HAVING COUNT(*) > 1` returns zero rows on migrated keys.
- [ ] Money consistency: sum of ledger amounts per booking equals sum of line items; commission equals 15% of eligible labour only, in integer paise.
- [ ] Booking statuses remain within the allowed set — `REQUESTED(1)`, `ACCEPTED(2)`, `EN_ROUTE(3)`, `STARTED(4)`, `COMPLETED(5)`, `CLOSED(6)`, `CANCELLED_BY_CUSTOMER(7)`, `CANCELLED_BY_TECHNICIAN(8)`, `REJECTED(9)`, `EXPIRED(10)`, `NO_SHOW(11)`, `RESCHEDULED(12)`, `REFUND_PENDING(13)`, `REFUNDED(14)`, `DISPUTED(15)`.
- [ ] No `INVALID` index left behind by `CREATE INDEX CONCURRENTLY`; no abnormal blocking after the migration; query plans for the top critical endpoints unchanged or improved — no unexpected sequential scan on a hot path.

**6.7 Migration sign-off**

| Item | Value |
|---|---|
| Migration files / class | `<FILES>` — EXPAND / MIGRATE / CONTRACT |
| Reversible? | `YES` / `NO — compensating migration: <ID>` |
| Rehearsal snapshot (date / size) / runtime | `<SNAPSHOT>` — `<DURATION>` |
| Backfill estimate | `<DURATION>` for `<ROW_COUNT>` rows |
| Max observed replication lag | `<LAG>` |
| Database Owner sign-off | `<NAME>` / `<DATE>` |

---

## 7. Production deployment checklist

> **Order matters.** Steps are strictly sequential; do not start a step until the previous one is complete and recorded.
> The canary observation window is **5 minutes** after each step and the health gate is evaluated at the end of it.
> **Health gate (all six must hold):** 5xx < 1%; p95 latency < 1.5× pre-deploy baseline; no route more than 2× its baseline
> error rate; queue depth not growing; worker error rate < 1%; `/health/ready` green.

**7.1 Pre-deploy**

- [ ] **T-60 min** — Release ticket opened with release version, commit SHA, artefact digest and the attached checklists; deploy window confirmed (Tue–Thu 10:00–16:00 IST, or a documented hotfix exception); on-call confirmed present — deployer plus a second engineer reachable (SOD-8).
- [ ] **T-50 min** — Pre-deploy baseline recorded and stored: current 5xx rate, p95 latency per critical route, error rate per route, queue depth, worker error rate.
- [ ] **T-45 min** — Current production version confirmed; rollback target version identified and known-good; production backup verified current with a restore point confirmed; migration step plan reviewed a final time with the compensating migration staged and ready.
- [ ] **T-30 min** — Customer-impact assessment reviewed; support briefed; maintenance/incident banner text prepared (`§13`); vendor-impact assessment reviewed — Razorpay, WhatsApp Business Platform, FCM, Google Maps, cloud telephony (toll-free `1800-XXX-XXXX` — **placeholder**), SMS, transactional email.
- [ ] **T-25 min** — Every feature flag for this release confirmed **off** in production; dashboards open — API error rate, latency, queue depth, worker errors, database health, realtime connections.
- [ ] **T-20 min** — **Platform mode asserted `PRODUCTION` from `platform.platform_mode` (`38` §10) before anything is deployed to this infrastructure, and the value is read from the database, not from a variable, a flag or a screen.** Record the value and the read. A deploy onto infrastructure that resolves `TESTING` is blocked here, not later: the guard the mode is supposed to arm is off while the mode says `TESTING`, so live data would sit behind an unarmed guard (`19` `R-49`). If the assertion fails, the release does not proceed — the mode is changed by the `38` §5 ceremony with its own audit trail, and **never** by demoting or promoting to make a deploy go through (`25` §25.0). `[PROPOSED]` — this step exists only if `ADR-026` is accepted; it is unchecked until then.

**7.2 Migration step (before the app deploy)**

- [ ] Migration step started and watched live — never left unattended; logs streaming, no long lock waits, replication lag below the pause threshold for the whole run.
- [ ] Migration step exited `0`; post-migration verification queries executed (`§6.6`) with outputs captured.

**7.3 App deploy — canary 10%**

- [ ] Artefact pulled by **immutable tag/digest**, never `latest`; release layout populated at `/opt/ammpal/apps/<app>/<version>/` for `api`, `worker` and `realtime`; symlink `/opt/ammpal/apps/<app>/current` repointed to the new version.
- [ ] `ammpal-api` restarted → `/health/live` green; `ammpal-worker` restarted → heartbeat observed; `ammpal-realtime` restarted → `/ws` accepts a connection; `/health/ready` green and `/health/ready?deep=1` green — deep check covers database, Redis and queue connectivity.
- [ ] **Canary 10% traffic enabled** in the reverse proxy; health gate at the end of the 5-minute window: 5xx < 1%; p95 < 1.5× baseline; no route > 2× baseline error rate; queue depth not growing; worker error rate < 1%; `/health/ready` green.
- [ ] **Health gate evaluated: PASS** — recorded with the metric values, not just the word "PASS".

**7.4 Canary 50%**

- [ ] 5 minutes of soak at 10% with no alert firing — a clean gate with an alert open is not a clean gate.
- [ ] Traffic increased to 50%; health gate re-evaluated across a **new 5-minute window**; no new P0/P1 defect reported by support or the Control Center; queue depth and worker error rate still within bounds.
- [ ] **Health gate evaluated: PASS** — recorded with metric values.

**7.5 Full rollout 100%**

- [ ] 50% canary soaked for the agreed minimum duration with no alert firing; traffic increased to 100%; health gate re-evaluated across a **new 5-minute window** — 5xx < 1%; p95 < 1.5× baseline; no route > 2× baseline error rate; queue depth not growing; worker error rate < 1%; `/health/ready` green.
- [ ] Reverse proxy configuration reloaded without dropping in-flight requests; all instances reporting the new version.
- [ ] Static surfaces rolled — Public Website bundle and Control Center bundle refreshed, CDN cache purged where required; mobile app distribution triggered or scheduled (`§15.3`; store rollout is a separate, slower step).
- [ ] **Health gate evaluated: PASS** — recorded with metric values.

**7.6 Customer-impact and vendor-impact sign-off**

- [ ] Customer impact reviewed: no booking flow broken, no unexpected pricing change, no notification regression, no outage window beyond the agreed communication threshold.
- [ ] Vendor impact reviewed: payment capture and refunds working, WhatsApp templates delivered, FCM push delivered, SMS OTP delivered, cloud-telephony IVR reachable (`1800-XXX-XXXX` — placeholder), email delivered, object storage readable/writable, queue processing.
- [ ] Any customer-visible change has its communication dispatched (`§13`) or scheduled for the correct time; support notified that the release is live with a short "what changed" note; **deployer and approver sign-off recorded** in `§16`.

**7.7 Immediate automatic rollback triggers**

> The pipeline performs an automatic rollback on any health-gate failure. These triggers require a human decision **without** waiting for the window to expire.

- [ ] Any 5xx rate ≥ 1% sustained for 2 minutes; any P0 defect opened (financial loss, data loss, security breach, total outage).
- [ ] `/health/ready` red or flapping; queue depth growing monotonically across two consecutive checks; replication lag above the abort threshold.
- [ ] Payment capture failing for any customer transaction; any state corruption observed (money, booking status, settlement).

---

## 8. Post-deployment verification checklist

> Run within 60 minutes of the 100% rollout, and again at the next business morning.

**8.1 Health, errors, latency and queues**

- [ ] `/health/live`, `/health/ready` and `/health/ready?deep=1` healthy on every instance; systemd units `ammpal-api`, `ammpal-worker`, `ammpal-realtime` all `active` with no restarts and no `OOM` kills; reverse proxy returns 200 for `www.ammpalservice.com`, `admin.ammpalservice.com`, `api.ammpalservice.com/v1/*` and `/ws`; TLS valid on every hostname with no expiry within 30 days.
- [ ] 5xx rate < 1% across the post-deploy observation period; p95 latency < 1.5× pre-deploy baseline on every critical route; no route above 2× its baseline error rate.
- [ ] 4xx rate not materially above baseline — a spike suggests a broken client contract; request volume matches expectation (a drop may mean clients fail before reaching the server).
- [ ] BullMQ queue depth at or below baseline; worker error rate < 1%; no jobs stuck in a retry loop; dead-letter queue empty or explained; job processing latency within expected range.

**8.2 Functional spot checks (real, end-to-end)**

| # | Check | Expected result | Result |
|---|---|---|:--:|
| 1 | **Real test booking** — create one end-to-end through the Public Website with a test customer account | Booking created in `REQUESTED(1)`; confirmation received; correct price snapshot; correct commission (15% on eligible labour only) | ☐ |
| 2 | **Real test payment** — capture payment for that booking via Razorpay (test mode unless a controlled live-mode check is authorised) | Payment captured; amount equals the quoted total; webhook processed; invoice issued; money stored as integer paise | ☐ |
| 3 | **Settlement dry-run** — generate a statement for the test technician over the current Mon–Sun accrual week without executing payment | Statement totals match the accrual; commission on eligible labour only; amount equals sum of expected line items; **no money is actually moved** | ☐ |
| 4 | **Notification delivery** | WhatsApp template delivered; SMS OTP delivered; transactional email delivered; FCM push delivered on a test device | ☐ |
| 5 | **Tracking** | Technician location visible in the Control Center and the Customer App; `/ws` pushes a status change to a subscribed client | ☐ |
| 6 | **Control Center login** | Login succeeds with a real operator account; dashboard, booking list, technician roster and settlement report all load | ☐ |
| 7 | **Call handling** | A test call to the cloud-telephony provider's sandbox/toll-free path is logged with a recording reference (number `1800-XXX-XXXX` — **placeholder**) | ☐ |
| 8 | **Complaint → rework → refund** (GP-4 path) | Complaint raised, rework assigned, refund initiated, status reaches `REFUND_PENDING(13)` → `REFUNDED(14)` | ☐ |

- [ ] Every test artefact created in production is clearly marked as a test and is cleaned up or retained under an agreed retention rule; no real customer data was used, copied or exposed.

**8.3 Monitoring and alerting sanity**

- [ ] Every alert introduced by the release fired at least once in a controlled test, or is explicitly confirmed as untested and risk-accepted; no alert is permanently muted or silenced.
- [ ] Dashboard panels show live data, not a stale cached view; log aggregation receives logs from all three units at the expected volume; on-call rota updated for the next 24 hours with handover notes written.
- [ ] Release ticket updated with the final timeline, metrics and links to evidence.

---

## 9. Rollback and hotfix procedures

**9.1 Roll back or fix forward?**

| Situation | Action |
|---|---|
| Defect introduced by this release, no data written by the defect | **Roll back.** |
| Defect introduced by this release, written data is corruptible without risk | **Roll back**, then run the documented data repair. |
| Defect introduced by this release, written data is meaningful and must be kept | **Fix forward** with a hotfix, provided the fix ships faster than the data can be repaired. |
| Migration already applied and irreversible | **Fix forward.** The app may only be rolled back if it is backward-compatible with the new schema — otherwise it must stay forward. |
| Vendor-side outage, not our code | **Do not roll back.** Escalate to the vendor; consider a kill switch for the affected capability. |
| Performance degradation, not a correctness failure | **Fix forward** if a small patch fixes the cause; **roll back** if the degradation is systemic to the release. |
| Partial deployment (one instance bad) | **Roll back the instance**, then re-run the health gate from 10%. |

**9.2 The decision rule**

> **If the release is the cause and a rollback returns the system to a known-good state within the release type's
> rollback expectation, roll back. Fix forward only when rollback is impossible, unsafe, or slower than the fix —
> and never as a way to avoid the decision.**

| Rule | Detail |
|---|---|
| **DR-1** | Any P0 → roll back immediately, unless the rollback itself would cause data loss. |
| **DR-2** | P1 with no workaround → roll back. P1 with a workaround and a fix ready inside the window → fix forward, with the workaround communicated. |
| **DR-3** | If the rollback target version is not backward-compatible with the current schema, **the application cannot be rolled back** — this is exactly why the Expand/Migrate/Contract doctrine exists. |
| **DR-4** | The Engineering Lead decides, with the QA Lead consulted, and records the decision and the reasoning in the release ticket. The author of the change may be consulted but must not be the sole decision-maker (SOD-1). |

**9.3 Symlink-swap rollback**

> The rollback mechanism is a symlink swap, executed per app. Placeholders: `<APP>` ∈ {`api`, `worker`, `realtime`}, `<VERSION>` is the last known-good version.

- [ ] Previous known-good version confirmed present on disk at `/opt/ammpal/apps/<app>/<VERSION>/`; rollback authorised by the Engineering Lead (or by the automatic pipeline gate) and announced in the release channel.
- [ ] For each app, the `current` symlink is repointed to the previous version and the corresponding systemd unit restarted; health verified — `/health/live`, `/health/ready`, `/health/ready?deep=1`; reverse proxy upstream weights reset to the pre-deploy split.
- [ ] Background job workers drained before the worker restart so partially processed jobs are retried, not abandoned; realtime clients reconnect — long-lived `/ws` connections are expected to drop and must reconnect cleanly.
- [ ] Environment at `/opt/ammpal/shared/env/*.env` (mode `0600`) is **not** changed by a code rollback; an env change is only made if the rollback requires one, is version-controlled, and is recorded.
- [ ] Rollback completion time recorded and compared to the release type expectation (`§3`); incident record opened if unplanned.

**9.4 Data-migration compensation rule**

> **"Rollback does not un-migrate."** Rolling back the application does **not** reverse a schema migration or a
> backfill. If the migration was irreversible, or data was written under the new schema, the previous application
> version may not even run against the reverted schema.

- [ ] The release record states, per migration step: **reversible**, **irreversible**, or **irreversible with compensating migration**.
- [ ] If irreversible, a **compensating migration** (not a `git revert` of the schema) is executed — designed, rehearsed and tested *before* the release; where data was written under the new structure the compensating migration preserves or transforms that data rather than deleting it.
- [ ] Where money was affected, the Finance Owner signs the compensating action before execution; a compensating migration is itself a release — pipeline step, approvers, window, sign-off.
- [ ] Where no safe compensation exists, the release is **forward-only**, and this is stated in the go/no-go decision.

**9.5 Hotfix procedure**

| Step | Action |
|---|---|
| 1 | Classify severity: P0, P1, P2 or P3 (`§17.1`). Only P0/P1 justify a hotfix; freeze all other deploys until the hotfix ships or the incident is resolved. |
| 2 | Branch `hotfix/<slug>` from `main`; smallest possible diff; no refactors; no unrelated upgrades; full CI green including the affected golden path and the money-path tests if applicable. |
| 3 | Approval: Eng Lead + QA Lead (+ Infra if infrastructure-affecting; + Finance if money-path; + Security if security-related). |
| 4 | Deploy to staging and run the affected smoke + golden path — unless a P0 with active customer impact is approved for direct-to-production with a written rationale. |
| 5 | Deploy to production in the same canary sequence: 10% → 5-minute health gate → 50% → 5-minute health gate → 100%; verify per `§8`, at least the checks relevant to the defect. |
| 6 | Back-merge `hotfix/<slug>` into the next release branch; close the hotfix branch; post-incident review within 48 hours, and every process gap becomes a ticket in the release that closes it. |

**9.6 Post-rollback verification**

- [ ] `/health/live`, `/health/ready` and `/health/ready?deep=1` green on every instance; all three systemd units active with no restart loop; version marker reports the rolled-back version on every instance.
- [ ] 5xx rate and p95 latency returned to pre-deploy baseline; queue depth draining rather than stuck; no jobs lost — reconcile the dead-letter queue; worker error rate < 1%.
- [ ] Every booking created during the failed window checked individually for correctness; every payment captured during the failed window reconciled against the payment provider; any settlement accrual affected by the failed window corrected in the next statement, not silently absorbed.
- [ ] Customer and partner communication issued if the failure was customer-visible (`§13`); root-cause ticket opened with timeline, failing metric and corrective action.

---

## 10. Feature-flag release procedure

**10.1 Rules**

| # | Rule |
|---|---|
| **FF-1** | **Default off in production.** A flag ships with the production default **off**, always. Enabling is a separate, deliberate act. |
| **FF-2** | **Named owner.** Every flag has one accountable owner — a person, not a team. Unowned flags are removed. |
| **FF-3** | **Expiry date.** Every flag carries an expiry date at creation. A flag with no expiry date is not approved. |
| **FF-4** | **Removal within 2 releases.** The flag and its dead code path are removed within **2 releases** of full rollout, or of the release that made it unnecessary. |
| **FF-5** | **Targeting is explicit.** Targeting states percentage, cohort (role, branch, city, category, technician, customer) or allowlist. "Everyone" must be written down as such. |
| **FF-6** | **Gradual enablement.** 1% → 10% → 50% → 100% with a soak at each step, unless the Product Owner and Engineering Lead jointly record a reason to do otherwise. |
| **FF-7** | **Observable.** The flag has a metric or log line showing whether the flagged path is exercised and whether it succeeds. |
| **FF-8** | **No flag on a money path without Finance.** A flag changing pricing, commission, settlement or refund behaviour requires the Finance Owner as owner or co-owner. |
| **FF-9** | **Kill switch.** Turning a flag off is a one-action operation taking effect within 5 minutes, with no deploy required. |
| **FF-10** | **No permanent flags.** A flag that becomes permanent business logic is migrated into configuration and the flag is removed. |

**10.2 Flag registry template** — maintained in the repository, reviewed at each release, one row per flag.

| Flag key | Description | Owner | Created (release) | Targeting | Prod default | Expiry | Removal release | Metric |
|---|---|---|---|---|---|---|---|---|
| `<flag_key>` | `<one line>` | `<NAME>` | `<VERSION>` | `<1% / cohort / allowlist>` | **OFF** | `<YYYY-MM-DD>` | `<VERSION + 2>` | `<METRIC>` |

**10.3 Enablement procedure**

- [ ] Flag exists in production with the default **off** and the correct targeting configuration; owner, expiry and removal release recorded in the registry; enabling announced in the release channel with the cohort, the ramp plan and the abort criteria.
- [ ] Ramp 1% → soak → check → 10% → soak → check → 50% → soak → check → 100%; at each step error rate, latency, queue depth and the flag-specific metric are compared against baseline.
- [ ] Any anomaly → roll the flag back to the previous step, or off, and diagnose; on full rollout create the removal ticket with a due release, and remove the flag from code, configuration and registry within 2 releases.

---

## 11. Release calendar and freeze windows

**11.1 Standard windows**

| Day | Window | Policy |
|---|---|---|
| **Monday** | 10:00–16:00 IST | Available. Also the day weekly settlement statements are generated (Mon–Sun accrual) — avoid overlapping unless the release is settlement-neutral. |
| **Tuesday** | 10:00–16:00 IST | **Preferred release day.** |
| **Wednesday** | 10:00–16:00 IST | **Preferred release day.** |
| **Thursday** | 10:00–16:00 IST | Available, but not after 15:00 IST unless it is a Hotfix — leave buffer before the freeze. |
| **Friday** | — | **No deploys.** Friday-evening deploys are prohibited; Friday is the freeze day. |
| **Saturday / Sunday** | — | **No deploys.** |
| **Public / statutory holidays** | — | **No deploys** in the period preceding a holiday, unless it is a Hotfix. |
| **Any time** | — | **Hotfixes only** (P0/P1), with the approvals in `§9.5`. |

**11.2 Freeze rules**

- [ ] **FR-1 — No Friday-evening deploys.** No production deploy after 16:00 IST on any day, and none at all on Friday.
- [ ] **FR-2 — No pre-holiday deploys.** No production deploy in the 2 working days before a public/statutory holiday, unless it is a Hotfix.
- [ ] **FR-3 — Change freeze during a P0 incident.** All non-hotfix deploys are frozen from incident declaration until the incident is closed and a post-incident review is scheduled.
- [ ] **FR-4 — Financial-close freeze.** A freeze is declared around the monthly settlement run and any statutory filing period; dates are set by the Finance Owner and published in the release calendar.
- [ ] **FR-5 — One release at a time.** Only one production release may be in flight at any moment; no concurrent deploys.
- [ ] **FR-6 — Deploy cap.** At most **one** scheduled production release per day, so monitoring capacity is never shared between two changes.
- [ ] **FR-7 — Batch releases.** Several small changes are batched into one release — but a release containing a risky change ships alone, because a risky change cannot be rolled back cleanly alongside an unrelated one.
- [ ] **FR-8 — Frozen artefacts.** An artefact in the freeze window is not promoted to production by any means, including manual promotion.
- [ ] **FR-9 — Freeze announcement.** Freezes are announced in the release channel at least 3 working days in advance, except incident freezes.

**11.3 Release train notes.** The weekly train promotes changes to staging on Tuesday and to production on Wednesday
or Thursday within 10:00–16:00 IST. A change that misses the train waits one week; a P1 is escalated to a hotfix rather
than waiting. The train is cut on **Tuesday 09:00 IST** — after the cut only a P0/P1 joins the same release with
Engineering Lead approval, everything else rides the next train. Each train release has one release manager and one set
of sign-offs, so there is no per-change sign-off ritual inside a single deploy. A release containing a schema change is
placed **first** in the train so its observation period is not squeezed by a later deploy. The release calendar is
maintained by the Engineering Lead and published with the quarter's freeze dates.

---

## 12. Versioning scheme

**12.1 SemVer for API and releases.** **MAJOR** — a breaking change: a public API contract breaks, a database column's semantics change, a status value is removed or repurposed, a money model changes, a required integration changes. **MINOR** — a backward-compatible addition: a new endpoint, a new optional field, a new non-breaking enum value, a new feature behind a default-off flag. **PATCH** — a backward-compatible fix that does not change the contract. The API version is carried in the path — `https://api.ammpalservice.com/v1/*` — and the application release version matches the API major for that release. Pre-1.0 releases use `0.MINOR.PATCH`; the first stable public release is `1.0.0`. A release that changes the API contract bumps the version **in the same release** — never "we'll bump it later".

**12.2 Git tag format**

| Element | Rule | Example |
|---|---|---|
| Application release tag | `v<semver>` on `main` | `v1.4.2` |
| Pre-release / hotfix tag | `v<semver>-<preid>` · `v<semver>-hotfix.<n>` | `v1.5.0-rc.1` · `v1.4.3-hotfix.1` |
| API contract tag | `api-v<major>` on the OpenAPI document | `api-v1` |
| Database migration tag | `db-v<semver>` marking the highest applied migration set | `db-v1.4.2` |
| Web / mobile build tags | `web-v<semver>` · `app-v<semver>` | `web-v1.4.2` |

Tags are annotated, signed, and created only by the Release Manager from a `main` commit that has passed the full
pipeline. Tags are immutable — a mistake is corrected by a new tag, never by moving an existing one.

**12.3 Version manifest.** Every release carries a manifest written into the artefact and readable at runtime: `version`
(SemVer), `commitSha`, `buildNumber` (monotonic), `builtAt` (ISO-8601 UTC), `openApiVersion`, `migrationVersion` (highest
migration set expected to be applied), and `flavour` (`api` / `worker` / `realtime` / `web` / `control-center` /
`customer-app` / `partner-app`).

**12.4 OpenAPI major-version policy.** The OpenAPI document is the contract of record, committed to the repository and validated in CI. Any change that breaks a documented request, response, error code or field semantics is a **breaking change**: it requires a **MAJOR** bump and a **new path prefix** (`/v2/*`), with the old prefix still serving for a published deprecation period — default **2 releases**. Breaking changes are **never** shipped in the same release as the deprecation notice; the notice ships first. Within a major version, additive changes only; CI fails on any drift between the committed and generated documents and flags any breaking change for explicit approval. Client applications pin a contract version, and the Control Center displays the contract version it is using so a mismatch is visible. Deprecation is communicated to integrators before removal, with the removal release named in the notice.

**12.5 Flutter build numbers.** `version` (user-visible) is the SemVer of the release and matches the backend release the app is built against. `buildNumber` (Android `versionCode`) and iOS `CFBundleVersion` are monotonically increasing integers, incremented for **every** upload including rebuilds of the same version, and the last uploaded build number per store is recorded and never reused. Store rollouts are staged (5% → 20% → 50% → 100%) with crash-free-session and ANR thresholds checked between steps. The Control Center can require a minimum app version; an out-of-date app shows a forced-update screen.

**12.6 Database migration ordering.** Migrations are named `<YYYYMMDDHHMMSS>_<short_slug>.sql`; the timestamp is the ordering key and is unique. Migrations are applied in **timestamp order**, always, on every environment. Each migration declares its class (`EXPAND` / `MIGRATE` / `CONTRACT`) in a header comment and its dependency on prior migrations. A migration applied in any shared environment is **immutable** — a correction is a new migration, never an edit. The migration set is versioned with the release (`db-v<semver>`) and `migrationVersion` is declared in the release manifest. Migrations run **before** the app deploy in the pipeline, and the app deploy asserts the applied migration set is ≥ the manifest's `migrationVersion`. Expand and Contract steps for the same structure are separated by at least one full release.

---

## 13. Release notes and communication templates

> **Placeholders only.** Replace `<...>` before sending. Do not include internal system names, hostnames, error codes,
> incident identifiers or financial detail in customer-facing or partner-facing text.
> **Nothing in this section has been sent to anyone** — these are templates, with no execution history.

**13.1 Customer-facing release note**

```
Subject: What's new in AmmPal — <DATE>
Hi <CUSTOMER_FIRST_NAME>,
We've made some improvements to how you book and track services on AmmPal.
• <FEATURE_OR_IMPROVEMENT_1> — <ONE_SENTENCE_EXPLAINING_THE_CUSTOMER_BENEFIT>
• <FEATURE_OR_IMPROVEMENT_2> — <ONE_SENTENCE_EXPLAINING_THE_CUSTOMER_BENEFIT>
• <FIX_1> — <PLAIN_LANGUAGE_DESCRIPTION>
These changes are live now. No action is needed from you — your existing bookings and
account details are unaffected. If you have any questions, please contact us at
<SUPPORT_PHONE_OR_EMAIL>. Thank you for using AmmPal.
— The AmmPal Team
```

**13.2 Partner-facing release note**

```
Subject: AmmPal Partner Update — <DATE>
Dear <PARTNER_NAME>,
We have released an update to the AmmPal Partner App / dashboard.
What changed:
• <CHANGE_1> — <WHAT_IT_MEANS_FOR_THE_PARTNER>
• <CHANGE_2> — <WHAT_IT_MEANS_FOR_THE_PARTNER>
What you need to do:
• <ACTION_1> — <DEADLINE_OR_NONE>
• <ACTION_2> — <DEADLINE_OR_NONE>
Payments, commissions and statements continue to work exactly as before, unless
noted above. Questions? Reply to this message or contact <PARTNER_SUPPORT_CONTACT>.
— AmmPal Partner Support
```

**13.3 Internal changelog entry**

```
## [<VERSION>] — <YYYY-MM-DD> — <RELEASE_TYPE>
**Release manager:** <NAME> | **Approved by:** <ENGINEERING_LEAD>, <QA_LEAD>[, <OTHER>]
**Commit:** <COMMIT_SHA_SHORT>
**Artefacts:** api=<TAG>, worker=<TAG>, realtime=<TAG>, web=<TAG>, control-center=<TAG>, customer-app=<TAG>, partner-app=<TAG>
**Changes:** <AREA>: <CHANGE> (<PR_OR_TICKET>)
**Migrations:** <MIGRATION_FILE> — EXPAND|MIGRATE|CONTRACT — reversible: YES|NO — compensating: <ID|N/A>
**Feature flags:** <FLAG_KEY> — default OFF — owner <NAME> — expiry <DATE> — removal release <VERSION>
**Known issues:** <ISSUE> — impact <IMPACT> — workaround <WORKAROUND> — ticket <ID>
**Rollback:** target <PREVIOUS_VERSION> | symlink swap of /opt/ammpal/apps/<app>/current | expected time <DURATION>
**Verification:** GP-1 <PASS|FAIL>, GP-2 <PASS|FAIL>, GP-3 <PASS|FAIL>, GP-4 <PASS|FAIL> | health gate at 100%: 5xx <X>% (limit 1%), p95 <X>× baseline (limit 1.5×), worker errors <X>% (limit 1%), /health/ready GREEN
```

**13.4 Incident / rollback communication**

```
Subject: AmmPal service issue — <DATE> <TIME> IST — <SEVERITY> — <STATUS>
What happened
<PLAIN_DESCRIPTION_OF_THE_ISSUE_AND_WHICH_FEATURES_ARE_AFFECTED>
Who is affected
<WHO_CANNOT_BOOK|WHO_CANNOT_TRACK|WHO_CANNOT_PAY|ALL_CUSTOMERS> — affected from <TIME> IST. <ANY_DATA_IMPACT: YES|NO>
What we are doing
<WHAT_IS_HAPPENING_NOW>
What you can do
<CUSTOMER_WORKAROUND_OR_NONE>
Updates
We will send an update <EVERY_N_MINUTES_HOURS> until this is resolved, even if there is no change.
Need help?
Call <SUPPORT_CONTACT> or reply to this message. For urgent job issues, reference <REFERENCE>.
— AmmPal Support
```

**13.5 Communication rules**

- [ ] Customer communication is issued when customer-visible behaviour changes, or when an incident exceeds the agreed notification threshold.
- [ ] Partner communication is issued when partner-facing behaviour, commission, settlement or app behaviour changes; internal changelog is published for **every** release, including hotfixes.
- [ ] Communications are factually identical to observed behaviour — no speculation about causes before the post-incident review; no customer or partner data appears in any release note or incident communication.
- [ ] The toll-free number is referenced only as `1800-XXX-XXXX` until a real number is provisioned; it is a **placeholder**.

---

## 14. City / territory activation checklist

> **GATING CHECKLIST.** A city or territory **must not become bookable** until every **Blocking** row is satisfied with
> evidence. Activation is a one-way switch for customers: once a city is bookable, bookings, prices, invoices,
> commissions and settlements are all live.
>
> **Current status of every row below: `NOT STARTED`.** No city has been activated; no evidence has been produced.

| # | Gate item | Status | Owner | Evidence required | Blocking? | Who signs |
|---|---|---|---|---|:--:|---|
| 1 | **Approved operating territory** — defined service-area boundary, named operating branch, documented go-live date | `NOT STARTED` | Founder + Operations Lead | Approved territory note with boundary definition and branch assignment | ✔ | Founder |
| 2 | **Legal and tax review complete** — entity structure, registration, GSTIN, invoicing configuration and local tax applicability reviewed by counsel and Finance | `NOT STARTED` | Finance Owner + Founder | Counsel sign-off note; tax applicability memo | ✔ | Founder + Finance Owner |
| 3 | **Correct legal supplier and invoice issuer configured** — the supplying entity and the invoice-issuing entity are correctly configured for this territory | `NOT STARTED` | Backend Owner + Finance Owner | Configuration record; sample invoice rendered and reviewed | ✔ | Finance Owner |
| 4 | **Partner and employee capacity** — sufficient technicians (and partners, where the partner-branch model applies) to meet expected demand, contracted and onboarded | `NOT STARTED` | Operations Lead | Roster with counts, contracts signed, per-technician onboarding checklist | ✔ | Operations Lead + Founder |
| 5 | **Verified skills and categories** — each technician's skills, categories and service areas verified against the catalogue, covering the sub-₹10,000 Android device matrix where field tooling is used | `NOT STARTED` | Operations Lead + QA Lead | Skills verification register; category coverage matrix | ✔ | Operations Lead |
| 6 | **Approved prices and commission rules** — price books, taxes, coupons and 15% commission on eligible labour only configured and approved; amounts in integer paise, rates in basis points | `NOT STARTED` | Finance Owner + Product Owner | Approved price book; golden-master fixtures match; commission configuration reviewed | ✔ | Finance Owner |
| 7 | **Payment and refund readiness** — Razorpay configured for the territory; refunds and reversals verified; refund path tested end-to-end | `NOT STARTED` | Backend Owner + Finance Owner | Payment configuration record; test capture and test refund evidence | ✔ | Finance Owner |
| 8 | **Serviceability testing passed** — address → service area → available category → price → bookable verified across representative, boundary and non-covered addresses | `NOT STARTED` | QA Lead | Serviceability test report with covered and uncovered samples | ✔ | QA Lead |
| 9 | **Customer support and escalation coverage** — staffing, hours, language coverage, escalation matrix and contact channels defined, including the toll-free path (placeholder `1800-XXX-XXXX` until provisioned) | `NOT STARTED` | Operations Lead | Support roster and escalation matrix; published on-call contacts | ✔ | Operations Lead |
| 10 | **Cancellation and dispute process configured** — cancellation rules, no-show handling, rescheduling policy and the 5-business-day dispute window configured and communicated | `NOT STARTED` | Product Owner + Operations Lead | Policy configuration record; customer-facing text reviewed | ✔ | Product Owner |
| 11 | **Notification templates configured** — WhatsApp Business Platform, SMS (registered), email templates and push copy configured and approved for the territory's language(s) | `NOT STARTED` | Operations Lead + Product Owner | Template registry with approval status per channel and language | ✔ | Product Owner |
| 12 | **Operational reporting live** — territory-level booking, revenue, commission and settlement reporting works and reconciles | `NOT STARTED` | Backend Owner + Finance Owner | Report output; reconciliation against source data | ✔ | Finance Owner |
| 13 | **Infrastructure capacity verified** — headroom on the VPS (4 vCPU, 16 GB RAM, 200 GB NVMe, 16 TB bandwidth — **planning target, not a guarantee**) for the territory's expected load | `NOT STARTED` | Infra / SRE Owner | Capacity model and monitoring dashboards live | ✔ | Infra Owner |
| 14 | **Backup and restore verified** — production database backup runs and a **restore has been rehearsed** at this territory's data volume | `NOT STARTED` | Infra / SRE Owner + Database Owner | Backup job logs; restore rehearsal record with timings | ✔ | Infra Owner |

**14.1 Activation switch**

- [ ] All 14 rows above are `COMPLETE` with evidence attached — no row may be `NOT STARTED`, `IN PROGRESS` or `WAIVED`; any waived row has a written deviation signed by the Founder and the QA Lead, with an expiry date, recorded in `§17.2`.
- [ ] The serviceability check re-run on the activation day, immediately before flipping the switch; the city enabled in the catalogue in a **staging** configuration first and verified there.
- [ ] Activation is performed as a release — through the pipeline, in the standard window, with the full sign-off in `§16`; a city feature flag exists, defaults **off**, and is enabled with a named owner and an expiry (`§10`).
- [ ] Post-activation monitoring for 24 hours — booking success rate, acceptance rate, cancellation rate, first-response time; post-activation review within 7 days, and any defect above P2 triggers a rollback of the city activation.

**14.2 Deactivation.** A city can be made non-bookable without deleting its bookings, invoices, statements or settlement history. In-flight bookings are allowed to complete, with the SLA and policy documented before deactivation, and partners and technicians in the territory are notified beforehand.

---

## 15. First-day operational checklist

> Applies to the **first operational day** of a newly activated city, or of the first production release of the
> platform. No such day has occurred; this is a designed control with no execution history.

**15.1 On-call and coverage**

- [ ] On-call rota published for the first day, with names, phone numbers and escalation order; an engineer, a QA/on-call engineer and an operations lead are simultaneously reachable.
- [ ] Handover from the release team to the operations team completed in writing; platform incident channel open for the duration of the day.
- [ ] Escalation matrix published — who to call for a P0, who for a P1, and the fallback if the primary is unreachable.
- [ ] Vendor escalation contacts recorded (Razorpay, WhatsApp Business Platform, FCM, Google Maps, cloud telephony, SMS, email, S3-compatible storage, VPS provider) — **held in the internal runbook, not in this document**.

**15.2 Support staffing**

- [ ] Support staffed for the full operating hours of the day, with a named person per shift.
- [ ] Support trained on the booking flow, the four golden paths, the cancellation and dispute process, the 5-business-day dispute window, the refund path and the escalation matrix.
- [ ] Support holds the current price book and commission rules so pricing questions are answered correctly; known-issue sheet prepared listing the releases and defects open on day one; customer-facing FAQ updated for anything not previously communicated.

**15.3 Technician app distribution**

- [ ] Partner App / technician app build submitted with staged rollout configured (5% → 20% → 50% → 100%); build number incremented per `§12.5` and the registry updated with the last uploaded build number.
- [ ] Install instructions issued to technicians (Play Store / App Store, or direct install where the store path is not yet available); device coverage checked against the priority Android matrix (top 5 models by share in the Odisha market, including sub-₹10,000 devices) — see `OD-QA-04` `[OPEN]`.
- [ ] Crash-free-session threshold set **before** the rollout begins, with rollout stopped if breached; login, job feed, accept, start and complete verified on a real device by the operations team before the day opens.

**15.4 Seed roster verification**

- [ ] Seed roster matches the actual roster — every active technician has a verified skill set, service area and contact number; no technician remains in the roster with unverified skills or an empty service area, because a technician visible to customers who cannot accept jobs is a P1 on day one.
- [ ] Branch assignment correct for every technician in the territory; operating hours configured per branch and out-of-hours behaviour verified; technician onboarding checklist completed per technician.

**15.5 Monitoring and dashboards**

- [ ] Dashboards open: API error rate, latency percentiles, queue depth, worker error rate, database health, and the city-level booking funnel (search → price → book → accept → arrive → complete); payment success-rate dashboard live, segmented by provider response code.
- [ ] Alert routing tested — each P0 alert confirmed to reach a person who can act within 5 minutes; alert thresholds set for day-one volumes rather than steady state (higher absolute thresholds, tighter relative ones); daily metrics summary scheduled for the first two weeks.

**15.6 Kill switch and emergency controls**

- [ ] The city-activation kill switch is known to every person on call and has been **walked through once** on a non-production configuration; the kill switch for each feature flag is known, tested and reachable without a deploy.
- [ ] The process for pausing the booking feed (accepting no new bookings while in-flight work completes) is documented and rehearsed; the processes for pausing the cloud-telephony IVR, the SMS sender and the WhatsApp sender independently are documented.
- [ ] The documented path to disable payments is known and its consequence for in-flight bookings is understood; the rollback procedure (`§9`) is printed or pinned where the on-call engineer can reach it without searching.

**15.7 Day-one close**

- [ ] End-of-day review held: bookings created, completed and cancelled, payment failures, support tickets, incidents; every P0/P1/P2 defect logged with severity, owner and target release.
- [ ] Reconciliation performed for the day's payments (captures and refunds); any commission/settlement-affecting defect flagged to the Finance Owner before the next statement runs.
- [ ] Day-two changes, if any, planned and scheduled within the release window.

---

## 16. Release sign-off record template

> One copy per release. Copy the table, complete it, attach it to the release ticket, and link it from the release
> channel announcement. **No sign-off record exists for any release — no release has occurred.**

**16.1 Release identification**

| Field | Value |
|---|---|
| Release version / type | `<VERSION>` — `Hotfix` / `Patch` / `Minor` / `Major` / `Feature-flagged` / `Database-only` |
| Commit SHA / artefact digests | `<SHA>` — `api=<DIGEST>, worker=<DIGEST>, realtime=<DIGEST>, web=<DIGEST>, control-center=<DIGEST>` |
| Release manager / target window (IST) | `<NAME>` — `<DATE> <START>–<END>` |
| Migration set / previous version (rollback target) | `db-v<VERSION>` — `<VERSION>` |
| Release ticket / checklists attached (with evidence links) | `<LINK>` — `§4` ☐ · `§5` ☐ · `§6` ☐ · `§7` ☐ · `§8` ☐ · `§9` ☐ · `§10` ☐ · `§14` ☐ · `§15` ☐ |

**16.2 Signatures**

| Role | Name | Decision | Date/time (IST) | Signature / reference |
|---|---|---|---|---|
| Engineering Lead | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |
| QA Lead | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |
| Infra / SRE Owner | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |
| Database Owner | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |
| Mobile Lead | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |
| Security Owner | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |
| Finance Owner | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |
| Product Owner | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |
| Operations Lead | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |
| Founder / Sponsor (Major + city activation) | `<NAME>` | ☐ Approve ☐ Reject ☐ N/A | `<TIMESTAMP>` | `<REF>` |

**16.3 Post-release sign-off**

| Item | Value |
|---|---|
| Deploy executed by / witnessed by (SOD-2, SOD-8) | `<NAME>` / `<NAME>` |
| Health gate at 10% / 50% / 100% | `PASS` / `PASS` / `PASS` — metric values attached |
| Rollback performed? | `NO` / `YES` — reason and timings: `<REF>` |
| Deviations granted | `NONE` / list with expiry: `<REF>` |
| Post-release review scheduled / release closed by | `<DATE>` — `<NAME>` / `<DATE>` |

---

## 17. Unresolved items

> Items that must close before this checklist can be relied upon as an operational document. None has been decided;
> the references below point to open-decision IDs already recorded in `21`.

| # | Item | Linked OD | Impact on release governance | Owner | Needed by | Status |
|---|---|---|---|---|---|---|
| U-01 | **Managed Postgres for production vs self-hosted on the VPS** — affects backup, PITR, failover and the migration-rehearsal design. | `OD-DEV-01` | The rehearsal in `§5.4` and the backup/restore gates in `§4.7` and `§14` row 14 depend on the answer. | Eng Lead + Founder | Before production provisioning | `[OPEN]` |
| U-02 | **Managed Redis vs self-hosted** — affects worker isolation during canary and the queue-depth health gate. | `OD-DEV-02` | Canary routing of `ammpal-worker` and the "queue depth not growing" gate need a defined source of truth. | Eng Lead | Before the pipeline | `[OPEN]` |
| U-03 | **CI runner: GitHub-hosted vs self-hosted on the VPS** — a self-hosted runner on a 4 vCPU VPS would contend with production. | `OD-DEV-03` | Determines whether the release pipeline can run during a production incident without degrading prod. | Eng Lead | Before the pipeline | `[OPEN]` |
| U-04 | **Error-tracking / crash-reporting vendor (Sentry recommended).** | `OD-DEV-04` | Determines whether the monitoring checks in `§8.3` and mobile crash thresholds in `§15.3` have a system to check. | Eng Lead | Before Phase 1 | `[OPEN]` |
| U-05 | **Self-hosted MinIO vs managed S3-compatible provider.** | `OD-DEV-05` | Determines the object-storage smoke check in `§5.7` and the artefact storage path. | Eng Lead | Before Phase 1 | `[OPEN]` |
| U-06 | **WAF (Cloudflare) in front of the API and Control Center.** | `OD-DEV-06` | A WAF changes the 5xx baseline used by the health gate and may mask origin errors. | Security + Eng Lead | Before Phase 1 | `[OPEN]` |
| U-07 | **Separate staging environment from Phase 2.** | `OD-DEV-07` | Without dedicated staging, the `§5` gate is not meaningful and cannot gate production. | Leadership | Before Phase 2 | `[OPEN]` |
| U-08 | **Are the phase durations realistic for the planned team?** | `OD-RM-01` | Determines whether release capacity (one deploy per day, two-person deploy rule) is realistic. | Founder | Before Phase 1 | `[OPEN]` |
| U-09 | **Does Cuttack launch in Phase 3 or immediately after Bhubaneswar?** | `OD-RM-02` | Determines how many city activations are planned and the cadence of `§14` gating cycles. | Founder + Ops | Before Phase 3 | `[OPEN]` |
| U-10 | **Target date for the first city go-live.** | `OD-RM-03` | The `§14` activation cycle and the `§15` first-day checklist are anchored to this date. | Founder | Before Phase 1 | `[OPEN]` |
| U-11 | **One category at launch or two (appliance repair + cleaning recommended)?** | `OD-RM-04` | Determines the size of the first release's catalogue seed and the scope of the `§5.7` smoke matrix. | Founder + Product | Before Phase 1 | `[OPEN]` |
| U-12 | **Is the partner-branch model piloted in Phase 3?** | `OD-RM-05` | Partner-branch economics change the `§14` row 4 capacity gate and the commission sign-off path. | Founder | Before Phase 3 | `[OPEN]` |
| U-13 | **Testcontainers in CI vs managed ephemeral Postgres.** | `OD-QA-01` | Determines whether the integration stage of the release pipeline can be trusted as the `§4.2` gate. | QA + Eng Lead | Before the pipeline | `[OPEN]` |
| U-14 | **Flutter integration testing (device-level) in scope for v1.0?** | `OD-QA-02` | Determines whether `§15.3` can rely on automated device-level verification or manual checks only. | Mobile + QA | Before Phase 2 | `[OPEN]` |
| U-15 | **External penetration test before Phase 2 — budget and firm?** | `OD-QA-03` | The security gate (0 critical/high) has no external corroboration until this is scheduled. | Founder | Before Phase 2 go-live | `[OPEN]` |
| U-16 | **Priority real Android device test matrix.** | `OD-QA-04` | `§15.3` device coverage cannot be verified until the matrix is defined. | Product + QA | Before Phase 1 | `[OPEN]` |
| U-17 | **Dedicated performance environment separate from staging?** | `OD-QA-05` | `§5.2` results may be contaminated by other activity on a shared staging environment. | Eng Lead | Before Phase 3 | `[OPEN]` |
| U-18 | **Cross-branch acceptance — company technician in a partner branch's service area.** | `OD-LOC-01` | Affects roster verification in `§14` row 4 and the capacity model in row 13. | Product | Before Phase 2 | `[OPEN]` |
| U-19 | **Coverage fallback when a technician has no live GPS (home pin vs centroid).** | `OD-LOC-02` | Affects the tracking smoke check in `§5.7` and the GP-3 assertion in `§5.1`. | Eng Lead | Before Phase 1 | `[OPEN]` |
| U-20 | **City-level price overrides — state + branch only for v1.0 recommended.** | `OD-LOC-03` | Determines the shape of the price book used in `§14` row 6 and the golden-master fixtures. | Product + Finance | Before Phase 2 | `[OPEN]` |
| U-21 | **May a service area span two branches of different types during transition?** | `OD-LOC-04` | Determines whether a city activation can cover contiguous areas under one branch. | Product | Before Phase 3 | `[OPEN]` |
| U-22 | **"First available" (open feed) bookings at launch, or named-technician only?** | `OD-BK-02` | Changes the booking smoke checks and the GP-1/GP-2 E2E assertions. | Product | Before the booking module | `[OPEN]` |
| U-23 | **Maximum advance per category (25% or ₹99, whichever is higher, for appliance repair; 0% for cleaning).** | `OD-BK-03` | Changes the price-snapshot golden-master fixtures and the payment/refund readiness gate in `§14` row 7. | Finance | Before Phase 1 | `[OPEN]` |
| U-24 | **Cash collection at launch as a controlled manual payment (receipt reference, daily reconciliation, finance ticket).** | `OD-BK-04` | Requires a settlement-dry-run variant in `§8.2` and a reconciliation step in the day-one close (`§15.7`). | Finance + Product | Before Phase 1 | `[OPEN]` |
| U-25 | **Rescheduling free before `ACCEPTED`, ₹50 fee after, waived for platform delay or technician no-show.** | `OD-BK-05` | Adds a `RESCHEDULED(12)` path that must be exercised in `§5.1` and reconciled in `§8.2`. | Product | Before Phase 1 | `[OPEN]` |
| U-26 | **What "UI design approval" means, who gives it and what evidence it leaves.** | `OD-COM-03`, `OD-DOC-30`/`31`/`32`, `19` `R-45` | `§4.8` cannot be executed while the design system is `PROPOSED`, and `26` §4.1 attaches ₹1,00,000 to the same undefined event. A release that ships branded UI has, in practice, been approved by whoever wrote the CSS. | Founder + Product Design Lead | Before any UI ships | `[OPEN]` |
| U-27 | **No release gate verifies localisation, and no phase schedules it.** | `OD-DOC-35`, `12` §8 i18n-03, `FR-CAT-08`, `13` §7 `US-07`, `17` §7 | `12` §8 requires 100 % `or` and `hi` coverage with a 30 % expansion tolerance; **no item anywhere in this checklist tests for either** (verified by scanning §1–§18 for `i18n`, `locale`, `Odia`, `localis*` — the only hits are this row), and `17` names no i18n phase, so the requirement passes every gate while unmet. Compounded by `OD-DOC-32`: without the self-hosted subset Indic face, Odia text falls back rather than rendering, and `13` §5.2's `font-src 'self'` blocks the `<link>` that would have loaded it. | QA Lead + Product Lead + Frontend Lead | Before the locale decision closes; the check itself before the first multi-locale release | `[OPEN]` |
| U-28 | **No gate can be automated yet, and the tooling that would run the design rules does not exist.** `37` §11.2 lists nine checks meant to run on every pull request — contrast measured, hex outside the token package, undeclared `z-index`, un-admitted dependency, off-budget animation, untagged motion, empty `permissionToken`, missing placeholder prop, missing component contract row. `OD-14-12` (workshop and visual-regression tooling) and `OD-14-13` (token build) are the two decisions standing between that list and a manual reviewer. | `OD-14-12`, `OD-14-13`, `19` `R-48` | §4.8's structure, dependency and component items are prose until this closes — a reviewer can tick every box in §11.1 and still not know whether a value was measured or eyeballed. | Design + QA + Eng Lead | Before the design-gate review | `[OPEN]` |
| U-29 | **The mode guard as literally stated would block this document's own contract step, and the release gate cannot be written until that is decided.** `38` §6 class A refuses `DROP COLUMN` / `DROP TABLE` / `TRUNCATE` in `PRODUCTION`; §6.1's Expand → Migrate → Contract doctrine is built from exactly those statements and runs on production by design. Three readings exist (§6.1's `[OPEN]` note: operator-initiated only / absolute / mode-aware exception) and `DEC-03` forbids picking one here. Separately, **no gate in §4 or §5 can be executed at all yet** — §7.1's new `T-20` mode assertion and §4.2's new `TE-06` row both depend on `ADR-026`, which is `Proposed`, and on the fourth database identity `OD-DOC-43` has not authorised. | `OD-DOC-43`, `OD-DOC-40`, `ADR-026`, `15` `TE-06`, `19` `R-50` | Any release containing a contract step inherits the blockage; a deploy onto infrastructure resolving `TESTING` would run with the guard unarmed (`R-49`). Both new checklist items are `[PROPOSED]` and are not evidence that the gate exists. | Eng Lead + Database Owner + Security Owner | Before the first migration that removes anything | `[OPEN]` |

**17.1 Defect severity definitions used by this document**

| Severity | Definition | Release response |
|---|---|---|
| **P0** | Financial loss, data loss, security breach, or total outage | Immediate rollback or kill switch; incident process; post-incident review within 48 hours |
| **P1** | Core flow broken with no workaround | Same-day fix; hotfix path if a scheduled release cannot resolve it in time |
| **P2** | Non-core flow broken, workaround exists | Fix in the next scheduled release |
| **P3** | Cosmetic | Backlog; batch into a future release |

**17.2 Deviation log.** Every waived Blocking item is recorded here, with the release, the item waived, the reason, the person who accepted the risk, the expiry and the date. **No deviation has been recorded.** Format: `<#>` | `<RELEASE>` | `<ITEM>` | `<REASON>` | `<RISK ACCEPTED BY>` | `<EXPIRY>` | `<DATE>`.

---

## 18. Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.5 | 2026-10-21 | DevOps Lead (tooling and backup relocation) | §4.8's asset-integrity item now gives `validate_assets.py`'s new path and names the directory it must be run from, because the script resolves both `design-assets/` and `Docs/` against the working directory — an all-green run from the wrong folder is a broken invocation, not a passed gate. **No gate was added, removed or ticked**: the item remains untickable while 0 of the 93 inventory rows carry `APPROVED`, and this suite still describes no release that has passed through §4 at all. | §4.8 |
| 1.4 | 2026-10-21 | Eng Lead + QA Lead (platform-mode pass) | Four changes, all of them about this document's own steps. §7.1 gained a **T-20 pre-deploy assertion** — read `platform.platform_mode` from the database and record it, and **stop the deploy** if production infrastructure resolves `TESTING`, with the explicit prohibition on demoting or promoting to make a release go through (`25` §25.0). §4.2 gained a **`TE-06` mode-guard CI stage row**, marked `[PROPOSED]` because `ADR-026` is not accepted. §6.1 gained an `[OPEN]` note recording a collision this document cannot paper over: the doctrine's own **Contract phase** is made of `DROP COLUMN` / `DROP TABLE` / `TRUNCATE`, which `38` class A refuses in `PRODUCTION` — three readings exist, `DEC-03` forbids choosing one here, and a release ticket containing a contract step inherits the blockage. §17 gained **`U-29`** saying the same thing from the gate side. **No threshold, gate, severity band, role or sign-off rule was changed, and no gate in this document has ever been executed** — no release and no scaffold exist. | §4.2, §6.1, §7.1, §17 |
| 1.3 | 2026-10-21 | Engineering Lead + QA Lead (design-engineering structure pass) | §4.8 is renamed **Visual, asset, structure and component gate** and gained **eight items**, none of them invented: every new file must sit in a directory `35` names (`PS-01`, placement test §9); no dependency outside `36` §4/§5 (`LB-01`…`LB-08`); nothing may load a remote font, CDN script, icon font or un-nonce’d injected style (`13` §5.2 through `36` §3); every new component passes `37` §11.1’s fourteen items **with its evidence**, the four unmeasurable-by-eye items called out; no hex, duration or undeclared `z-index` outside the token package (`PS-11`, `CA-09`…`CA-15`); no component name added outside `12` §6.2 (`CA-00`) and no motion outside the nine recipes (`CA-16`); no navigation item shipped with an empty `permissionToken` (`PS-14`, gated by `OD-10-06`/`OD-DOC-29`); and **`OD-DOC-38` closed before anything is scaffolded or `git init` runs** (`19` `R-48`). §17 gained **`U-28`**: `37` §11.2 lists nine checks meant to run on every pull request, and until `OD-14-12`/`OD-14-13` close they are prose a reviewer may tick. **No threshold, gate, role, sign-off rule or release type was changed**, and the gate still has never been passed, because no release and no scaffold exist. | §4.8, §17, Revision History, header |
| 1.2 | 2026-10-21 | Engineering Lead + QA Lead (palette, storage and prompt-pack pass) | §4.8 gained **three items, all traceable to a document rather than to taste**: every image origin in the build must appear in `13` §5.2's `img-src` — with the explicit note that an off-list CDN renders in development and fails in production, and that **no validator in this workspace checks a serving origin** (`32` §4), so the gate is the only place the constraint exists while `OD-DOC-34` `[BLOCKER]` is open; a screen shipping with placeholder containers (`30` §5.3) may not be described as approved design work, and the release notes must say the artwork is outstanding (`OD-DOC-36`); and any `GENERATED` asset is blocked from the bundle by name, because `GENERATED` is not `APPROVED` (`32` §6, `34` §6). §17 gained **U-27** — no item anywhere in this checklist tests localisation, verified by scanning §1–§18 for `i18n`/`locale`/`Odia`/`localis*`, while `12` §8 i18n-03 requires 100 % `or`/`hi` and a 30 % expansion tolerance, `17` §7 names no i18n phase and `OD-DOC-32` leaves Odia without a subset face to render with. **No existing gate, threshold, role, severity band or sign-off requirement was changed, and no new `OD-*` row was created here** — `21` owns those. | §4.8, §17, header, Revision History |
| 1.1 | 2026-10-21 | Engineering Lead + QA Lead (design-system and asset pass) | §4.8 **Visual and asset gate** added and labelled `[PROPOSED]` — it has never been executed, because no release exists. Eight items: the asset validator exits clean; **no shipped screen may reference an asset that is not `APPROVED`, and today none of the 93 inventory rows is** (83 `PLANNED`, 6 `BLOCKED`, 4 `REGISTERED`); the four reference infographics are `NOT_FOR_PRODUCTION` and stay out of every bundle; token values rather than literals, with contrast measured per pair; `a11y_treatment` and alt text validated in both directions; **no animation, skeleton or optimistic UI accepted as evidence of server state**; any new image or font re-checked against the `13` §2.2 budgets, which are themselves unmeasured on a device; store screenshots only from an actual approved build. §17 gains **U-26**, that the approval event `26` §4.1 pays ₹1,00,000 on is undefined (`OD-COM-03`, `OD-DOC-30`/`31`/`32`, `19` `R-45`) — a release shipping branded UI has, in practice, been approved by whoever wrote the CSS. No existing gate, threshold, role or severity band was changed, and no new `OD-*` row was created. | §4.8, §17, header, Revision History |
| 1.0 | 2026-10-21 | Engineering Lead + QA Lead | Initial release-governance reference. Purpose and usage rules (`§1`), roles and separation of duties (`§2`), release types (`§3`), pre-release readiness (`§4`), staging verification (`§5`), database migration (`§6`), production deployment (`§7`), post-deployment verification (`§8`), rollback and hotfix (`§9`), feature-flag procedure (`§10`), release calendar and freezes (`§11`), versioning (`§12`), communication templates (`§13`), city activation gating (`§14`), first-day operations (`§15`), sign-off record (`§16`), unresolved items (`§17`). **Designed control only — no release, deployment, rehearsal or checklist has been executed.** | All (§1–§18) |

---

*End of document — AMM-SVC-DOC-29 v1.0.*
