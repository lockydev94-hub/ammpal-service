# 15 — QA & Test Strategy

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-15 |
| Version | 1.3 |
| Status | Approved for Design & Development |
| Owner | QA Lead + Engineering Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `04`, `07`, `13`, `14` §7 |

---

## 1. Objectives

| # | Objective | Measure |
|---|---|---|
| QA-1 | A defect that could cause **financial loss** never reaches production | 100% of money-path logic covered by golden-master tests |
| QA-2 | The four golden paths (book → serve → pay → settle) always work | 100% E2E coverage, green on every release |
| QA-3 | Regressions are caught before deploy | ≥ 85% of escaped defects were previously covered by a test that failed |
| QA-4 | Test feedback is fast | Unit suite < 5 min; integration < 15 min; E2E < 25 min |
| QA-5 | The domain is provably correct, not just exercised | Property-based tests on money and state transitions |

---

## 2. Test Pyramid

```
        ╱ E2E ╲               ~5%   — 4 golden paths + critical regressions
      ╱─────────╲
     ╱ Contract  ╲            ~10%  — OpenAPI drift, generated clients, vendor contracts
    ╱─────────────╲
   ╱  Integration  ╲          ~30%  — API + real Postgres/PostGIS + Redis + adapters
  ╱─────────────────╲
 ╱    Unit + Property ╲        ~55%  — domain modules, pure logic, money arithmetic
```

| Layer | Tool | Runs on | Target |
|---|---|---|---|
| Unit | Jest (api), Vitest (web/cc) | Every push | ≥ 80% lines on domain modules; ≥ 95% on `pricing`, `commission`, `billing` |
| Property-based | fast-check | Every push | ≥ 200 cases per property |
| Integration | Jest + Supertest + Testcontainers (Postgres+PostGIS, Redis) | Every push | ≥ 90% of API endpoints |
| Contract | Spectral + dredd + generated-client tests | Every push | 0 drift |
| E2E | Playwright (web + Control Center), Flutter integration tests | Every merge to main | 4 golden paths — GP-1 on dev + staging + prod smoke, GP-2…GP-4 on dev + staging (`§8`) |
| Mobile | `flutter test` + `integration_test` | Every push | Widget tests for all stateful widgets; golden tests for 5 key screens |
| Performance | k6 | Nightly + pre-release | `13` §2 targets |
| Security | OWASP ZAP (DAST), npm audit, Trivy (images), Semgrep (SAST), Gitleaks | Every push + nightly | 0 critical/high |
| Accessibility | axe-core (web), TalkBack/VoiceOver manual pass | Every release | WCAG 2.1 AA |

---

## 3. Test Data Strategy

| Rule | Detail |
|---|---|
| TD-01 | Factories in `packages/testing` build valid domain objects. Tests never hand-write a full entity. |
| TD-02 | Fixtures are deterministic — a seeded RNG where randomness is needed. |
| TD-03 | Each test gets a **fresh, isolated database** (a per-worker schema or a truncated-and-reset template). No test depends on another's state. |
| TD-04 | Production data is **never** used in tests. A sanitised snapshot may be used in staging. |
| TD-05 | Tests create their own geography, branch, price book and coupon rather than depending on seeded reference data. |
| TD-06 | Time is injected via a `Clock` abstraction. Tests can set "now" — no `Date.now()` in domain code. |
| TD-07 | Money test values include boundary cases: 0, 1 paisa, ₹0.01, ₹99.99, very large, and a value that triggers rounding. |

---

## 4. Test Levels by Module

| Module | Unit | Property | Integration | E2E |
|---|:--:|:--:|:--:|:--:|
| `pricing` | ✔ | ✔✔ | ✔ | ✔ |
| `commission` | ✔ | ✔✔ | ✔ | ✔ |
| `billing` | ✔ | ✔ | ✔ | ✔ |
| `booking` | ✔ | ✔ | ✔ | ✔ |
| `workflow` | ✔ | ✔ | ✔ | — |
| `catalog` | ✔ | — | ✔ | — |
| `organization` | ✔ | — | ✔ | — |
| `rbac` / `identity` | ✔ | — | ✔ | ✔ |
| `partner` | ✔ | — | ✔ | — |
| `support` | ✔ | — | ✔ | ✔ |
| `notification` | ✔ | — | ✔ | — |
| `reporting` | ✔ | — | ✔ | — |
| `integration` | ✔ (adapters mocked) | — | ✔ (contract tests) | — |

---

## 5. Financial Correctness Testing

This is the highest-risk area and gets the deepest treatment.

### 5.1 Golden-Master Tests

The pricing and commission domain modules are **pure functions**. Their expected outputs are stored
as fixtures. Any change to an output is a deliberate, reviewed change.

```
apps/api/src/modules/pricing/__golden__/
  ac_repair_standard.json
  ac_repair_platform_coupon.json
  ac_repair_partner_coupon.json
  ac_repair_shared_coupon.json
  cleaning_2bhk.json
  inter_state_igst.json
  parts_with_mrp_margin.json
  diagnostic_charge.json
  ...
```

Each fixture holds the complete expected `PriceSnapshot` — every line, discount, tax component,
total and commission figure.

### 5.2 Worked-Example Regression

The documented worked example from `07` §4 is a **permanent test**:

| Input | Expected |
|---|---|
| Labour 600, Visiting 99, Parts 250, Platform coupon −50, Partner coupon 0 | Subtotal 949, GST 170.82, Total 1119.82 |
| Eligible labour | 600 |
| Commission @ 15% | 90 |
| GST on commission @ 18% | 16.20 |
| Commission invoice | 106.20 |
| Partner labour earnings | 510.00 |

Any deviation fails the build.

### 5.3 Property-Based Tests

| Property | Statement |
|---|---|
| P1 | `Σ(line amounts) + Σ(tax) = grand total` — for any input |
| P2 | `Σ(invoice lines) = invoice.total` — for any invoice |
| P3 | `Σ(settlement lines) + Σ(adjustments) = settlement.net` — for any settlement |
| P4 | `Σ(ledger debits) = Σ(ledger credits)` — for any posting |
| P5 | A platform-funded discount never changes the partner's net earnings |
| P6 | A partner-funded discount reduces both the commission base and the partner's net, consistently |
| P7 | Commission ≤ eligible labour, always |
| P8 | Every computed amount is an integer; no value is ever fractional |
| P9 | Rounding never changes the total by more than 1 paisa per line |
| P10 | A booking produces **exactly one** commission ledger entry (property: uniqueness under concurrency) |
| P11 | Settlement generation is idempotent — running it twice yields the same statement |
| P12 | The coupon's total usage never exceeds its cap under any concurrent redemption order |

### 5.4 Concurrency & Race Tests

| Scenario | Assertion |
|---|---|
| 100 concurrent redemptions of a coupon with `max_uses_total = 10` | Exactly 10 succeed; 90 get `COUPON_USAGE_LIMIT_REACHED` |
| Two technicians accept the same offer concurrently | Exactly one succeeds; the other gets `409 STATE_CONFLICT` |
| Complete + cancel race on one booking | One transition wins; the state machine remains consistent; the invoice exists iff the job completed |
| Duplicate payment webhook | One payment row; one invoice transition |
| Settlement generation run twice in parallel | One statement (unique constraint) |
| Two admins approve the same partner concurrently | One approval; the other gets `409` |

### 5.5 Reconciliation Tests

A nightly CI job asserts, against a seeded dataset:

```
SUM(invoice_lines.amount) = SUM(invoices.total)          → 0 difference
SUM(invoice_lines.tax)    = SUM(invoices.tax)            → 0 difference
SUM(settlement_lines) + SUM(adjustments) = SUM(net)       → 0 difference
SUM(commission_ledger) grouped by booking = COUNT(DISTINCT booking_id) → equal
SUM(ledger_entries debit) = SUM(ledger_entries credit)   → 0 difference
```

---

## 6. State Machine Testing

The booking state machine (`04` §4) is tested exhaustively.

| Test type | Assertion |
|---|---|
| Table-driven | Every (from, event) pair in the transition table is exercised; every undeclared pair throws `INVALID_STATE` |
| Reachability | Every status is reachable from `REQUESTED` |
| Terminality | No transition leaves a terminal status except the admin `reopen` |
| Invariant | `booking_events` contains an ordered, gapless sequence for every booking |
| Property | A booking's event log, replayed, always reproduces the current status |
| Fuzz | Random event sequences never produce an illegal state |

---

## 7. RBAC & Scope Testing

| Test type | Assertion |
|---|---|
| Matrix completeness | Every (role, permission) pair in `03` §4 is asserted — a permission not granted in the matrix is denied |
| Default deny | A permission not in any role is denied |
| Scope isolation | A `BRANCH`-scoped user cannot read a row from another branch, on **every** list and detail endpoint (automated sweep) |
| Cross-scope write | Returns `403 SCOPE_VIOLATION` and writes a security event |
| Ownership | A customer cannot read another customer's booking (returns `404`, not `403`) |
| No privilege escalation | A user cannot assign a role that grants more than their own permissions |
| Self-approval | The approving account cannot be the requesting account |
| SoD | An account holding `settlement:issue` cannot hold `settlement:approve` |
| Field restrictions | The fields listed in `03` §5 are rejected for the restricted roles |

The scope sweep is an automated test that enumerates every tenant-scoped endpoint and asserts the
isolation property — this is the highest-value security test in the suite.

---

## 8. Golden Paths (E2E)

| # | Path | Steps | Environments |
|---|---|---|---|
| **GP-1** | **Book → Serve → Pay → Review** | Customer registers → selects location → sees a service → compares technicians → books → pays advance → technician accepts → travels → customer verifies OTP → technician completes the checklist → invoice generated → balance paid → customer rates | dev, staging, prod (smoke) |
| **GP-2** | **Book → Accept → Settle** | A completed booking accrues commission → the weekly run generates a statement → a commission invoice is issued → the partner pays → reconciliation matches → the settlement closes | dev, staging |
| **GP-3** | **Call → Book → Track** | The customer calls the toll-free number → the IVR collects language and reason → the caller is identified → the CCO sees the screen-pop → the CCO books → the customer receives an SMS → the customer tracks the technician on the web | dev, staging |
| **GP-4** | **Complaint → Rework → Refund** | A customer raises a complaint → it escalates to the branch → a rework is assigned to a different technician → the balance is refunded → the ticket closes with a CSAT | dev, staging |

Each golden path is scripted in Playwright against the **real** stack (a seeded Postgres), with
vendor adapters in a deterministic mock mode.

---

## 9. API Contract Testing

| Check | Tool | Gate |
|---|---|---|
| OpenAPI drift | Generated spec committed; CI regenerates and diffs | Fail on any diff |
| Spectral lint | Spectral ruleset (naming, descriptions, examples, security) | Fail on error |
| Generated client compatibility | Run the generated client's contract tests | Fail on any error |
| Consumer-driven contracts | Pact-style contracts for the vendor adapters (payment, telephony, WhatsApp) | Fail on a breaking change |
| Backward compatibility | `oasdiff` against the last released spec | Fail on a breaking change within `/v1` |

---

## 10. Performance Testing

| Scenario | Tool | Target |
|---|---|---|
| Booking search under load | k6 | p95 < 800 ms at the Phase 3 profile |
| Booking creation | k6 | p95 < 350 ms |
| Complete-job flow (with the invoice transaction) | k6 | p95 < 500 ms |
| Settlement generation for 5,000 jobs | k6 / script | < 60 s |
| Concurrency spike | k6 | No errors, no connection-pool exhaustion |
| Soak (24 h at 1.5×) | k6 | No memory leak, no connection leak, stable p95 |
| Report queries | k6 | p95 < 900 ms with a warm cache |

**Rule PERF-01** — The performance suite runs nightly against `staging` with production-like data
volume, so regressions are detected before a release, not after.

---

## 11. Security Testing

| Check | Tool / method | Frequency |
|---|---|---|
| Dependency vulnerabilities | `npm audit`, OSV scanner | Every push; critical blocks |
| Container image vulnerabilities | Trivy | Every push; critical/high blocks |
| Static analysis | Semgrep (OWASP rules) + ESLint security plugin | Every push |
| Secret leakage | Gitleaks | Every push + pre-commit |
| API fuzzing | Schemathesis (property-based, OpenAPI-driven) | Nightly |
| DAST | OWASP ZAP baseline + active scan | Nightly against staging |
| Authorisation sweep | Custom scope-isolation suite (§7) | Every push |
| Rate-limit verification | Automated test | Every push |
| Penetration test | External consultant | Before Phase 2 go-live, then annually |

---

## 12. Accessibility Testing

| Check | Tool | Gate |
|---|---|---|
| Automated axe scan | axe-core on every key web route | 0 serious/critical |
| Keyboard navigation | Manual + automated tab-order checks | All flows completable by keyboard |
| Screen reader | VoiceOver (iOS/macOS), TalkBack (Android) manual pass on the 5 key screens | No blockers |
| Contrast | Automated + manual | WCAG AA |
| Touch targets | Automated on Flutter golden screens | ≥ 48 dp |
| Motion | `prefers-reduced-motion` honoured | Verified |

---

## 13. Manual & Exploratory Testing

| Category | Focus | Who |
|---|---|---|
| Exploratory charters | Each of the 9 booking stages; the 6 call use cases; each service category workflow | QA + Product |
| Device testing | The 5 most common Android devices in the target market (₹8k–₹15k), 2 iPhones | QA |
| Network testing | 3G/poor-4G, high latency, packet loss, offline mid-job | QA + Ops |
| Payment edge cases | Gateway timeout, webhook delay, double-tap, insufficient funds, cancelled checkout | QA + Finance |
| Localisation review | Odia/Hindi text expansion, truncation, font fallback | QA + Design |
| Usability review | Task-based with 5 real customers per persona | Product + Design |
| Rehearsal | A full dry-run of a launch day in a new city | Ops + QA + Engineering |

---

## 14. Release Quality Gates

A release cannot be deployed unless **all** are green:

| # | Gate | Threshold |
|---|---|---|
| G-01 | Unit + property tests | 100% pass; coverage ≥ 80% (95% for money modules) |
| G-02 | Integration tests | 100% pass |
| G-03 | Contract tests | 0 drift, 0 breaking changes |
| G-04 | E2E golden paths | All 4 pass on staging |
| G-05 | Security scans | 0 critical, 0 high |
| G-06 | Performance suite | All targets met on staging |
| G-07 | Accessibility | 0 serious/critical issues |
| G-08 | Migration rehearsal | Applies cleanly to a production-like snapshot; rollback rehearsed |
| G-09 | Documentation | The affected docs in `Docs/` are updated; no stale rule statements |
| G-10 | Manual QA sign-off | QA Lead approves the release notes |
| G-11 | Change management | Database changes are backward-compatible with the current production version |
| G-12 | Feature flags | New behaviour is behind a flag; the flag defaults to off for non-production |

---

## 15. Defect Management

| Severity | Definition | Response | Release policy |
|---|---|---|---|
| **P0** | Financial loss, data loss, security breach, total outage | Immediate, all hands | Fix-forward; hotfix as needed |
| **P1** | Core flow broken for a subset of users; no workaround | < 4 h | Must fix before release |
| **P2** | Non-core flow broken; workaround exists | < 2 days | Fix if related to the change |
| **P3** | Cosmetic; low impact | Next sprint | Backlog |

| Rule | Detail |
|---|---|
| DM-01 | Every defect links to a ticket, a severity and (for P0/P1) a repro. |
| DM-02 | A P0/P1 defect triggers a post-mortem under `25` §28, due within **5 working days** (Rule `25` OPS-30 — the single post-mortem clock; there is no separate 48 h rule). |
| DM-03 | Regression tests are added for every P0/P1 fix **before** it is closed. |
| DM-04 | "Won't fix" requires a written rationale and an owner. |

---

## 16. Test Environments & Data

| Environment | Data | Purpose |
|---|---|---|
| Local | Seeded synthetic | Developer work |
| `dev` | Synthetic, reset daily | Integration |
| `staging` | Production-like volume and shape (synthetic, 5,000 bookings) | Release verification, performance, E2E |
| `prod` | Real | Live |

| Rule | Detail |
|---|---|
| TE-01 | Staging mirrors production's **shape** (counts, distributions, cardinality) even though the data is synthetic. |
| TE-02 | A nightly job resets `dev` and reseeds `staging`. |
| TE-03 | Vendor adapters run in a deterministic **mock mode** in test environments; a subset of sandbox-mode real calls runs nightly. |
| TE-04 | A sanitised production snapshot may be loaded into staging for performance work, with all PII tokenised. |
| TE-05 | A **rehearsal** release is deployed to staging using the exact production deploy pipeline before a production release. |
| TE-06 | The platform mode (`38`) is a **test-data requirement, not a deployment detail.** A test that can pass while
  `PRODUCTION` mode permits a hard delete is not a test of this feature: `15` asserts the guard at the service layer
  **and** the database-privilege layer (`38` §7 L2/L3), asserts that a `prod` target booting in `TESTING` is refused
  (`PM-04`), and asserts that the class-D retention purges and the class-B soft-delete path still succeed in
  `PRODUCTION` — a guard that blocks those is a failed implementation, not a safer one (`09` §6). Origin marking is
  asserted too: a `TEST`-origin booking must be invisible to `FR-RPT` reports, commission accrual (`07` §7) and
  settlement generation (`PM-17`), and no `T-`-series document may be delivered as an invoice. |

---

## 17. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| OD-QA-01 | Testcontainers in CI vs a managed ephemeral Postgres service? Testcontainers is simpler; a service is faster. | QA + Engineering | Phase 0 |
| OD-QA-02 | Is Flutter integration testing (device-level) in scope, or widget + unit only for v1.0? | Mobile + QA | Phase 1 |
| OD-QA-03 | Do we hire an external penetration test firm before Phase 2, and at what budget? | Leadership | Phase 1 |
| OD-QA-04 | Which real Android devices are the priority test matrix (model list from Odisha market data)? | Product + QA | Phase 1 |
| OD-QA-05 | Do we need a dedicated performance environment separate from staging? | Engineering | Phase 2 |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.3 | 2026-10-21 | QA Lead + Eng Lead (platform-mode pass) | §16 gained **`TE-06`**, because a guard nobody asserts at the layer that enforces it is a rumour of a guard: assert the refusal at **both** L2 (the handler) and L3 (the bound database privilege), assert that production infrastructure resolving `TESTING` refuses staff mutations at boot, assert that **soft delete and the retention purge still work** (a guard that also blocks class B and D is a regression, not a control), and assert that `TEST`-origin rows are invisible to reports, commission accrual and settlement. The negative assertions are deliberate — the most likely way this feature ships is a guard that blocks the wrong things. | §16 |
| 1.2 | 2026-10-21 | QA Lead + Engineering Lead | Audit pass 3. §2 E2E scope re-stated as it is actually achievable: **GP-1 runs on dev + staging + a production smoke, GP-2…GP-4 on staging only** — the previous "4 golden paths × 3 environments" implied four production E2E runs, which cannot be executed against live customer data and no environment list in `16` §2 supports. §15 `DM-02` post-mortem clock aligned to the **single** clock in `25` §28/Rule `OPS-30` (**5 working days**) instead of the 48 hours asserted here; the two documents disagreed and `25` owns incident process. | §2, §15 |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Added the state-machine, serviceability, supplier-resolution and coupon-concurrency test obligations identified by the audit; cross-referenced the two-layer model and the golden-master worked example. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
