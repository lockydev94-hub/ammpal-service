# 17 — Roadmap & Delivery Plan

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-17 |
| Version | 1.5 |
| Status | Approved for Design & Development |
| Owner | Product Lead + Engineering Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `00`, `01`, `14` |

---

## 1. Phase Model

| Phase | Name | Duration | Outcome |
|---|---|---|---|
| **0** | Foundation | 4 weeks | Design signed off; stack decided; repo, CI and environments live; master data modelled; seed data |
| **1** | Core Platform | 8 weeks | Customers can book; technicians can execute; payments work; the central admin can operate |
| **2** | Service & Money | 8 weeks | Workflow engine, pricing rules, coupons, invoices, commission, weekly settlement, tax |
| **3** | Branch & Scale | 8 weeks | Branch model live; branch & partner-branch dashboards; support console; analytics; second and third cities |
| **4** | Growth | Ongoing | Multi-state, partner-branch expansion, new categories, optimisation, subscriptions |

> Durations assume a team of the size in `18` §2. They are **estimates for planning**, not commitments.

> **The calendar is `[OPEN]` (`OD-DOC-08` / `OD-RM-03`).** Phases 0–3 total **28 weeks**, while
> `26` §4 states a **six-month** delivery target — six months is roughly 26 weeks, so the commercial
> document is about two weeks shorter than the plan that supports it, before any contingency. Neither
> figure is wrong on its own; they are two different commitments with no reconciliation between them.
> Until `OD-RM-03` sets a date and `OD-COM-11` states whether the six-month figure is absolute,
> **no duration or date in this document may be quoted to the development partner, a branch or a
> customer as a delivery commitment.**

---

## 2. Phase 0 — Foundation (Weeks 1–4)

| # | Deliverable | Exit Criterion |
|---|---|---|
| P0-01 | All Phase 0 decisions in `21` closed | Every OD-xxx due in Phase 0 has an owner decision recorded |
| P0-02 | Stack and tooling decisions closed | `OD-14-01` … `OD-14-05` decided |
| P0-03 | Monorepo scaffolded | `apps/*` and `packages/*` build; CI runs green on an empty app |
| P0-04 | CI pipeline complete | `14` §9 stages implemented, with the quality gates in `15` §14 |
| P0-05 | Environments provisioned | `dev`, `staging` live; `prod` VPS provisioned and hardened |
| P0-06 | Auth + RBAC foundation | OTP login, JWT, roles, permissions, scope guards, audit log |
| P0-07 | Organization module | States, cities, branches, partner orgs, zones, service areas, territory allocation |
| P0-08 | Catalog module | Categories, services, variants, skills, price book — seeded for Odisha |
| P0-09 | Seed data | Bhubaneswar HQ branch with zones, areas, price book for 3 categories. `[OPEN]` — the **3** here, the **4** in P2-02 below, the **6** launch families in `06` §4 and `OD-RM-04`'s recommended **2** are four answers to one question; see `OD-DOC-27`. This row is the one a design or asset estimate has to read, so it is the row that should carry the number once it is decided |
| P0-10 | Design system + tokens | `packages/design-tokens`; a component library in Figma. `[OPEN]` — **this deliverable presumes two undecided things**: `OD-12-01` never chose the design tool (Figma is written here as if settled), and the token **values** in `30` §3–§7 are `PROPOSED` pending `OD-DOC-30`/`31`/`32`. `33` §3–§4 is the screen list this must cover, and its §5 names eight components with no designed non-happy state. The gate that consumes this output is `26` §4.1's second instalment (`R-45`) |
| P0-11 | OpenAPI contract | Generated from the API; published; clients generated |
| P0-12 | Observability baseline | Logs, metrics, traces, dashboards, alerts |
| P0-13 | Backup + restore | Automated backup and a **successful** restore drill |
| P0-14 | Tax advisor engagement | `OD-07-01`, `OD-07-02`, `OD-07-03` answered in writing |
| P0-15 | Platform mode + origin marker (`38`) | `platform.platform_mode` exists with its append-only history, the
  `record_origin` column is in the **first** migration that creates a transaction table, and the guard is asserted at
  `15` `TE-06`. `[PROPOSED]` — this is an owner addition of 2026-10-21 (`01` §4.11), **not** part of the signed scope,
  and it is blocked by `OD-DOC-38` (which backend writes it), `OD-DOC-40`/`41` and `22` `ADR-026`. Sequencing note:
  P0-08/P0-09 seed the first city's data, so doing those before this row leaves every seeded row origin-unknown |

**Phase 0 exit gate** — a new engineer can clone, run, test and deploy; the founder can log into the Control Center and see a seeded Bhubaneswar branch; the tax treatment is written down.

---

## 3. Phase 1 — Core Platform (Weeks 5–12)

### 3.1 Scope

| Area | Deliverables |
|---|---|
| **Customer** | Registration (OTP, social), address book with geocoding, service browsing, technician discovery & comparison, slot selection, booking, price breakdown, advance payment, booking history, live tracking, cancellation, rating, support ticket, notifications |
| **Partner App** | Onboarding (KYC docs, skills, service areas, bank details), job feed, accept/reject, navigate, OTP-verified job start, checklist, parts, evidence, invoice, collect balance, earnings, availability |
| **Website** | Home, category, service detail, technician list/profile, booking flow, booking detail/tracking, partner registration, support pages, SEO basics |
| **Control Center** | Role-based dashboard, user & role administration, branch/partner/technician approval, territory allocation, booking list & detail, manual assignment, job feed monitor, technician roster |
| **Payments** | Razorpay orders, hosted checkout, webhooks, refunds, daily reconciliation |
| **Platform** | Notifications (push + SMS), realtime tracking, audit log, feature flags |

### 3.2 Milestones

| Milestone | Weeks | Deliverable |
|---|---|---|
| M1.1 | 5–6 | Auth, catalog, discovery, address/geo resolution |
| M1.2 | 7–8 | Booking creation, offer dispatch, accept/reject, assignment |
| M1.3 | 9 | Partner app core: feed, travel, OTP start, checklist, complete |
| M1.4 | 10 | Payments: advance + balance + refund + reconciliation |
| M1.5 | 11 | Website booking flow + tracking + rating |
| M1.6 | 12 | Control Center MVP: dashboard, approvals, job feed, roster |

### 3.3 Phase 1 Exit Criteria

| # | Criterion | Measure |
|---|---|---|
| E1-1 | Golden path GP-1 passes end-to-end in staging | Automated |
| E1-2 | 50 seeded technicians in Bhubaneswar, each with valid KYC | Data |
| E1-3 | A real booking completes with a real (small-value) payment | Manual |
| E1-4 | Fill rate ≥ 80% in the seed area over a 2-week simulated run | Report |
| E1-5 | p95 booking creation < 350 ms; search p95 < 800 ms | Performance suite |
| E1-6 | No P0/P1 open defects | QA sign-off |
| E1-7 | Internal dogfooding: 20 team members complete real bookings | Ops |

---

## 4. Phase 2 — Service & Money (Weeks 13–20)

| # | Deliverable | Exit Criterion |
|---|---|---|
| P2-01 | Workflow engine | Templates, versions, instances, step execution, checklists, evidence, overrides |
| P2-02 | Service-type workflows | Appliance repair, cleaning, plumbing, electrical published and configurable. `[OPEN]` — **4** categories named, against **3** in P0-09, **6** in `06` §4 and **2** recommended by `OD-RM-04` (`OD-DOC-27`) |
| P2-03 | Pricing rules engine | State → city → zone → service-area resolution with a provenance chain |
| P2-04 | Branch price overrides | In-band customisation with DB-level enforcement |
| P2-05 | Coupon engine | Platform / partner / shared funding, all rules, auto-validation at booking and billing |
| P2-06 | Tax engine | Place of supply, CGST/SGST/IGST, per-registration treatment, versioned rates |
| P2-07 | Invoicing | Gapless numbering, itemised lines, adjustments, downloadable PDFs, delivery |
| P2-08 | Commission engine | Eligible-labour rules, versioned rates, immutable ledger, accrual |
| P2-09 | Weekly settlement | Statement generation, commission invoice with GST, payout tracking, reconciliation, disputes, adjustments |
| P2-10 | General ledger | Double-entry postings, nightly balance assertion |
| P2-11 | Call support | Telephony provider, IVR, smart routing, call logs, CCO console, the 6 use cases |
| P2-12 | Ticket system | Categories, priorities, SLA timers, escalation, CSAT |
| P2-13 | WhatsApp + email + SMS integration | Templates, localisation, delivery log, fallback chain |
| P2-14 | Finance Control Center | Commission ledger, settlements workbench, reconciliation, tax registrations, disputes |
| P2-15 | Penalty & scoring engine | Technician score, customer score, penalties, ranking impact |
| P2-16 | Compliance | DPDP consent, privacy notice, retention jobs, grievance channel |

### 4.1 Phase 2 Exit Criteria

| # | Criterion | Measure |
|---|---|---|
| E2-1 | Golden path GP-2 (settle) passes end-to-end | Automated |
| E2-2 | Golden master suite green; the `07` §4 worked example passes | CI |
| E2-3 | Three consecutive weekly settlements generated, issued, paid and reconciled with **zero** manual adjustments | Finance run |
| E2-4 | Nightly reconciliation reports 0 differences across invoices, settlements and the ledger | Report |
| E2-5 | Tax advisor has reviewed a sample of 20 real invoices and 3 real commission invoices | Sign-off |
| E2-6 | 100 support calls simulated through the IVR and console | QA |
| E2-7 | An external penetration test is complete with no high/critical findings | Report |
| E2-8 | Cancellation, refund and penalty policies are enforced end-to-end | E2E |

---

## 5. Phase 3 — Branch & Scale (Weeks 21–28)

| # | Deliverable | Exit Criterion |
|---|---|---|
| P3-01 | Branch dashboards | Branch Manager, Branch Coordinator, Branch Finance, Partner Branch Admin views |
| P3-02 | Partner branch onboarding | Self-service application → Operator/Super Admin approval → scoped accounts |
| P3-03 | Territory management | Allocation UI, conflict detection, override with a reason, reallocation |
| P3-04 | City expansion | Cuttack, then Puri — each with seeded technicians, price book and service areas. **`[OPEN]` (`OD-DOC-08`):** `02` §3.1 places Cuttack in **Phase 2**, not here. Until the launch map is reconciled, no city may be announced to a partner with a phase attached |
| P3-05 | Coverage board | Service-area × service health with RED/AMBER/GREEN |
| P3-06 | Analytics | Funnel, SLA, revenue, margin, technician performance, branch P&L |
| P3-07 | Exports | CSV/XLSX for all finance and ops reports, audited |
| P3-08 | Scale-out | Managed Postgres, Redis separation, API horizontal scaling, CDN |
| P3-09 | Load test | Phase 3 profile passed (`13` §2.4) |
| P3-10 | Marketing | Campaigns, platform-funded coupons, content management, coupon analytics |
| P3-11 | Referral & repeat | "Book again" optimisation, favourite technicians |
| P3-12 | Multi-category launch | Cleaning + Plumbing live in 2 cities with distinct workflows |

### 5.1 Phase 3 Exit Criteria

| # | Criterion | Measure |
|---|---|---|
| E3-1 | 3 cities live and profitable at the contribution-margin level (which three depends on `OD-DOC-08`; `00` BO-2 assumes all six by Phase 3) | Finance |
| E3-2 | ≥ 90% fill rate in each launch service area | Report |
| E3-3 | The Phase 3 load profile passes on the scaled topology | Performance report |
| E3-4 | RTO ≤ 2 h demonstrated in a full DR drill | Runbook |
| E3-5 | A partner branch is live, with its own settlement and P&L | Live |
| E3-6 | Median rating ≥ 4.3 platform-wide; no branch below 4.0 | Report |
| E3-7 | Contribution margin positive at the platform level | Finance |

---

## 6. Phase 4 — Growth (Ongoing)

| Track | Items |
|---|---|
| **Geography** | Rourkela, Sambalpur, Berhampur; then other states (Jharkhand, West Bengal, Maharashtra) |
| **Partner branches** | A repeatable partner-branch playbook, onboarding kit and economics |
| **Categories** | Home salon, beauty parlour, AC servicing, pest control, carpentry, painting, CCTV, water purifier, moving `[OPEN]` — **`HOME_SALON` and `BEAUTY_PARLOUR` are listed here as Phase 4 while `06` §4.3/§4.4 place both inside the section titled "Launch Catalogue"**, with a Phase 2 decision deadline in `06` §8 `OD-06-01`, and `README` §1 calls them "additional categories". Registered as `OD-DOC-28`; neither text has been edited into the other (`DEC-07`). The count in this whole row is also unreconciled — 3 / 4 / 6 (`OD-DOC-27`) |
| **Monetisation** | Subscription packages (e.g. annual AC servicing), platform fee line, surge pricing `[PROPOSED]` |
| **Acquisition** | Referral programme, hyperlocal partnerships, WhatsApp campaigns, geo-targeted content |
| **Supply** | Technician training and certification programmes, skill-level verification, franchise technician outlets |
| **Platform** | Extract `reporting` and `notification` as services when the gates in `08` §8 are met |
| **Compliance** | SOC 2 / ISO 27001 readiness, e-invoicing readiness, TDS/Form 16A automation |

---

## 7. Cross-Phase Workstreams

These run continuously across all phases.

| Workstream | Activities | Owner |
|---|---|---|
| **Quality** | Test automation growth, defect triage, performance baselines, accessibility | QA Lead |
| **Security** | Dependency patching, access reviews, penetration tests, incident drills | Security Owner |
| **Data & analytics** | Event pipeline, read models, metric definitions, dashboards | Data Lead |
| **Content & localisation** | Odia/Hindi copy, workflow labels, notification templates | Growth + Product |
| **Operations readiness** | Technician onboarding playbooks, city launch checklists, support playbooks | Ops Lead |
| **Partner enablement** | Partner training material, onboarding kit, KYC support | Partner Ops |
| **Documentation** | Keep `Docs/` current with every rule change | Product Lead |

> **`[OPEN]` — `OD-DOC-35`.** "Content & localisation" is the only place in this document where Odia and
> Hindi appear, and a continuous workstream is not a milestone: no §3–§6 phase item, no §3.3, §4.1 or §5.1 exit criterion
> and no `29` §4 gate checks that a locale exists. `12` §8 i18n-03 states 100 % `or` and `hi` coverage as
> a launch requirement, and `13` §7 `US-07` cannot be met by translation alone because Odia also has to
> *render* (`OD-DOC-32`'s self-hosted subset face). The owner has directed English-first at design time
> with the other two locales after design and programming — `[REPORTED]`, and not yet attached to a
> phase. Until it is, the requirement is asserted but never scheduled and never verified. **What that
> direction does *not* defer:** the 30 % layout-expansion rule in `12` §8 i18n-03 binds the first English
> screen, so screens must be drawn without fixed-height text containers and without width-fitted labels
> from the start (`30` §4.1, §5.3). Naming the phase and adding the release check is the decision; this
> note is not it.

---

## 8. Release Cadence

| Cadence | Activity |
|---|---|
| Daily | Production deploy window (Tue–Thu, 10:00–16:00 IST) |
| Weekly | Iteration review; metric review (funnel, SLA, quality, finance); risk register review |
| Fortnightly | Steering review with the founder; roadmap re-plan; open decisions review |
| Monthly | Access review; dependency/infra review; backup restore drill; partner/branch performance review |
| Quarterly | Penetration test; DR drill; tax & compliance review; documentation audit |

---

## 9. Milestone Gate Checklist

Every phase gate requires all of the following before proceeding:

- [ ] All deliverables in the phase are complete and accepted by their owner
- [ ] The phase's exit criteria are met and evidenced
- [ ] No P0/P1 defects are open
- [ ] The performance and security suites pass
- [ ] The affected documents in `Docs/` are updated and consistent
- [ ] The risk register is updated; no new unmitigated high risk
- [ ] Financial reconciliation is clean for the period
- [ ] Stakeholder sign-off recorded in the charter approval table (`00` §14)

---

## 10. Dependencies & Critical Path

```
P0: Stack decision ─┬─> Monorepo scaffold ─> CI/CD ─> Environments
                    ├─> Auth + RBAC ─> Organization ─┐
                    └─> Catalog ──────────────────┴─> Booking ─> Payments ─> Workflow ─> Pricing ─> Commission ─> Settlement
                                                                    │
                                                                  Support (Call) ── in parallel from Phase 2
```

**Critical path**: stack decision → RBAC + organization → catalog → booking → payments → workflow → pricing → commission → settlement.

**Parallelisable**: the website design/content, the Control Center shell, the notification templates, the vendor onboarding (telephony, WhatsApp), the seed-data preparation, the technician onboarding programme.

**Rule RM-01** — Vendor account setup (payment gateway, telephony, WhatsApp, SMS, email) starts in **Phase 0**, because merchant KYC and template approval have a lead time measured in weeks and are on the critical path for Phase 2.

---

## 11. Risks to the Plan

| Risk | Impact | Mitigation |
|---|---|---|
| Payment merchant KYC delayed | Phase 1 slips | Start in Phase 0; keep a sandbox account for development |
| GST/tax treatment unclear | Phase 2 slips | Tax advisor engaged in Phase 0; a written opinion is a Phase 0 exit criterion |
| Thin technician supply at launch | Poor fill rate, bad first impression | Seed 50 technicians before launch; daily onboarding push; partner-branch recruitment |
| WhatsApp template approval delayed | Notification quality drops | SMS fallback is a first-class channel from Day 1 |
| Scope creep from new categories | Everything slips | The workflow engine is the enforcement mechanism — a new category is configuration; any category needing code is a scope change, not a task |
| Team ramp-up time | Phase 1 slips | The monorepo + CI + documented contracts make onboarding cheap; the `Docs/` set is the ramp-up curriculum |

---

## 12. Definition of Done (for every task)

A task is done when:

1. The code is merged, reviewed and behind a feature flag where applicable.
2. Tests are written at the appropriate level and pass.
3. The OpenAPI contract is updated (if the API changed) and the clients regenerated.
4. Mocks, fixtures and seed data are updated.
5. Logs, metrics and audit events exist for the new behaviour.
6. The affected document in `Docs/` is updated.
7. The acceptance criteria in the ticket are demonstrably met.
8. The feature is enabled in staging and verified.

---

## 13. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| OD-RM-01 | Are the phase durations realistic for the planned team, or should the team be increased? | Leadership | Phase 0 |
| OD-RM-02 | Should Cuttack launch in Phase 3 or immediately after Bhubaneswar proves the model? | Founder + Ops | Phase 2 |
| OD-RM-03 | What is the target date for the first city go-live? | Founder | Phase 0 |
| OD-RM-04 | Do we launch with **one** category (appliance repair), **two**, or **three**? — `21` asks the same question in the same words and carries the recommended answer (two: appliance repair + cleaning). Phase 1, Phase 2 and the seed-data volume in `18` §2 all scale with this number, so it must close before Phase 1 is planned, not during it. | Founder + Product | Phase 0 |
| OD-RM-05 | Is the partner-branch model piloted in Phase 3 or held until Phase 4? | Founder | Phase 2 |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.5 | 2026-10-21 | Product Lead + Eng Lead (platform-mode pass) | Phase 0 gained **`P0-15`** — the mode row, the transition history and the `record_origin` marker exist **before the first transactional migration**, marked `[PROPOSED]` and blocked by `OD-DOC-38`, `OD-DOC-40` and `OD-DOC-41`. The sequencing is not a preference: an origin column can be back-filled onto rows whose provenance is still recorded, but not onto rows written before the column existed, where the only honest value is unknown. Putting this work in Phase 1 guarantees a guess; guessing in a money schema is what `ADR-015` exists to prevent. **No phase, date, dependency or exit criterion was altered, and nothing here is a commitment that the six-month plan absorbs the new work** — it does not, and `OD-COM-13` prices the question. | Phase 0 (§4) |
| 1.4 | 2026-10-21 | Product Lead (i18n and palette pass) | §7 gained an `[OPEN]` note on the **Content & localisation** workstream for `OD-DOC-35`: the owner's English-first direction is `[REPORTED]` and unphased, Odia and Hindi appear nowhere else in this document, and a continuous workstream is not a milestone — no §3–§6 phase item, no §3.3/§4.1/§5.1 exit criterion and no `29` §4 check verifies that a locale exists, while `12` §8 i18n-03 states 100 % `or`/`hi` coverage as a launch requirement. The note separates what the direction legitimately defers (translation production, until a phase names it) from what it must not (the 30 % expansion tolerance, which binds the first English screen). **No phase, duration, milestone, exit criterion, date or owner was changed, and no new `OD-RM-*` row was added** — `DEC-01` puts this question in `21` §7, and §13 deliberately still carries only `OD-RM-01`…`05`. | §7, header, Revision History |
| 1.3 | 2026-10-21 | Product Lead + Engineering Lead (design-system and asset pass) | Three rows annotated; **no phase, milestone, duration, exit criterion or dependency changed**. **P0-10** "Design system + tokens" is marked `[OPEN]` because it presumes two undecided things: `OD-12-01` has never chosen the design tool, so "a component library in Figma" states as fact what is still a recommendation, and the token **values** themselves are `PROPOSED` in `30` §3–§7 pending `OD-DOC-30`/`31`/`32`. The row now names `33` §3–§4 as the screen list it must cover, `33` §5 as the eight components with no designed non-happy state, and `26` §4.1 / `19` `R-45` as the payment this gate feeds. **P0-09**, **P2-02** and **§6** carry the category-count conflict (`OD-DOC-27`: 3 here, 4 in P2-02, 6 in `06` §4, 2 in `OD-RM-04`) and the salon/beauty launch-versus-Phase-4 conflict (`OD-DOC-28`). Both sides annotated per `DEC-07`; none is decided. | §2 P0-09, §2 P0-10, §4 P2-02, §6, header, Revision History |
| 1.2 | 2026-10-21 | Product Lead + Engineering Lead | Audit pass 3. §1 now carries the calendar warning: Phases 0–3 total **28 weeks** while `26` §4 commits a **six-month** delivery, and no document reconciles them — so until `OD-DOC-08`/`OD-RM-03`/`OD-COM-11` close, **nothing in this document may be quoted as a delivery commitment**. Registered rather than averaged, per `DEC-07`. §5: `P3-04` (Cuttack) marked `[OPEN]` because `02` §3.1 places Cuttack in Phase 2 and this document places it in Phase 3; `E3-1` qualified, because "3 cities" names none of them and `00` BO-2 assumes all six by Phase 3. §13: `OD-RM-04` restated as one/two/three to match the register's wording (`OD-DOC-09`). | §1, §5, §13 |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Cross-referenced the audit additions: the city activation gate, the two-layer status model, and the open-decision impact map. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
