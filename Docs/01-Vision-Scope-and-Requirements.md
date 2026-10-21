# 01 — Vision, Scope & Requirements

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-01 |
| Version | 1.2 |
| Status | Approved for Design & Development |
| Owner | Product Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `00-Project-Charter` |

---

## 1. Personas

Every requirement in §4 traces to at least one persona.

### P1 — Customer (Ramesh, 38, Bhubaneswar)
Has a refrigerator not cooling. Books from the AmmPal Service app at 9pm because that's when the
problem is noticed. Wants a firm price and a definite arrival time.

| Attribute | Detail |
|---|---|
| Goals | Find a trusted technician fast; know the price upfront; know when someone arrives; get it fixed |
| Frustrations | "Prices on call are different from the app"; technicians don't call back; no accountability |
| Success | Job completed on first visit, invoice matches quote, technician rated ≥ 4 |
| Channels | Mobile app (primary), website, toll-free call |
| Key journeys | Search → Compare → Book → Track → Pay → Review → Support |

### P2 — Service Technician (Suresh, 31, Cuttack)
AC repair specialist. 180 completed jobs, 4.6 rating. Wants a steady flow of nearby jobs and
predictable weekly income.

| Attribute | Detail |
|---|---|
| Goals | Consistent job flow within travel radius; clear instructions; fast, reliable payment; visible reputation |
| Frustrations | Jobs from the wrong area; unclear earnings maths; delayed settlements; no-show customers |
| Success | ≥ 12 jobs/week, ≥ ₹8k weekly net earnings, rating ≥ 4.5 |
| Channels | AmmPal Partner app |
| Key journeys | Onboard → Verify → Set skills → Accept job → Travel → Execute → Invoice → Settle |

### P3 — Branch Manager (Priya, 36, Bhubaneswar branch OD-BBI-001)
Runs the Bhubaneswar operation. Owns technician supply, SLA and local complaints.

| Attribute | Detail |
|---|---|
| Goals | Fill every booking; keep technicians busy; keep the rating up; resolve escalations fast |
| Frustrations | Manual allocation of unclaimed jobs; no coverage visibility; disputes with platform on commission |
| Success | Fill rate ≥ 95%, median accept ≤ 6 min, complaint rate < 2% |
| Channels | Control Center (branch-scoped) |
| Key journeys | Monitor feed → Intervene on SLA → Manage roster → Review quality → Reports |

### P4 — Partner Branch Admin (Sanjay, 41, platform-partner branch, Puri)
Runs an authorised partner territory. Manages their own technician team and local price customisation.

| Attribute | Detail |
|---|---|
| Goals | Operate the territory profitably; control local pricing within bands; keep technicians earning |
| Frustrations | Platform rules unclear; settlement disputes; slow support resolution |
| Success | Positive unit economics per job; ≥ 90% on-time settlement; ≥ 4.2 local rating |
| Channels | Control Center (partner-branch-scoped) |
| Key journeys | Manage team → Set local price → Monitor jobs → Raise query → Settle |

### P5 — Operator (Anil, 29, Platform Ops)
Onboards partners and branches, manages booking operations, resolves operational issues.

| Attribute | Detail |
|---|---|
| Goals | Fast partner onboarding; no unassigned bookings; fast issue resolution; clean data |
| Frustrations | Manual verification; scattered data; no single operational view |
| Success | Partner approval < 48 h; unassigned booking rate < 1% |
| Channels | Control Center (central-scoped) |
| Key journeys | Approve partner → Allocate territory → Monitor feed → Resolve issue |

### P6 — CCO (Meera, 27, Customer Support)
Handles toll-free calls and tickets. Answers in Odia, Hindi and English.

| Attribute | Detail |
|---|---|
| Goals | Resolve at first contact; protect the rating; record everything accurately |
| Frustrations | No customer context on call; missing call recordings; repeat tickets |
| Success | FCR ≥ 70%, CSAT ≥ 4.3, AHT ≤ 6 min |
| Channels | Support console + telephony |
| Key journeys | Receive call → Verify → Resolve → Ticket → Follow-up → Close |

### P7 — Accountant (Suresh Kumar, 40, Finance)
Owns commission, settlement, GST and reconciliation.

| Attribute | Detail |
|---|---|
| Goals | Every rupee traceable; settlements accurate; GST filings correct; no manual spreadsheets |
| Frustrations | Mismatched gateway settlements; manual invoice correction; ambiguous commission base |
| Success | 100% settlement auto-match; zero post-issue edits; on-time filing |
| Channels | Control Center (finance-scoped) |
| Key journeys | Accrue → Generate statement → Issue invoice → Reconcile → Dispute → Close |

### P8 — Super Admin (Founder's operations lead, 45)
Owns master data, permissions and global configuration.

| Attribute | Detail |
|---|---|
| Goals | Correct master data; least-privilege access; safe global changes; auditability |
| Frustrations | Duplicate master data; over-broad roles; untracked config changes |
| Success | 100% config changes audited; zero orphan records; quarterly access review |
| Channels | Control Center (global scope) |
| Key journeys | Add master data → Assign role & scope → Monitor platform → Audit |

---

## 2. Product Principles

| # | Principle | Implication in design |
|---|---|---|
| PP-1 | **Location-first** | Location resolution happens before service, technician, or price is shown |
| PP-2 | **Price is a promise** | The quote at booking is the invoice at completion, by construction (snapshot) |
| PP-3 | **Config over code** | A new service category = workflow template + price book + tax rule, not a release |
| PP-4 | **Every state is visible** | Customers, technicians, branches and finance see the same booking status |
| PP-5 | **Automation with human override** | Rules act automatically; authorised humans can override — and every override is logged |
| PP-6 | **Nothing leaves the ledger** | Cash, commission and settlement are always reconcilable to a booking |

---

## 3. Scope Model

```
                            ┌─────────────────────────────────────────┐
                            │           PLATFORM (Central)            │
                            │  Super Admin · Admin · Operator · CCO  │
                            │  Accountant · Partner Support · Mktg Ops│
                            └───────────────┬─────────────────────────┘
                                            │ owns configuration & rules
        ┌───────────────────────────────────┼───────────────────────────────────┐
        │                                   │                                   │
┌───────▼────────┐              ┌───────────▼──────────┐            ┌───────────▼──────────┐
│ COMPANY BRANCH │              │ COMPANY BRANCH       │            │ PARTNER BRANCH      │
│ OD-BBI-001 HQ  │              │ OD-CTC-002 Cuttack   │            │ PT-OD-0042 (Puri)   │
└───────┬────────┘              └───────────┬──────────┘            └───────────┬──────────┘
        │                                   │                                   │
   Zone → Service Area              Zone → Service Area              Zone → Service Area
        │                                   │                                   │
   ┌────▼─────┐                       ┌────▼─────┐                       ┌────▼─────┐
   │ Technician│                      │Technician│                       │Technician│
   │ (Partner) │                      │ (Partner)│                       │ (Partner)│
   └──────────┘                       └──────────┘                       └──────────┘
        ▲                                   ▲                                   ▲
        └───────────────────────────────────┴───────────────────────────────────┘
                                            │
                                    ┌───────┴────────┐
                                    │    CUSTOMER    │
                                    │ App · Web · Tel│
                                    └────────────────┘
```

**Layer rules**

| Layer | Owns | Cannot |
|---|---|---|
| Platform | Master data, price bands, commission %, tax config, roles, workflow templates, coupons policy, partner approval | Execute a job |
| Branch | Territory, technician roster, service areas, local price customisation (in band), local coupons, local ops | Change master data, price bands, commission %, roles |
| Service area | Technician availability, job feed, capacity | Pricing, territory |
| Technician | Execution, parts, invoice, evidence | Set price, accept out-of-area jobs |

---

## 4. Functional Requirements

Legend: **M** = Must (v1.0) · **S** = Should (Phase 3) · **C** = Could (Phase 4)

### 4.1 Identity, Access & Organisation — FR-ID

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-ID-01 | Customer registers via mobile OTP; social login (Google, Facebook) optional | M | OTP verified session in ≤ 60 s; OTP rate-limited 5/hour/number |
| FR-ID-02 | Technician registers via mobile OTP, submits KYC + identity/address documents, sets skills, categories and service areas | M | Document upload with type + expiry; incomplete profile cannot go live |
| FR-ID-03 | Partner branch registers with legal entity, GSTIN (optional by state), operating cities, and territory proposal | M | Cannot be activated without Operator/Super Admin approval |
| FR-ID-04 | Central staff accounts are created by Super Admin / Admin only | M | No self-registration for central roles |
| FR-ID-05 | Every account has a **scope** (GLOBAL / STATE / BRANCH / SERVICE_AREA) restricting data visibility | M | API layer enforces scope; cross-scope read/write returns `403 SCOPE_VIOLATION` |
| FR-ID-06 | RBAC permissions are granular (resource + action), assignable per role, overridable per user | M | Permission check is server-side on every endpoint |
| FR-ID-07 | Technician document expiry triggers a grace period, then automatic deactivation | S | Grace = 15 days; deactivation blocks new job acceptance, existing jobs continue |
| FR-ID-08 | Branch allocation is performed by Operator or Super Admin, with a territory conflict check | M | Overlapping allocation blocked unless explicitly overridden with a logged reason |
| FR-ID-09 | All authentication events (login, logout, OTP, failed attempt, lockout) are audited | M | Retention = 24 months |
| FR-ID-10 | Account lockout after 5 failed attempts; admin unlock with audit | M | 15-minute cooldown |

### 4.2 Catalog & Discovery — FR-CAT

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-CAT-01 | Catalog is a 3-level hierarchy: Category → Service → Service Variant (e.g. AC Repair → Split AC → 1.5 Ton) | M | Every booking stores all three IDs |
| FR-CAT-02 | Each service carries a **workflow template** defining required steps, checklist, evidence, SLA timers | M | See `06` |
| FR-CAT-03 | Availability is location-aware: a service is offered only where ≥ 1 active technician with the skill and an active service area exists | M | API never offers a service with zero eligible technicians |
| FR-CAT-04 | Discovery returns technicians ordered by a configurable score (distance, rating, completion rate, response rate) | M | Rank changes are explainable; weights are admin-configurable |
| FR-CAT-05 | Technician card shows name, photo, skills, rating, completed jobs, price range, ETA, verified badges | M | Matches `04` §3.2 |
| FR-CAT-06 | Category browsing, service detail pages, and price-range display are available on web and app | M | — |
| FR-CAT-07 | Services can be paused per service area without a deployment | S | Paused service is hidden from search and new bookings |
| FR-CAT-08 | Multi-language service content (Odia, Hindi, English) | M | Content per category/service per locale |

### 4.3 Booking & Scheduling — FR-BK

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-BK-01 | Booking captures customer, address (with geo-pin), service, variant, slot, technician, price snapshot, coupon | M | Booking ID issued on success |
| FR-BK-02 | Address is geo-coded and snapshotted (lat/lng) so later map changes do not affect historical jobs | M | `booking.address_geo` immutable after creation |
| FR-BK-03 | Slot is offered from the technician's availability calendar, within the service area | M | No slot offered outside coverage |
| FR-BK-04 | Price breakdown is computed and frozen at booking (labour, visiting, parts estimate, discounts, GST, advance, balance) | M | See `07` §3 |
| FR-BK-05 | Coupons are validated server-side at booking: category, service, branch, dates, min/max discount, per-technician usage, per-customer usage, opt-in | M | Rejected coupon returns a specific reason code |
| FR-BK-06 | Advance payment is optional and configured per service/category/branch | M | Booking can complete with zero advance |
| FR-BK-07 | Technician has an acceptance window (default 5 min for direct assign, 10 min for open feed) | M | Auto-expire → next candidate |
| FR-BK-08 | Booking can be rescheduled subject to policy; a change fee may apply | M | Fee = 0 before service start (per `04` §6) |
| FR-BK-09 | Customer can request a technician change; eligibility and possible charge are computed | M | See `05` §6 (use case C) |
| FR-BK-10 | Cancellation by customer or technician applies policy + penalty | M | Penalty and refund computed, never hand-entered |
| FR-BK-11 | Booking events emit notifications on every state change per channel policy | M | See `11` §4 |
| FR-BK-12 | Live technician location is broadcast to the customer while `EN_ROUTE` / `STARTED` | M | WebSocket + poll fallback |
| FR-BK-13 | Booking cannot be created for a paused service, unverified technician, or out-of-area address | M | Guarded server-side |
| FR-BK-14 | Rebooking a completed job creates a new booking linked to the original | S | `parent_booking_id` populated |

### 4.4 Job Execution — FR-JOB

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-JOB-01 | Technician starts a job only after customer OTP confirmation | M | OTP verified event recorded with timestamp |
| FR-JOB-02 | Service-specific checklist must be completed before the job can be marked complete | M | Checklist from the workflow template |
| FR-JOB-03 | Parts used are captured with part name, qty, unit price, margin basis | M | Parts are excluded from commission base (unless policy says otherwise) |
| FR-JOB-04 | Photo evidence (before/after) is required for configured categories | M | Min 1 photo per configured evidence point |
| FR-JOB-05 | Technician generates the final invoice in-app; it reconciles to the booking price snapshot plus adjustments | M | Discrepancy > ₹0 must be explained |
| FR-JOB-06 | Remaining payment is collected via gateway (UPI/card/netbanking) with a payment link fallback | M | Payment recorded against the booking, never as a loose transaction |
| FR-JOB-07 | Job can be marked complete only after all mandatory checklist items and evidence are present | M | Blocked otherwise |
| FR-JOB-08 | Warranty period per category is recorded and shown to the customer | S | Stored on the booking |
| FR-JOB-09 | Technician performance score is recalculated on job completion | M | See `FR-QA-04` |

### 4.5 Support & Service Recovery — FR-SUP

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-SUP-01 | Toll-free number with multi-language IVR (Odia, Hindi, English) and reason selection | M | See `05` §3 |
| FR-SUP-02 | Smart routing uses caller number, customer profile, active bookings, detected city/branch, language, issue type, agent skill and availability | M | Agent sees the customer context on screen-pop |
| FR-SUP-03 | CCO can verify identity via OTP before sensitive changes | M | Logged |
| FR-SUP-04 | Six call use cases are supported: New booking, Existing booking support, Change technician, Payment/invoice/refund, Complaint/service quality, Partner/technician support | M | Each follows the documented step sequence |
| FR-SUP-05 | Every call creates a call log with ID, time, duration, recording reference, linked customer and ticket | M | Recording retained per policy |
| FR-SUP-06 | Support ticket with category, priority, assignment and status lifecycle | M | Priority SLA timers start on creation |
| FR-SUP-07 | Notifications on ticket create/update/close via SMS/WhatsApp/email/app | M | — |
| FR-SUP-08 | Supervisor dashboard: call volume, queue time, agent performance, missed calls and callbacks, CSAT | M | Refresh ≤ 5 min |
| FR-SUP-09 | Complaints escalate to Branch Manager automatically when unresolved at SLA | M | Escalation chain defined per complaint category |
| FR-SUP-10 | Rework/refund can be arranged from a complaint per policy | M | Refund links to the original booking's payment transaction |

### 4.6 Pricing, Billing & Settlement — FR-FIN

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-FIN-01 | Platform sets base labour price + min/max band + default for a service per state/city/zone | M | Out-of-band partner price rejected server-side |
| FR-FIN-02 | Partner/branch may set a custom labour price within the band and confirm the visiting charge | M | Band violation returns `PRICE_OUT_OF_RANGE` |
| FR-FIN-03 | Visiting charge is platform-set (fixed or range); optional diagnostic charge supported | M | — |
| FR-FIN-04 | Spare-parts pricing follows platform rules: MRP or allowed margin, with min/max | M | — |
| FR-FIN-05 | Discounts are funded by **platform**, **partner** or **shared**; each funding type has a defined commission-base effect | M | See `07` §5 |
| FR-FIN-06 | GST is computed on the customer invoice per place of supply and per branch registration | M | Tax is itemised per line |
| FR-FIN-07 | Commission is computed on **eligible labour only** at the configured rate (default 15%) | M | Commission base explicitly excludes visiting, parts, transport, customer GST |
| FR-FIN-08 | Commission is accrued per completed job into a commission ledger | M | Ledger entries are immutable and booking-referenced |
| FR-FIN-09 | Weekly settlement: Mon–Sun accrual → statement issued following Monday → payment due within 7 calendar days | M | Statement is booking-wise and immutable |
| FR-FIN-10 | Settlement invoice is issued to the partner with applicable GST | M | Distinct from the customer invoice |
| FR-FIN-11 | Payment receipt reconciliation matches gateway settlements to booking payments | M | Auto-match rate reported |
| FR-FIN-12 | Disputes and adjustments are recorded as credit/debit notes against a settlement, never as edits | M | Full audit trail |
| FR-FIN-13 | Branch-wise revenue, commission and margin reports are available | M | — |
| FR-FIN-14 | Commission rate is configurable and versioned; historical jobs always use the rate captured at completion | M | Version pinned on the ledger entry |

### 4.7 Quality, Ratings & Penalties — FR-QA

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-QA-01 | Customer rates the technician after completion (stars + text + category attributes) | M | One rating per booking |
| FR-QA-02 | Technician performance score computed from rating, completion rate, punctuality, acceptance speed, complaints | M | Documented weights, admin-configurable |
| FR-QA-03 | Customer score computed from cancellations, no-shows, disputes | M | Used for policy decisions |
| FR-QA-04 | Penalties apply for late cancellation and no-show, with configured amounts | M | Penalty ledger, never ad-hoc |
| FR-QA-05 | Scores affect technician visibility/ranking and future booking eligibility | M | Ranking weight configurable |
| FR-QA-06 | Auto score recalculation runs on relevant events (completion, cancellation, complaint) | M | Idempotent, replayable |

### 4.8 Compliance & Tax — FR-CMP

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-CMP-01 | Platform GST registration per operating state; registration matrix maintained by Super Admin | M | Used to select the tax treatment |
| FR-CMP-02 | Place of supply = customer address state, not branch state | M | Recorded per booking |
| FR-CMP-03 | Platform commission invoice includes GST as per law | M | 18% illustrative; rate is configuration |
| FR-CMP-04 | Technician GST treatment depends on individual vs. registered business | M | Per-partner configuration |
| FR-CMP-05 | Every invoice, statement and credit note is number-sequenced, immutable and retrievable | M | Gapless per entity + fiscal year |
| FR-CMP-06 | Financial records are tamper-evident (hash-chained audit log) | M | See `13` §5 |

### 4.9 Reporting & Analytics — FR-RPT

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-RPT-01 | Booking funnel: search → view → book → accept → start → complete → pay → review | M | Conversion at each step |
| FR-RPT-02 | SLA dashboards: acceptance time, arrival time, job duration, complaint SLA | M | Filterable by branch/zone/category/date |
| FR-RPT-03 | Revenue, commission, payout and margin reports by branch/partner/category/period | M | — |
| FR-RPT-04 | Technician leaderboard and underperformers list | M | — |
| FR-RPT-05 | Support analytics: call volume, AHT, queue time, FCR, CSAT, ticket backlog | M | — |
| FR-RPT-06 | Coverage report: service areas with fewer than N eligible technicians | M | N configurable (default 3) |
| FR-RPT-07 | Export to CSV/XLSX for all finance and ops reports | M | — |
| FR-RPT-08 | Every report honours the viewer's scope | M | Central vs branch views differ |

### 4.10 Notifications & Platform Services — FR-NTF

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-NTF-01 | Channels: FCM push, SMS, WhatsApp, email, in-app | M | Channel preference honoured |
| FR-NTF-02 | A notification template registry with variables, per-channel content and versioning | M | Templates localisable per language |
| FR-NTF-03 | All notifications are queued with retry and dead-letter handling | M | At-least-once delivery |
| FR-NTF-04 | Deep links from push/WhatsApp open the exact relevant screen | M | — |
| FR-NTF-05 | Notification preferences per customer (per category) | S | Transactional messages exempt |
| FR-NTF-06 | WhatsApp templates are pre-approved business-initiated messages | M | Free-form only within 24-hour customer service window |

### 4.11 Platform Mode and Data Lifecycle — FR-MODE

Added on the owner's instruction of 2026-10-21 (*"another think need that mode of platform like
'Testing' and 'Production' … default mode is Test, when make production then will be need super admin
email OTP verification … production mode data not able to delete from database"*). Recorded as
`[PROPOSED]`: `38` is the specification, `22` ADR-026 is the decision record, and this is a **v1.0
requirement addition** — under §8 it needs a charter amendment (`00` §14 approval) and under
`26` §3.2 it is an item outside the initial-scope list until the agreement is changed in writing.
**No part of it is implemented** (`22` ADR-025-02).

| ID | Requirement | P | Acceptance |
|---|---|---|---|
| FR-MODE-01 | The platform runs in exactly one of two modes, `TESTING` or `PRODUCTION`, held as server-side database state — not an environment variable, a feature flag or a client setting | M | `38` §3 PM-01…PM-04; any code that reads the mode from anywhere but `platform.platform_mode` is a defect |
| FR-MODE-02 | The default mode is `TESTING`; production infrastructure resolving to `TESTING` without a recorded, time-boxed bootstrap exception refuses staff mutations and alerts on-call | M | `38` §10; asserted by the `16` §5 pipeline and a `29` §4 gate item |
| FR-MODE-03 | Promotion to `PRODUCTION` requires a freshly verified email OTP to the super-admin address of record, a non-empty reason and a second-account acknowledgement; demotion requires at least the same | M | `38` §5 — `[OPEN]`: `OD-DOC-42`, and the email provider is **not procured** (`24` P-06, `24` §15 A-06, `OD-MAIL-01`) |
| FR-MODE-04 | In `PRODUCTION`, operator-initiated hard deletes, truncates and data-destructive DDL are refused; soft delete (`03` §3.2) and the code-defined retention purge (`09` §6) continue to work | M | `38` §6; `403 MODE_PROTECTED` (`10` §6.1) |
| FR-MODE-05 | Every inserted row records its origin, `TEST` or `LIVE`; reports, settlements and invoices read `LIVE` only unless a labelled diagnostic run opts in | M | `38` §8.1/§8.2; `09` Rule DB-30 |
| FR-MODE-06 | `TESTING` must not consume the live statutory document number series | M | `38` §8.3 — `[OPEN]`: `OD-DOC-41`, because `FR-CMP-05` gaplessness plus `ADR-015` immutability means a test invoice cannot be deleted without breaking the series |
| FR-MODE-07 | The effective mode is displayed on every staff surface and export header, and `TESTING` shows a persistent, non-dismissible indicator on customer and technician surfaces | M | `38` §9; no component is named here (`37` `CA-00`) |
| FR-MODE-08 | Every mode transition is durably audited — an append-only transition row plus a hash-chained audit event | M | `38` PM-07; `09` §4.15, `13` §5.1 |

> **Deliberately absent from this family.** Whether statutory DPDP erasure is permitted in
> `PRODUCTION` (`OD-DOC-40`), which factor the ceremony uses (`OD-SEC-01`, `OD-DOC-42`), at which layer
> the guard is enforced (`OD-DOC-43`) and where the control sits in the Control Center (`OD-DOC-44`,
> blocked by `OD-10-06`). Writing those in here would be an invented approval (`27` §4).

---

## 5. Non-Functional Requirements (Summary)

Full detail in `13-Non-Functional-Requirements.md`.

| Area | Target |
|---|---|
| Availability | 99.5% monthly (API + customer surfaces) |
| API latency | p95 < 400 ms; booking search p95 < 800 ms; track endpoint p95 < 200 ms |
| Scale (Phase 3) | 50k registered customers · 5k technicians · 100k bookings/year |
| RPO / RTO | RPO ≤ 15 min · RTO ≤ 2 h |
| Payment compliance | PCI-DSS via gateway; no card data stored |
| Data residency | India |
| Accessibility | WCAG 2.1 AA for web surfaces |
| Localisation | Odia, Hindi, English |
| Privacy | DPDP Act 2023 aligned; consent, purpose limitation, retention, erasure |

---

## 6. Out of Scope for v1.0

See `00` §5.2. Restated here as explicit non-goals to protect scope:

AI dynamic pricing · centralised spare-parts warehousing · third-party marketplace syndication ·
multi-currency · self-service partner-branch onboarding · ERP replacement · in-house logistics.

---

## 7. Traceability

| Requirement Group | Persona(s) | Design Document | Data Model |
|---|---|---|---|
| FR-ID | P3, P4, P5, P8 | `03`, `08` §4 | `09` §3.1–3.3 |
| FR-CAT | P1, P2 | `06` | `09` §3.4 |
| FR-BK | P1, P2, P3, P5 | `04`, `08` §5 | `09` §3.5–3.6 |
| FR-JOB | P1, P2 | `04` §5, `06` | `09` §3.7 |
| FR-SUP | P1, P2, P6 | `05` | `09` §3.9 |
| FR-FIN | P3, P4, P7 | `07` | `09` §3.8, §3.10 |
| FR-QA | P1, P2, P3 | `04` §7 | `09` §3.11 |
| FR-CMP | P7 | `07` §6, `19` | `09` §3.10 |
| FR-RPT | P3, P4, P6, P7 | `12` §5 | `09` §3.12 |
| FR-NTF | P1, P2, P6 | `11` | `09` §3.13 |
| FR-MODE | P5, P8 | `38`, `12` §6 | `09` §4.15 |

---

## 8. Change Control

Requirements are numbered and versioned. Any change to a **Must (M)** requirement in v1.0 requires
a charter amendment (`00` §14 approval). Changes to Should/Could are re-prioritised per release.

**FR-MODE is an addition, not a change**, and it is treated as the more consequential of the two: it
asks for a new state machine, a new authentication ceremony, a change to what `delete` means in the
permission model, and new tables — while `OD-DOC-38` still gates the backend it would be written for.
It inherits both approval routes above (`00` §14, `26` §3.2) and nothing in §4.11 may be built before
they are completed.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.2 | 2026-10-21 | Product Lead + Founder (platform-mode pass) | The owner's 2026-10-21 instruction asked for a **Testing/Production mode**: all data saved in the database, default Test, promotion to Production requiring super-admin **email OTP verification**, and production data **not deletable**. It is recorded verbatim in `38` §1 and, per `DEC-03`, as a requirement rather than an approval. **§4.11 added — `FR-MODE-01`…`08`, eight rows, all M, all `[PROPOSED]`**: mode is server-side database state; default `TESTING` fails closed; promotion needs OTP + reason + second-account acknowledgement; `PRODUCTION` refuses class-A operator deletes while soft delete (`03` §3.2) and the code-defined purge (`09` §6) continue; every row records a `TEST`/`LIVE` origin; `TESTING` must not consume the live statutory series; the mode is displayed on every staff surface; every transition is durably audited. A **deliberately-absent** note names the four things this family does *not* decide (`OD-DOC-40`/`41`/`42`/`43`/`44`), and §7 gained the `FR-MODE` traceability row. §8's change-control paragraph now says what a requirement **addition** costs: `00` §14 charter approval plus a written change to `26` §3.2 — an owner sentence describing a feature is neither. **No requirement was deleted, renumbered or re-marked; the FR total moved 91 → 99 by counting, not by asserting.** | §4.11 (new), §7, §8 |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Added the `[CONFIRMED] / [PROPOSED] / [OPEN] / [DEPENDENT] / [IMPLEMENTED]` status vocabulary; added requirements for legal-entity separation, serviceability reason codes, add-ons, eligibility rules, spare-parts catalogue, estimated duration, emergency/after-hours charge, gateway fee, coupon reservation/release, quotes, customer approvals, callbacks, call events, WhatsApp conversations, idempotency keys, waitlist and MFA; corrected the AS-3 pointer to the tax-decision register. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
