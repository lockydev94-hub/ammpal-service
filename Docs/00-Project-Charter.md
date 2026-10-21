# 00 — Project Charter

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-00 |
| Version | 1.2 |
| Status | Approved for Design & Development |
| Sponsor | Founder / Platform Owner |
| Owner | Product & Engineering Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Project Label | `AMMPAL-SERVICE-PROJECT-MASTER` |

---

## 1. Executive Summary

AmmPal Service is a **technology platform** that operates a multi-service home-services marketplace
connecting customers with verified, location-scoped service technicians, organised through a
central platform and a distributed branch network.

The platform's primary business is **home appliance repair**, extended to cleaning, home salon,
beauty parlour, plumbing, electrical and other categories. Launch is **Odisha-first**
(Bhubaneswar as HQ), with a designed path to multi-state operation via both **company-owned
branches** and **platform-partner-owned branches**.

The platform captures value through a **commission on eligible labor** (default 15%), and pays
technicians through a **weekly settlement cycle** with GST-compliant commission invoices.

This charter defines *why* the platform exists, *what* it will deliver, and *how success will be
measured*. It is the reference against which scope changes are evaluated.

---

## 2. Problem Statement

Home services in tier-2/tier-3 Indian cities are fragmented and low-trust:

| Problem | Consequence | AmmPal's Response |
|---|---|---|
| No reliable way to find a good technician near you | Customers rely on word-of-mouth; quality is a lottery | Location-based discovery with verified profiles, ratings, completed-job counts and transparent price ranges |
| No price transparency | Overcharging, no comparison basis | Platform-set min/max/default price bands; partner customisation only **within** the band; customer sees final price breakdown before booking |
| No visibility after booking | Customers chase technicians for ETA and status | Booking state machine, WebSocket live tracking, SMS/WhatsApp/FCM notifications, toll-free support |
| No accountability | Complaints go nowhere; poor technicians keep working | Ratings, technician performance score, customer score, penalties, auto-scoring, SLA-driven escalation |
| Technicians have unstable work | Income is irregular, no guarantees, no reputation | Verified onboarding, skill-based job feed, in-app wallet, guaranteed weekly settlement, earnings ledger |
| Central operations cannot scale | Every city needs a person; work is unmanaged | Branch/zone/service-area hierarchy, location-scoped dashboards, location-scoped job distribution, multi-tenant data model |
| Manual, error-prone finance | Commission leakage, tax mistakes, no reconciliation | Automated price snapshot per booking, commission ledger, weekly settlement statements, GST treatment per place of supply, dispute handling, audit trail |

---

## 3. Vision, Mission, Values

### 3.1 Vision
> *To become the most trusted home-services platform in Eastern India — where a customer can book
> any home service in under two minutes, and a technician is guaranteed a fair, on-time payment.*

### 3.2 Mission
> *To build a location-intelligent, multi-service operations platform that gives customers
> dependable home services, technicians dependable work and income, and operators complete
> visibility — across every branch, in every city, in every state we operate in.*

### 3.3 Operating Values

| # | Value | Operational Meaning |
|---|---|---|
| V1 | **Location is truth** | Every booking, technician, price, invoice and settlement resolves to a physical location (state → city → zone → service area). Nothing is "global" unless it truly is. |
| V2 | **Trust is engineered** | Verification, ratings, penalties, SLA timers and audit logs are system features, not manual processes. |
| V3 | **Money is transparent** | The customer sees the price breakdown before paying. The technician sees exactly how earnings were computed. Finance sees the same ledger. |
| V4 | **One platform, many branches** | Branch autonomy never compromises platform consistency. Configuration is centralised; execution is local. |
| V5 | **Design for the next state** | Every module is built with a documented extraction path, so scale never forces a rewrite. |

---

## 4. Objectives

### 4.1 Business Objectives

| ID | Objective | Target |
|---|---|---|
| BO-1 | Establish a functioning marketplace in Bhubaneswar | Launch 3 categories (Appliance Repair, Cleaning, Plumbing) by end of Phase 2 `[OPEN]` — the **3** here, the **4** in `17` P2-02, the **6** launch families in `06` §4.1–§4.6 and **2** recommended by `OD-RM-04` are four answers to one question; registered as `OD-DOC-27`, and no side has been edited into another (`DEC-07`) |
| BO-2 | Extend to Odisha's 6 priority cities | Bhubaneswar, Cuttack, Puri, Rourkela, Sambalpur, Berhampur by end of Phase 3 |
| BO-3 | Achieve service quality parity across branches | Platform-wide median rating ≥ 4.3 / 5 with no branch below 4.0 |
| BO-4 | Become the default choice for appliance repair in Odisha | ≥ 25% of monthly category bookings from repeat customers by end of Phase 3 |
| BO-5 | Prove partner-branch expansion viability | ≥ 1 platform-partner branch live with positive unit economics by end of Phase 4 |
| BO-6 | Reach operational profitability | Contribution margin positive at platform level by end of Phase 4 |

### 4.2 Product Objectives

| ID | Objective | Measure |
|---|---|---|
| PO-1 | Fastest booking path in category | Customer books in ≤ 3 minutes on mobile app; ≤ 2 minutes on web (target median) |
| PO-2 | Reliable partner operations | ≥ 95% of jobs auto-accepted by the matching technician within the SLA window |
| PO-3 | One ledger, no reconciliation surprises | ≥ 99.5% of weekly settlements auto-matched without manual intervention |
| PO-4 | Multi-tenant ready from day one | A new branch or partner branch is onboarded without schema change or code deployment |
| PO-5 | Service-type extensibility | A new service category is added by **configuration** (workflow template + price book), not a code release |

### 4.3 Engineering Objectives

| ID | Objective | Measure |
|---|---|---|
| EO-1 | Availability | ≥ 99.5% monthly for the API and customer-facing surfaces |
| EO-2 | Performance | p95 API latency < 400 ms (excluding third-party calls); booking search p95 < 800 ms |
| EO-3 | Financial correctness | Zero tolerance — see §8.2 |
| EO-4 | Auditability | 100% of money-touching state transitions produce an immutable audit record |
| EO-5 | Deployability | Independent, reversible deploys per surface; no full-stop release train |

---

## 5. Scope

### 5.1 In Scope (v1.0 — Phases 1–4)

**Customer-facing**
- Service catalog with location-based availability
- Technician discovery: nearest-available, rating, completed jobs, price range, ETA
- Booking with slot selection, coupon application, advance payment
- Live tracking, status timeline, reschedule, technician change request
- OTP-verified job start and completion, in-app digital invoice, remaining payment
- Rating, review, warranty/request rebooking, support via ticket and toll-free

**Partner / Technician-facing**
- Technician onboarding: registration, KYC, document upload, skill & category selection, service-area pin
- Job feed, accept/reject with timer, navigation, job checklist, part usage capture, photo evidence
- Earnings ledger, wallet, weekly settlement view, commission & GST breakdown, invoice download
- Ratings received, performance score, penalties, profile health

**Branch / Partner-of-Platform-facing**
- Branch-scoped dashboard: bookings, SLAs, technician roster, service areas, price book, coupons, complaints, performance
- Technician management, availability and capacity management, service-area configuration
- Local price customisation within platform bands, partner-funded coupons

**Central Platform-facing**
- Master data: states, cities, zones, service areas, categories, services, price books, taxes, documents, reasons
- Role & permission administration (Super Admin → Admin → Operator → CCO → Accountant → Partner Support → Marketing & Ops)
- Partner onboarding & approval, branch approval, territory allocation
- Pricing rule engine (state → city → zone → service-area bands), coupon engine, commission configuration
- Commission ledger, weekly settlement generation, GST invoices, reconciliation, dispute management
- Toll-free support console: IVR, smart routing, call log, ticket management, CSAT & analytics
- Reporting & analytics: funnel, SLA, revenue, commission, technician performance, branch P&L

**Platform / Infrastructure**
- Website, Customer app, Partner app, Control Center (admin dashboard)
- Payment gateway, maps, push, SMS, WhatsApp, email, telephony
- Audit logging, RBAC, encryption, backups, monitoring

### 5.2 Out of Scope (v1.0)

| Excluded | Rationale | Revisit |
|---|---|---|
| Native iOS & Android app store distribution of the *admin* surfaces | Control Center is web-only by design | v1.1 |
| Third-party marketplace listing (Justdial, Sulekha) | Requires a separate integration programme | Phase 5 |
| In-house logistics / spare-parts warehousing | Parts sold at MRP or allowed margin, not stocked centrally | Phase 5 |
| Direct-to-consumer consumables (FMCG) | Different fulfilment model | Not planned |
| Multi-currency | Single market (India) | Not planned |
| AI-driven dynamic pricing | Price bands are deterministic; predictability matters more | Phase 5 `[PROPOSED]` |
| Full ERP / accounting suite replacement | AmmPal covers commission, settlement, GST and reconciliation only | Phase 5 |
| Self-serve customer onboarding of *partner branches* | Partner branches are onboarded by Operator/Super Admin | Phase 4 |

### 5.3 Success Metrics (Launch → Phase 4)

**Growth**
- Registered customers, monthly active customers, bookings per active customer
- CAC vs. contribution margin per booking (must be positive by Phase 3)

**Marketplace**
- **Fill rate**: % of bookings accepted within SLA (target ≥ 95%)
- **Time-to-accept**: median minutes from request → accept (target ≤ 6 min)
- **Coverage**: % of service requests in a service area with ≥ 3 eligible technicians
- **Repeat rate**: % of bookings from returning customers

**Quality**
- Median rating (target ≥ 4.3), technician score, complaint rate, rework rate
- Cancellation rate (customer / technician), no-show rate, SLA breach rate

**Financial**
- Average order value, gross margin per booking, commission rate realisation vs. configured
- Settlement accuracy (auto-match rate), settlement cycle time (target ≤ 7 days from accrual)
- DSO on partner payables, dispute rate and value

**Support**
- Call abandonment rate, average handle time, first-call resolution, CSAT, ticket reopen rate

---

## 6. Assumptions

| ID | Assumption | Validity Check |
|---|---|---|
| AS-1 | Payment gateway (Razorpay) supports UPI, cards and netbanking with settlement to a single Indian account | Confirm during Phase 0 |
| AS-2 | GST is charged on the platform's **commission** (18% intra-state) and on the **customer invoice** as applicable to the place of supply | Tax advisor sign-off required before Phase 2 billing |
| AS-3 | Individual technicians are treated as service providers (no GST registration obligation via platform) | `[PROPOSED]` — tax advisor sign-off; see `21` (OD-07-02, OD-07-03) |
| AS-4 | WhatsApp Business Platform official API is available for the business entity | Confirm in Phase 0 |
| AS-5 | Indian cloud-telephony provider supports DND-compliant commercial voice, IVR and call recording | Provider evaluation in Phase 0 |
| AS-6 | Initial load is low enough for a 4 vCPU / 16 GB single-VPS footprint | Revisit at Phase 3 load test |
| AS-7 | Google Maps Platform billing is within the startup tier for Phase 1–2 | Track monthly in Phase 2 |
| AS-8 | Branch onboarding is a commercial/operations event, not a self-service event | Confirmed by founder model |

---

## 7. Constraints

| ID | Constraint |
|---|---|
| CN-1 | 4 vCPU / 16 GB Linux VPS is the initial hosting target — the system must be vertically efficient |
| CN-2 | Indian regulatory environment: GST, place of supply, data residency expectations, DND/telephony rules |
| CN-3 | Payments in India are UPI-dominant; the booking funnel must work with advance = ₹0 for many bookings |
| CN-4 | Multilingual support (Odia, Hindi, English) is a requirement, not an enhancement |
| CN-5 | Launch is Odisha-first; multi-state must be *possible* but must not slow Odisha delivery |
| CN-6 | Branch and partner-branch onboarding is manual and operator-driven — no self-service provisioning in v1.0 |

---

## 8. Key Business Rules (Non-Negotiable)

These rules are **confirmed** from the source infographics and the founder's model. Any change requires
a charter amendment.

### 8.1 Booking & Acceptance
- BR-01 — A technician is **location-scoped**. Technicians register centrally; **jobs are offered by location**.
- BR-02 — A partner branch operates **only** within its allocated territory; its dashboard is fully location-dependent.
- BR-03 — The platform sets **minimum, maximum and default** prices. A partner may only customise **within** the band.
- BR-04 — **Commission is charged on eligible labor only** — not on visiting charge, transport, spare parts, or customer GST.
- BR-05 — Partner earnings are settled on a **weekly cycle** (Mon–Sun accrual, statement following Monday, payment due within 7 calendar days).

### 8.2 Financial Integrity (Zero-Tolerance)
- FR-01 — The complete price breakdown is computed and **snapshotted** at booking confirmation and never recomputed from live configuration.
- FR-02 — Every invoice line and commission ledger entry is derived from the booking's price snapshot.
- FR-03 — All arithmetic is performed in integer minor units; rounding follows a single documented rule.
- FR-04 — Settlement statements are immutable once issued; corrections are made via **adjustments / credit notes**, never edits.
- FR-05 — Every money-touching state transition emits an immutable audit record.

### 8.3 Location
- BR-06 — The location hierarchy is **State → City → Zone → Service Area → Branch**. Branch is the operational unit.
- BR-07 — Every booking resolves to exactly one service area and one branch.
- BR-08 — Partner branches are "allowed" into the platform by **Operator** or **Super Admin** only.

---

## 9. Stakeholders

| Stakeholder | Interest | Engagement | Owner |
|---|---|---|---|
| Founder / Platform Owner | Business model, unit economics, expansion | Steering review fortnightly; decision authority | — |
| Super Admin | Master data, permissions, global configuration | Daily | Platform Ops |
| Admin (Manager) | Cross-functional performance, escalations | Daily | Platform Ops |
| Operator | Partner & branch onboarding, booking operations, issue resolution | Daily | Platform Ops |
| CCO | Customer & technician support, call quality | Daily | Customer Support |
| Accountant | Commission, settlement, GST, reconciliation | Daily/weekly cycle | Finance |
| Partner Support | Partner enablement, KYC, wallet queries | Daily | Partner Ops |
| Marketing & Operations | Campaigns, coupons, content, analytics | Weekly | Growth |
| Branch Manager (company branch) | Local P&L, technician roster, SLA | Daily | Branch Ops |
| Partner Branch Admin | Local territory execution | Daily | Partner Ops |
| Technician | Work, earnings, reputation | Daily (app) | Partner Ops |
| Customer | Reliable service, fair price, fast booking | Continuous | Product |

---

## 10. High-Level Approach

### 10.1 Delivery phases

```
Phase 0  Foundation     ── Design sign-off, stack, repo, CI, environments, master data model
Phase 1  Core Platform  ── Auth, RBAC, catalog, booking, technician feed, payments, basic admin
Phase 2  Service & Money ── Workflow engine, pricing rules, coupons, invoices, commission, settlement
Phase 3  Branch & Scale ── Branch model, branch/partner-branch dashboards, support console, analytics
Phase 4  Growth         ── Multi-state, partner-branch expansion, new categories, optimisation
```

### 10.2 Architecture stance

**Modular monolith with micro-ready extraction boundaries** (see `08-System-Architecture.md` §2).
Rationale: a pre-scale marketplace cannot afford microservices operational overhead, but it must not
be architected in a way that requires a rewrite to scale. Every module is defined with strict
boundaries, an owned schema namespace, an explicit public interface, and asynchronous communication
through a durable queue — so any module can be extracted independently later using a strangler-fig
migration without touching its consumers.

### 10.3 Technology stance

TypeScript across the whole stack. NestJS modular API, PostgreSQL + PostGIS as the system of record,
Redis + BullMQ for cache and async work, Next.js for the website, React + Vite for the Control Center,
Flutter for the Customer and Partner apps, and a vendor-neutral integration layer (Maps, Payments,
Telephony, WhatsApp, FCM, SMS, Email).

### 10.4 Quality stance

Contract-first API design (OpenAPI generated), pricing and commission logic implemented once as a
pure, independently unit-tested domain module, and end-to-end coverage of the four golden paths
(book, serve, pay, settle) in every release.

---

## 11. Dependencies

| ID | Dependency | Owner | Needed By |
|---|---|---|---|
| DP-1 | Payment gateway merchant account (Razorpay) + settlement account | Finance | Phase 1 |
| DP-2 | Cloud telephony provider with DND-compliant commercial voice + IVR + recording | Support | Phase 2 |
| DP-3 | WhatsApp Business Platform verification | Growth | Phase 2 |
| DP-4 | Google Maps Platform billing account | Engineering | Phase 1 |
| DP-5 | Business PAN/GSTIN + service tax registrations per operating state | Finance | Phase 2 |
| DP-6 | Technician KYC vendor (optional; manual fallback required) | Partner Ops | Phase 2 |
| DP-7 | SMS provider with transactional templates approved | Engineering | Phase 1 |
| DP-8 | Domain `ammpalservice.com` + TLS + CI/CD secrets vault | Engineering | Phase 0 |

---

## 12. Risks (Summary — full register in `19`)

| ID | Risk | Sev | Mitigation |
|---|---|---|---|
| R-01 | Commission/settlement miscalculation → financial loss & trust loss | Critical | Pure domain module, snapshot-based pricing, golden-master tests, dual-approval on settlement |
| R-02 | GST / place-of-supply error → notice, penalty | High | Tax advisor sign-off, state matrix, per-branch registration config, pre-launch reconciliation review |
| R-03 | Thin technician supply in a new city → poor fill rate | High | Coverage dashboard per service area, seeded onboarding before launch, category-scoped capacity alerts |
| R-04 | Branch adoption stalls → stranded cities | Medium | Owner-assigned branch P&L, weekly ops review, partner-branch model as low-capex fallback |
| R-05 | Single-VPS failure → full outage | High | Daily backups + PITR, tested restore, provider-level redundancy for critical managed deps |
| R-06 | Misrouted complaints → SLA breach, churn | Medium | Smart routing rules, QA sampling, CSAT loop, escalation matrix |
| R-07 | Scope creep across 6 service categories | Medium | Workflow-engine + price-book configuration instead of per-category code; category launch gate. `[OPEN]` — this row assumes **6** while `BO-1` above commits to **3**; the unreconciled pair is `OD-DOC-27` |
| R-08 | Partner fraud / collusion on price or rating | Medium | Price band enforcement server-side, audit logs, anomaly detection on ratings and rejections |

---

## 13. Success Definition

The project is **successful** when, for a customer in Bhubaneswar who needs a refrigerator repair:

1. They can find, compare and book a verified technician in **under 2 minutes**.
2. The technician is **notified within seconds**, accepts, and their live location is visible.
3. The price they saw at booking **is** the price on the final invoice — no surprise.
4. The technician is **paid within 7 days** of job completion, automatically, with a transparent breakdown.
5. The platform **knows** whether it worked: the rating, the complaint, the settlement, the margin.

...and the same is true in every city, for every category, without a code change.

---

## 14. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Sponsor / Founder | | | |
| Product Lead | | | |
| Engineering Lead | | | |
| Finance Lead | | | |
| Operations Lead | | | |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.2 | 2026-10-21 | Product Lead + Founder (design-system and asset pass) | Two rows annotated; no objective, target or risk reworded. **BO-1** now carries the **3 / 4 / 6 / 2** contradiction against `17` P2-02, `06` §4.1–§4.6 and `OD-RM-04` (`OD-DOC-27`), and **§12 R-07** is marked as assuming 6 in the same document that commits to 3 — the pair sits one screen apart, which is how it survived three audit passes. Both annotations follow `DEC-07`: each competing statement is named on its own side and neither has been edited into the other. This is not only wording — the launch category count is what fixes how many category assets `31` and `33` must account for. | §4.1 BO-1, §12 R-07, header, Revision History |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Added the explicit no-implementation statement and the implementation-status rule (ADR-025); recorded the VPS planning envelope (4 vCPU / 16 GB / 200 GB NVMe / 16 TB bandwidth) as a planning target; added BR-09 to BR-18 (branch vs legal entity, serviceability, exclusive booking ownership, immutable snapshot, append-only finance, bounded support permissions, city activation gate); cross-referenced the ADRs and new documents. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
