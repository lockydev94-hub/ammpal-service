# 06 — Service Catalog & Workflow Engine

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-06 |
| Version | 1.3 |
| Status | Approved for Design & Development |
| Owner | Product Lead + Engineering Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `01` §4.2, `02` §3, `04` §3.6 |

---

## 1. Design Principle

> **A new service category must be launchable by configuration, not by a code release.**

The founder's model states that partners are **typed by service** — a home-appliance partner follows
the home-appliance repair workflow, a beautician partner follows the beauty workflow. That is a
**workflow template** attached to a service category, not a fork of the codebase.

This document defines:

1. The catalog hierarchy (Category → Service → Service Variant).
2. The **workflow template** model and its execution semantics.
3. The per-category workflow definitions for the launch catalogue.
4. The rule engine that decides which technician may execute which job.

---

## 2. Catalog Hierarchy

> **This hierarchy is also the unresolved unit of visual design (`OD-DOC-33`).** The design brief asks for one image per *appliance category*, which is neither a family here nor a variant: `31` §4 measured the mapping and found 1 line that names a documented service, 2 that name future families, and **six of nine that appear in no document at all** — `09` §4.3 declares no media field for any of the three levels either (`OD-DOC-26`). Until the unit is fixed, the count of catalogue assets in `31` and `33` is a range, not a number.

```
Category (APPLIANCE_REPAIR)
 └── Service (AC_REPAIR)
      ├── Variant (AC_REPAIR_SPLIT_1_5T)
      ├── Variant (AC_REPAIR_WINDOW_1T)
      └── Variant (AC_REPAIR_COMMERCIAL_3T)

Category (CLEANING)
 └── Service (HOME_DEEP_CLEAN)
      ├── Variant (HOME_DEEP_CLEAN_2BHK)
      └── Variant (HOME_DEEP_CLEAN_3BHK)
```

| Entity | Definition | Key Attributes |
|---|---|---|
| **Category** | A top-level business line. Owns workflow family, default commission policy, default SLA | `code`, `name`, `workflow_family`, `is_active` |
| **Service** | A bookable service line within a category | `code`, `category_id`, `name`, `requires_diagnosis`, `default_advance_pct`, `warranty_days`, `estimated_duration_minutes` |
| **Service Variant** | The specific configuration a customer books (capacity, brand tier, package size) | `code`, `service_id`, `name`, `attributes` (JSONB), `price_overrides` |
| **Add-on** | An optional extra the customer can attach to a booking — e.g. "install", "remove old unit", "extended warranty", "annual filter" | `code`, `service_id`, `name`, `price_paise`, `duration_delta_minutes`, `is_active`, `max_quantity` |
| **Spare Part (catalogue)** | A platform-approved part with its pricing rule. A technician may also record a **manually approved part** that is not in the catalogue, subject to the margin rule and a required reason | `code`, `name`, `category_id`, `mrr_paise`, `allowed_min_paise`, `allowed_max_paise`, `pricing_rule` |
| **Price Book Entry** | The price band for a (variant × geography × effective window) | `min`, `max`, `default`, `visiting_charge`, `diagnostic_charge`, `emergency_charge` |
| **Skill** | A capability tag a technician can hold | `code`, `name`, `category_id` |
| **Service-Skill Requirement** | The skills (and minimum proficiency) a service needs | `service_id`, `skill_id`, `min_level` |
| **Eligibility Rule** | A rule constraining who may perform a service — by skill, category, city, branch, time window or equipment | `service_id`, `rule_type`, `rule_value` |

### 2.0a Add-ons, estimated duration and eligibility

| Concern | Rule |
|---|---|
| ADD-01 | An add-on is **optional** and priced independently of the base service. It may carry its own band in the price book. |
| ADD-02 | An add-on may extend the estimated duration and therefore the arrival SLA. The slot picker must account for the added duration. |
| ADD-03 | An add-on that is not permitted for a service variant must be rejected server-side at quote time, not merely hidden in the UI. |
| ADD-04 | An add-on's price is **labour** unless explicitly configured otherwise, and therefore participates in the commission base under the same rules as the base labour charge. `[PROPOSED]` — see `21` |
| ADD-05 | A platform-funded add-on discount is subject to the same funding rules as a coupon discount (`07` §5). |
| DUR-01 | Every service declares an `estimated_duration_minutes`, used for slot planning and SLA calculation. The duration is a **snapshot** on the booking; a later catalogue change does not alter a booked slot. |
| DUR-02 | The technician's actual duration is recorded and compared to the estimate for the punctuality score (`04` §7). |
| ELG-01 | An eligibility rule is evaluated server-side during candidate filtering, alongside the skill and category hard filters (`06` §5.1). |
| ELG-02 | Eligibility rules may express: required skill level, permitted branches, permitted cities, permitted time windows, required equipment or certification. |
| PART-01 | A part used in a job must either exist in the **spare-parts catalogue** or be recorded as a **manually approved part** with a mandatory reason and a price inside the platform's allowed margin. A technician cannot invent a price outside the rule (`FR-JOB-03`). |

### 2.1 Rules

- CAT-01 — A variant inherits all attributes of its service and category unless explicitly overridden.
- CAT-02 — A service is bookable only if it has at least one active variant and a published price band for the booking's geography.
- CAT-03 — Category, service and variant codes are **immutable** after creation. Renaming changes only the display name.
- CAT-04 — Every service declares a `workflow_family`. Services in the same family share a workflow template shape but may have independent instances.

---

## 3. Workflow Template Model

### 3.1 Structure

```jsonc
{
  "template_code": "WT_APPLIANCE_REPAIR_V1",
  "category_id": "CAT_APPLIANCE_REPAIR",
  "version": 1,
  "status": "PUBLISHED",
  "applies_to": { "category_id": "CAT_APPLIANCE_REPAIR" },
  "steps": [
    {
      "key": "diagnose",
      "label": { "en": "Diagnose the issue", "or": "ସମସ୍ଯାର ନିର୍ଣୟ", "hi": "समस्या का पता लगाएं" },
      "sequence": 10,
      "type": "CHECKLIST",
      "mandatory": true,
      "sla_minutes": 20,
      "items": [
        { "code": "diag.inspect", "label": "Physical inspection", "type": "CHECK", "mandatory": true },
        { "code": "diag.photo",   "label": "Photo of the fault",  "type": "PHOTO", "mandatory": true, "min_count": 1 },
        { "code": "diag.note",    "label": "Diagnosis notes",    "type": "TEXT",  "mandatory": true, "min_length": 20 }
      ]
    },
    {
      "key": "approval",
      "label": { "en": "Customer approval for work & parts" },
      "sequence": 20,
      "type": "APPROVAL",
      "mandatory": true,
      "requires_customer_action": true,
      "timeout_minutes": 60,
      "on_timeout": "ESCALATE_TO_BRANCH"
    },
    {
      "key": "repair",
      "label": { "en": "Carry out the repair" },
      "sequence": 30,
      "type": "CHECKLIST",
      "mandatory": true,
      "items": [
        { "code": "repair.action", "label": "Repair action performed", "type": "TEXT", "mandatory": true },
        { "code": "repair.parts",  "label": "Parts replaced (if any)", "type": "PARTS", "mandatory": false },
        { "code": "repair.photo_after", "label": "Photo after repair", "type": "PHOTO", "mandatory": true, "min_count": 1 }
      ]
    },
    {
      "key": "test",
      "label": { "en": "Test & handover" },
      "sequence": 40,
      "type": "CHECKLIST",
      "mandatory": true,
      "items": [
        { "code": "test.run",   "label": "Run & test the appliance", "type": "CHECK", "mandatory": true },
        { "code": "test.demo",  "label": "Demonstrate working to customer", "type": "CHECK", "mandatory": true }
      ]
    }
  ],
  "required_evidence": [
    { "code": "before", "label": "Before photo", "min_count": 1, "mandatory": true },
    { "code": "after",  "label": "After photo",  "min_count": 1, "mandatory": true }
  ],
  "sla": {
    "arrival_minutes": 120,
    "completion_minutes": 120,
    "warranty_days": 30
  },
  "requires_customer_otp_on_start": true,
  "allows_parts": true,
  "parts_pricing_rule": "MRP_OR_ALLOWED_MARGIN",
  "commission_base": "LABOUR_ONLY"
}
```

### 3.2 Step Types

| Type | Semantics | Blocking completion? |
|---|---|---|
| `CHECKLIST` | A set of items (CHECK / TEXT / PHOTO / PARTS / NUMBER) | Yes, if `mandatory` |
| `APPROVAL` | Explicit customer confirmation (OTP or in-app) | Yes |
| `PHOTO_SET` | A capture group (before / after) | Yes, if `mandatory` |
| `OTP` | Customer identity verification at a point in the flow | Yes |
| `SIGNATURE` | Customer digital signature (optional categories) | No |
| `INFORMATION` | Read-only instruction shown to the technician | No |
| `AUTO` | System-computed step (invoice generation, commission accrual) | Yes |

### 3.3 Execution Semantics

| Rule | Statement |
|---|---|
| WF-01 | A workflow instance is created when the booking is accepted. It is a **snapshot** of the published template — later template edits do not affect in-flight jobs. |
| WF-02 | Steps execute strictly in `sequence` order; a step cannot be completed before its predecessor is complete. |
| WF-03 | A mandatory step blocks `COMPLETED` until satisfied. |
| WF-04 | A non-mandatory step may be skipped only with a reason, which is audited and visible to the branch. |
| WF-05 | A step may be **skipped with override** (`blocked` → `skipped_with_override`) by a technician with `job:override`, requiring a reason; a blocked/overridden item is flagged in the QA report. |
| WF-06 | `APPROVAL` steps have a timeout; on timeout the job escalates to the branch and the technician cannot complete. |
| WF-07 | Template versions are immutable once published. A change creates a new version, effective-dated. |
| WF-08 | Every step transition is timestamped and attributed to the actor. |

### 3.4 Workflow Instance State

```
PENDING → ACTIVE → COMPLETED
            │  ↑
            │  └── STEP_REOPENED (branch re-open, audited)
            ├── PAUSED (awaiting customer approval)
            ├── TIMED_OUT (approval timeout)
            └── CANCELLED (booking cancelled)
```

---

## 4. Launch Catalogue — Per-Category Workflows

> **Two conflicts are registered against this section's title, and neither side has been edited into the
> other (`DEC-07`).** §4.1–§4.6 declare **six** launch families, while `00` §4.1 BO-1 and `17` P0-09 say
> **three**, `17` P2-02 names **four**, and `OD-RM-04` recommends **two** — that is `OD-DOC-27`, and it is
> the number the asset and design estimate in `31` has to be built on. Separately, §4.3 `HOME_SALON` and
> §4.4 `BEAUTY_PARLOUR` sit under a heading that says *Launch Catalogue* while `17` §6 places both in
> **Phase 4 — Growth**, and `06` §8's own `OD-06-01` gives them a Phase 2 deadline; that is
> `OD-DOC-28`. Both carry rules a first release may not be able to host — `BP-02` is a mandatory consent
> step and `BP-01` a skill-gated paramedical rule — so `OD-DOC-28` is a compliance question as well as a
> sequencing one. **Nothing here is decided**; this section is the six-family specification, and the launch
> subset is what `OD-DOC-27` must name.

### 4.1 APPLIANCE_REPAIR — *Primary Business*

| Attribute | Value |
|---|---|
| Workflow family | `REPAIR_WITH_DIAGNOSIS` |
| Customer OTP on start | Yes |
| Customer approval for parts | **Yes** (mandatory) |
| Parts allowed | Yes (MRP or allowed margin) |
| Evidence | Before + after photo |
| Warranty | 30 days (parts), 15 days (labour) |
| Commission base | Labour only (diagnostic charge counts as labour) |
| Typical duration | 60–120 min |

**Steps**

| Seq | Step | Mandatory | Detail |
|---|---|:--:|---|
| 10 | Diagnose | ✔ | Inspect, photograph the fault, note the diagnosis |
| 20 | Customer approval | ✔ | Approve the repair + any parts and the price. OTP or in-app |
| 30 | Repair execution | ✔ | Record the action performed; add parts; photo after repair |
| 40 | Test & handover | ✔ | Run the appliance, demonstrate to the customer |
| 50 | Invoice | ✔ | Auto — from the price snapshot + adjustments |
| 60 | Warranty registration | ✔ | Auto — warranty window opens on completion |

**Category rules**
- `PR-01` — A job whose diagnosis says "not repairable" is completed with **no charge for labour**; the visiting charge applies. The system offers a replacement-service flow.
- `PR-02` — If the actual parts cost exceeds the estimate by > 20%, a fresh customer approval is required.
- `PR-03` — Warranty visits are flagged `bookings.is_warranty_job = true` (`09` §4.6); they do **not** generate commission, and the technician receives a flat warranty-visit incentive from a separate pool. The flag was not declared in the data model before `09` v1.2, so this rule was unimplementable — it is now a column, not an assumption. **The size of the flat incentive and the "separate pool" are not defined anywhere**, so `PR-03` cannot be configured yet (`OD-06-10`).

### 4.2 CLEANING

| Attribute | Value |
|---|---|
| Workflow family | `PACKAGE_SERVICE` |
| Customer OTP on start | Optional `[PROPOSED]` — see OD-06-02 |
| Parts allowed | No |
| Evidence | Before/after photos of the primary area |
| Warranty | 7 days (re-clean) |
| Commission base | Labour only |
| Typical duration | 90–240 min (size dependent) |

**Steps**

| Seq | Step | Mandatory | Detail |
|---|---|:--:|---|
| 10 | Confirm scope | ✔ | Checklist of rooms/areas against the package |
| 20 | Supplies & setup | ◐ | Text + checklist |
| 30 | Cleaning execution | ✔ | One checklist item per included task (floor, bathroom, kitchen, etc.) |
| 40 | Quality check | ✔ | Technician self-check checklist |
| 50 | Photo evidence | ✔ | Before/after |
| 60 | Customer sign-off | ◐ | Signature or in-app confirm |

**Category rules**
- `CL-01` — Cleaning checklists are **package-derived**: the 2 BHK package has a different task list than 3 BHK.
- `CL-02` — **No parts** are permitted; adding a part blocks completion.
- `CL-03` — Cleaning is sold with **no advance** by default; the advance rule is configurable.

### 4.3 HOME_SALON

| Attribute | Value |
|---|---|
| Workflow family | `PERSONAL_SERVICE` |
| Customer OTP on start | No `[PROPOSED]` — see OD-06-01 |
| Parts allowed | No (products are platform-supplied or included) |
| Evidence | Optional before/after photo (customer consent) |
| Warranty | Not applicable; **redo window = 24 h** |
| Commission base | Labour only (package value) |
| Typical duration | 60–150 min |

**Steps**

| Seq | Step | Mandatory | Detail |
|---|---|:--:|---|
| 10 | Service & package confirmation | ✔ | Select package, therapist preference (if offered) |
| 20 | Therapist arrival | ✔ | Technician confirms arrival; customer may confirm in-app |
| 30 | Service execution | ✔ | Checklist of included items (haircut, spa, facial…) |
| 40 | Post-service check | ✔ | Quality checklist |
| 50 | Invoice & payment | ✔ | Auto |
| 60 | Feedback | ◐ | Rating + review |

**Category rules**
- `HS-01` — The appointment has a strong **slot-occupancy** character: the technician is reserved for the window, and a no-show is penalised.
- `HS-02` — **Gender preference** for the therapist is supported as a filter on the candidate list, not as a hard rule.
- `HS-03` — Products are included in the package price; no part capture is possible.
- `HS-04` — A 24-hour redo window is offered instead of a warranty.

### 4.4 BEAUTY_PARLOUR

| Attribute | Value |
|---|---|
| Workflow family | `PERSONAL_SERVICE` (advanced) |
| Customer OTP on start | No `[PROPOSED]` |
| Parts allowed | No |
| Evidence | Before/after photo with consent |
| Warranty | Not applicable; **redo window = 24 h** |
| Commission base | Labour only |
| Typical duration | 60–180 min |

**Steps**

| Seq | Step | Mandatory | Detail |
|---|---|:--:|---|
| 10 | Consultation | ✔ | Record the customer's stated look/requirement |
| 20 | Service selection confirmation | ✔ | Confirm procedures and the final price |
| 30 | Service execution | ✔ | Procedure checklist |
| 40 | Post-service presentation | ✔ | Photo evidence (consent-based), stylist sign-off |
| 50 | Invoice & payment | ✔ | Auto |

**Category rules**
- `BP-01` — Paramedical/advanced services (e.g. chemical peels, laser) are restricted to technicians holding the required **skill level**, enforced at candidate selection.
- `BP-02` — A **consent record** step is mandatory for treatments requiring it.
- `BP-03` — Advanced-service price books are per-variant with narrower bands (advanced work has tighter margins).

### 4.5 PLUMBING

| Attribute | Value |
|---|---|
| Workflow family | `REPAIR_WITH_DIAGNOSIS` |
| Customer OTP on start | Yes |
| Customer approval for parts | **Yes** |
| Parts allowed | Yes |
| Evidence | Before/after photo |
| Warranty | 30 days |
| Commission base | Labour only |
| Typical duration | 60–180 min |

**Steps** — Diagnose → Customer approval (materials + scope) → Execute (materials recorded) → Test (leak/pressure test) → Handover.

**Category rules**
- `PL-01` — Materials are captured as parts with quantity and unit price; the margin rule applies.
- `PL-02` — A "not repairable" outcome follows `PR-01`.

### 4.6 ELECTRICAL

| Attribute | Value |
|---|---|
| Workflow family | `REPAIR_WITH_DIAGNOSIS` |
| Customer OTP on start | Yes |
| Customer approval for parts | **Yes** |
| Parts allowed | Yes |
| Evidence | Before/after photo |
| Warranty | 30 days |
| Commission base | Labour only |
| Typical duration | 60–180 min |

**Steps** — Diagnose & isolate → Customer approval → Execute (with a **safety checklist**: main switch off, earthing verified, no live work) → Test → Handover.

**Category rules**
- `EL-01` — A mandatory safety checklist (`main_isolated`, `earthing_checked`, `ppe_used`) must be completed before any execution step.
- `EL-02` — Electrical jobs require a **minimum skill level**; the candidate filter is strict.

### 4.7 Future Categories (Configured, Not Coded)

`AC_SERVICING` · `PEST_CONTROL` · `CARPENTRY` · `PAINTING` · `ROOFING` · `FURNITURE_REPAIR` · `TV & APPLIANCE INSTALLATION` · `MOVING & SHIFTING` · `CCTV INSTALLATION` · `WATER PURIFIER SERVICE` · `ROOF & GUTTER` · `DEEP CLEANING` · `INTERIOR PAINTING`

Each is created by cloning a family template and adjusting checklists, evidence, SLA, warranty and price book.

---

## 5. Technician Eligibility Engine

### 5.1 Match Factors

| Factor | Source | Enforcement |
|---|---|---|
| Category | `technician.categories` | Hard filter |
| Skill + minimum level | `technician.skills` | Hard filter |
| Service-area pin | `technician.service_area_pins` | Hard filter |
| Verification state | `technician.verification_state` | Hard filter |
| Document validity | `technician_documents` | Hard filter |
| Accepting new jobs | `technician.availability` | Hard filter |
| Capacity for the slot | `technician.capacity` | Hard filter |
| Distance | Live location or centroid | Soft (ranking) |
| Rating, completion rate, on-time rate | Score tables | Soft (ranking) |

### 5.2 Selection Rule

```
CANDIDATES(service, address, slot) =
    { t | hard_filter(t) = true }
    ORDER BY score(t) DESC
```

**Rules**
- EL-01 — A technician who does not satisfy every hard filter is **never** offered a job, regardless of ranking.
- EL-02 — "First available" (open feed) books to the top candidate; the feed then rotates to the next candidate on rejection/expiry.
- EL-03 — Skill levels are hierarchical (`1` Trainee, `2` Certified, `3` Senior, `4` Master). A service declares the minimum level; a technician at a higher level is eligible.
- EL-04 — Category membership is a many-to-many; a technician can belong to several categories.
- EL-05 — Service-area pins may be many (a technician typically covers 2–5 areas). A pin may be a **polygon** (primary) or a **radius around a home point** (secondary, auto-expanded on approval).

### 5.3 Coverage Diagnostics

For every (service area × service), the platform computes:

| Metric | Definition | Target |
|---|---|---|
| `eligible_count` | Technicians passing all hard filters | ≥ 3 |
| `active_count` | Currently accepting jobs | ≥ 2 |
| `avg_rating` | Mean rating of eligible technicians | ≥ 4.0 |
| `last_30d_jobs` | Jobs completed in the area | trend |

`coverage_health` = `RED` if `eligible_count < 1`, `AMBER` if `< 3`, `GREEN` otherwise. The Operations
dashboard alerts on `RED` and `AMBER` areas (`FR-RPT-06`).

---

## 6. Catalogue Configuration Workflow

```
Draft → Review → Published → (New version) → Retired
```

| Transition | Actor | Approval | Notes |
|---|---|---|---|
| Draft → Review | Category owner (Admin / Marketing Ops) | — | Drafts are invisible to the apps |
| Review → Published | Admin | Admin | Publishing activates it for eligible areas |
| Published → Retired | Admin | Admin | Existing bookings keep their snapshot; no new bookings |

**Publishing checklist**
1. Category, services and variants created with localised names.
2. Workflow template published and validated.
3. Skill requirements defined.
4. Price book populated for at least one geography per launch city.
5. Test booking executed end-to-end in a **test area**.
6. Support macros and notification templates created.
7. Commission rate confirmed by Finance.

---

## 7. Content Localisation

| Object | Localised | Fallback |
|---|---|---|
| Category / Service / Variant names | Yes | English |
| Workflow step labels and checklist item labels | Yes | English |
| Evidence prompts | Yes | English |
| Notification templates | Yes | English |
| Price book | No (currency amounts are global) | — |
| Terms & policy documents | Yes | English |

**LOC-01** — Locale codes are BCP-47: `en`, `or` (Odia), `hi` (Hindi). `or` is the default for Odisha branches.

---

## 8. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| OD-06-01 | Is customer OTP mandatory for HOME_SALON / BEAUTY_PARLOUR job start? | Product + Ops | Phase 2 |
| OD-06-02 | Do cleaning jobs need customer OTP on start, or is the technician's arrival sufficient? | Product | Phase 2 |
| OD-06-03 | Which skill levels do we certify, and who certifies them (AmmPal or the partner branch)? | Partner Ops | Phase 2 |
| OD-06-04 | Is a **subscription / recurring** model (e.g. monthly AC servicing) in v1.0? | Product | Phase 3 |
| OD-06-05 | Do we need per-technician **surge pricing** for peak demand (e.g. festival/heatwave)? | Product + Finance | Phase 3 |
| OD-06-06 | Is a "no-show appliance / not accessible" workflow needed, and is it billed? | Product | Phase 2 |
| OD-06-07 | Are add-ons in v1.0 scope, and does an add-on price enter the commission base? (full text in `21`) | Product + Finance | Phase 1 |
| OD-06-08 | Is the spare-parts catalogue seeded, or manually approved parts only? (full text in `21`) | Product + Ops | Phase 1 |
| OD-06-09 | Are eligibility rules needed in v1.0 beyond skill + category + service area? (full text in `21`) | Product | Phase 2 |
| OD-06-10 | What is the **flat warranty-visit incentive** in `PR-03`, and which pool pays it? No document sets an amount, a funding source or a ledger treatment, so the rule that exempts a warranty visit from commission has no replacement earning for the technician. | Product + Finance | Before Phase 1 |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.3 | 2026-10-21 | Product Lead + Engineering Lead (design-system and asset pass) | Two blockquotes added; no hierarchy, family, service, variant, workflow step or rule changed. **§2** now records that the Category→Service→Variant hierarchy is also the unresolved **unit of visual design** (`OD-DOC-33`): `31` §4 measured the design brief against it and found six of nine named appliance lines absent from every document, and `09` §4.3 declares no media field at any of the three levels (`OD-DOC-26`). **§4** now states that its own title, "Launch Catalogue", is the disputed side of two registered conflicts — the 3 / 4 / 6 / 2 category count (`OD-DOC-27`), and `HOME_SALON` / `BEAUTY_PARLOUR` being launch families here, Phase 4 in `17` §6 and a Phase 2 deadline in this document's own §8 `OD-06-01` (`OD-DOC-28`), with `BP-01`'s skill gate and `BP-02`'s mandatory consent step named as the reason the second is a compliance question and not only a sequencing one. Both sides annotated per `DEC-07`. | §2, §4, header, Revision History |
| 1.2 | 2026-10-21 | Product Lead + Engineering Lead | Audit pass 3. `PR-03` now names the column it depends on (`bookings.is_warranty_job`, added in `09` v1.2) instead of assuming a `warranty_job` flag the data model never declared, and flags that the flat warranty-visit incentive has **no amount, no funding source and no ledger treatment in any document** (`OD-06-10`) — the rule is unconfigurable as written. §8 extended with `OD-06-07`…`OD-06-10`, mirroring the full text held in `21`. Note for the owner: the four catalogue entities this document specifies in §2 — spare-parts catalogue, add-on, eligibility rule, manually approved part — have **no tables in `09`**; registered as `OD-DOC-17`. | §4.1, §8 |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Added add-ons, estimated duration, eligibility rules and the spare-parts catalogue to the entity model with rules ADD-01..05, DUR-01..02, ELG-01..02 and PART-01; cross-referenced the workflow versioning ADR and the technician eligibility engine. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
