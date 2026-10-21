# 19 — Risk, Compliance & Register

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-19 |
| Version | 1.8 |
| Status | Approved for Design & Development |
| Owner | Founder / Sponsor + Engineering Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `00` §12, `13` §6, `21` §1, `26` §4 |

---

## 1. Risk Management Approach

| Aspect | Approach |
|---|---|
| Method | Qualitative risk assessment: **Likelihood (L)** × **Impact (I)** = **Severity (S)** |
| Scale | L and I each 1–5. S = L × I. |
| Bands | S ≥ 20 **Critical** · 12–19 **High** · 6–11 **Medium** · ≤ 5 **Low** |
| Cadence | Reviewed weekly by the delivery leads; formally quarterly with the founder |
| Ownership | Every risk has a single named owner |
| Escalation | Any risk that increases by ≥ 3 severity points, or any Critical risk, goes to the founder within 24 h |
| Treatment | **Mitigate** (reduce L or I) · **Avoid** (don't do it) · **Transfer** (insurance/vendor SLA) · **Accept** (with a documented rationale) |
| Closure | A risk is closed only when the underlying condition no longer exists — not when the mitigation is in place |

---

## 2. Risk Register

**50 risks** — R-01…R-37 as originally issued, R-38…R-44 added in audit pass 3, **R-45** added by the
design-system pass, **R-46**/**R-47** added by the visual-system and storage pass, **R-48** added by
the design-engineering structure pass, and **R-49**/**R-50** added by the platform-mode pass. Under the §1 bands only one row is **Critical** (S ≥ 20): **R-44**, the decision
backlog — which is honest, because
its impact is the amplification of every other row. The highest-scoring **High**-band rows in the register
are **R-46** (S 16 — production imagery blocked at the CSP, the media-store direction), **R-48** (S 16 —
the backend framework is specified two ways at the moment of scaffolding, `OD-DOC-38`), **R-50** (S 16 —
the delete protection as stated collides with the erasure and purge promises in `09` §6) and the two
pre-existing rows **R-04** and **R-22**, all at 16, so the new rows do not outrank them; **R-49** (S 15 —
the guard real only where data can be deleted anyway) joins the 15 band with R-39, R-41 and R-42; then come R-39
(the settlement direction is contradicted across the documents, `OD-DOC-01`), R-41 and R-42 (the
development partner holds the access and the ownership position is unsettled, `OD-COM-06`/`OD-COM-12`)
at S 15 each, with R-38 (partner fraud) and R-45 at S 12. No pre-existing risk reached S 20, which is itself worth noting: with L and I
capped at 5, a register where nothing is Critical usually means the scoring is being read as
"probability of an outage" rather than "consequence of a wrong decision".

### 2.1 Technical & Platform Risks

| ID | Risk | L | I | S | Owner | Mitigation | Contingency | Status |
|---|---|:--:|:--:|:--:|---|---|---|---|
| R-01 | Commission or settlement miscalculation causing financial loss | 3 | 5 | **15** | Eng Lead + Finance | Pure domain module; ≥95% coverage; golden-master suite; immutable ledgers; nightly reconciliation assertions; SoD on issue/approve | Halt settlement runs; reconcile from the ledger; issue credit notes | Open |
| R-02 | Snapshot drift — a booking priced differently from its invoice | 2 | 5 | **10** | Eng Lead | Snapshot written in the same transaction; immutable triggers; invoice derived from the snapshot; provenance chain | Rebuild affected invoices from snapshots; credit notes | Open |
| R-03 | Coupon abuse / double redemption | 3 | 3 | 9 | Eng Lead | Unique redemption per booking; server-side validation; usage caps in a transaction; velocity anomaly detection | Freeze the coupon; reconcile redemptions | Open |
| R-04 | Technical supply shortfall in a new city → poor fill rate | 4 | 4 | **16** | Ops Lead | Seed 50 technicians pre-launch; coverage board; daily onboarding; category-scoped capacity alerts | Pause the city launch; redirect demand to a covered area with a clear ETA | Open |
| R-05 | Single-VPS failure → full outage | 2 | 5 | 10 | DevOps | Automated backups; WAL archiving; monthly restore drill; documented DR runbook; 2 API instances | Provision a new VPS and restore (< 2 h) | Open |
| R-06 | Payment gateway outage blocks booking | 2 | 4 | 8 | Eng Lead + Finance | `PAY_AFTER` mode; webhook queue; the gateway is not on the synchronous path for booking creation | Route to UPI-direct collection; reconcile manually | Open |
| R-07 | Telephony provider outage blocks the call channel | 2 | 3 | 6 | Support Lead | In-app/web booking unaffected; callback queue; provider SLA | Route to a secondary number; WhatsApp-first support | Open |
| R-08 | Data loss from a bad migration | 2 | 5 | 10 | Eng Lead + DevOps | Expand→migrate→contract; rehearsal on a production-like snapshot; auto-rollback; backups | Restore from backup + WAL replay | Open |
| R-09 | Third-party API change breaks a critical path | 3 | 4 | **12** | Eng Lead | Adapter pattern; contract tests; a manual fallback for every integration | Feature-flag the integration off and use the fallback | Open |
| R-10 | Google Maps quota/billing exhaustion | 3 | 3 | 9 | DevOps | Geocode caching (30 days); Distance Matrix batching; quota alerts | PostGIS-only operation with pincode fallback | Open |
| R-11 | Push notification delivery failure (FCM) | 2 | 3 | 6 | Eng Lead | WhatsApp/SMS fallback chain | SMS-only mode | Open |
| R-12 | Key-person dependency on the money-path code | 3 | 4 | **12** | Eng Lead | Mandatory training; two engineers with money-path access; pairing; documented invariants | Bring in a finance-domain consultant | Open |
| R-13 | Performance degradation as bookings scale | 2 | 3 | 6 | Eng Lead | Indexing discipline; cursor pagination; read models; caching; a nightly performance suite | Scale horizontally; move the DB to managed | Open |
| R-14 | The modular monolith develops accidental coupling and becomes hard to change | 3 | 3 | 9 | Eng Lead | Enforced module boundaries via an architecture test; `domain/` purity; contract-first APIs | Extract the offending module per `08` §8.2 | Open |
| R-48 | **The backend framework is specified two different ways at the exact moment a repository would be created.** `ADR-011` is **Accepted** (NestJS + TypeScript, Redis 7 + BullMQ) and the same tree is copied into `14` §2, `08` §9 and `27` §6; the owner's direction of 2026-10-21 asks for a **FastAPI** folder and file structure to be the reference design and engineering follow. Nothing is scaffolded yet, so the cost today is one decision; after the first commit it is a re-platform. **Status 2026-10-21 — the "yet" is gone and the cliff moved, not removed:** the owner directed "scaffold as base on docs", `git init` produced a documentation-only baseline, and `14` §2 / `35` §3+§5–§8 exist as **221 empty directories** (`.gitkeep` only, in 164 leaves; `README` §16). That is the cheap-to-reverse part — a folder rename is not a re-platform, and the skeleton carries no `package.json` precisely so it stays that way. The exposure is now the **first source file and the first migration**, which is where the score's "after the first commit" clause actually bites. | 4 | 4 | **16** | Founder + Eng Lead | Close `OD-DOC-38` **before** the first source file, `package.json` or migration (`git init` and the empty directory skeleton already happened, so that clause is now historical): either a new ADR supersedes `ADR-011`'s backend row (`22` §5) with matching edits to `14`/`08`/`15`/`16`/`27`/`README` in one change (`DC-04`), or the instruction is withdrawn. `35` §4 documents the contingent Python layout so the 16 module boundaries, `ES-01` purity and `ADR-012`'s OpenAPI bridge survive either answer, and `35` §2.1 lists the eight coupled items rather than letting them be discovered | Every client is **generated** from the OpenAPI document, so a change of backend language does not invalidate the Flutter apps (which already share no types — `ADR-011`'s own acknowledged limitation) or the React screens; the salvage path is a rewritten `apps/api` package plus its pipeline, not four rewritten front ends | Open |
| R-49 | **The delete protection is real on paper and absent where the data actually lives.** Three independent routes reach the same outcome: `PM-03` makes `TESTING` the default, so a freshly provisioned production database with no mode row is **unprotected until someone runs a ceremony that has no reason to exist yet** (`38` §10); a guard implemented at the UI or API layer only (`38` §7 L1/L2) is bypassed by anyone holding a connection string, including the development partner whose access position `R-41`/`R-42` already flag; and an operator who has just watched a screen refuse a delete has been taught that refusals are cosmetic. | 3 | 5 | **15** | Eng Lead + Security Owner | Close `OD-DOC-43` and `OD-DOC-44`; enforce at L3 (a role with no `DELETE` grant) and not only at L2; make the `16` §5 pipeline fail a `prod` deploy that would boot in `TESTING` without a recorded bootstrap exception (`38` PM-04, `14` `ENV-07`); show the mode on every staff surface (`PM-16`) so the state is never a guess; add the `29` §4/§7 gate items. `19` scores this below `R-48` deliberately — the framework decision is a fork in the road, this one is a hole in a fence | Recover from the backup and WAL chain (`13` §10, `16` §5.6) — which is exactly why `17` P0-13's **successful** restore drill is a pre-condition of promotion (`38` PM-22) and not a Phase 2 nicety. Without it the contingency is a story | Open |
| R-50 | **The protection as literally stated is unimplementable without breaking a promise the suite already makes.** "Production data cannot be deleted" collides with `09` §6 (DPDP erasure on request; `webhook_inbox` 30 days; `notification_deliveries` 90 days; tracking history 90 days; `audit_events` payload 24 months), with `03` §7.3's `ACTIVE ⇄ DELETED` identity state and with `01` §5's erasure commitment. A blanket trigger blocks the purges the retention design depends on; a targeted trigger plus an operator-editable exception list re-creates the delete button the feature exists to remove. Either way the platform ends up either non-compliant or unprotected, and the choice gets made by whoever writes the first migration. | 4 | 4 | **16** | Founder + compliance owner, with counsel (`ADR-024`) | Close `OD-DOC-40` **before** any guard code exists, and `OD-DOC-41` before the first invoice-sequence migration. Implement the four-class taxonomy (`38` §6.1): soft delete permitted, code-defined retention purge permitted on a reviewed allow-list, statutory erasure routed through a named dual-controlled routine if reading (i) is chosen, and only class A refused. `22` `ADR-026` keeps the decision visible as `Proposed` rather than burying it in a schema | Ship the guard with the purge allow-list **hard-coded and code-reviewed** (never dashboard-editable, `03` `FL-10`) and defer class C by queueing erasure requests with a dated acknowledgement to the data principal — lawful only while `OD-DOC-40` is genuinely undecided, and it must be recorded as an open compliance exposure, not as silent behaviour | Open |

### 2.2 Financial & Tax Risks

| ID | Risk | L | I | S | Owner | Mitigation | Contingency | Status |
|---|---|:--:|:--:|:--:|---|---|---|---|
| R-15 | GST / place-of-supply error → notice and penalty | 3 | 4 | **12** | Finance + Tax advisor | Tax advisor opinion before Phase 2; per-registration config; CGST/SGST/IGST logic in a pure, tested module; 20-invoice pre-launch review | Voluntary correction; reissue corrected invoices | Open |
| R-16 | Platform/partner role mischaracterised (agent vs principal) → wrong invoices | 2 | 5 | 10 | Finance + Legal | Written legal opinion (`OD-07-03`) before invoicing goes live | Reissue invoices as credit/debit notes | Open |
| R-17 | TDS under 194C not deducted → interest and penalties | 3 | 3 | 9 | Finance | Tax advisor opinion (`OD-07-02`); TDS fields on the commission invoice; Form 16A generation | Deduct in the next cycle with interest | Open |
| R-18 | Settlement dispute volume overwhelms finance | 3 | 3 | 9 | Finance + Ops | Clear booking-wise statements; self-serve dispute in the Partner App; dispute SLA | Temporary dedicated dispute queue | Open |
| R-19 | Partner pays late → technician income and retention suffer | 3 | 3 | 9 | Finance + Ops | D+5 reminder, D+7 escalation; wallet/credit as an interim instrument `[PROPOSED]` | Advance the disputed amount from a float | Open |
| R-20 | Cash/collection leakage or unreconciled gateway amounts | 3 | 4 | **12** | Finance | Daily gateway reconciliation; manual payments audited with a reference; daily ledger balance assertion | Freeze payouts; reconcile line by line | Open |
| R-38 | **Partner fraud or collusion** — a branch creates repeat bookings through a friendly customer or technician to farm coupons, ratings or settlement credit | 3 | 4 | **12** | Finance + Ops | Coupon funding rules separate platform and partner money (`07` §5); the same-device / same-phone / same-address clustering on `bookings`; commission accrued but not paid until the settlement dispute window closes (`ADR-009`); an eligibility ceiling on how many jobs one customer phone can book per week | Hold the settlement line, open a `PARTNER_SUPPORT` ticket, suspend the branch under `23` §9 | Open |
| R-39 | **The settlement money direction is contradicted across the documents** (`OD-DOC-01`), so a payment run can be executed the wrong way | 3 | 5 | **15** | Founder + Finance | `07` is named the money document of record; the billing module may not be built until `OD-DOC-01` closes; a two-person check on any outbound transfer | Reverse via a credit/debit note pair (`ADR-015`) — never an edit. A wrong-direction payment is not a clerical error, it is a recoverability problem | Open |
| R-40 | **Cash instalments leave no auditable record.** `26` §4.2 reports the first tranche collected in cash with a receipt that is not in the repository | 4 | 3 | **12** | Founder + Finance | Settle the remaining instalments by bank transfer against a GST invoice (`OD-COM-02`); file every receipt with a hash and a date; no `[CONFIRMED]` marker is applied to a commercial fact on the strength of a report alone | Reconstruct from bank records; obtain written confirmation from the counterparty | Open |

### 2.3 Operational & Supply Risks

| ID | Risk | L | I | S | Owner | Mitigation | Contingency | Status |
|---|---|:--:|:--:|:--:|---|---|---|---|
| R-21 | Branch adoption stalls → stranded cities | 3 | 4 | **12** | Founder + Ops Lead | Owner-assigned branch P&L; weekly ops review; the partner-branch model as a low-capex fallback | Convert the branch to a partner branch or close it | Open |
| R-22 | Technician quality varies → rating falls → demand falls | 4 | 4 | **16** | Ops Lead + Partner Ops | KYC verification; skill levels; performance scoring; penalties; branch quality checks; rating-weighted ranking | Pause low-rated technicians; tighten onboarding | Open |
| R-23 | Support volume exceeds staffing → long waits, lost bookings | 3 | 3 | 9 | Support Lead | IVR deflection; queue dashboards; callback queue; agent productivity metrics | Extend hours; add temporary agents | Open |
| R-24 | Technician no-show / late arrival → SLA breaches | 3 | 4 | **12** | Ops Lead | Acceptance timers; arrival SLA with escalation; penalties; punctuality in the score; a backup technician pool | Auto-reassign to the next candidate | Open |
| R-25 | Partner branch underperforms → reputational damage | 2 | 4 | 8 | Partner Ops | Approval with a due-diligence checklist; quality audits; clear territory terms; suspension rights | Suspend the branch and absorb the territory | Open |
| R-26 | Technician onboarding pipeline stalls (KYC backlog) | 3 | 3 | 9 | Partner Ops | 48 h approval SLA; daily approval queue; manual KYC fallback | Temporarily raise the acceptance threshold | Open |

### 2.4 Security, Legal & Regulatory Risks

| ID | Risk | L | I | S | Owner | Mitigation | Contingency | Status |
|---|---|:--:|:--:|:--:|---|---|---|---|
| R-27 | Data breach of customer PII | 2 | 5 | 10 | Security Owner | Encryption at rest and in transit; RBAC + scope; log redaction; pen testing; DPDP controls; a breach runbook | Breach notification within 72 h; credential rotation; customer advisory | Open |
| R-28 | Insider misuse of financial data | 2 | 4 | 8 | Founder + Eng Lead | SoD; override logging; masking; quarterly access review; audit alerts | Revoke access; forensic audit; disciplinary action | Open |
| R-29 | Insecure direct object reference exposes another branch's data | 2 | 5 | 10 | Eng Lead | Scope predicates in SQL; ownership checks; an automated scope-isolation sweep in CI | Disable the endpoint; audit affected access logs | Open |
| R-30 | Non-compliance with consumer protection rules (pricing clarity, refunds) | 2 | 4 | 8 | Legal + Product | Published pricing policy; displayed cancellation policy; a grievance officer; a complaint SLA | Policy correction; proactive refunds | Open |
| R-31 | WhatsApp template rejection → notification quality drops | 3 | 3 | 9 | Growth | Templates submitted early; SMS as a first-class fallback; an approval tracker | SMS-only mode; in-app notifications | Open |
| R-32 | Payment merchant account delay or freeze | 2 | 5 | 10 | Founder + Finance | Apply in Phase 0; maintain a sandbox account; keep a second gateway evaluated | Manual collection with a reconciliation process | Open |
| R-41 | **Concentration of access in the development partner.** `26` §6.1 records that domain, DNS, hosting and server administration stay under Locky Dev's access during the engagement — one party can take the platform offline, change DNS, or read production data | 3 | 5 | **15** | Founder | Named break-glass platform accounts held by the business, not the developer; documented credential custody and rotation (`25`); an export-and-migration rehearsal that proves the business can operate without that access (`26` §6.3, `OD-COM-06`) | Immediate credential rotation and DNS transfer; invoke the continuity clauses agreed under `OD-COM-06` | Open |
| R-42 | **Ownership of the domain, the source and the documentation is not settled** (`OD-COM-06`, `OD-COM-12`), so a handover dispute could leave the business unable to prove it owns what it is running | 3 | 5 | **15** | Founder + counsel | Register the domain and every account in the **business's** name from day one, regardless of who administers them; assign IP in writing before the second instalment; keep the documentation set under version control the business controls | Counsel letter; escrow of credentials and source; the register in `26` §6.3 is the fallback | Open |
| R-43 | **Regulatory change during the build** — e-invoicing thresholds, GST rate or place-of-supply clarifications, or DPDP rules crystallising after the schema is fixed | 3 | 4 | **12** | Legal + Finance | Tax and rate values are configuration, never literals (`07` §6, `OD-DOC-02`); the audit trail and retention matrix already satisfy the record-keeping obligations in `19` §3; a Phase 2 compliance re-review gate in `29` §17 | Re-run the tax advisor opinion; adjust configuration and reissue documents as credit/debit notes, not edits | Open |
| R-45 | **The second instalment is triggered by an event nothing defines.** `26` §4.1 makes ₹1,00,000 payable "after UI design approval", but no document says what is approved, by whom, in what form, or what happens if approval is partial — while `OD-DOC-30` (the palette), `OD-DOC-31` (dark mode), `OD-DOC-32` (font sourcing) and `OD-COM-03` (the acceptance conditions §4.1 refers to) are all open and `30`–`37` are `PROPOSED`. Two parties can each reasonably believe the gate has, or has not, occurred | 3 | 4 | **12** | Founder + development partner, in writing | Before any design work is presented: a written definition of the design gate (which surfaces, which states, which evidence — `30` §12's twelve decisions are the natural checklist), a named approver, and an explicit statement that a partial approval does not trigger the instalment. Record the approval as a dated artifact, not a conversation (`DEC-03`) | Negotiate the trigger before invoicing rather than after; the `26` §4.1 table is `[PROPOSED]` and has never been signed, so the clause is still open to be written properly | Open |
| R-46 | **Production imagery is blocked by the platform's own CSP, or its privacy rule is broken — whichever way the storage question is answered.** The owner's `[REPORTED]` direction makes Cloudinary the primary media store (`OD-DOC-34`) while `13` §5.2's `img-src 'self' …` does not list it, `24` §11 states that no bucket, prefix or object is publicly readable, and `09` §8 classifies job photos as `PERSONAL` ("job photos can contain a person and their home"). Either every image fails to render in production, or a public CDN object is created against the stated rule, or `PERSONAL` media is moved to a third-party processor nobody has assessed. Development works, production does not, and the customer discovers it. | 4 | 4 | **16** | Founder + Eng Lead + Security Owner | Decide **per data class** before any upload is coded: catalogue and marketing imagery on a CDN host **named in `img-src`**; job evidence and any `PERSONAL`-derived media on the platform's own storage behind short-lived signed URLs. Amend `13` §5.2 and `24` §11 in the same change, not in a follow-up. Confirm the processor position with counsel before any real job photo leaves the platform's boundary — this row names the exposure, it reaches no legal conclusion | Serve every image from `'self'` with no third-party processor: contradicts no document and needs no CSP edit, but forgoes the transformation and optimisation the storage direction was asked for | Open |

### 2.5 Product & Market Risks

| ID | Risk | L | I | S | Owner | Mitigation | Contingency | Status |
|---|---|:--:|:--:|:--:|---|---|---|---|
| R-33 | Incumbent competitor responds with aggressive pricing | 3 | 4 | **12** | Founder + Growth | Quality differentiation; fast time-to-service; transparent pricing; technician loyalty | Category focus on niches incumbents serve poorly | Open |
| R-34 | Scope creep from service-category expansion | 4 | 3 | **12** | Product Lead | The workflow engine enforces "configuration, not code"; a category launch gate; a published catalogue plan | Defer categories to Phase 4 | Open |
| R-35 | Low repeat rate — customers try once and leave | 3 | 4 | **12** | Product + Growth | "Book again"; favourite technicians; quality; reminder campaigns; a warranty/redo promise | Push subscription packages | Open |
| R-36 | Negative early reviews damage launch momentum | 3 | 4 | **12** | Ops Lead | Seeded quality technicians; a review moderation process; rapid complaint resolution | Temporarily pause paid acquisition in a weak area | Open |
| R-37 | Pricing transparency backfires (customers anchor on the lowest band) | 3 | 2 | 6 | Product + Finance | Show the expected price for the chosen technician, not only the range; the "why this price" explainer | Adjust the band presentation | Open |
| R-44 | **The decision backlog outruns the build.** 231 open decision rows, 45 of them blockers, none formally closed; every document in the set is written against recommendations rather than decisions, and `DEC-05` has no cadence to enforce | 5 | 4 | **20** | Founder | A weekly decision slot with the founder, worked strictly in the `README` §13.2 order; a blocker closed is recorded in `21` §10 the same day and moves the affected documents from `[OPEN]` to `[CONFIRMED]`; no module enters build while a `[BLOCKER]` in its own area is open (`DEC-06`) | Apply the documented recommendation as the default and record it as a decision, accepting the rework — a wrong assumption that is *known and owned* is cheaper than an open question that blocks five documents | Open |
| R-47 | **The design gate is certified against screens that contain no designed content.** The owner directed placeholder-first delivery (`30` §5.3, `OD-DOC-36`), so every image slot is a blank container while `26` §4.1's second ₹1,00,000 instalment hangs on "UI design approval" and `33` marks all 68 screens `UNDESIGNED`. A layout review is not an image review: approving a screen with empty containers and then treating that as brand approval means the artwork that carries a marketing hero or a store listing is never looked at by the person whose signature pays for it — and `R-45`'s undefined trigger gets "answered" by an event that proves nothing. Deliberately scored one band below `R-45` to avoid double-counting the same money event. | 3 | 3 | **9** | Founder + Product Design Lead | Write the gate's evidence list before presenting anything: tokens applied (`30` §3–§5), all 68 screens at their `33` §5 state matrix, one vendored stroke-consistent vector icon set, **at least one real content set** rendered, accessibility measured. Record the approval as a dated artifact with that list attached, and state that a partial (layout-only) approval does not trigger the instalment | Ship placeholder-only screens and generate artwork after the upload system exists — acceptable **only** if the gate is explicitly recorded as layout-only, otherwise the money event has been certified against an empty page | Open |

---

## 3. Compliance Register

| Area | Obligation | How AmmPal Meets It | Owner | Status |
|---|---|---|---|---|
| **GST registration** | Registration per operating state | `tax_registrations` per entity and state; selected at invoicing | Finance | Pending — `OD-07-01` |
| **GST invoicing** | Correct tax components per the place of supply | CGST+SGST intra-state, IGST inter-state, itemised per line | Finance + Eng | Designed (`07` §6) |
| **Place of supply** | Determined by the customer's location | Captured on the booking from the address snapshot | Eng | Designed |
| **Tax on commission** | GST on the platform's commission | `commission_invoices` carry the tax | Finance | Designed |
| **Invoice numbering** | Gapless, sequential per entity and financial year | `invoices.number` with a unique constraint per entity + FY | Eng | Designed |
| **Record retention** | Statutory books retention (8 years) | Retention policy in `09` §6 with purge jobs | Finance + Eng | Pending — `OD-NFR-06` |
| **TDS (Sec. 194C)** | Deduct at source on commissions, if applicable | Pending a tax opinion | Finance | Open — `OD-07-02` |
| **Agent vs principal** | Determines who the supplier on the customer invoice is | Pending a legal opinion | Legal + Finance | Open — `OD-07-03` |
| **E-invoicing / e-way bill** | If thresholds are crossed | Not in v1.0 scope; monitored | Finance | Deferred |
| **DPDP Act 2023** | Consent, purpose limitation, minimisation, retention, rights, breach notification | Consent records; retention schedule; erasure flow; grievance channel; breach runbook | Legal + Eng | Designed (`13` §6.1) |
| **Data residency** | India | All infrastructure and vendors in India | Eng | Designed |
| **TRAI / DND** | Commercial voice respects DND; transactional exempt | Outbound campaign suppression; transactional flows documented | Support + Eng | Designed (`11` §5) |
| **WhatsApp Business** | Pre-approved templates for business-initiated messages | Versioned, approved template registry; approval tracker | Growth | Designed |
| **PCI-DSS** | SAQ-A via the gateway (no card data stored) | Hosted checkout only; no PAN/CVV in any system | Eng | Designed |
| **Consumer Protection (E-Commerce) Rules** | Pricing clarity, grievance officer, no dark patterns, refund policy display | Published pricing and cancellation policies; a grievance channel; an explicit price breakdown | Legal + Product | Designed |
| **Professional tax / labour welfare** | State-level obligations per branch | Tracked as a configurable compliance item per branch | Finance | Open |
| **Access to records** | Statutory access to books and records | Immutable, exportable records with an audit trail | Eng | Designed |
| **Call recording consent** | Recording disclosure and consent | IVR disclosure; a retention policy; a 90-day purge | Support + Legal | Pending — `OD-SUP-04` |

---

## 4. Internal Control Framework

### 4.1 Segregation of Duties (SoD)

| Control | Rule | Enforcement |
|---|---|---|
| SOD-01 | Settlement **issue** and settlement **approval** must be held by different accounts | Blocked at the service layer (`03` §2.1) |
| SOD-02 | No account holds both `SUPER_ADMIN` and `ACCOUNTANT` | Blocked at role assignment |
| SOD-03 | An account holding `finance:*` write permissions cannot hold `booking:*` write for the same branch | Checked at assignment and re-checked at runtime |
| SOD-04 | No user approves their own request (self-approval blocked) | `403 SELF_APPROVAL_BLOCKED` |
| SOD-05 | Out-of-band price overrides require a distinct permission, a reason, and generate a finance alert | `audit_override_log` + an `ADMIN` monthly report |

### 4.2 Key Controls

| ID | Control | Frequency | Evidence |
|---|---|---|---|
| IC-01 | Nightly reconciliation: invoices, settlements and the general ledger balance | Daily | Reconciliation report; a mismatch is P0 |
| IC-02 | Audit chain verification (hash continuity) | Daily | Verification job; a break is P0 |
| IC-03 | Access review (all internal accounts, roles and scopes) | Monthly | Signed review record |
| IC-04 | Override report review | Monthly | `ADMIN` review with actions |
| IC-05 | Bank reconciliation (gateway settlements vs. recorded payments) | Daily | Finance report |
| IC-06 | Tax review (a sample of invoices per state) | Monthly | Finance sign-off |
| IC-07 | Backup restore drill | Monthly | Drill record |
| IC-08 | Vulnerability & dependency review | Monthly | Scan report |
| IC-09 | Document expiry review (technician KYC, partner GSTIN) | Daily (automated) | Expiry report |
| IC-10 | Partner settlement dispute review | Weekly | Dispute log |
| IC-11 | Complaint root-cause review | Weekly | QA report |
| IC-12 | Price band compliance sweep (no out-of-band prices without an override) | Daily | Automated report |

### 4.3 Policy Documents to Publish

| Document | Audience | Owner |
|---|---|---|
| Privacy policy | Customers, partners, technicians | Legal |
| Terms of service | Customers, partners, technicians | Legal |
| Refund & cancellation policy | Customers | Product |
| Warranty & redo policy | Customers | Product |
| Technician partner agreement | Technicians | Legal |
| Partner branch agreement | Partner orgs | Legal |
| Pricing & commission policy | Partners, technicians | Finance |
| Fair usage & acceptance policy | Technicians | Ops |
| Grievance redressal policy | Public | Legal |
| Acceptable use & code of conduct | All users | Legal |

---

## 5. Incident Response

### 5.1 Severity

| Level | Definition | Examples | Response |
|---|---|---|---|
| **P0** | Critical business impact | Financial loss, data loss, breach, total outage | Immediate; phone the on-call and the founder |
| **P1** | Significant impact, no workaround | Core flow broken for many users; the settlement job fails | Within 15 min; WhatsApp the on-call |
| **P2** | Limited impact, workaround exists | One surface degraded; a vendor is down with a fallback | Business hours |
| **P3** | Minor | A cosmetic defect; a non-critical report error | Backlog |

### 5.2 Response Process

```
Detect → Triage (severity + scope) → Contain → Communicate → Resolve → Verify → Recover → Learn
```

| Step | Target | Owner |
|---|---|---|
| Detect | Alert fires within 5 min of impact | Monitoring |
| Triage | Severity assigned within 10 min | On-call |
| Contain | Within 30 min for P0 | On-call + Eng Lead |
| Communicate (internal) | Within 30 min for P0 | Eng Lead |
| Communicate (customers/partners) | Within 2 h for P0 | Support Lead + Growth |
| Resolve | Workaround within 4 h; full fix per severity | Eng Lead |
| Verify | Health checks + a reconciliation pass + a test booking | On-call + QA |
| Recover | Full service + backlog clearance | Eng Lead |
| Learn | Post-mortem within 5 working days | Eng Lead |

### 5.3 Post-Mortem Template

1. **What happened** — a plain, factual timeline.
2. **Impact** — users, bookings, money, partners affected.
3. **Root cause** — the technical and the organisational cause.
4. **What went well** — what limited the blast radius.
5. **What went poorly** — where the response failed.
6. **Actions** — each with an owner and a due date; P0/P1 actions become tickets.
7. **Rule changes** — if a business rule must change, an entry in `21` and an update to the affected documents.

**Rule IR-01** — A post-mortem is blameless. It names systems and decisions, not people.

---

## 6. Business Continuity

| Scenario | Continuity measure | Activation time |
|---|---|---|
| A single API instance fails | The load balancer routes to the second | < 30 s |
| The API fails entirely | Failover to the standby region/VPS per the DR runbook | < 2 h |
| Postgres is corrupted | Restore + WAL replay | < 2 h |
| Redis is lost | Cache rebuilds; queues resume from the outbox | < 30 min |
| The payment gateway is down | `PAY_AFTER` mode; manual UPI collection | Immediate |
| Telephony is down | Web/app booking; WhatsApp support | Immediate |
| Maps is down | Pincode → city; PostGIS still resolves areas | Immediate |
| A city must be paused | A feature flag disables bookings for that branch | < 5 min |
| A category must be paused | A feature flag / service-area disable | < 5 min |

**Rule BC-01** — Every business-critical function has a documented degraded mode, and the degraded
mode is exercised at least once per quarter.

---

## 7. Risk Review Template

| Field | Value |
|---|---|
| Risk ID | R-xx |
| Description | What could happen, and under what conditions |
| Category | Technical / Financial / Operational / Security / Legal / Product |
| Likelihood (1–5) | |
| Impact (1–5) | |
| Severity | L × I |
| Owner | A single named person |
| Treatment | Mitigate / Avoid / Transfer / Accept |
| Mitigation actions | Specific, owned, dated |
| Contingency | What we do if it happens |
| Residual severity | After mitigation |
| Review date | Next review date |
| Status | Open / Mitigated / Transferred / Accepted / Closed |

---

## 8. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| OD-RSK-01 | Do we need professional indemnity or cyber insurance before Phase 2? | Founder | Phase 1 |
| OD-RSK-02 | Should a formal data protection officer / grievance officer be appointed from Day 1? | Legal | Phase 1 |
| OD-RSK-03 | What insurance covers partner-branch failures? | Legal | Phase 3 |
| OD-RSK-04 | Is a business continuity insurance policy needed given the DR runbook? | Founder | Phase 3 |
| OD-RSK-05 | Do we need an ISO 27001 readiness programme for enterprise partner contracts? | Founder | Phase 4 |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.8 | 2026-10-21 | Security Owner + Product Lead (scaffold and git-baseline pass) | `R-48` was re-statused after the owner’s scaffold direction and the `git init`. Its description now carries **"Status 2026-10-21 — the ‘yet’ is gone and the cliff moved, not removed"**: the repository and the directories exist, so the risk is no longer an unversioned workspace, it is code being written into a tree whose backend framework is still contested. The mitigation cell now reads *Close `OD-DOC-38` **before** the first source file, `package.json` or migration*. The lead count is re-measured unchanged at **50 rows** (`R-01`…`R-50`, no gap, no duplicate). **No score, owner, band or status field was altered and no risk was closed.** | §2 lead, R-48 |
| 1.7 | 2026-10-21 | Security Owner + Product Lead (platform-mode pass) | Two risks registered from measuring the mode instruction against requirements this suite already carries, rather than from the instruction itself. **`R-49`** (L3 × I5 = **15**, High): the default is `TESTING`, and nothing in day-to-day operation ever forces a promotion, so live data can sit behind an unarmed guard indefinitely while every screen looks correct. **`R-50`** (L4 × I4 = **16**, High): read literally, 'production data cannot be deleted' collides with a data subject's erasure right and with `09` §6's retention purges — the control either becomes unlawful or is bypassed by the job that erases. §2's lead count re-measured **48 → 50 rows** (`R-01`…`R-50`, no gap, no duplicate) and the band statement moved: `R-50` at 16 joins `R-46`/`R-48`/`R-04`/`R-22`, `R-49` sits in the 15 band. **No score was inherited and no risk was closed.** | §2 lead, R-49, R-50 |
| 1.6 | 2026-10-21 | Founder + Engineering Lead (design-engineering structure pass) | **One risk added: `R-48`, S 16 (L 4 × I 4), `High` — §2 now reads 48 risks.** The trigger was the owner asking this session for a “backend Fast API folder and files structure” while `ADR-011` (Accepted, Founder + Engineering Lead) names NestJS and the same NestJS tree is copied into `14` §2, `08` §9 and `27` §6. It is registered as a risk and as `OD-DOC-38` (`[BLOCKER]` in `21` §7) rather than resolved: `35` §2/§4 documents both layouts and decides neither, because the choice is the Founder’s and Engineering Lead’s act in `22` §5, not a documentation edit (`DEC-07`, `DEC-03`). Mitigation is “close `OD-DOC-38` before any scaffold or `git init`, with a superseding ADR”; contingency is “generated clients (`ADR-012`) confine a rewrite to `apps/api`” — the two Flutter surfaces consume only a generated client, which is why the blast radius is 4 and not 5. `R-48` ties `R-46`, `R-04` and `R-22` at the top of the High band, so §2’s band statement now names all four; `R-44` remains the only `Critical` row and its backlog figure was re-measured from `21` rather than incremented by hand — **231 open rows, 45 blockers**. No score, severity band or owner of any pre-existing row was altered, and no risk was closed. | §2, `R-48`, `R-44`, Revision History, header |
| 1.5 | 2026-10-21 | Founder + Engineering Lead (propagation only) | **No risk added, removed, re-scored or re-worded in substance; the band statement is unchanged and `R-44` remains the only Critical row.** Two corrections of fact rather than of judgement: §2's opening now names **R-46** as the register's highest **High**-band row (S 16, tied with the pre-existing R-04 and R-22, so the earlier "four highest additions are R-39/R-41/R-42/R-38" claim was no longer true as written, and the superseded claim is corrected here rather than left to be rediscovered), and `R-45`'s mitigation now points at `30` §12's **twelve** decisions instead of eight and describes the unapproved span as `30`–`34`, since `34` exists. §2's risk count was re-scanned (`R-01`…`R-47`, contiguous, unduplicated) rather than trusted from the previous row. | §2, R-45, Revision History, header |
| 1.4 | 2026-10-21 | Founder + Engineering Lead + Product Lead (visual-system and storage pass) | **Two risks added, one figure restated, and a destructive-script incident recorded honestly.** Added **`R-46`** (§2.4, 4 × 4 = **16**, High): the `[REPORTED]` Cloudinary-primary media direction collides with `13` §5.2's `img-src 'self'`, with `24` §11's "no object is publicly readable" and with `09` §8's `PERSONAL` classification of job photos — three incompatible statements, none of them edited to fit the new instruction (`DEC-07`), registered as `OD-DOC-34` `[BLOCKER]`. Added **`R-47`** (§2.5, 3 × 3 = **9**, Medium): placeholder-first delivery (`30` §5.3, `OD-DOC-36`) lets a layout-only review satisfy a ₹1,00,000 trigger that `R-45` already says is undefined; scored one band below `R-45` so the same money event is not counted twice. R-44 restated **220 → 224 open rows, 43 → 44 blockers** (`21` §7 added `OD-DOC-34`…`37`: one blocker, three important). §2's register size is now **47 risks**; the band statement is unchanged — still exactly one **Critical** row (`R-44`). **Incident, recorded rather than hidden:** a splice script for this step mis-truncated the file at §2.5, and `19` §3–§7 and §8 were rebuilt from `Docs.backup-20261021-083739` (which carries v1.1). §3–§7 contain no post-v1.1 edit and are restored intact; §8's `OD-RSK-01`…`05` list is **byte-identical** to the backup, so the v1.2 entry's "§8" in its *Sections changed* column describes an edit that produced no content change — that claim is now known to be unverifiable and is left as issued rather than quietly corrected. The v1.2 and v1.3 entries below were re-appended verbatim from this session's own record. **Nothing in `19` was approved, re-scored or closed by this row except the two additions.** | §2, §2.4, §2.5, §3–§8 (rebuilt), header, Revision History |
| 1.3 | 2026-10-21 | Founder + Engineering Lead (design-system and asset pass) | Register restated as **45 risks** after **R-45** (§2.4): `26` §4.1 makes the second ₹1,00,000 instalment payable "after UI design approval", and no document defines that event, its approver or its evidence — while `OD-DOC-30`/`31`/`32`, `OD-COM-03` and `30`–`33`'s `PROPOSED` status are all live. Scored 3 × 4 = **12** (**High**), owner **Founder + development partner in writing**, mitigation is to define the gate **before** any design is presented, using `30` §12's eight decisions as the checklist, and to record the approval as a dated artifact rather than a conversation (`DEC-03`). R-44's backlog figure re-derived from `21` §1: **211 → 220 open rows**, blockers **unchanged at 43** (the nine `OD-DOC-25`…`33` rows the design pass registered are all `[IMPORTANT]`). §2's band statement is otherwise unchanged — still exactly one **Critical** row. No existing risk was re-scored, reworded or closed. | §2, §2.4, header, Revision History |
| 1.2 | 2026-10-21 | Product Lead + Engineering Lead + Founder | Audit pass 3. Added **R-38** partner fraud/collusion, **R-39** the settlement-direction contradiction (`OD-DOC-01`), **R-40** cash instalments with no auditable record, **R-41** concentration of access in the development partner (`26` §6.1), **R-42** unsettled domain/source/documentation ownership (`OD-COM-06`/`OD-COM-12`), **R-43** regulatory change during the build, **R-44** the decision backlog itself. Recorded the register size and the band distribution in §2. Corrected the v1.1 entry, which claimed four risks that do not exist in this register. *Same pass, continued:* R-44's backlog figure was re-derived from the register rows rather than inherited — **211 open rows and 43 blockers**, replacing the 190/38 and then 202/41 that `README` §13, `27` §4 and `28` §2 were carrying; the recount is row-anchored and accepts `ORG-*`-led rows as well as `OD-*`, which is where the earlier figures were short; the register size statement in §2 above is unaffected (`19` has 44 risks and that count was verified). | §2, §8, Revision History |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Added the risks surfaced by the audit: the branch/legal-entity conflation risk, the serviceability false-positive risk, the non-serviceable demand loss, and the coupon reservation race. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
