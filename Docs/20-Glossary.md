# 20 — Glossary

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-20 |
| Version | 1.2 |
| Status | Approved for Design & Development |
| Owner | Product Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |

---

## 1. How to Use This Glossary

This is the **canonical vocabulary** for AmmPal Service. If a term appears in a document, a ticket,
a database column, an API field or a UI label and it is not defined here, it is either not decided
yet or it is defined in one of the other documents — in which case this glossary points to it.

**Rules**
- A term has exactly one meaning across the whole platform.
- New terms are added here before they are used in code.
- If a term needs two meanings, it is two terms.

---

## 2. Organisation & Tenancy

| Term | Definition |
|---|---|
| **Platform** | The AmmPal central operation — the technology, pricing policy, finance, marketing and quality control that governs all branches. |
| **Central** | The platform-level administrative scope, as opposed to branch-level. |
| **Branch** | The **operational unit** of AmmPal. Owns technicians, service areas, price customisation, bookings, and settlement. Two types: `COMPANY` and `PARTNER`. |
| **Company branch** | A branch owned and operated by AmmPal Central. |
| **Partner branch** | A branch owned by an authorised platform partner operating in an allocated territory. |
| **Partner Organisation** | The legal entity that operates one or more partner branches. Holds KYC, GSTIN and the bank account. |
| **Partner of Platform** | An authorised platform partner operating a branch. A business role, not a system account. |
| **Partner** | Ambiguous by design — see §9. Always qualify as *partner branch* or *partner organisation* in writing. |
| **Zone** | A named geographic cluster within a city. Carries zone-level price overlays and capacity targets. |
| **Service Area** | The smallest operational geography. The unit of job distribution and technician coverage. |
| **Territory** | The set of service areas allocated to one branch. |
| **Scope** | The data boundary attached to an account: `GLOBAL`, `STATE`, `BRANCH`, `SERVICE_AREA` or `SELF`. |
| **Central Office** | AmmPal Central — platform ownership, technology, pricing, finance, marketing, quality control. |
| **Branch code** | e.g. `OD-BBI-001` — `<STATE2>-<CITY3>-<NNN>`. Not an open-decision ID. |

---

## 3. Roles

| Term | Definition |
|---|---|
| **Super Admin** | Master administrator. Owns master data, roles and permissions, and global configuration. |
| **Admin (Manager)** | Platform manager. Supervises Operators and Accountants; handles escalations above Operator level. |
| **Operator** | Booking & partner operations. Onboards partners, technicians and branches; allocates territory; resolves operational issues. |
| **CCO (Customer Care Officer)** | Customer Care Officer. Handles inbound calls and support tickets for customers, partners and technicians. |
| **Accountant** | Finance. Commission, settlement, GST, reconciliation, disputes, partner payment tracking. |
| **Partner Support** | Partner enablement — KYC, wallet queries, app usage, document updates. |
| **Marketing & Operations** | Growth. Campaigns, platform-funded coupons, content, content analytics. |
| **Branch Manager** | Manager of a company-owned branch. |
| **Partner Branch Admin** | Owner/manager of a partner branch. |
| **Branch Coordinator** | Front-desk/dispatch for a branch; creates bookings on behalf of customers. |
| **Branch Finance** | Read-mostly finance view for one branch. |
| **Customer** | A person who books services. The source of bookings. |
| **Service Technician** | A platform technician who executes jobs. Also called *partner technician* or *service partner*. |
| **Technician Crew** | An assistant to a lead technician. Cannot accept jobs or invoice independently. |
| **RBAC** | Role-Based Access Control — permissions granted by role, narrowed by scope and ownership. |

---

## 4. Catalogue & Services

| Term | Definition |
|---|---|
| **Category** | A top-level service line (e.g. Appliance Repair). Owns a workflow family and a default commission policy. |
| **Service** | A bookable service within a category (e.g. AC Repair). |
| **Service Variant** | The specific configuration booked (capacity, brand tier, package size). |
| **Skill** | A capability tag a technician holds, with a level from 1 (Trainee) to 4 (Master). |
| **Skill Level** | 1 Trainee · 2 Certified · 3 Senior · 4 Master. |
| **Workflow Template** | The configurable definition of the steps, checklists, evidence and SLAs for a category. |
| **Workflow Family** | A group of templates sharing a shape (e.g. `REPAIR_WITH_DIAGNOSIS`, `PACKAGE_SERVICE`, `PERSONAL_SERVICE`). |
| **Workflow Instance** | A workflow template bound to one booking. A snapshot; later template edits do not affect it. |
| **Checklist** | The set of items a technician must complete within a workflow step. |
| **Evidence** | Photos, signatures or documents proving the work was done. |
| **Primary Business** | Home Appliance Repair — the launch category. |

---

## 5. Booking & Job

| Term | Definition |
|---|---|
| **Booking** | The record of a service request from creation to closure. Also called *job* or *request*. |
| **Booking Code** | The customer-facing identifier: `AMM-YYYYMMDD-XXXXXX`. |
| **Status** | The persisted state of a booking. Six canonical codes plus nine exception states. |
| **Stage** | A narrative phase of the lifecycle (9 stages). Not the same as a status. |
| **Offer** | A job request extended to a specific technician for acceptance. |
| **Direct assign** | An offer to one named technician the customer chose. |
| **Open feed** | An offer broadcast to ranked candidates; rotates on rejection/expiry. |
| **Acceptance window** | The time a technician has to accept an offer before it expires. |
| **Assignment** | The link between a booking and the technician executing it. A booking can have several over its life. |
| **Visit / Visiting charge** | A fixed platform charge for attending the customer site. |
| **Diagnostic charge** | An optional charge for diagnosing the issue. Counts as labour. |
| **Diagnostic** | The process of identifying the fault before repair. |
| **Spare Part** | A physical part used in the job. Billed at MRP or an allowed margin. |
| **OTP verification (job start)** | The customer-provided code proving the technician arrived. |
| **Warranty** | A period after completion during which the same issue is re-attended free of charge. |
| **Redo window** | A short re-service window used instead of a warranty (salon/beauty). |
| **Fill rate** | The percentage of bookings accepted within the SLA window. |
| **Time-to-accept** | The elapsed time from an offer being sent to a technician accepting it. |
| **Coverage** | The availability of eligible technicians for a service in a service area. |
| **Coverage health** | `RED` (< 1 eligible technician) · `AMBER` (< 3) · `GREEN`. |

---

## 6. Money

| Term | Definition |
|---|---|
| **Price Snapshot** | The frozen, itemised price of a booking at the moment of booking. Immutable. |
| **Price Book** | The platform's price bands (min / max / default) per service and geography. |
| **Price band** | The `[min, max]` range within which a branch may set a custom price. |
| **Out-of-band price** | A price outside the band. Requires a special permission, a reason, and is fully audited. |
| **Provenance chain** | The record of how a price was resolved (default → state → city → branch). |
| **Labour charge** | The charge for the technician's work. The primary commission basis. |
| **Eligible labour** | The labour amount that commission is calculated on, after funding rules. |
| **Commission** | The platform's fee, calculated on eligible labour. Default 15%. |
| **Commission base** | The amount commission is calculated on. Excludes visiting charge, transport, parts and customer GST (unless policy says otherwise). |
| **Platform-funded discount** | Absorbed by the platform. Does not reduce partner earnings. |
| **Partner-funded discount** | Absorbed by the partner. Reduces the labour amount and the commission base. |
| **Shared discount** | Split between the platform and the partner per a configured allocation. |
| **Invoice (customer)** | The itemised bill to the customer, including GST. |
| **Advance payment** | A part of the total paid at booking. Optional. |
| **Balance** | The amount due after the service. |
| **Commission invoice** | The invoice to the partner for the commission (and GST on it) for a settlement period. |
| **Settlement** | The weekly statement of commission due to a partner for a period, with booking-wise detail. |
| **Accrual** | Recording commission against a completed job, before it is settled. |
| **Accrual period** | The ISO week (e.g. `2026-W43`) a commission entry belongs to. |
| **Adjustment** | A credit or debit note against a settlement. Never an edit. |
| **Dispute** | A partner's challenge to one or more settlement lines. |
| **Reconciliation** | Matching gateway settlements, recorded payments, invoices and ledger entries. |
| **Ledger** | The append-only record of commission accruals and settlements. |
| **General ledger** | The double-entry record of all financial postings. |
| **Place of supply** | The state where the supply is treated as occurring — the customer's location. |
| **GST** | Goods and Services Tax. CGST + SGST intra-state; IGST inter-state. |
| **Paise** | The minor unit of INR. All money is stored as integer paise. |
| **Basis points (bps)** | The unit for rates: 1500 bps = 15.00%. |
| **Wallet** | The technician's display of accrued earnings. `[PROPOSED]` as a spendable balance — see `OD-UX-02`. |

---

## 7. Support & Quality

| Term | Definition |
|---|---|
| **IVR** | Interactive Voice Response — the automated menu a caller navigates. |
| **Smart routing** | Automatically selecting the queue and agent for an inbound call. |
| **Screen-pop** | The customer context displayed to the CCO when a call connects. |
| **Call log** | The record of a call: time, duration, IVR path, recording reference, disposition. |
| **Support ticket** | A tracked case with a category, priority, owner and SLA. |
| **SLA (support)** | The response and resolution time targets for a ticket priority. |
| **Escalation** | Moving a case to a higher level when it is not resolved in time. |
| **CSAT** | Customer Satisfaction rating, collected after a call or a closed ticket. |
| **FCR** | First Call Resolution — the share of cases resolved on the first contact. |
| **AHT** | Average Handle Time. |
| **Complaint** | A formal expression of dissatisfaction, tracked as a ticket with a category. |
| **Rework** | A repeat visit to correct a failed job, normally by a different technician. |
| **Penalty** | A system-computed charge for a policy breach (late cancellation, no-show). |
| **Technician performance score** | A composite of rating, completion rate, punctuality, acceptance rate and complaints. |
| **Customer score** | A measure of customer reliability (cancellations, no-shows, disputes). |
| **Quality check** | A branch review of a completed job. |

---

## 8. Platform & Technology

| Term | Definition |
|---|---|
| **AmmPal Service (app)** | The customer application. |
| **AmmPal Partner (app)** | The technician/partner application. |
| **AmmPal Control Center** | The administrative web dashboard. |
| **Modular monolith** | A single deployable backend with strict, enforced module boundaries. |
| **Module** | A bounded unit of business capability owning its tables and exposing a typed contract. |
| **Extraction boundary** | The mechanism by which a module can later become an independent service without a rewrite. |
| **Scope guard** | The server-side check restricting a query to the caller's scope. |
| **Ownership check** | The server-side check restricting a resource to its owner. |
| **Outbox** | A transactional pattern that guarantees an event is published only if its transaction committed. |
| **Snapshot** | An immutable copy of data taken at a point in time. |
| **Idempotency key** | A client-supplied key that makes a repeated create request safe. |
| **Golden master** | A stored expected output used to detect unintended change in critical logic. |
| **Golden path** | A critical end-to-end journey that must always work: book → serve → pay → settle. |
| **Feature flag** | A server-side switch that enables behaviour for a subset of users. |
| **Platform mode** | The database-resident state `TESTING` or `PRODUCTION` that governs whether data may be destroyed (`38`). **Not** a deployment environment, **not** a feature flag, **not** provider sandbox credentials. |
| **Step-up verification** | A fresh authentication challenge required *for one specific action* on top of an existing session — here, the email OTP that gates a mode transition (`38` §5). Distinct from the login factor (`OD-SEC-01`). |
| **Record origin** | The `TEST` / `LIVE` stamp on a row, written from the mode in force when it was inserted (`38` PM-12). Reporting and settlement read `LIVE` only. |
| **Hard delete vs soft delete** | A **soft delete** sets `deleted_at` / `is_active` and is the normal `delete` verb (`03` §3.2) — permitted in both modes. A **hard delete** removes the row irreversibly and is what `PRODUCTION` mode refuses. |
| **Canonical status code** | The numeric code (1–15) of a booking status. |
| **Service area** | (see §2) |
| **Surge pricing** | Price variation for peak demand. `[PROPOSED]` — `OD-06-05`. |

---

## 9. Ambiguity Rules

| Term pair | Rule |
|---|---|
| **Partner** | Always qualify. *Partner branch* = a branch of an external partner organisation. *Partner organisation* = the legal entity. *Partner technician* = a service technician on the platform. |
| **Technician** | A person executing jobs. A **service technician** on the platform is not the same as a **third-party appliance technician** — never mix the two in one conversation. |
| **Booking vs Job** | Synonyms in conversation; in the system, `booking` is the record and `job` is the execution instance. |
| **Discount vs Coupon** | A **coupon** is the mechanism (a code with rules); a **discount** is the resulting amount. |
| **Commission vs Platform fee** | **Commission** is charged on eligible labour. A **platform fee** is a separate, additional charge `[PROPOSED]` — `OD-07-08`. |
| **Branch vs Zone vs Service Area** | A branch is an organisation; a zone is a cluster; a service area is a coverage polygon. |
| **Warranty vs Redo window** | A warranty is a defined period with terms; a redo window is a short re-service offer. |
| **Settlement vs Payout** | A **settlement** is the statement; a **payout** is the money actually transferred. |
| **Accountant vs Finance** | *Accountant* is the role in `03`; *Finance* is the function/team. |
| **Mode vs Environment** | **Mode** is a row in one database and decides what may be destroyed (`38`). **Environment** is a deploy target — `local`/`dev`/`staging`/`prod` (`08` §6.1). They are orthogonal, and "production infrastructure in `TESTING` mode" is a defect, not a configuration preference (`38` §10). Never write "prod mode" for either. |

---

## 10. Frequently Used Acronyms

| Acronym | Expansion |
|---|---|
| API | Application Programming Interface |
| AHT | Average Handle Time |
| AAB | Android App Bundle |
| CDR | Customer Data Record |
| CGST | Central Goods and Services Tax |
| CI/CD | Continuous Integration / Continuous Delivery |
| CSAT | Customer Satisfaction Score |
| D2C | Direct to Consumer |
| DPDP | Digital Personal Data Protection (Act, 2023) |
| DND | Do Not Disturb |
| E2E | End to End |
| FCR | First Call Resolution |
| GTM | Go To Market |
| GST | Goods and Services Tax |
| IGST | Integrated Goods and Services Tax |
| IVR | Interactive Voice Response |
| KYC | Know Your Customer |
| MVP | Minimum Viable Product |
| OTP | One Time Password |
| P&L | Profit and Loss |
| P0/P1/P2/P3 | Incident and defect severity levels |
| p95/p99 | 95th / 99th percentile latency |
| QA | Quality Assurance |
| RBAC | Role-Based Access Control |
| RPO | Recovery Point Objective |
| RTO | Recovery Time Objective |
| SaaS | Software as a Service |
| SLA | Service Level Agreement |
| SGST | State Goods and Services Tax |
| SLA | Service Level Agreement |
| SMS | Short Message Service |
| SOP | Standard Operating Procedure |
| TDS | Tax Deducted at Source |
| UPI | Unified Payments Interface |
| VAPT | Value Added Services Tax |
| WA | WhatsApp |

---

## 11. Domain Vocabulary by Locale

Notification templates and customer-facing copy must use the approved localised term. The table below
is the seed for the translation glossary.

| English | Odia | Hindi | Notes |
|---|---|---|---|
| Booking | ବୁକିଂ | बुकिंग | Transliterated |
| Technician | ଟେକନିସିଆନ | तकनीशियन | Transliterated |
| Service | ସେବା | सेवा | Translated |
| Payment | ପେଇମେଣ୍ଟ | भुगतान | Translated |
| Invoice | ଇନ୍ଭୋଇସ | इनवॉइस | Transliterated |
| Complaint | ଅଭିଯୋଗ | शिकायत | Translated |
| Appointment | ନିର୍ବାର୍ତ୍ତ | अपॉइंटमेंट | Transliterated |
| Warranty | ୱାରେଣ୍ଟୀ | वारंटी | Transliterated |

**Rule GLO-01** — Technical and platform terms that customers will not understand are transliterated;
functional terms are translated. The final wording is set by the Odia-speaking content owner during Phase 1.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.2 | 2026-10-21 | Product Lead (platform-mode pass) | §8 gained four terms that this suite now uses with one meaning each: **Platform mode** (`TESTING`/`PRODUCTION` database state — explicitly *not* an environment, not a feature flag, not a provider sandbox), **Step-up verification** (a fresh factor check inside an already-authenticated session, distinct from login MFA), **Record origin** (`TEST`/`LIVE`, write-once), and **Hard vs soft delete** (row removed vs row marked — the guard speaks only of the first). §9 gained the ambiguity rule **Mode vs Environment**, because the two words were already being used interchangeably in the instruction that produced the feature, and the conflation is exactly how a `prod` host ends up running with the guard disarmed. | §8, §9 |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Renamed the ambiguous `OD-CITY` glossary entry to `Branch code` so it no longer collides with the open-decision ID prefix; added the audit entities to the vocabulary. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
