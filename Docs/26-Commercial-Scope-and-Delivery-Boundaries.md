# 26 — Commercial Scope & Delivery Boundaries

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-26 |
| Version | 1.6 |
| Status | **Approved for Design & Development — commercial terms are PROPOSED and NOT YET LEGALLY EXECUTED** |
| Owner | Founder / Project Owner |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `00`, `17`, `18`, `19`, `21` |

---

## 1. Purpose and Evidence Status

This document records the **commercial and delivery context** of the AmmPal Service project so that
engineering, operations and finance can understand what is being built, what is being paid for,
and where the boundary of the engagement lies.

It is deliberately kept **separate from the technical specification**. The technical documents
(`00`–`25`, `27`–`29`) describe *what the platform is*. This document describes *what has been
agreed commercially* and, critically, **what has not**.

### 1.1 Evidence Labels Used in This Document

The five-status vocabulary is defined once, in `README` §4, and is **not** redefined here. Because a
commercial term needs a stronger evidence standard than a product rule, this document adds one
label of its own rather than tightening the meaning of `[CONFIRMED]`.

| Label | Meaning |
|---|---|
| `[REPORTED]` | Stated by the project owner or in the project context. Recorded faithfully. **Not independently verified by the documentation author.** |
| `[PROPOSED]` | A commercial term discussed or drafted but **not** countersigned, or not confirmed in a final agreement. |
| `[EXECUTED]` | **This document's extra label.** Present in a signed, countersigned agreement held on file. **At the date of this document, nothing qualifies — no executed agreement is on file in this repository**, so no figure here carries `[EXECUTED]`. |
| `[DEPENDENT]` | Depends on an external party (tax advisor, legal counsel, a vendor, a bank). |
| `[OPEN]` | Requires a decision by the project owner. |

> **Why the change.** Earlier editions of this document used `[CONFIRMED]` to mean "present in an
> executed agreement", while `README` §4, `28` §1.1 and `29` §1 use `[CONFIRMED]` to mean "established
> in project context or an accepted decision record". The same word carried two evidence standards in
> one document set, and the stricter one was the more quotable — a reader of `26` alone could conclude
> that a rule marked `[CONFIRMED]` in `07` had been signed, or that nothing in `26` was confirmed at
> all. `[EXECUTED]` is unambiguous, so a commercial claim can never be mistaken for a product claim
> and vice versa.

### 1.2 The Critical Limitation

> **No signed agreement, invoice, receipt, bank record or countersigned statement is present in this
> repository.** Every commercial figure in this document is either `[REPORTED]` or `[PROPOSED]`.
> No figure here may be represented to a customer, a vendor, a bank, an investor or a statutory
> authority as a binding commitment of the platform or of the development partner.

---

## 2. Development Partner

| Field | Value |
|---|---|
| Organisation | **Locky Dev** |
| Website | `https://www.lockydev.cloud/` |
| Contact | `7978322649` |
| Email | `support@lockydev.cloud` |
| Address | Gothapatana, Bhubaneswar, Odisha – 751003 |

**Status:** `[REPORTED]` — these details are as provided by the project owner and have not been
independently verified by the documentation author. They are recorded so that the project context is
complete. Before use in any executed document, they should be confirmed against the partner's own
records (GST registration, PAN, authorised signatory, current address).

---

## 3. Delivery Scope

### 3.1 In Scope for the Initial Development Fee

The following is the `[PROPOSED]` scope that the initial development fee is understood to cover.

| # | Area | Deliverables | Document |
|---|---|---|---|
| 1 | Platform backend | NestJS modular monolith — all 16 modules, the RBAC and scope model, the audit trail | `08`, `09`, `10` |
| 2 | Public website | Next.js — discovery, location-based pages, booking entry points, partner registration, support | `12` §2 |
| 3 | Customer app | Flutter — registration, discovery, booking, tracking, payment, rating, support | `12` §3 |
| 4 | Partner app | Flutter — onboarding, job feed, execution, evidence, invoice, earnings, settlements | `12` §4 |
| 5 | Control Center | React + Vite — role-based dashboards for Super Admin, Admin, Operator, CCO, Accountant, Partner Support, Marketing Ops | `12` §5 |
| 6 | Financial engine | Pricing resolution, coupons, invoices, commission accrual, weekly settlement, reconciliation | `07` |
| 7 | Workflow engine | Versioned per-category workflow templates and the execution engine | `06` |
| 8 | Support console | IVR integration, smart routing, call logs, tickets, escalation | `05` |
| 9 | Integrations | Maps, payments, push, WhatsApp, SMS, email, telephony, object storage — **integration effort only** | `11`, `24` |
| 10 | Infrastructure | Environment provisioning, CI/CD pipeline, monitoring, backups, deployment | `16` |
| 11 | Documentation | This documentation suite | `Docs/` |
| 12 | Initial city configuration | Bhubaneswar — one branch, zones, service areas, price book, seed catalogue | `02`, `29` §14 |

### 3.2 Explicitly Outside the Initial Development Fee

| # | Item | Reason | Treatment |
|---|---|---|---|
| 1 | **Recurring third-party consumption** — SMS, OTP, WhatsApp conversations, Google Maps API calls, payment gateway charges, telephony minutes, email, object storage, CDN | Consumption-based and billed by each vendor directly | The platform owner procures and pays these directly with their own vendor accounts. `[PROPOSED]` — must be confirmed in the final agreement |
| 2 | **Vendor account procurement and merchant KYC** | Requires the platform owner's PAN/GSTIN, bank account, business proof | Owner-led, with the development partner assisting |
| 3 | **Production cloud and server costs** (VPS, backup storage, managed services) | Ongoing infrastructure | Owner-provisioned and paid; see §6 |
| 4 | **App store accounts and developer fees** | Apple Developer ($99/yr) and Google Play ($25 one-time) accounts | Owner-provisioned |
| 5 | **Domain registration and renewal** | `ammpalservice.com` | Owner-provisioned |
| 6 | **Tax, legal and compliance advisory** | GST opinions, TDS advice, consumer-protection review, DPDP review, contract drafting | Owner-provisioned. See §7 |
| 7 | **Recruitment, training and certification of technicians** | Supply-side operation | Platform owner's operational cost |
| 8 | **Customer support staffing beyond the build** | CCO headcount | Platform owner's operating cost |
| 9 | **Marketing, campaigns and content production** | Growth | Platform owner's operating cost |
| 10 | **Data entry and seed content beyond the seed catalogue** | Ongoing | Platform owner's operating cost |
| 11 | **Second and subsequent cities** | Each city activation is configuration + operational readiness (`ADR-017`) plus operational cost | Priced separately; see §4.4 |
| 12 | **Native iOS apps before Phase 3** | Noted in `21` (OD-UX-05) | Deferred by default |
| 13 | **Partner web dashboard** | Conditional surface (`ADR-021`, `21` open item) | Priced separately if included |
| 14 | **Hardware** — technician devices, phones, tablets, test devices | | Platform owner |
| 15 | **The platform-mode feature (`38`, `01` §4.11 `FR-MODE-01`…`08`, `22` `ADR-026`)** — the mode table and transition history, the promotion ceremony, the delete guard at L2 **and** L3, the `record_origin` column on all 88 tables, the mode indicator on four surfaces and the `TE-06` test set | Not one of §3.1's twelve areas; it was instructed on 2026-10-21, after this list was written. It also carries a **non-trivial infrastructure ask** that §3.1 item 10 does not plainly cover: L3 enforcement needs an additional database connection identity per environment (`OD-DOC-43`) | **Outside the initial development fee until the agreement is changed in writing.** `[PROPOSED]`, unapproved, unpriced — see §3.1's scope-creep control and `OD-COM-13`. Recording it here is a scope statement, not a decision to build it and not a price |

> **Scope creep control.** Any item not in §3.1 requires a written change to the executed agreement
> before work begins. This is recorded here so that the boundary is unambiguous.
>
> **Item 15 is the first live case of that control.** `01` §8 treats the `FR-MODE` family as a **v1.0
> requirement addition** needing a charter amendment (`00` §14 approval), and this section treats it as
> **outside the fee** until the agreement changes — the two are separate approvals and neither follows
> from the owner describing the feature. `DEC-03` forbids reading an instruction as a signed variation,
> so nothing in `38` has been priced, scheduled or accepted here. The consequences worth naming before
> anyone agrees to a date: the migration cost is spread across **every** table (the origin column), the
> L3 layer needs infrastructure §3.1 does not currently fund, and the promotion ceremony consumes a
> transactional-email channel that is **not procured** (§3.2 item 1, `24` P-06, `OD-MAIL-01`) — so the
> feature cannot be delivered end-to-end without two owner-side procurements happening first.

---

## 4. Commercial Terms

### 4.1 Initial Development Fee

| Field | Value | Status |
|---|---|---|
| Total development fee | **₹3,00,000** | `[PROPOSED]` |
| First instalment | **₹1,00,000** at project start | `[PROPOSED]` |
| Second instalment | **₹1,00,000** after UI design approval | `[PROPOSED]` |
| Third instalment | **₹1,00,000** before production deployment, subject to agreed acceptance and handover conditions | `[PROPOSED]` |
| Target delivery period | **Within six months**, subject to approved scope and dependencies | `[PROPOSED]` |

> **"After UI design approval" is not defined anywhere in this suite, and it is a payment trigger.**
> §4.1 names no approver, no scope for the approval, no evidence and no rule for partial approval, yet
> ₹1,00,000 becomes payable on it — so the phrase is registered as risk `R-45` and is tied to
> `OD-COM-03` (the acceptance conditions this table refers to) and to `OD-DOC-30`…`39`, which are the
> design decisions an approval would have to be *about*. `30` §12 lists the twelve owner decisions the
> design gate consists of. **`OD-DOC-36` asks the logically prior question, and it is unresolved:** under
> the owner's placeholder-first direction (`30` §5.3) a screen may be reviewed with every media slot an
> empty container, so a partial approval of a *layout* could be presented as the event that triggers this
> instalment. **The design-system and palette passes that produced `30`–`34` did not approve anything and
> did not trigger anything**: all five documents are `PROPOSED`, no image has been generated, and no
> document here may be read as the owner's sign-off. **The same applies to `35`–`37`, added by the
> design-engineering pass:** a folder tree, an admitted library and a component contract are not a
> designed screen — they describe how approved design would be built, and none of the three is approved.
> Nothing in this table is signed — `OD-COM-01` is open.

### 4.2 Payment Report

> `[REPORTED]` — The project owner has stated that the **first ₹1,00,000 instalment was collected in
> cash and a receipt was prepared.** The documentation author has **not** independently verified this
> payment, and no receipt copy, bank record or countersigned acknowledgement is present in this
> repository. The statement is recorded faithfully for project continuity.

**Action required before invoicing or corporate bookkeeping.** The remaining two instalments should
be settled through a traceable instrument — bank transfer to a declared business account against a
GST invoice — rather than cash. A cash instalment has weak evidentiary value for both parties and may
create a record-keeping gap for the platform owner's GST returns. This is flagged as `[OPEN]` in §9.

### 4.3 Annual Technical Service — Single City

| Field | Value | Status |
|---|---|---|
| Annual technical service (initial single-city) | **₹60,000 / year** | `[PROPOSED]` |

### 4.4 Annual Technical Service — Multi-City Ranges

| Tier | Annual service range | Status |
|---|---|---|
| Multi-city, Odisha | **₹5,00,000 – ₹10,00,000 / year** | `[PROPOSED]` |
| Large-scale multi-city / multi-state | **₹10,00,000 – ₹20,00,000 / year** | `[PROPOSED]` |

### 4.5 Critical Caveat on All Annual Service Figures

> The annual figures in §4.3 and §4.4 are **ranges and starting points for negotiation**. They are
> **not** automatically applicable and they are **not** unlimited-service commitments.

Before any annual service engagement is treated as binding, the following must be written into the
agreement:

| # | Term that must be defined | Why it matters |
|---|---|---|
| 1 | **Scope of service** — what is included (patching, security updates, monitoring, backup verification, incident response, vendor integration upkeep, documentation updates) and what is not | Without it, "annual service" is unbounded |
| 2 | **Service levels** — response and resolution targets, P0/P1 handling, support hours, on-call expectations | The current NFRs in `13` are *targets*, not contractual SLAs |
| 3 | **Cost allowance** — a monthly cap on third-party consumption included in the fee, or explicit exclusion | Vendor consumption can exceed the entire annual fee (§3.2) |
| 4 | **Hosting arrangement** — who owns the VPS, who pays the provider, who renews the domain | See §6 |
| 5 | **Renewal date and notice period** — auto-renewal, the window in which either party may exit | Prevents a surprise renewal |
| 6 | **Expansion pricing** — how a new city or state is priced and when the tier moves | Directly affects §4.4 |
| 7 | **Change-management process** — how a new requirement is priced and scheduled | Prevents unbounded scope |
| 8 | **Data continuity** — what happens to the data, the repository, the documentation and the infrastructure if the engagement ends | See §6.3 |
| 9 | **Security obligations in both directions** — production access approval, audit, confidentiality | `13` §5 — `[OPEN]`: §5 contains no production-access rule, only application-layer controls; the missing control is registered as `OD-DOC-22` and this citation does not create it |
| 10 | **Tax treatment of the service fee** — GST on professional/technical services | `[DEPENDENT]` — tax advisor |
| 11 | **IP and licensing** — ownership of the source code, the documentation and the design assets | Not yet documented |
| 12 | **Liability, warranty and acceptance criteria** | Not yet documented |

---

## 5. Acceptance and Handover

### 5.1 Acceptance Criteria (Proposed)

The third instalment is described as payable *"before production deployment, subject to agreed
acceptance and handover conditions"*. Those conditions are **not yet defined**. The following
minimum set is proposed, drawn from `15` §14 (release quality gates) and `29`:

| # | Acceptance gate | Evidence |
|---|---|---|
| A-1 | All four golden paths pass end-to-end on a staging environment: GP-1 Book→Serve→Pay→Review; GP-2 Book→Accept→Settle; GP-3 Call→Book→Track; GP-4 Complaint→Rework→Refund | Automated test report |
| A-2 | The golden-master financial suite passes, including the documented worked example in `07` §4 | CI report |
| A-3 | Nightly reconciliation reports zero differences across invoices, settlements and the ledger | Reconciliation report |
| A-4 | The scope-isolation security sweep passes on every tenant-scoped endpoint | Test report |
| A-5 | The performance suite meets the targets in `13` §2 | Performance report |
| A-6 | The migration rehearsal and the rollback rehearsal are complete on a production-like snapshot | Rehearsal record |
| A-7 | The documentation suite in `Docs/` is current and internally consistent | Documentation audit |
| A-8 | A production-like backup has been restored successfully at least once | Restore drill record |
| A-9 | The Control Center, website and both apps are deployed and functional for Bhubaneswar | Deployment record |
| A-10 | A handover pack is delivered: repository access, environment inventory, credential handover procedure, vendor account inventory, runbooks | Handover checklist |

### 5.2 Handover Deliverables

| # | Item | Notes |
|---|---|---|
| H-1 | Source repository access | Owner or an agreed organisation with full history |
| H-2 | Infrastructure inventory and access | Host, DNS, TLS, object storage, backups |
| H-3 | Vendor account inventory | Every provider account, its owner, and the renewal date |
| H-4 | Credential handover procedure | Documented, **without** secrets committed to the repository |
| H-5 | Runbooks (`25`) and the release checklist (`29`) | |
| H-6 | Documentation suite (`Docs/`) | This is a primary deliverable, not an appendix |
| H-7 | Known limitations and open decisions (`21`) | Transferred with the project, not left behind |
| H-8 | A support escalation path during the annual service term | |

---

## 6. Access, Administration and Continuity Model

### 6.1 The Discussed Position

`[REPORTED]` — The parties have discussed that **domain and server administration remain under
Locky Dev's access** during the engagement.

This is a workable operating model for a single-city launch, and it is recorded here accurately.
It is also a **concentration-of-access risk** that must be documented rather than left implicit.

### 6.2 Required Access Model

| # | Control | Requirement |
|---|---|---|
| 1 | **Named accounts only** | Every infrastructure and vendor access is held by a **named individual** account. Never a shared personal account. |
| 2 | **Least privilege** | Access is granted per role and scope, matching the RBAC model in `03`. Production access requires explicit approval and is time-bound for one-off tasks. |
| 3 | **No direct production mutation** | All production changes flow through the pipeline (`16` §3). Administrative emergency access is logged and reviewed. |
| 4 | **Auditability** | Every production access and every override is recorded in `audit_events` and reviewed in the monthly access review (`19` §4.2, IC-03). `[OPEN]` — two parts of this sentence are not yet true: the cadence is quarterly in `13` §5 (`OD-DOC-21`), and a shell on the production host is not an `audit_events` actor at all (`OD-DOC-22`). |
| 5 | **No credentials in documentation** | Secrets live in the server's secret store with `0600` permissions and are never written into Markdown, code, or a ticket (`16` §7). |
| 6 | **Rotation** | Credentials rotate on a defined schedule, and immediately on any suspected compromise (`16` §7). |
| 7 | **Access log handover** | The platform owner receives periodic access reports (who accessed what, when) whether or not they hold the credentials themselves. |

### 6.3 Continuity, Export and Migration — Mandatory Before Go-Live

| # | Requirement | Detail |
|---|---|---|
| 1 | **Repository ownership** | The platform owner (or a named organisation they designate) is the repository owner with full history from day one, so the code is never dependent on one person's account. |
| 2 | **Credential escrow** | A documented, tested procedure for the platform owner to obtain all production and vendor access — not a promise, a rehearsed handover. |
| 3 | **Backup ownership** | Backup copies are held in an account the platform owner controls, or in a second location they control. A backup that only the development partner can restore is not an owner-protectable backup. |
| 4 | **Data export** | A tested export path for all platform data (customer, technician, booking, financial, support) in a documented, portable format (database dump + object-store copy + a data dictionary). |
| 5 | **Migration readiness** | The documentation suite, the OpenAPI contract, the deployment runbooks and the environment inventory are sufficient for a different team to operate the platform. `Docs/` exists for this purpose (`ADR-018`). |
| 6 | **Exit assistance** | If the engagement ends, a defined handover and knowledge-transfer window at no additional cost, with a fixed timeline. |
| 7 | **Domain and DNS** | The platform owner should hold the domain registration directly rather than through an intermediary, so ownership is never in question. `[PROPOSED]` |

### 6.4 Dependency Register for the Access Model

| Dependency | Owner | Status |
|---|---|---|
| `ammpalservice.com` registrar account | Platform owner | `[OPEN]` — confirm the registrar and the registrant |
| DNS / nameserver management | Locky Dev (current model) | `[PROPOSED]` — move to owner-held accounts with delegated access |
| VPS provider account | Locky Dev (current model) | `[PROPOSED]` — owner-held preferred |
| Object storage account | To be decided | `[OPEN]` — `21` OD-08-05 |
| Payment gateway merchant account | Platform owner | `[OPEN]` — required, `21` OD-07-03 dependency |
| Google Maps billing account | Platform owner | `[OPEN]` |
| WhatsApp Business account | Platform owner | `[OPEN]` — `21` OD-INT-02 |
| Telephony account (toll-free) | Platform owner | `[OPEN]` — `21` OD-INT-01 |
| SMS / email provider accounts | Platform owner | `[OPEN]` — `21` OD-14-05 |
| Firebase project | Platform owner | `[OPEN]` |
| OIDC / staff identity provider | Platform owner | `[OPEN]` |

---

## 7. Commercial Dependencies Outside the Development Engagement

These are `[DEPENDENT]` — the platform cannot launch or invoice customers without them, and they are
not the development partner's deliverable.

| # | Dependency | Why | Owner | Register |
|---|---|---|---|---|
| 1 | **PAN and GSTIN** for the platform entity | Required to invoice customers and to register as a marketplace | Platform owner | `19` §3 |
| 2 | **Bank settlement account** for gateway payouts | Razorpay requires a registered business account | Platform owner | — |
| 3 | **Written GST opinion** — treatment, place of supply, supplier identity, TDS | `ADR-024` | Platform owner + tax advisor | OD-07-01, OD-07-02, OD-07-03 |
| 4 | **Legal review** — consumer protection, DPDP, telecom, contracts with partners and technicians | `13` §6, `19` §3 | Platform owner + counsel | — |
| 5 | **Business registration** for the operating entity | Branch cannot be `ACTIVE` without it | Platform owner | `ADR-017` |
| 6 | **Partner agreements** with partner organisations and technicians | Basis for the territory and earnings model | Platform owner | — |
| 7 | **Insurance** | Cyber before Phase 2 (`21` OD-RSK-01) | Platform owner | — |

---

## 8. What the Documentation Suite Does and Does Not Cover

| Covered | Not covered |
|---|---|
| The complete technical specification of the platform | Any executed contract |
| The business rules, workflows and financial formulas | Any signed acceptance certificate |
| The architecture, data model, API contract, security model | Any vendor agreement or merchant approval |
| The test strategy and release gates | Any bank record or tax filing |
| The commercial and delivery **context** | Any verification of the payment reported in §4.2 |
| The open decisions that must be closed | Any legal or tax conclusion |
| The visual system, asset plan, screen catalog, prompt pack and design-engineering rules as **specification** (`30`–`37`) | **Any UI design approval.** `30`–`37` are `PROPOSED`; §4.1's second-instalment trigger has therefore not occurred and no document in this suite constitutes it (`R-45`, and `OD-DOC-36` on what would count as evidence) |

---

## 9. Open Commercial Decisions

| ID | Question | Owner | Deadline | Severity |
|---|---|---|---|---|
| OD-COM-01 | Is a written agreement executed, and where is it filed? The technical suite has no copy. | Project owner | Before the next instalment | `[BLOCKER]` |
| OD-COM-02 | Should the remaining instalments be settled by bank transfer against a GST invoice rather than cash? | Project owner | Before the second instalment | `[BLOCKER]` |
| OD-COM-03 | What are the defined acceptance and handover conditions referenced in §4.1? | Project owner + development partner | Before the third instalment | `[BLOCKER]` |
| OD-COM-04 | What exactly is included in the ₹60,000/year single-city service? | Both parties | Before the first renewal | `[IMPORTANT]` |
| OD-COM-05 | Who is the contractual counterparty for the platform itself — the development partner, a platform entity, or the owner individually? This determines who invoices the customer. | Project owner + counsel | Before production invoicing | `[BLOCKER]` |
| OD-COM-06 | Which entity owns the domain, the source code and the documentation? | Both parties | Before go-live | `[BLOCKER]` |
| OD-COM-07 | What is the third-party consumption cost allowance inside the annual service fee? | Both parties | Before the first renewal | `[IMPORTANT]` |
| OD-COM-08 | Is the Partner web dashboard in the initial scope, and at what price? | Project owner | Before Phase 1 | `[IMPORTANT]` |
| OD-COM-09 | Is there a defect-correction window after acceptance, and for how long? | Both parties | Before the third instalment | `[IMPORTANT]` |
| OD-COM-10 | Who is liable for a data breach originating from the platform — and is there cyber insurance? | Both parties + counsel | Before Phase 2 | `[IMPORTANT]` |
| OD-COM-11 | Is the six-month delivery target absolute, or conditional on the §3.2 dependencies being ready on time? | Both parties | Immediately | `[IMPORTANT]` |
| OD-COM-12 | What is the IP position on the design assets, the generated clients and the documentation? | Both parties | Before the second instalment | `[IMPORTANT]` |
| OD-COM-13 | **Is the platform-mode feature (`38`) inside the initial development fee, or is it a priced variation?** It is §3.2 item 15 today, which is to say outside until the agreement changes in writing. Two sub-questions decide the money: whether L3 enforcement's additional database identity (`OD-DOC-43`) is "environment provisioning" under §3.1 item 10 or new infrastructure, and who pays for the transactional-email channel the promotion ceremony needs, since channel consumption is already owner-side under §3.2 item 1 and the channel is **not procured** (`24` P-06, `OD-MAIL-01`). | Both parties | Before Phase 1 work starts on `FR-MODE`, and before any date is quoted for it | `[IMPORTANT]` |

---

## 10. Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.6 | 2026-10-21 | Founder + Product Lead (platform-mode pass) | §3.2 gained **item 15** and the scope-creep control gained its first live case. The platform-mode feature is **not one of §3.1's twelve areas** — it was instructed on 2026-10-21, after that list was written — so this document states it as **outside the initial development fee until the agreement is changed in writing**, `[PROPOSED]`, unapproved and **unpriced**. The note records what that actually costs: the `record_origin` migration touches all 88 tables, L3 enforcement needs an extra database connection identity (`OD-DOC-43`), and the promotion ceremony consumes a transactional-email send that is **not procured** (`24` P-06, `OD-MAIL-01`) — so two owner-side procurements gate a feature nobody has yet priced. **§9 gained `OD-COM-13`** asking exactly that, mirrored into `21` §7.1 in the same act. **No amount, instalment, percentage, deliverable or payment trigger was changed**, and nothing here constitutes agreement to build the feature. | §3.2 item 15 + note, §9 |
| 1.5 | 2026-10-21 | Product Lead + Founder (design-engineering structure pass) | **No amount, instalment, trigger, term, date, deliverable, exclusion or scope boundary was altered.** §4.1’s annotation was restated with the register’s measured span (`OD-DOC-30`…`37` → `OD-DOC-30`…`39`) and gained the sentence this pass makes necessary: `35`, `36` and `37` — a folder tree, an admitted library table and a component contract — **are not a designed screen**, so none of the three can be read as the event on which the second ₹1,00,000 becomes payable. `R-45` (no approver for “UI design approval”) and `OD-DOC-36` (whether an empty container can certify the gate) are untouched and still open; this pass sharpens the distinction rather than closing either. | §4.1, Revision History, header |
| 1.4 | 2026-10-21 | Product Lead + Founder (palette, storage and prompt-pack pass) | §4.1's annotation **restated, not relaxed — no amount, instalment, trigger, term or date changed.** The decision span tied to the UI-approval trigger widened from `OD-DOC-30`…`33` to `OD-DOC-30`…`37` and the checklist it points at from eight to **twelve** decisions (`30` §12), because the palette pass registered four more. The note now names `OD-DOC-36` as the logically prior question the payment trigger depends on: under the owner's placeholder-first direction (`30` §5.3) a reviewable screen may have every media slot as an empty container, so a layout-only approval could be presented as the event that makes ₹1,00,000 payable — which is `R-45` sharpened, not a new risk. §8's corresponding row widened to `30`–`34` and records that **no image has been generated** in this workspace. `OD-COM-01` (no executed agreement) and every amount above remain `[PROPOSED]`. | §4.1, §8, header, Revision History |
| 1.3 | 2026-10-21 | Product Lead + Founder (design-system and asset pass) | §4.1 annotated, **no amount, trigger or term altered**: the phrase "after UI design approval" is a payment trigger that no document defines — no approver, no scope, no evidence, no partial-approval rule — so it is now named as risk `R-45` (`19` §2.4) and tied to `OD-COM-03` and `OD-DOC-30`…`33`. §8 gains the row the table was missing: the suite specifies the visual system and asset plan but does **not** cover any UI design approval, and because `30`–`33` are `PROPOSED` the second instalment's trigger has not occurred. The design pass explicitly did not approve or trigger anything. All amounts remain `[PROPOSED]` and `OD-COM-01` (no signed agreement) is still open. | §4.1, §8, header, Revision History |
| 1.2 | 2026-10-21 | Product Lead | Audit pass 3 (continued). Two citation defects marked, neither resolved here because both are the founder's to close. §4.5 item 9 assigns **production access approval** to `13` §5, and `13` §5 contains no such rule — registered as `OD-DOC-22` (`[BLOCKER]`, before provisioning production), so until it closes the item is a commitment with no referent. §6.2 item 4's claim that every production access is recorded in `audit_events` and reviewed monthly by IC-03 now points at `OD-DOC-21` (the access review is monthly here and in `19` §4.2, quarterly in `13` §5.3 and `19` R-28) and at the fact that `audit_events` records authenticated application principals, not a shell on a host. All amounts and terms remain `[PROPOSED]` and nothing in this document is executed. | §4.5, §6.2, Revision History |
| 1.1 | 2026-10-21 | Product Lead | Audit pass 3. §1.1 evidence standard restated: the stricter commercial rule ("an assertion is `[CONFIRMED]` only when a signed document or verifiable record exists") is now labelled **`[EXECUTED]`**, because `README` §4 reserves `[CONFIRMED]` for statements established in project context or an accepted decision record, and applying it to a *standard* rather than to a *statement* was the only use of that label in the suite that did not match its definition. The rule itself is unchanged and remains the stricter of the two — this is a vocabulary fix, not a relaxation. Nothing in §4 is a committed figure; all amounts remain `[PROPOSED]`. §9's twelve commercial decisions are now mirrored into `21` §7.1 so `21` is the register of record. | §1.1, §9 |
| 1.0 | 2026-10-21 | Product Lead | Initial commercial and delivery-boundary document. Records the reported commercial context, defines the initial scope boundary, and raises 12 commercial decisions. | All |

---

## 11. Related Documents

| Document | Relevance |
|---|---|
| `00-Project-Charter` | Objectives, scope in/out, dependencies |
| `17-Roadmap-and-Delivery-Plan` | Phase plan and exit criteria that map to §5.1 acceptance |
| `18-Team-Structure-and-RACI` | Who performs and signs each deliverable |
| `19-Risk-Compliance-and-Register` | Supplier, tax and data risks |
| `22-Architecture-Decision-Records` | ADR-021 (partner dashboard), ADR-024 (tax review) |
| `29-Release-and-Deployment-Checklist` | The release gates behind §5.1 |
| `21-Open-Decisions-and-Questions` | The technical open-decision register |
