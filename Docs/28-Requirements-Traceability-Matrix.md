# 28 — Requirements Traceability Matrix

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-28 |
| Version | 1.7 |
| Status | Approved for Design & Development |
| Owner | Product Lead + QA Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-22 |
| Depends On | `01`, `03`, `04`, `06`, `07`, `09`, `10`, `12`, `15`, `21`, `22`, `30`, `31`, `32`, `33`, `34` |

---

## 1. Purpose

This matrix maps every material requirement to its definition, owner, workflow, data entities, API
surface, permission, test coverage, source document and open dependencies.

It answers the question a reviewer actually asks: **"if I want to verify this requirement, where do
I look, and how do I know it is met?"**

### 1.1 Status Vocabulary

| Status | Meaning |
|---|---|
| `CONFIRMED` | Established in project context or an accepted ADR |
| `PROPOSED` | Designed and specified; awaiting approval |
| `OPEN` | Awaiting a business decision (`21`) |
| `DEPENDENT` | Blocked on an external provider, legal/tax review, or operational readiness |
| `IMPLEMENTED` | Verified in an inspectable artifact — **no requirement qualifies in this repository** (ADR-025) |

### 1.2 Evidence Convention

Because nothing is implemented, the **Test** column names the *planned* test that will prove the
requirement, and the **Evidence** column names the artifact that will hold the proof once built.
No row claims present-tense verification.

---

## 2. Requirement Classes and ID Namespaces

| Class | Prefix | Defined in | Count |
|---|---|---|---|
| Functional requirements | `FR-<GROUP>-<NN>` | `01` §4 | 99 (the `38` pass added `FR-MODE-01`…`08` in `01` §4.11; 91 before) |
| Business rules | `BR-xx`, `PR-Pxx`, `PR-xx`, `DSC-xx`, `TAX-xx`, `STL-xx`, `CX-xx`, `HS-xx`, `WF-xx`, `TRK-xx` | `00`, `04`, `06`, `07` | 75 (BR 18 · PR 16 · STL 8 · WF 8 · TAX 7 · DSC 6 · CX 5 · HS 4 · TRK 3) |
| Permissions | `<domain>:<action>` and `<domain>:<resource>:<action>` | `03` §3–§4 | 92 distinct tokens from 96 matrix cells (66 three-part, 26 two-part, 19 wildcards) |
| State transitions | `T-xx` booking 37 · `WS-xx` workflow 6 · `CP-xx` coupon 3 · `FP-xx` payment 4 · `CS-xx` settlement 4 · `TK-xx` ticket 4 · `TC-xx` technician change 4 · `PA-xx` partner approval 4 · `TR-xx` transfer 6 | `23` | 72 |
| Data entities | table names | `09` §4 | 88 distinct names across 86 `####` headings (two headings declare three and two tables; `tax_registrations` is declared in §4.1 and restated in §4.3). `38` added **2**: `platform_mode` and `platform_mode_transitions` (`09` §4.15) |
| API endpoints | REST method + path | `10` §4 | 122 rows (116 distinct paths); 130 rows / 124 paths counting the 8 auth rows in §3. `38` added **5 rows / 4 paths** to §4.3 |
| Architecture decisions | `ADR-xxx` | `22` | 26 |
| Non-functional | `PF-xx` 1 · `RI-xx` 10 · `SC-xx` 1 · `MT-xx` 6 · `OB-xx` 11 · `AV-xx` 1 | `13` | 30 (further rule families live in their own documents: `DB-xx` in `09`, `SEC-*`/`NFR-*` in `13` §5 and `14`, `CI-xx`/`INF-xx` in `14`/`16`) |
| Quality gates | `G-xx` | `15` §14 | 12 |
| Open decisions | `OD-xxx`, `OD-COM-xx`, `ORG-xx` | `21`, `26` | 237 rows (47 blockers) |
| Risks | `R-xx` | `19` §2 | 50 |
| Screens | `SCR-<SURFACE>-<NN>` | `12` §2.1/§3.2/§4.2/§5.2, `33` §3–§4 | 68 (WEB 9 · CUS 26 · PAR 21 · CC 12); **every row is `UNDESIGNED`** — no `SCR-PD-*` issued for the conditional partner dashboard |
| Visual & brand assets | `AMM-<SURFACE>-<TYPE>-<SUBJECT>-<SIZE>-v<NN>` | `32` §2 | 105 inventory rows (77 `PLANNED` · 18 `GENERATED` · 6 `BLOCKED` · 4 `REGISTERED`); **0 `APPROVED`** — a `GENERATED` file is not an accepted one (`32` §6) |

**How these counts were produced, and why the earlier ones were wrong.** Each figure is a count of
*distinct identifiers in the named document*, taken by a row- or token-anchored scan — not by
counting occurrences in prose, which double-counts every cross-reference. The previous edition of
this table carried `140+` permissions, `45+` entities, `130+` endpoints and `~70` business rules,
none of which any scan reproduced. **Audit pass 3 replaced them with figures that were themselves
not all reproducible, and they have now been measured a second time:** the `83` tables became **86**
(the pass-3 scan counted `####` headings, and two headings declare three and two tables
respectively), `123` endpoint rows became **117** in §4 with `125` counting §3, `89` permission tokens
became **92** (a token is the backticked first cell of a §4.1–§4.4 row; the five `read/update`
shorthands are expanded), `53` business rules became **75** (the pass-3 scan matched only table rows,
and most rules in `00` and `04` are declared as list items), and `37` risks became **44**, then **45**,
**47** and **48** across the design passes. **The platform-mode pass then moved four of these rows again,
each by re-scanning the source document and not by adding to the last prose figure:** entities 86 → **88**
(`platform_mode`, `platform_mode_transitions`), §4 endpoints 117 → **122 rows / 116 distinct paths**, ADRs
25 → **26** (`ADR-026`), FRs 91 → **99** (`FR-MODE-01`…`08`), open decisions 231 → **237 rows / 47
blockers** (the five `OD-DOC` rows plus `OD-COM-13`, registered in `26` §9 and mirrored into `21` §7.1 in
the same act) and risks 48 → **50** (`R-49`, `R-50`). Two of those moves are corrections of this pass's own
earlier arithmetic, which is worth stating: an intermediate figure of **123** endpoint rows and the
**236 / 142** register total written into `21` §1 both failed to reproduce and were replaced by what the
scan returns. A risk total that moves only when a row is registered — `R-01`…`R-50`, no gap, no
duplicate, re-scanned rather than incremented — is the standard the rest of the table is held to.
`AV-xx` has been removed from the business-rule row: `AV-01` is a resilience rule in `13` and is
already counted once in the non-functional row. Two consequences of the corrected counts worth
naming: the model declares **88** tables where the matrix claimed 45+, so more than half the schema
had no row reachable from this document, and an entity-by-entity review of the sort `09` §7–§8 now
provides was not possible against a `45+` figure. `TM-06` is the control meant to keep this table
honest, and it is marked `[PROPOSED]` because the repository has no pipeline to run it in — which is
also why three of the five errors above survived a pass that claimed to have removed them.
**The two rows the design pass added were measured the same way**: 93 asset rows by counting data lines
in `design-assets/manifests/asset-inventory.csv` (the file `gen_asset_inventory.py` generates, never
hand-edited — `validate_assets.py` refuses a row whose ID, name grammar, alt-text treatment or `doc_ref`
is wrong), and 68 screens by counting `SCR-*` data rows in `33` §3–§4. Both figures are therefore
regenerable; neither is a prose count.

**Coverage as at the platform-mode pass.** All **99 of 99** functional requirements in `01` §4 now have a
row in §3 (91 at audit pass 3, plus `FR-MODE-01`…`08` in §3.10), verified by a two-way set diff of the
`FR-*` first cells in `01` against this file — both directions empty, no duplicate row. The eight new
rows are `PROPOSED`, so **coverage and approval are now different facts** and must be read apart: every
FR is traced, and none of the eight is approved (`01` §8, `26` §3.2). The diff was produced by a
row-anchored scan of `01` against this file rather than by the CI check in
`TM-06`, which does not exist yet. Four of the pass-3 rows name a **data-model gap** rather than a test
(`FR-CAT-07` → `OD-09-06`, `FR-JOB-08` → warranty columns added in `09` v1.2, `FR-BK-14` →
`OD-BK-06`, `FR-RPT-*` → `OD-09-07`): a requirement that cannot be traced to a table is not testable,
and saying so is the point of the matrix. The §3.10 rows are traced to tables that exist in the model
text (`platform_mode`, `platform_mode_transitions` in `09` §4.15), but `FR-MODE-05` is the one row in
this document whose data dependency is a **column on all 88 tables** rather than a table of its own —
which is why `17` puts it in Phase 0 (`P0-15`) and why the entity count above did not move when it was
written.

---

## 3. Master Traceability Matrix

### 3.1 Identity, Access & Organisation

| Req ID | Description | Status | Owner | Workflow | Data entities | API | Permission | Planned test | Evidence | Source | Open dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-ID-01 | Customer registers via mobile OTP | CONFIRMED | Eng Lead | `03` §7.3 | `users`, `otp_requests`, `customers` | `POST /auth/otp/*` | public | `auth.otp.spec` | test report + OpenAPI | `01` §4.1 | OD-14-05 (SMS provider) |
| FR-ID-02 | Technician registers with KYC, skills, service areas | CONFIRMED | Partner Ops | `06` §5 | `technicians`, `technician_documents`, `technician_skills`, `technician_area_pins` | `POST /technicians/me/*` | `technician:*` | `technician.onboarding.spec` | test report | `01` §4.1 | OD-INT-07 (KYC vendor) |
| FR-ID-03 | Partner branch registers with legal entity and territory | CONFIRMED | Operator | `23` §9 | `partner_orgs`, `branches`, `legal_entities` | `POST /admin/partner-orgs` | `platformOps:partnerOrg:*` | `partner.approval.spec` | test report | `01` §4.1 | OD-07-03 (supplier identity) |
| FR-ID-04 | Central staff accounts created by Super Admin / Admin only | CONFIRMED | Eng Lead | `03` §7.1 | `users`, `user_roles`, `user_scopes` | `POST /admin/users` | `platform:user:create` | `rbac.matrix.spec` | test report | `01` §4.1 | — |
| FR-ID-05 | Every account has a scope restricting data visibility | CONFIRMED | Security Owner | `03` §4–§6 | `user_scopes` | all | scope guard | `scope-isolation.sweep` | sweep report | `01` §4.1 | OD-09-01 (RLS) |
| FR-ID-06 | Granular per-resource, per-action permissions | CONFIRMED | Security Owner | `03` §3 | `roles`, `permissions`, `role_permissions` | all | `PermissionsGuard` | `rbac.matrix.spec` | test report | `01` §4.1 | — |
| FR-ID-07 | Document expiry → grace → automatic deactivation | CONFIRMED | Partner Ops | `23` §9 | `technician_documents`, `technicians` | `GET /admin/technicians` | `platformOps:technician:*` | `document.expiry.spec` | test report | `01` §4.1 | — |
| FR-ID-08 | Territory allocation with conflict detection | CONFIRMED | Operator | `02` §5 | `territory_allocations`, `service_areas` | `POST /admin/territories/allocate` | `platformOps:territory:*` | `territory.conflict.spec` | test report | `01` §4.1 | — |
| FR-ID-09 | Authentication events audited, 24-month retention | CONFIRMED | Security Owner | `03` §7.1 | `audit_events` | — | system | `audit.chain.spec` | nightly verification | `01` §4.1 | — |
| FR-ID-10 | Lockout after 5 failed attempts | CONFIRMED | Eng Lead | `03` §7.1 | `users` | `POST /auth/otp/verify` | public | `auth.lockout.spec` | test report | `01` §4.1 | — |
| BR-06 | Location hierarchy State → City → Zone → Service Area → Branch | CONFIRMED | Product Lead | `02` §2 | `states`, `cities`, `zones`, `service_areas`, `branches` | `GET /catalog/service-areas/resolve` | scoped | `org.hierarchy.spec` | test report | `00` §8.3 | — |
| BR-08 | Partner branches are allowed only by Operator or Super Admin | CONFIRMED | Founder | `23` §9 | `branches`, `audit_events` | `POST /admin/branches/{id}/approve` | `platformOps:branch:approve` | `partner.approval.spec` | test report | `00` §8.3 | — |
| ADR-003 | Branch ≠ legal entity; supplier resolved via entity + registration | CONFIRMED | Finance + Eng | `23` §6 | `legal_entities`, `tax_registrations` | `GET /admin/invoices/{id}` | `finance:invoice:read` | `supplier-resolution.spec` | test report | `22` | OD-07-01, OD-07-03 |

### 3.2 Catalogue, Discovery & Serviceability

| Req ID | Description | Status | Owner | Workflow | Data entities | API | Permission | Planned test | Evidence | Source | Open dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-CAT-01 | 3-level catalogue: Category → Service → Variant | CONFIRMED | Product Lead | `06` §2 | `categories`, `services`, `service_variants` | `GET /catalog/*` | public | `catalog.hierarchy.spec` | test report | `01` §4.2 | — |
| FR-CAT-02 | Each service carries a versioned workflow template | CONFIRMED | Eng Lead | `06` §3 | `workflow_templates`, `workflow_versions` | `GET /admin/workflows` | `catalog:service:*` | `workflow.versioning.spec` | test report | `01` §4.2 | — |
| FR-CAT-03 | A service is offered only where ≥ 1 eligible technician exists | CONFIRMED | Product Lead | `23` §5 | `technician_area_pins`, `technician_skills` | `GET /catalog/coverage` | public | `serviceability.spec` | test report | `01` §4.2 | — |
| FR-CAT-04 | Technicians ranked by configurable score | CONFIRMED | Product Lead | `04` §3.2 | `technician_scores` | `GET /search/technicians` | public | `ranking.spec` | test report | `01` §4.2 | — |
| FR-CAT-05 | Technician card shows rating, jobs, price range, ETA, badges | CONFIRMED | Design Lead | `12` §3.2 #8 | `ratings`, `technicians` | `GET /search/technicians` | public | `search.contract.spec` | API snapshot | `01` §4.2 | — |
| FR-CAT-08 | Multi-language catalogue content (en, or, hi) | CONFIRMED | Growth | `06` §7 | `categories`, `services` | `GET /catalog/*` | public | `i18n.coverage.spec` | test report | `01` §4.2 | OD-06-03 |
| FR-CAT-06 | Category browsing, service detail pages, price-range display on web and app | CONFIRMED | Design Lead | `12` §3.2 | `categories`, `services`, `service_variants`, `price_book_entries` | `GET /catalog/*` | public | `catalog.pages.spec` | test report | `01` §4.2 | — |
| FR-CAT-07 | A service can be **paused per service area** without a deployment | CONFIRMED | Product Lead | `06` §2 | `services.is_active` is **global**; `09` §4.3 declares no per-area offering table, so this requirement has no home | — | `catalog:service:*` | `service.pause.spec` | — | `01` §4.2 | **`OD-09-06`** — needs a `service_area_services` entity |
| ADR-004 | Serviceability is a backend-resolved property with reason codes | CONFIRMED | Eng Lead | `23` §5 | `service_areas`, `tax_registrations`, `price_book_entries` | `POST /bookings` | server-enforced | `serviceability.spec` (6 conditions × reason code) | test report | `22` | — |
| ADR-023 | Non-serviceable → waitlist / callback / enquiry, never a booking | PROPOSED | Product Lead | `04` §3.1 | `waitlist_entries` (new) | `POST /waitlist` | public | `waitlist.spec` | test report | `22` | OD-COM-08 scope |

### 3.3 Booking Lifecycle

| Req ID | Description | Status | Owner | Workflow | Data entities | API | Permission | Planned test | Evidence | Source | Open dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-BK-01 | Booking captures customer, address, service, slot, technician, snapshot, coupon | CONFIRMED | Product Lead | `04` §3.3 | `bookings`, `price_snapshots` | `POST /bookings` | `booking:create` | `booking.create.spec` | test report | `01` §4.3 | — |
| FR-BK-02 | Address geo-snapshotted immutably | CONFIRMED | Eng Lead | `04` §3.3 | `bookings.address_geo` | `POST /bookings` | server | `geo.snapshot.spec` | test report | `01` §4.3 | — |
| FR-BK-03 | Slots from technician availability within the service area | CONFIRMED | Eng Lead | `04` §3.3 | `technician_availability` | `GET /search/availability` | public | `availability.spec` | test report | `01` §4.3 | — |
| FR-BK-04 | Price breakdown frozen at booking | CONFIRMED | Finance | `04` §3.3, `23` T-01 | `price_snapshots` | `POST /quotes`, `POST /bookings` | server | `golden-master` | golden fixture | `01` §4.3 | — |
| FR-BK-05 | Coupons validated server-side at booking | CONFIRMED | Product | `07` §5 | `coupons`, `coupon_reservations` | `POST /bookings` | server | `coupon.validation.spec` | test report | `01` §4.3 | — |
| FR-BK-06 | Advance optional, configurable per service/branch | PROPOSED | Finance | `07` §3 | `services.default_advance_pct`, `branches.settings` | `POST /bookings` | server | `advance.spec` | test report | `01` §4.3 | OD-BK-03, OD-07-06 |
| FR-BK-07 | Acceptance window (5 min direct / 10 min feed) | CONFIRMED | Product Lead | `23` T-05..T-08 | `booking_offers` | `POST /technicians/me/offers/{id}/accept` | `booking:offer:accept` | `offer.window.spec` | test report | `01` §4.3 | — |
| FR-BK-08 | Reschedule subject to policy; fee may apply | CONFIRMED | Product Lead | `23` T-30 | `bookings.reschedule_count` | `POST /bookings/{id}/reschedule` | `booking:reschedule` | `reschedule.spec` | test report | `01` §4.3 | OD-BK-05 |
| FR-BK-09 | Technician change with eligibility and possible fee | CONFIRMED | Product Lead | `23` T-28 | `bookings.technician_change_count`, `booking_assignments` | `POST /bookings/{id}/change-technician` | `booking:changeTechnician` | `techchange.spec` | test report | `01` §4.3 | OD-BK-05 |
| FR-BK-10 | Cancellation policy + system-computed penalty | CONFIRMED | Product Lead | `04` §6 | `bookings.cancellation_penalty_paise` | `POST /bookings/{id}/cancel` | `booking:cancel` | `cancellation.spec` | test report | `01` §4.3 | OD-BK-05 |
| FR-BK-11 | Notifications on every state change | CONFIRMED | Eng Lead | `04` §7, `11` §8 | `notification_deliveries` | — | system | `notification.pipeline.spec` | test report | `01` §4.3 | OD-INT-02 |
| FR-BK-12 | Live location broadcast while EN_ROUTE / STARTED | CONFIRMED | Eng Lead | `08` §5.3 | `realtime_presence` (Redis) | `GET /bookings/{id}/track` | `booking:read` | `tracking.spec` | test report | `01` §4.3 | — |
| FR-BK-13 | No booking for a paused service, unverified technician, or out-of-area address | CONFIRMED | Eng Lead | `23` §5 | multiple | `POST /bookings` | server | `guard.spec` | test report | `01` §4.3 | — |
| FR-BK-14 | Re-booking a completed job creates a **new** booking linked to the original | CONFIRMED | Product Lead | no rebooking flow is documented — `09` §4.6 declares `bookings.parent_booking_id` and `23` T-37 covers the rework chain, but `04` §3 has no stage for it | `bookings.parent_booking_id` | `POST /bookings` (with `parentBookingId`) | `booking:create` | `rebook.link.spec` | test report | `01` §4.3 | **`OD-BK-06`** — the rebooking entry point is undefined |
| T-01..T-37 | The 37 booking transitions with guards, side effects and audit | CONFIRMED | Eng Lead | `23` §3 | `booking_events` | — | per transition | `state-machine.spec` (table-driven + fuzz) | test report | `23` | `OD-DOC-12` — technician attendance has no transition |
| ADR-005 | Booking ownership exclusive; transfers audited | CONFIRMED | Product Lead | `23` §7 | `booking_transfers` (new) | `POST /admin/bookings/{id}/transfer` | `booking:override` | `transfer.spec` | test report | `22` | — |

### 3.4 Job Execution & Workflow Engine

| Req ID | Description | Status | Owner | Workflow | Data entities | API | Permission | Planned test | Evidence | Source | Open dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-JOB-01 | Job start requires customer OTP | CONFIRMED | Product Lead | `23` T-12 | `booking_events` | `POST /bookings/{id}/otp` | `booking:read` | `otp.spec` | test report | `01` §4.4 | OD-06-01, OD-06-02 (salon/cleaning) |
| FR-JOB-02 | Service-specific checklist must complete before completion | CONFIRMED | Product Lead | `06` §3 | `workflow_step_items` | `POST /bookings/{id}/complete` | `job:complete` | `workflow.blocking.spec` | test report | `01` §4.4 | — |
| FR-JOB-03 | Parts captured with name, qty, unit price, margin basis | CONFIRMED | Finance | `07` §3 | `booking_adjustments` | `POST /bookings/{id}/parts` | `job:parts:add` | `parts.spec` | test report | `01` §4.4 | — |
| FR-JOB-04 | Photo evidence required for configured categories | CONFIRMED | Product Lead | `06` §4 | `workflow_evidence` | `POST /bookings/{id}/evidence` | `job:evidence:upload` | `evidence.spec` | test report | `01` §4.4 | — |
| FR-JOB-05 | Final invoice reconciles to the snapshot + adjustments | CONFIRMED | Finance | `07` §4.3 | `invoices`, `invoice_lines` | `POST /bookings/{id}/invoice` | `job:invoice:generate` | `invoice.reconciliation.spec` | nightly report | `01` §4.4 | — |
| FR-JOB-06 | Remaining payment via gateway; payment link fallback | CONFIRMED | Finance | `07` §4.3 | `payments` | `POST /bookings/{id}/collect-payment` | `payment:collect` | `payment.spec` | test report | `01` §4.4 | — |
| FR-JOB-07 | A job may be marked complete **only** when every mandatory checklist item and every required evidence artefact is present | CONFIRMED | Product Lead | `06` §3, `06` §4 | `workflow_step_items`, `workflow_evidence` | `POST /bookings/{id}/complete` | `job:complete` | `completion.blocking.spec` (blocked otherwise) | test report | `01` §4.4 | — |
| FR-JOB-08 | The warranty period for the category is recorded and shown to the customer | CONFIRMED | Product Lead | `06` §4 rule `PR-03` | `services.warranty_days` → `bookings.warranty_days` / `warranty_expires_at` (**added in `09` v1.2**; `01` requires it "stored on the booking", which the earlier model did not allow) | `GET /bookings/{id}` | `booking:read` | `warranty.window.spec` | test report | `01` §4.4 | `OD-BK-06` (warranty vs repeat rebooking) |
| FR-JOB-09 | Technician performance score recalculated on completion | CONFIRMED | Ops Lead | `04` §7 | `technician_scores` | `GET /technicians/me/score` | `technician:*` | `scoring.spec` | test report | `01` §4.4 | — |
| ADR-010 | Categories configured via versioned workflow templates | CONFIRMED | Eng Lead | `06` | `workflow_versions` | `POST /admin/workflows/{id}/publish` | `catalog:service:*` | `workflow.versioning.spec` | test report | `22` | — |
| WS-01..WS-06 | Step ordering, blocking, override, timeout rules | CONFIRMED | Eng Lead | `23` §6 | `workflow_steps` | — | `job:complete` | `workflow.engine.spec` | test report | `23` | — |

### 3.5 Pricing, Coupons, Commission & Settlement

| Req ID | Description | Status | Owner | Workflow | Data entities | API | Permission | Planned test | Evidence | Source | Open dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-FIN-01 | Platform sets min/max/default price per service per geography | CONFIRMED | Finance | `07` §3.4 | `price_book_entries` | `POST /admin/price-book` | `catalog:priceBook:*` | `pricing.resolution.spec` | test report | `01` §4.6 | OD-LOC-03 |
| FR-FIN-02 | Partner may customise only within the band | CONFIRMED | Finance | `07` §3.4 | `branch_price_overrides` | `PUT /branch/prices/{variantId}` | `branch:priceBook:local` | `price.band.spec` (DB check) | test report | `01` §4.6 | — |
| FR-FIN-03 | Visiting charge platform-set; diagnostic charge supported | CONFIRMED | Finance | `07` §3 | `price_book_entries` | — | `catalog:priceBook:*` | `price.components.spec` | test report | `01` §4.6 | — |
| FR-FIN-04 | Parts pricing: MRP or allowed margin | CONFIRMED | Finance | `07` §3 | `price_book_entries.parts_pricing_rule` | `POST /bookings/{id}/parts` | server | `parts.margin.spec` | test report | `01` §4.6 | — |
| FR-FIN-05 | Discounts platform / partner / shared with defined commission effect | CONFIRMED | Finance | `07` §5 | `coupons`, `price_snapshots.discounts` | `POST /quotes` | server | `discount.funding.spec` (property) | golden fixture | `01` §4.6 | — |
| FR-FIN-06 | GST per place of supply and branch registration | DEPENDENT | Finance | `07` §6 | `tax_registrations`, `tax_rates` | `POST /quotes` | server | `tax.component.spec` | test report | `01` §4.6 | **OD-07-01** — tax advisor |
| FR-FIN-07 | Commission on eligible labour only | CONFIRMED | Finance | `07` §4.4 | `commission_ledger` | — | system | `golden-master` | golden fixture | `01` §4.6 | OD-07-03 |
| FR-FIN-08 | Commission accrued per completed job into an immutable ledger | CONFIRMED | Finance | `07` §7.2 | `commission_ledger` | — | system | `accrual.uniqueness.spec` | nightly report | `01` §4.6 | — |
| FR-FIN-09 | Weekly settlement Mon–Sun → statement → pay in 7 days | CONFIRMED | Finance | `07` §7.3 | `settlement_statements`, `settlement_lines` | `POST /admin/settlements/generate` | `finance:settlement:*` | `settlement.idempotency.spec` | test report | `01` §4.6 | OD-07-05 |
| FR-FIN-10 | Commission invoice issued with applicable GST | DEPENDENT | Finance | `07` §7.3 | `commission_invoices` | `GET /admin/settlements/{id}` | `finance:settlement:issue` | `settlement.invoice.spec` | test report | `01` §4.6 | **OD-07-01, OD-07-02** |
| FR-FIN-11 | Gateway reconciliation matches settlements to payments | CONFIRMED | Finance | `07` §10 | `payments` | `GET /admin/reconciliation` | `finance:reconciliation:*` | `reconciliation.spec` | nightly report | `01` §4.6 | — |
| FR-FIN-12 | Disputes and adjustments are credit/debit notes, never edits | CONFIRMED | Finance | `07` §7.5 | `adjustments` | `POST /admin/settlements/{id}/adjustments` | `finance:adjustment:create` | `immutability.spec` | test report | `01` §4.6 | — |
| FR-FIN-13 | Branch-wise revenue, commission and margin reports | CONFIRMED | Finance | `12` §5 | `report_snapshots` | `GET /admin/reports/*` | `report:finance` | `report.scope.spec` | test report | `01` §4.6 | — |
| FR-FIN-14 | Commission rate versioned and pinned at completion | CONFIRMED | Finance | `07` §7.1 | `commission_rate_versions` | `POST /admin/commission/rates` | `finance:commission:*` | `rate.versioning.spec` | test report | `01` §4.6 | — |
| ADR-006 | Snapshot immutable; invoice derived from it | CONFIRMED | Finance | `23` T-17 | `price_snapshots` | `POST /bookings` | server | `snapshot.immutable.spec` | test report | `22` | — |
| ADR-007 | Commission base excludes GST, visiting, transport, parts | CONFIRMED | Finance | `07` §4.5 | `commission_ledger` | — | system | `golden-master` | golden fixture | `22` | OD-07-02 |
| ADR-008 | Coupon usage reserved at booking, released on cancellation | CONFIRMED | Finance | `07` §5 | `coupon_reservations`, `coupon_redemptions` | `POST /bookings` | server | `coupon.concurrency.spec` | test report | `22` | — |
| ADR-009 | Settlement weekly, per branch, immutable | CONFIRMED | Finance | `07` §7.3 | `settlement_statements` | `POST /admin/settlements/*` | `finance:settlement:*` | `settlement.idempotency.spec` | test report | `22` | OD-07-05 |
| ADR-015 | Financial records append-only once issued | CONFIRMED | Finance | `23` §11 | `invoices`, `settlement_statements` | — | system | `immutability.spec` (DB trigger) | test report | `22` | — |
| RND-01..06 | Single rounding rule set for all money | CONFIRMED | Finance | `07` §8 | — | — | system | `property P8/P9` | golden fixture | `07` | — |
| §9.2 | Advance amounts are examples (₹27, ₹99), configurable | OPEN | Finance | `07` §3 | `services.default_advance_pct` | — | — | `advance.spec` | — | `07` | **OD-BK-03, OD-07-06** |
| §9.1 | Emergency/night charges and gateway fees are distinct components | PROPOSED | Finance | `07` §3 | `price_book_entries` | `POST /quotes` | server | `price.components.spec` | test report | `07` | OD-COM-04 |

### 3.6 Support, IVR & Notifications

| Req ID | Description | Status | Owner | Workflow | Data entities | API | Permission | Planned test | Evidence | Source | Open dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-SUP-01 | Toll-free with multi-language IVR | DEPENDENT | Support Lead | `05` §3 | `call_logs` | provider webhooks | — | `ivr.spec` | test report | `01` §4.5 | **OD-INT-01** — provider not procured |
| FR-SUP-02 | Smart routing on number, profile, bookings, city/branch, language, issue, skill | CONFIRMED | Support Lead | `05` §3.4 | `call_logs` | — | — | `routing.spec` | test report | `01` §4.5 | OD-INT-01 |
| FR-SUP-03 | OTP verification before sensitive changes | CONFIRMED | Security Owner | `05` §3.5 | `otp_requests` | `POST /auth/otp/verify` | — | `cco.otp.spec` | test report | `01` §4.5 | — |
| FR-SUP-04 | Six call use cases implemented | CONFIRMED | Support Lead | `05` §5 | `call_logs`, `support_tickets` | `POST /bookings`, `POST /admin/tickets/*` | `booking:create`, `support:ticket:*` | `usecase.spec` | test report | `01` §4.5 | OD-SUP-01 |
| FR-SUP-05 | Every call produces a call log with recording reference | CONFIRMED | Support Lead | `05` §4 | `call_logs` | `GET /admin/calls` | `support:call:read` | `calllog.spec` | test report | `01` §4.5 | OD-SUP-04 |
| FR-SUP-06 | Ticket with category, priority, assignment, status | CONFIRMED | Support Lead | `05` §6 | `support_tickets` | `POST /admin/tickets/{id}/status` | `support:ticket:*` | `ticket.spec` | test report | `01` §4.5 | — |
| FR-SUP-07 | Notify on ticket **create / update / close** via SMS, WhatsApp, email and app | CONFIRMED | Support Lead | `05` §6.3, `11` §8 | `support_tickets`, `notification_deliveries` (keyed by `dedupe_key`, `ticket_id`) | `POST /tickets`, `POST /admin/tickets/{id}/status` | system | `ticket.notify.spec` | test report | `01` §4.5 | OD-INT-02, OD-14-05 |
| FR-SUP-08 | Supervisor dashboard: volume, queue time, agent performance, CSAT | CONFIRMED | Support Lead | `12` §5 | `call_logs`, `support_tickets` | `GET /admin/reports/*` | `report:operations` | `report.spec` | test report | `01` §4.5 | `OD-09-07` |
| FR-SUP-09 | Complaints escalate to Branch Manager on SLA breach | CONFIRMED | Support Lead | `23` §13 | `ticket_events` | `POST /admin/tickets/{id}/status` | `support:complaint:escalate` | `escalation.spec` | test report | `01` §4.5 | — |
| FR-SUP-10 | Rework/refund arrangable from a complaint | CONFIRMED | Support Lead | `05` §5 E | `support_tickets.rework_booking_id` | `POST /admin/tickets/{id}/status` | `support:ticket:*` | `rework.spec` | test report | `01` §4.5 | — |
| ADR-016 | Support agents have bounded financial permissions | CONFIRMED | Finance + Security | `03` §4.1 | `role_permissions` | — | `PermissionsGuard` | `rbac.matrix.spec` | test report | `22` | OD-RBAC-01, OD-RBAC-04 |
| FR-NTF-01 | Channels: push, SMS, WhatsApp, email, in-app | CONFIRMED | Growth | `11` §7 | `notification_templates`, `notification_deliveries` | `GET /notifications` | `notification:preference` | `notification.pipeline.spec` | test report | `01` §4.10 | OD-INT-02, OD-14-05 |
| FR-NTF-02 | A **template registry** with variables, per-channel content and versioning | CONFIRMED | Growth | `11` §7.2 | `notification_templates` (`code`, `channel`, `locale`, `variables`, `version`) | `PUT /admin/notification-templates` | `platform:template:*` | `template.versioning.spec` | test report | `01` §4.10 | OD-06-03 (locale coverage) |
| FR-NTF-03 | Notifications queued with retry and dead-letter | CONFIRMED | Eng Lead | `11` §8 | `notification_deliveries` | — | system | `retry.spec` | test report | `01` §4.10 | — |
| FR-NTF-04 | Deep links from push/WhatsApp open the **exact** relevant screen | CONFIRMED | Growth | `11` §7.1 rule `NTF-03` | `notification_templates.variables` carries `deeplink`; `notification_deliveries` has **no deep-link column**, so the target exists only in the rendered payload | — | system | `deeplink.contract.spec` (per screen) | test report | `01` §4.10 | `12` §3 defines the push/deep-link target screens |
| FR-NTF-05 | Per-customer **notification preferences** by category; transactional messages exempt | CONFIRMED | Growth | `11` §8.2 | `notification_preferences` — PK `(user_id, channel, category)` | `GET/PUT /me/notification-preferences` | `notification:preference` | `preference.exemption.spec` | test report | `01` §4.10 | OD-WA-04 |
| FR-NTF-06 | WhatsApp messages are **pre-approved business-initiated templates**; free-form only inside the 24-hour customer service window | DEPENDENT | Growth | `11` §6, `11` §6.1 | `whatsapp_conversations`, `whatsapp_messages` (`template_code`, `template_version`) | provider webhook | system | `wa.window.spec` | test report | `01` §4.10 | **OD-WA-02** — templates not authored or approved |
| ADR-014 | WhatsApp is never proof of payment or booking state | CONFIRMED | Eng Lead + Finance | `11` §6 | `whatsapp_messages` (new) | — | system | `whatsapp.notauthoritative.spec` | test report | `22` | OD-INT-02 |
| §10 | Toll-free number is a placeholder until procured | CONFIRMED | Support Lead | `05` §3.1 | — | — | — | — | — | `05` | **OD-INT-01** |

### 3.7 Quality, Compliance & Operations

| Req ID | Description | Status | Owner | Workflow | Data entities | API | Permission | Planned test | Evidence | Source | Open dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-QA-01 | Customer rating after completion | CONFIRMED | Ops Lead | `04` §3.8 | `ratings` | `POST /bookings/{id}/rate` | `rating:create` | `rating.spec` | test report | `01` §4.7 | — |
| FR-QA-02 | Technician performance score | CONFIRMED | Ops Lead | `04` §7 | `technician_scores` | `GET /admin/reports/*` | `report:operations` | `scoring.spec` | test report | `01` §4.7 | — |
| FR-QA-03 | **Customer** score computed from cancellations, no-shows and disputes | CONFIRMED | Ops Lead | `04` §6 | `customers.customer_score` | `GET /admin/customers/{id}` | `platformOps:customer:read` | `customer.score.spec` | test report | `01` §4.7 | **`OD-QA-06`** — the policy it feeds is undefined, and the no-show input is unreliable until `OD-DOC-12` closes |
| FR-QA-04 | Penalties for late cancellation and no-show | CONFIRMED | Ops Lead | `04` §6 | `penalties` | `GET /technicians/me/penalties` | — | `penalty.spec` | test report | `01` §4.7 | OD-BK-05 |
| FR-QA-05 | Scores affect technician **visibility, ranking and future booking eligibility** | CONFIRMED | Ops Lead | `04` §3.2, `06` §5 | `technician_scores`, `technicians.accepting_jobs` | `GET /search/technicians` | server | `ranking.weight.spec` | test report | `01` §4.7 | a score that removes a partner's earning is a deactivation by another route and needs the same notice and appeal as `23` §8 |
| FR-QA-06 | Auto score recalculation on relevant events | CONFIRMED | Eng Lead | `04` §7 | `technician_scores` | — | system | `scoring.idempotency.spec` | test report | `01` §4.7 | — |
| FR-CMP-01 | Platform GST registration per operating state | DEPENDENT | Finance | `07` §6 | `tax_registrations` | `POST /admin/tax/registrations` | `finance:tax:config` | `tax.registration.spec` | test report | `01` §4.8 | **OD-07-01** |
| FR-CMP-02 | Place of supply = customer address state | CONFIRMED | Finance | `07` §6.2 | `bookings`, `invoices.place_of_supply_state_id` | — | server | `place.of.supply.spec` | test report | `01` §4.8 | OD-07-01 |
| FR-CMP-03 | The platform **commission invoice** includes GST as per law | DEPENDENT | Finance | `07` §7.3 | `commission_invoices`, `tax_rates` | `GET /admin/commission-invoices/{id}` | `finance:invoice:read` | `settlement.invoice.spec` | test report | `01` §4.8 | **OD-07-01**, **OD-DOC-02** — 18% is a configured default, not a confirmed rate |
| FR-CMP-04 | A technician's GST treatment depends on whether they are an individual or a registered business | DEPENDENT | Finance | `07` §6.1–§6.2 | `tax_registrations` (`entity_type = TECHNICIAN`), `technicians` | — | server | `tax.regime.spec` | test report | `01` §4.8 | **OD-07-01**, **OD-07-03** — per-partner configuration is asserted but no column stores it |
| FR-CMP-05 | Gapless, immutable, retrievable financial documents | CONFIRMED | Finance | `07` §9 | `invoices.number` | `GET /admin/invoices/{id}` | `finance:invoice:read` | `gapless.spec` | nightly report | `01` §4.8 | — |
| FR-CMP-06 | Tamper-evident audit log (hash chain) | CONFIRMED | Security Owner | `13` §5 | `audit_events` | `GET /admin/audit-events` | `platform:audit:read` | `audit.chain.spec` | nightly verification | `01` §4.8 | — |
| §13 DPDP | Consent, minimisation, retention, erasure, breach | DEPENDENT | Legal | `13` §6.1 | `customer_consents` (new) | `PATCH /customers/me` | — | `consent.spec` | test report | `13` | **OD-NFR-05**, OD-09-03 |
| ADR-017 | City activation gate | CONFIRMED | Founder + Ops | `29` §14 | `branches`, `cities` | `POST /admin/branches/{id}/approve` | `platformOps:branch:approve` | `activation.gate.spec` | signed checklist | `22` | OD-RM-03, OD-RM-04 |
| ADR-025 | Implementation status requires an inspectable artifact | CONFIRMED | Eng Lead | `27` §2 | — | — | — | — | — | `22` | — |
| §14 Security | MFA where appropriate (`OD-DOC-20` — the scope is stated four ways across `13`, `README`, `24` and here), secret rotation, TLS, rate limiting, upload handling | PROPOSED | Security Owner | `13` §5 | `sessions`, `audit_events` | all | — | `security.suite` | scan report | `13` | OD-NFR-01 |
| §14 Compliance | E-commerce operator obligations, e-invoicing thresholds | DEPENDENT | Legal + Finance | `19` §3 | — | — | — | — | — | `19` | **OD-07-01** |

### 3.8 Commercial & Delivery Requirements

| Req ID | Description | Status | Owner | Source | Evidence | Open dependency |
|---|---|---|---|---|---|---|
| §3.1 | Initial development fee covers the 12-item scope | PROPOSED | Project owner | `26` §3.1 | executed agreement | OD-COM-01, OD-COM-03 |
| §3.2 | Third-party consumption excluded from the fee | PROPOSED | Project owner | `26` §3.2 | executed agreement | OD-COM-01, OD-COM-07 |
| §3.2-15 | The platform-mode feature (`38`) is **outside** the initial development fee until the agreement changes in writing — it is not one of §3.1's twelve areas, and its L3 layer and email channel are unfunded additions (`26` §3.2's item-15 note) | PROPOSED | Both parties | `26` §3.2 item 15 | executed agreement, or a written variation | **OD-COM-13**, `OD-DOC-43`, `OD-MAIL-01` |
| §4.1 | ₹3,00,000 in three instalments | PROPOSED | Project owner | `26` §4.1 | executed agreement | OD-COM-01 |
| §4.2 | First ₹1,00,000 reported collected in cash; receipt prepared | REPORTED | Project owner | `26` §4.2 | receipt / bank record (not in repo) | OD-COM-02 |
| §4.3 | ₹60,000/yr single-city service | PROPOSED | Both parties | `26` §4.3 | executed agreement | OD-COM-04 |
| §4.4 | ₹5–10L / ₹10–20L multi-city ranges | PROPOSED | Both parties | `26` §4.4 | executed agreement | OD-COM-04, OD-COM-07 |
| §6 | Domain and server administration under Locky Dev access | REPORTED | Locky Dev | `26` §6.1 | — | OD-COM-06 |
| §6.3 | Continuity, export and migration arrangements | PROPOSED | Both parties | `26` §6.3 | executed agreement | OD-COM-06, OD-COM-10 |
| §7 | External commercial dependencies (PAN, GSTIN, bank, opinions) | DEPENDENT | Project owner | `26` §7 | — | OD-COM-05 |

### 3.9 Reporting & Analytics (`FR-RPT`)

Added in audit pass 3. These eight requirements were the largest single hole in the matrix: `12` §5
designs the reports and `03` grants `report:finance` / `report:operations` / `report:export`, but no
requirement row tied them together, so nothing connected a report to the scope guard that makes it
safe to show.

| Req ID | Description | Status | Owner | Workflow | Data entities | API | Permission | Planned test | Evidence | Source | Open dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-RPT-01 | Booking funnel: search → view → book → accept → start → complete → pay → review, with conversion at each step | CONFIRMED | Growth | `04` §3 | `booking_events`, `bookings` | `GET /admin/reports/{reportKey}` | `report:operations` | `report.funnel.spec` | test report | `01` §4.9 | `OD-09-07` |
| FR-RPT-02 | SLA dashboards: acceptance time, arrival time, job duration, complaint SLA — filterable by branch / zone / category / date | CONFIRMED | Ops Lead | `23` §3.3, `05` §6 | `bookings`, `booking_offers`, `support_tickets` (`sla_response_due_at`, `sla_resolution_due_at`) | `GET /admin/reports/{reportKey}` | `report:operations` | `report.sla.spec` | test report | `01` §4.9 | **`OD-DOC-12`** — arrival time has no terminal event when the technician fails to attend |
| FR-RPT-03 | Revenue, commission, **payout** and margin reports by branch / partner / category / period | DEPENDENT | Finance | `07` §7 | `commission_ledger`, `settlement_statements`, `partner_payouts` | `GET /admin/reports/{reportKey}` | `report:finance` | `report.money.spec` (reconciles to `ledger_entries`) | test report | `01` §4.9 | **`OD-DOC-01`** — "payout" is only meaningful once the settlement direction is decided |
| FR-RPT-04 | Technician leaderboard and underperformers list | CONFIRMED | Ops Lead | `04` §7 | `technician_scores`, `technicians` | `GET /admin/reports/{reportKey}` | `report:operations` | `report.leaderboard.spec` | test report | `01` §4.9 | `FR-QA-05` — ranking-based exclusion needs the same notice and appeal as deactivation |
| FR-RPT-05 | Support analytics: call volume, AHT, queue time, FCR, CSAT, ticket backlog | CONFIRMED | Support Lead | `05` §4, `05` §9 | `call_logs`, `call_events`, `callbacks`, `support_tickets`, `ratings` | `GET /admin/reports/{reportKey}` | `report:operations` | `report.support.spec` | test report | `01` §4.9 | `OD-INT-01` — queue time and AHT come from the provider, which is not selected |
| FR-RPT-06 | Coverage report: service areas with fewer than **N** eligible technicians (default 3) | CONFIRMED | Ops Lead | `23` §5, `02` §5 | `technician_area_pins`, `technician_skills`, `service_areas` | `GET /admin/reports/{reportKey}` | `report:operations` | `report.coverage.spec` | test report | `01` §4.9 | `OD-06-*` — "eligible" is resolved by `ADR-004`; the report must call the same resolver, not a second implementation |
| FR-RPT-07 | CSV/XLSX export for every finance and operations report | CONFIRMED | Eng Lead | `13` §6 (export redaction) | `report:export` guarded; exports carry the **viewer's** scope | `GET /admin/reports/{reportKey}/export` | `report:export` | `report.export.redaction.spec` | test report | `01` §4.9 | **`OD-09-02`** — whether an export to a branch may contain customer name/phone is undecided |
| FR-RPT-08 | **Every report honours the viewer's scope**; central and branch views differ | CONFIRMED | Security Owner | `03` §5–§6 | `user_scopes` applied in the query, not in the UI | `GET /admin/reports/*` | scope guard | `report.scope.spec` (one case per role × report) | sweep report | `01` §4.9 | `OD-09-01` (RLS as defence-in-depth) |

> **Cross-cutting.** `FR-RPT-08` is the reason `FR-RPT-01…07` are safe. A report that aggregates
> outside the viewer's scope leaks another branch's volumes, and an aggregate leaks even when no
> individual row is visible — so the scope predicate belongs in the SQL, and `report.scope.spec`
> runs the matrix of role × report rather than spot-checking.

---

### 3.10 Platform Mode & Data Lifecycle (`FR-MODE`)

Added on the owner's instruction of 2026-10-21. **All eight rows are `[PROPOSED]`, not `CONFIRMED`** —
`01` §4.11 records a requirement addition, `22` `ADR-026` is `Proposed`, and `38` is the specification.
Nothing here is built (`ADR-025`), and the `Permission` column is empty by fact rather than by
omission: `03` §4 still holds **92 tokens** because no token was allocated for the transition
(`03` `FL-09`), so naming one in this matrix would invent one (`OD-DOC-44`, downstream of `OD-10-06`).

| Req ID | Description | Status | Owner | Workflow | Data entities | API | Permission | Planned test | Evidence | Source | Open dependency |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-MODE-01 | Exactly one effective mode, `TESTING` or `PRODUCTION`, read from server-side database state | PROPOSED | Eng Lead | `38` §3 PM-01…PM-04 | `platform_mode` (one row, `CHECK (id=1)`) | `GET /admin/platform/mode` | — none allocated | `mode.state.source.spec` (a header, store or env var cannot change the effective mode) | not built | `01` §4.11 | `OD-DOC-43` (enforcement layer) |
| FR-MODE-02 | Default is `TESTING`; `TESTING` on production infrastructure refuses staff mutations and alerts | PROPOSED | DevOps Lead | `38` §10 | `platform_mode` | — | — | `mode.boot.assertion.spec` (deploy fails on the assertion, not on the day) | not built | `01` §4.11 | **`R-49`** — an unrun ceremony leaves live data unprotected |
| FR-MODE-03 | Promotion needs email OTP to the address of record + reason + second-account acknowledgement; demotion at least the same | PROPOSED | Security Owner | `38` §5 | `platform_mode_transitions` | `POST /admin/platform/mode/transitions`, `…/{id}/verify`, `…/{id}/acknowledge` | — SUPER_ADMIN only, step-up, **no token** (`03` `FL-09`) | `mode.promote.ceremony.spec` incl. `424 EMAIL_CHANNEL_UNAVAILABLE` | not built | `01` §4.11 | **`OD-DOC-42`** + email provider **not procured** (`24` P-06, `24` §15 A-06, `OD-MAIL-01`) |
| FR-MODE-04 | In `PRODUCTION`, class-A operator hard deletes / truncates / destructive DDL are refused; soft delete and code-defined purges continue | PROPOSED | Security Owner + Eng Lead | `38` §6 taxonomy A/B/C/D | all (guard is cross-cutting) | any `DELETE`, admin data-wipe | — | `mode.guard.refusal.spec` asserted at L2 **and** L3 (`15` `TE-06`), with classes B and D proven still working | not built | `01` §4.11 | **`OD-DOC-40`** — statutory DPDP erasure (class C) collides with an absolute ban (**`R-50`**) |
| FR-MODE-05 | Every insert records its origin, `TEST` or `LIVE`, write-once; reporting and settlement read `LIVE` only | PROPOSED | Data Owner | `38` §8 | every table (`record_origin` column) | — | — | `origin.write.once.spec`; `report.excludes.test.rows.spec` | not built | `01` §4.11 | `OD-DOC-43` (a column alone is advisory without the L3 role split) |
| FR-MODE-06 | `TESTING` must not consume the live statutory document number series | PROPOSED | Finance + Eng Lead | `38` §8.3 | `invoices`, `credit_notes`, series counters | — | — | `series.gapless.test.series.spec` | not built | `01` §4.11 | **`OD-DOC-41` [BLOCKER]** — `FR-CMP-05` gaplessness + `ADR-015` immutability + test invoices in one schema |
| FR-MODE-07 | The effective mode shows on every staff surface and export header; `TESTING` shows a non-dismissible indicator on customer and technician surfaces | PROPOSED | Product Lead + Design | `38` §9 | — | — | — | `mode.indicator.spec` (cannot be dismissed, cannot be hidden by scroll) | not built | `01` §4.11 | `OD-DOC-44` placement, downstream of `OD-10-06`; **no component named** (`37` `CA-00`) |
| FR-MODE-08 | Every transition is durably audited: append-only transition row + hash-chained audit event | PROPOSED | Security Owner | `38` PM-07 | `platform_mode_transitions` (`09` Rule DB-30) | `GET /admin/platform/mode/transitions` | — | `mode.audit.append.only.spec` (an UPDATE or DELETE on the history table must fail) | not built | `01` §4.11 | `OD-DOC-42` |

> **What this family changes about the matrix itself.** `FR-MODE-04` and `FR-MODE-05` are the only two
> rows here that reach every other row, because a guard on deletes and an origin column on inserts are
> properties of the whole schema rather than of one feature. That is why `38` §12 places them in
> **Phase 0** (`17` `P0-15`) before the first transactional migration: retrofitting `record_origin` onto
> rows already written is the part that cannot be done honestly later, since the origin of a row that
> predates the column can only be guessed.

---

## 4. Requirement → Test Coverage Map

| Test level | Tool | Target coverage | Gate |
|---|---|---|---|
| Unit | Jest / Vitest | ≥ 80% on domain modules; ≥ 95% on `pricing`, `commission`, `billing` | G-01 |
| Property-based | fast-check | ≥ 200 cases per property; the 12 properties in `15` §5.3 | G-01 |
| Golden-master | fixture suite | Every pricing/commission variant; the `07` §4 worked example | G-01 |
| Integration | Jest + Supertest + Testcontainers | ≥ 90% of API endpoints | G-02 |
| Contract | Spectral + dredd + generated-client | 0 drift, 0 breaking changes | G-03 |
| E2E | Playwright | GP-1..GP-4 on staging | G-04 |
| Scope isolation | Custom sweep | Every tenant-scoped endpoint | G-05 |
| State machine | Table-driven + fuzz | Every transition in `23`; every undeclared pair rejected | G-01 |
| Performance | k6 | `13` §2 targets | G-06 |
| Security | ZAP, Semgrep, Trivy, Gitleaks, npm audit | 0 critical/high | G-05 |
| Accessibility | axe-core + manual | WCAG 2.1 AA | G-07 |

**Coverage gap to close before Phase 1 exit.** The matrix above is the plan. No test exists yet,
because no code exists. The first milestone is to make the **golden-master** and **state-machine**
suites green, since they carry the financial and lifecycle risk.

---

## 5. Open Decision → Impact Map

Which requirements are blocked by which open decision. Use this to sequence decisions by blast radius.

| Open decision | Blocks | Phase impact if unresolved |
|---|---|---|
| **OD-07-01** (GST treatment) | FR-FIN-06, FR-FIN-10, FR-CMP-01, ADR-024, ADR-003 | Phase 2 billing cannot ship. **Highest blast radius.** |
| **OD-07-03** (principal vs agent) | FR-ID-03, FR-FIN-07, ADR-003, supplier resolution | Phase 2 invoice layout and the customer-facing supplier identity |
| **OD-07-02** (TDS 194C) | FR-FIN-10, ADR-007 | Phase 2 commission invoice format; Form 16A |
| **OD-BK-03 / OD-07-06** (advance) | FR-BK-06, `§9.2` | Phase 1 go-live; revenue recognition |
| **OD-BK-04** (cash collection) | FR-JOB-06, offline collection | Phase 1 — customers pay cash in this segment |
| **OD-LOC-01** (cross-branch acceptance) | FR-BK-07, job distribution | Phase 2 partner-branch expansion |
| **OD-06-03** (skill certification) | FR-ID-02, FR-CAT-03 | Phase 2 supply onboarding |
| **OD-SUP-01 / OD-INT-01** (telephony) | FR-SUP-01..04 | Phase 2 call channel; a documented 25% of bookings target |
| **OD-INT-02** (WhatsApp) | FR-NTF-01, ADR-014 | Phase 2 notification quality; SMS fallback exists |
| **OD-14-01** (ORM) | Every table in `09` | Phase 0 — blocks the repo scaffold |
| **OD-08-01** (Postgres hosting) | `16` §5.6 backups, RPO | Phase 0 — blocks prod provisioning |
| **OD-08-02** (Control Center SPA vs route) | `12` §5, `08` §9 | Phase 0 — blocks the front-end scaffold |
| **OD-RM-03 / OD-RM-04** (go-live date, launch categories) | ADR-017, `17` §3 | Phase 1 planning |
| **OD-COM-05** (contracting entity) | §8, ADR-003, invoice issuance | Blocks production invoicing entirely |
| **OD-COM-01/02/03** (agreement, payment method, acceptance) | `26` §4 | The next instalment |
| **OD-COM-13** (is the mode feature in the fee or a priced variation) | FR-MODE-01…08, `26` §3.2 item 15, `OD-DOC-43`, `OD-MAIL-01` | Phase 1 work on `38`. Nobody has priced the extra database identity or the transactional-email send, and both are owner-side costs on the current wording — so this is the row that decides whether the feature has a date at all |
| **OD-DOC-30** (blue/orange versus the measured teal/green) | `30` §3 colour tokens, every raster export in `32` §4, `26` §4.1's UI-approval trigger | The design gate. Blocks all model-raster production and, because the second instalment is payable **on UI approval**, is a money event as well as a design one |
| **OD-DOC-25 / 26 / 27 / 33** (catalogue imagery, no media column or serving path, category count, asset unit) | FR-CAT-01…10, `09` §4.3, `12` §3 screen 4, `31` §4 | Category and service artwork; the store listing; any customer-facing service image |
| **OD-DOC-29** (no screen → route → permission join) | The API and permission columns of all 68 rows in `33` §3–§4 (extends `OD-10-06`) | Front-end scaffolding and screen-level authorisation tests |
| **OD-DOC-32** (`font-src 'self'` versus unnamed font ownership) | `13` §5.2, `30` §4, `31` §3 | Typography on every surface — including Odia, which has no subset file anywhere in the workspace |
| **OD-DOC-34** (third-party media store versus `img-src 'self'` and no publicly readable object) `[BLOCKER]` | `13` §5.2, `24` §11, `16` §5.2, `09` §4.3, `32` §4's delivery assumptions, every run of `34` §4 | The first `<img>` and the first upload. Nothing raster can be served from a named CDN host until the CSP and the public-read rule are amended **per data class**, and `09` has nowhere to store the reference |
| **OD-DOC-35** (English-first design versus `12` §8 i18n-03's 100 % `or`/`hi`) | FR-CAT-08, `12` §8, `13` §7 `US-07`, `17` §7, `29` §4, `30` §4, `34` §2's no-text-in-images rule | Which asset exports are single-locale, and when the Indic subsets and the 30 %-expansion test get scheduled. The layout tolerance itself is **not** deferred |
| **OD-DOC-36** (placeholder-first versus what "designed" means at the design gate) | `26` §4.1's second instalment, all 68 `UNDESIGNED` rows in `33` §3–§4, `29` §4.8, `19` `R-45`, `30` §5.3 | Whether an approved-layout screen with empty media containers can certify the gate that triggers ₹1,00,000 — the same undefined trigger `R-45` scores |
| **OD-DOC-37** (super-admin storage-configuration surface no document can host) | `12` §5.2 (no such screen), `10` §4 (no route), `03` §4 (no token), `09` §4 (no table), `OD-10-06`, `OD-DOC-29` | Cannot be traced today at all: the screen → route → token join it would need is exactly what `OD-10-06` says does not exist. Sequenced **after** that blocker, before any storage module is built |
| **OD-DOC-38** (FastAPI as instructed versus `ADR-011` Accepted — NestJS) `[BLOCKER]` | `14` §1/§1.1/§2/§2.1, `08` §2/§9, `27` §6, `15` §2 and `16` §5/§9's pipeline units, `OD-14-01` (Prisma and Kysely are TypeScript-only), `packages/contracts`, `35` §2/§4, `36` §5's generated-client assumption | **The repository itself.** Every requirement whose acceptance test is an API integration test inherits this answer, and so does `git init`. `35` documents both trees; neither is adopted. Traced as `19` `R-48` |
| **OD-DOC-39** (worker placement — `14` §2 `apps/api/src/workers/` versus `08` §9 `apps/worker/`) | FR-NTF-*, FR-BK-15 (timeout sweep), `16` §5's deployable units, `08` §6.3's extraction gate, `35` §2.1/PS-01 | The first BullMQ processor. Two documents describe two deployables, so the pipeline that would build one cannot be written; rides with `OD-DOC-38` because the worker library is a consequence of the framework answer |
| **OD-14-09** (styling engine and component primitives) | `37` `CA-09`…`CA-15` (role variables), `36` §4, `12` §9's budgets, `30` §3's token consumption | The first component file. `13` §5.2's `style-src 'nonce-…'` is part of the question, so this is a security decision wearing a styling costume |
| **OD-14-10** (animation runtime) | `37` §6's nine recipes, `30` §7's motion tokens, `12` §9's budget, `29` §4.8's no-animation-as-proof rule | The first transition. Any runtime that injects un-nonce'd styles fails the CSP; any that animates layout properties fails the compositor-only rule `LB-05` |
| **OD-14-11** (charting and data-grid) | `12` §6.2's `DataTable`, `19` §2's dashboards, the Control Center reporting screens | Phase 1 reporting. Blocks nothing on the customer side and everything on the operator side |
| **OD-14-12** (component workshop and visual regression) | `37` §11.2's nine automatic checks, `15` §2's golden tests, `16` §9's pipeline stages, `29` §4.8 | The design-gate *evidence*. Without it the checklist is prose a reviewer may skip, which is the failure mode `37` §11.1 exists to prevent |
| **OD-14-13** (design-token build tooling) | `30` §3–§7 (the values), `35` §6 (the package layout), `37` §5 (the consumers), `PS-11` (no hand-copied hex) | The first token consumer. `PS-11` forbids copying a value by hand, so an unbuilt token package means either a violation of `PS-11` or no styling at all |
| **OD-DOC-40** (does the `PRODUCTION` delete guard yield to statutory erasure, or is it absolute) `[BLOCKER]` | FR-MODE-04, `01` §5's Privacy line (erasure), `13` §6.1, `09` §6, `19` §4.2, `38` §6 class C | **It is the only row here that can make a built feature unlawful.** An absolute ban contradicts a data subject's erasure right and the retention promises `09` §6 already makes; a yielding ban needs a named class-C path with its own audit. Blocks the first migration that ships a delete. Traced as `19` `R-50`. No legal conclusion is drawn here (`00` §11) — the question belongs to counsel |
| **OD-DOC-41** (how do `TESTING`-origin transactions coexist with a gapless statutory series) `[BLOCKER]` | FR-MODE-05/06, FR-CMP-05, `ADR-015`, `09` §4 invoice tables, `17` `P0-15` | The invoice number. `FR-CMP-05` demands gapless-per-entity-per-FY and `ADR-015` forbids editing a issued document, so a test invoice written into the live series is a hole a tax review can see and no one can explain. Blocks the first seed script. Recommended but unapproved: a separate non-statutory `T-` prefix series (`38` §8.3 option b) |
| **OD-DOC-42** (is demotion allowed, which factor is the step-up, and what happens while the email provider is unprocured) `[IMPORTANT]` | FR-MODE-03/08, `38` §5, `24` P-06 / §15 A-06, `OD-MAIL-01`, `OD-SEC-01`, `OD-DOC-20` | The ceremony cannot be built to close yet: the OTP channel is **not procured** and its factor type is undecided, so `POST /admin/platform/mode/transitions` has an acceptance test with no passable path. A promotion that can be requested but never completed is the failure `38` §5.1 names |
| **OD-DOC-43** (which layer enforces — L2 service, L3 database role, or both; a fourth/fifth DB identity) `[IMPORTANT]` | FR-MODE-01/04/05, `13` §5.1, `15` `TE-06`, `16` §5, `08` §9, `38` §7 | Decides whether the guard is real or bypassable, and it is the only row here with an **infrastructure cost**: L3 needs a second connection identity per environment, which `16` does not provision today. The origin column without L3 is advisory |
| **OD-DOC-44** (where the mode control sits in the Control Center) `[NICE]` | FR-MODE-07, `12` §3, `33` §4, `38` §9 | Deferred behind `OD-10-06` and `R-42` by design: the screen → route → token join the placement needs does not exist in this suite yet, so naming a surface now would invent a permission (`03` §4 stays at **92 tokens**) |

**What `30`–`37` contribute to traceability, and what they do not.** The design-system and asset passes
add **no new `FR-*` requirement** and therefore no new §3 row: `01` §4 has no UX requirement class at all,
so visual work is traced through its own namespaces (`SCR-*` in `33`, asset IDs in `32`) rather than
through this matrix. That is a real gap, not an oversight to paper over — inventing `FR-UX-*` IDs here
would create requirements that no owner approved, and `OD-DOC-37` is deliberately left untraceable for
the same reason. **The seven rows just added (`OD-DOC-38`, `OD-DOC-39`, `OD-14-09`…`13`) come from the
design-engineering pass and gate a different thing:** not the design gate but the *scaffold and the first
component*. They add no `FR-*` either, and they are traced to documents and rules (`35` `PS-*`, `36`
`LB-*`, `37` `CA-*`) rather than to requirements, because those rule families are this suite's own
identifier namespaces — the same treatment `33` and `32` get in §2. The design-gate rows above remain the
ones that block UI approval and therefore `26` §4.1's money event; `OD-DOC-28/31` in `21` are narrower and
are tracked there.

**What the platform-mode pass did differently, and why the difference matters.** `38` is the first pass in
this suite's history that **added requirements** rather than documents: `FR-MODE-01`…`08` exist in `01`
§4.11, so §3.10 above is a real §3 row set and the coverage figure moved 91 → 99. The two statements
cannot be collapsed into one. The design passes added rows to §5 only, and their work is traced through
their own namespaces; the mode pass added rows to **both** §3 and §5, and its rows are traced to `FR-*`
IDs that carry no approval yet (`01` §8 requires a charter amendment, `26` §3.2 requires a written scope
change). So §3.10's `PROPOSED` status is load-bearing: a reader who counts coverage here is counting
*traced*, not *agreed*.

**Sequencing recommendation.** Close, in order: OD-COM-01 → OD-COM-02 → OD-COM-05 → OD-07-01/02/03
→ **OD-DOC-38** → OD-14-01 → OD-08-01/02 → OD-BK-03/04 → OD-14-05 → OD-RM-03/04, with **OD-DOC-39**
answered in the same act as its parent and **OD-14-09/13** before the first component file and **OD-14-10**
before the first transition. Everything else can wait for its phase. `OD-DOC-38` sits **above** `OD-14-01`
because an ORM is chosen inside a framework: answering the data-layer question and then changing the
language asks it twice. **The mode rows do not sit in this chain — they sit underneath it.**
`OD-DOC-40` and `OD-DOC-41` are both `[BLOCKER]` and both gate the *first migration and the first seed
script*, not the first screen, so they are on the Phase 0 critical path (`17` `P0-15`) alongside
`OD-DOC-38`; `OD-DOC-42` gates only the completing half of one ceremony, and `OD-DOC-44` is deliberately
last because it is blocked by `OD-10-06` before it can be answered at all.

---

## 6. Traceability Maintenance Rules

| Rule | Detail |
|---|---|
| TM-01 | Every new requirement gets a stable ID and a row in this matrix before implementation. |
| TM-02 | IDs are **never reused or renumbered**. A withdrawn requirement is marked `WITHDRAWN` with a reason. |
| TM-03 | A requirement is only marked `IMPLEMENTED` when an inspectable artifact exists and is cited. (`ADR-025`) |
| TM-04 | A requirement blocked by an open decision shows `DEPENDENT` and the blocking `OD-xxx`. |
| TM-05 | When an open decision closes, every affected row is updated in the same change. |
| TM-06 | The matrix is regenerated and diffed in CI to detect rows added without a source document, or a source document changed without a matrix update. `[PROPOSED]` — the repository holds no pipeline today, so this is a target, not a control. Until it exists, the diff is produced by hand with a row-anchored scan of the ID columns in `01` against this file. |

---

## 7. Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.7 | 2026-10-22 | Product Lead + QA Lead (website-design pass) | §2's asset count re-measured from the regenerated register, not carried forward: **93 → 105 inventory rows**, and the status split restated as it now prints — 77 `PLANNED`, **18 `GENERATED`**, 6 `BLOCKED`, 4 `REGISTERED`, **0 `APPROVED`**. The `0 APPROVED` is the row's point and it survives the artwork: `32` §6 keeps a `GENERATED` file out of a build, so no requirement line gains a design asset it could ship. **No requirement ID, coverage figure, `FR`/`BP` classification, risk or open-decision count in this matrix changed** — the 68 screens remain `UNDESIGNED` and the traceability arithmetic is untouched. | §2, Revision History, header |
| 1.6 | 2026-10-21 | Product Lead + QA Lead (platform-mode pass) | **§3.10 added — `FR-MODE-01`…`08`, eight traceability rows**, and this is the first pass in the document's history that added **requirements** rather than documents, so coverage moved **91 of 91 → 99 of 99**, verified by a **two-way** set diff of `FR-*` first cells between `01` and this file (both directions empty, no duplicate). §2 re-measured from the source documents, not inherited: entities 86 → **88**, `10` §4 endpoints 117 → **122 rows / 116 paths**, ADRs 25 → **26**, FRs 91 → **99**, open decisions 231 → **237 / 47 blockers**, risks 48 → **50**. Two figures this pass had itself published were wrong and are named rather than smoothed away: an intermediate **123** endpoint rows and a **236 / 142** register total. §5 gained **six** impact-map rows (`OD-DOC-40`…`44` plus `OD-COM-13`) and the closing note distinguishes this pass from `30`–`37`: traced and approved are now different facts, and §3.10's `PROPOSED` status is load-bearing. **No row was renumbered, withdrawn or re-marked.** | §2, §3.8, §3.10 (new), §5, §1 |
| 1.5 | 2026-10-21 | Product Lead + QA Lead (design-engineering structure pass) | §2 restated **from the register rather than inherited**: open decisions 224 → **231 rows, 45 blockers**, risks 47 → **48**. §5 gained **seven rows** — `OD-DOC-38`, `OD-DOC-39` and `OD-14-09`…`13` — each mapped to the documents and rule families it actually blocks (`14` §1/§2/§2.1, `08` §9, `27` §6, `packages/contracts`, `16` §5/§9, and `35` `PS-*`, `36` `LB-*`, `37` `CA-*`). **They add no `FR-*` requirement**, and they are traced to documents and rules rather than to requirements for the same reason `32` and `33` are: those namespaces are this suite’s own. The distinction this pass introduces is between the **design-gate** rows, which block UI approval and therefore ₹1,00,000 (`26` §4.1, `R-45`), and the **construction** rows, which block the scaffold, the first component file and the first transition. §5’s sequencing recommendation now places `OD-DOC-38` **above** `OD-14-01`, because an ORM is chosen inside a framework and answering the data-layer question first asks it twice. | §2, §5, Revision History, header |
| 1.4 | 2026-10-21 | Product Lead + QA Lead (palette, storage and prompt-pack pass) | §2 restated from the register, not inherited: open decisions **220 → 224 rows, 43 → 44 blockers**, risks **45 → 47** (re-scanned as `R-01`…`R-47`, contiguous and unduplicated, rather than incremented from prose). §5 gained four rows — `OD-DOC-34` (`[BLOCKER]`: the third-party media store versus `13` §5.2's `img-src 'self'` and `24` §11's no-public-read rule, which blocks the first `<img>` and the first upload), `OD-DOC-35` (English-first versus `12` §8 i18n-03's 100 % `or`/`hi`), `OD-DOC-36` (placeholder-first versus what the design gate accepts as evidence — the `R-45` trigger seen from the asset side), and `OD-DOC-37` (the super-admin storage surface that **cannot be traced today at all**, because the screen → route → token join it would need is what `OD-10-06` says does not exist). The closing note widened to `30`–`34` and states that `34` adds no `FR-*` either, and that leaving `OD-DOC-37` untraceable is deliberate rather than an omission. `31` and `34` added to Depends On. **No §3 row was edited, renumbered or withdrawn, and no `FR-UX-*` ID was invented.** | §2, §5, §7, header |
| 1.3 | 2026-10-21 | Product Lead + QA Lead (design-system and asset pass) | Open-decision row restated **211 → 220 rows** (blockers unchanged at 43) per `21` §1, and risks **44 → 45** (`19` adds `R-45`, the undefined UI-approval trigger on `26` §4.1's second instalment). Two new ID namespaces measured and added: **68 screens** (`SCR-*`, `33` §3–§4, all `UNDESIGNED`) and **93 asset inventory rows** (`32`, from the generated CSV — 83 `PLANNED`, 6 `BLOCKED`, 4 `REGISTERED`, **0 `APPROVED`**). §5 gains four design-gate rows (`OD-DOC-30`, the `OD-DOC-25/26/27/33` cluster, `OD-DOC-29`, `OD-DOC-32`) and a note stating that `30`–`33` add **no** `FR-*` requirement: `01` §4 has no UX requirement class, screens and assets are traced by their own IDs, and inventing `FR-UX-*` here would create requirements no owner approved. `12` added to Depends On. No §3 row was edited, renumbered or withdrawn. | §2, §5, §7 |
| 1.2 | 2026-10-21 | Product Lead + QA Lead | Audit pass 3 (continued). §2 **re-measured for the second time**, because five of the figures this pass itself published did not reproduce: tables 83 → **86** (two `####` headings declare three and two tables), `10` §4 endpoint rows 123 → **117** (125 counting §3; 112 and 120 distinct paths), permission tokens 89 → **92** from 96 matrix cells (66 three-part, 26 two-part, 19 wildcards), business rules 53 → **75** (the earlier scan matched only table rows while most `00`/`04` rules are list items), risks 37 → **44**. `AV-xx` moved out of the business-rule row — `AV-01` lives in `13` and is counted in the non-functional row, so it had been counted twice. Open decisions restated as **211 rows / 43 blockers** per `21` §1 — the 202/41 first published by this pass had matched only `OD-*` first cells and so dropped the three `canonical / alias` rows and the four `ORG-*`-led rows; `ORG-xx` is now named in the ID-pattern column above. The note under §2 now records which pass-3 figures were wrong and why, rather than only that the pre-audit ones were. | §2 |
| 1.1 | 2026-10-21 | Product Lead + QA Lead | Audit pass 3. §2 counts **re-measured row-by-row instead of inherited** — the table carried `140+` permissions, `45+` entities, `130+` endpoints and `~70` business rules, none reproducible; the measured figures are **89 permission tokens, 83 tables, 123 endpoint rows, 53 business rules, 91 FRs, 25 ADRs, 44 risks, 12 gates**, and §2 now states the counting method (distinct-ID scan of register rows, not occurrence counts) so the figures can be regenerated rather than re-guessed. **22 functional requirements that existed in `01` were missing from §3** and are added — completing the map exposed four real defects, not clerical ones: no `service_area_services` table for per-area service availability, no warranty columns on `bookings`, no documented rebooking entry point, and no reporting entities behind `FR-RPT`. §3.9 Reporting & Analytics added (8 rows). `TM-06` downgraded to `[PROPOSED]`, because it asserts a CI-enforced gate and no pipeline exists in this repository. In §3.6 the `FR-SUP-09` citation to `23` §14 corrected to `23` §13, which is where the support-ticket machine lives. Coverage restated as **91 of 91** FRs. | §2, §3.2–§3.9, §6 |
| 1.0 | 2026-10-21 | Product Lead + QA Lead | Initial traceability matrix. 8 requirement classes mapped across 9 functional groups, plus a requirement-to-test coverage map and an open-decision impact map. | All |
