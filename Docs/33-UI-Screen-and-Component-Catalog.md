# 33 — UI Screen and Component Catalog

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-33 |
| Version | 1.3 |
| Status | **PROPOSED — not approved.** Every screen below is `UNDESIGNED`; no wireframe or build exists. |
| Owner | Product Design Lead + Frontend Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-22 |
| Depends On | `12` (canonical screens), `03`, `04`, `06`, `07`, `10`, `23`, `30`, `31`, `32`, `34`, `35` (which directory each screen's code lives in), `36` (what it may be built from), `37` (the contract each named component must satisfy) |

---

## 1. What this adds to `12`, and what it deliberately does not repeat

`12` §2–§5 already own the screen inventories — website IA and page detail, 26 customer-app screens,
21 partner-app screens, the Control Center navigation tree and 12 key screens. **Restating them in a
second document is the duplication `DEC-01` exists to prevent**, and it is how two "sources of truth"
start disagreeing. So `33` keeps only the columns `12` does not carry, keyed to `12` by stable IDs:

| ID | Points at | Purpose |
|---|---|---|
| `SCR-WEB-nn` | `12` §2.1 rows 1–9 | website page types |
| `SCR-CUS-nn` | `12` §3.2 rows 1–26 | customer app |
| `SCR-PAR-nn` | `12` §4.2 rows 1–21 | partner app |
| `SCR-CC-nn` | `12` §5.2 rows 1–12 | Control Center key screens |
| `SCR-PD-…` | **not issued** | `12` §1 conditional fifth surface (`ADR-021`) has no documented screens |

State legend used in the tables (each state is a *design requirement*, not an implementation claim):
**L** loading/skeleton · **E** empty · **F** failure/offline/retry · **P** permission-denied or
out-of-scope (renders as "not found" — `03` §5 step 3) · **S** no-serviceable-area (`23` §5, ADR-004) ·
**A** action-in-flight, control disabled (no double submit — `23` §3.2).

**Design status is `UNDESIGNED` for all 68 rows.** `README` §4.1 records that nothing in this
repository qualifies as `[IMPLEMENTED]`, so no screen here can be "built", and no asset in `31` has a
`APPROVED` record.

**Placeholder-first does not change a row's status.** The owner directed SVG or blank containers at design
time (`30` §5.3), so a screen in §3–§4 can have its layout, states and asset *slots* reviewed while every
`AMM-*` reference in its Assets column still resolves to an empty container. That is a layout review. It
is not a design approval, and under `OD-DOC-36` it is not yet clear that a layout-only approval can be the
event `26` §4.1 pays ₹1,00,000 on — which is `19` `R-45` seen from the screen side. **A row stays
`UNDESIGNED` until the design gate has a written definition and the owner signs it**, and no row was
re-marked here because containers exist. Where a raster is eventually generated, whoever runs `34` §4
produces it — this catalog names the slot, `34` holds the prompt, and neither duplicates the other.

---

## 2. Two joins that the documents do not currently support

This is the honest limit of the catalog, and it is why two columns are placeholders rather than data:

| Column | Why it cannot be filled | Registered as |
|---|---|---|
| **Related API** | No document joins a screen to an endpoint. `10` §4 lists 117 route rows; `12` §2–§5 lists screens; nothing maps one to the other. Guessing a mapping would fabricate a contract. | `OD-DOC-29` |
| **Permission token** | `OD-10-06` is already `[BLOCKER]`: nothing joins `10` §4's endpoints to `03` §4's 92 permission tokens (and 29 actions used in `03` §4 are outside the 11 declared in §3.2, while `delete` appears nowhere). A screen→token column built on that gap would be a security document that is wrong. | `OD-10-06`, extended by `OD-DOC-29` |

Both are owner/engineering decisions. Until they close, the RBAC model in `03` is the constraint on
*which* screens a role can reach (`12` §1.1 and §5.3 give that mapping), not on which call each screen
makes.

---

## 3. Website — 9 page types (`12` §2.1; 16 routes in `12` §2)

| ID | Page | States | Assets (from `31`) | Workflow / data | Design status |
|---|---|---|---|---|---|
| SCR-WEB-01 | Home | L, F | `AMM-WEB-HERO-HOMEPAGE-1600`, `AMM-SERVICE-*-ICON-24`, `AMM-BRAND-LOGO-HORIZONTAL` **+ the eight sections' artwork of `39` §3**: 5 × `AMM-WEB-ILLU-*-REPAIR-800`, 3 × `AMM-WEB-ILLU-STEP-*-800`, `AMM-WEB-ILLU-PRICING-TRANSPARENT-800`, `AMM-WEB-ILLU-TRUST-VERIFIED-800`, `AMM-WEB-ILLU-SERVICEABILITY-800`, `AMM-WEB-ILLU-SUPPORT-HELPLINE-800`, `AMM-BRAND-PATTERN-BACKGROUND` (offer strip at 6 %) | search entry, city picker, category rail — `12` §2.1; `06` §2 catalogue; section order and slot sizes — `39` §3 | UNDESIGNED |
| SCR-WEB-02 | Category listing | L, E, S | `AMM-SERVICE-*-ICON-24`; the 5 `AMM-WEB-ILLU-*-REPAIR-800` appliance tiles registered 2026-10-22; `AMM-SERVICE-*-CATEGORY-800` **BLOCKED** | `06` §2; availability badge needs ≥ 1 technician | UNDESIGNED |
| SCR-WEB-03 | Service detail | L, E, S | `AMM-SERVICE-*-CATEGORY-800` **BLOCKED**, `AMM-WEB-ILLU-SERVICEABILITY-800` | variant picker, location-specific price range — `07`, `06` | UNDESIGNED |
| SCR-WEB-04 | Technician list | L, E | `AMM-WEB-PLACEHOLDER-PARTNER-512` | `01` FR-CAT-05; rating from verified completed bookings only (`13` §5.3) | UNDESIGNED |
| SCR-WEB-05 | Technician profile | L, E | `AMM-WEB-PLACEHOLDER-PARTNER-512` | review moderation badge — `12` §2.1 | UNDESIGNED |
| SCR-WEB-06 | Booking flow (7-step stepper) | L, F, A | none | `04` §2 nine-stage lifecycle; `23` §3 transitions; address first | UNDESIGNED |
| SCR-WEB-07 | Booking detail + tracking | L, F | marker set `AMM-CONTROL-MARKER-*` | `23` §2.3 status, §3 transitions; socket then poll (`12` §3.3) | UNDESIGNED |
| SCR-WEB-08 | Partner registration (multi-step, resumable) | L, F, A | `AMM-WEB-HERO-PARTNER-1600` (the `/partner` landing above the form) | `23` §8 onboarding machine; KYC upload via presigned URL (`10` §11) | UNDESIGNED |
| SCR-WEB-09 | Support / FAQ / toll-free | L, E | `AMM-WEB-ILLU-SERVICEABILITY-800`, `AMM-WEB-ILLU-SUPPORT-HELPLINE-800` | `05` §3 call paths; IVR-08/09 (`05` §3.7) | UNDESIGNED |

Legal pages (`/terms`, `/privacy`, `/refund-policy`) and `/offers` are **routes without an approved
content source** — `12` §2 lists them, `26` §8 says legal content is not covered by this suite. They need
copy, not design, and no asset is claimed for them beyond OG images. `/pricing` and `/partner` moved out
of that sentence on 2026-10-22, because they now have registered artwork — `AMM-WEB-ILLU-PRICING-TRANSPARENT-800`
and `AMM-WEB-HERO-PARTNER-1600`. That is an artwork row, **not** an approved page: the copy these two
routes carry is still the owner's to supply, the price band is a server computation in integer paise
(`00` FR-01/FR-03), and no earning, payout or partner-count claim may be drawn into either file
(`26` §4.1, `34` §7).

---

## 4. Customer app — 26 screens (`12` §3.2)

| ID | Screen | States | Assets | Workflow / data |
|---|---|---|---|---|
| SCR-CUS-01 | Splash / auth (OTP, language pick) | L, F, A | `AMM-BRAND-MARK-MONOGRAM` | `04` §8 OTP timers; **validity conflict `OD-DOC-24`** (10 min in `04`/`23` vs 5 min recommended in `OD-SMS-03`) |
| SCR-CUS-02 | Home | L, E | `AMM-SERVICE-*-ICON-24`, offer strip | `12` §3.1 tabs |
| SCR-CUS-03 | Location picker | S, F | `AMM-WEB-ILLU-SERVICEABILITY-800`, markers | `23` §5 serviceability (ADR-004); pincode fallback (`12` §3.3) |
| SCR-CUS-04 | Category list | E | `AMM-SERVICE-*-ICON-24` **only** — icons + localised names, per `12` §3 screen 4 | `06` §2 |
| SCR-CUS-05 | Service list | E, S | `AMM-SERVICE-*-CATEGORY-800` **BLOCKED** | `06`, `07` price bands |
| SCR-CUS-06 | Service detail | E, S | as above | `06` §3 workflow templates |
| SCR-CUS-07 | Technician list | E | `AMM-WEB-PLACEHOLDER-PARTNER-512` | ranking reason shown (`12` §3.3) |
| SCR-CUS-08 | Technician profile | E | `AMM-WEB-PLACEHOLDER-PARTNER-512` | `01` FR-CAT-05 |
| SCR-CUS-09 | Slot picker | E, F | none | live availability, `12` §3.2; urgent slot is `OD-UX-04` |
| SCR-CUS-10 | Booking summary | L, A | none | `07` §3 price components; XS-02 money format |
| SCR-CUS-11 | Coupon apply | E, F | none | `23` §10 coupon machine; rejection reason required |
| SCR-CUS-12 | Payment | L, F, A | none | gateway-hosted sheet; `23` §11.2; `13` §5.2 `frame-src api.razorpay.com` |
| SCR-CUS-13 | Booking confirmation | L | `AMM-CUSTOMER-SUCCESS-BOOKING-600` | booking code XS-01; **no animation may imply a confirmed state** (`30` §7) |
| SCR-CUS-14 | Booking list (4 tabs) | E, F | `AMM-CUSTOMER-EMPTY-BOOKINGS-600` | cached offline (`12` §3.3) |
| SCR-CUS-15 | Booking detail | L, F | markers, `AMM-CUSTOMER-SUCCESS-BOOKING-600` | `23` §2.3/§3; XS-03 identical timeline on every surface |
| SCR-CUS-16 | Live tracking | F | `AMM-CONTROL-MARKER-TECHNICIAN-32` | socket → poll with honest freshness (`12` §3.3) |
| SCR-CUS-17 | Job start OTP | F, A | none | `23` §6 arrival/OTP; resend window per `OD-DOC-24` |
| SCR-CUS-18 | Approve work & parts | F, A | none | `23` §6 `AWAITING_CUSTOMER_APPROVAL` (60 min SLA); signature capture (`09` §4.7 `SIGNATURE`) |
| SCR-CUS-19 | Invoice | L, F | none | `09` §4.10 `document_url`; XS-02; **no InvoiceView component exists in `12` §6.2** |
| SCR-CUS-20 | Payment success | L | `AMM-CUSTOMER-SUCCESS-BOOKING-600` | `23` §11.2 — only a gateway-confirmed state may render success |
| SCR-CUS-21 | Rating & review | E, A | none | `13` §5.3 rating limited to verified completed bookings |
| SCR-CUS-22 | Wallet | E | `AMM-CUSTOMER-EMPTY-…` reuse | **scope undecided** — `OD-UX-02`; do not design until it closes |
| SCR-CUS-23 | Notifications | E | `AMM-CUSTOMER-EMPTY-NOTIFICATIONS-600` | `11` §3 |
| SCR-CUS-24 | Support | E, F | `AMM-CUSTOMER-EMPTY-SUPPORT-600` | `05` §5 use cases; §6 ticket model; ticket creation |
| SCR-CUS-25 | Account | L | none | addresses, language, privacy & consent (`13` §6.1 erasure — `OD-DOC-23`) |
| SCR-CUS-26 | Cancellation sheet | A | none | policy, refund amount, penalty — `04` §6; `07` §3; `23` §11.3 refund machine |

## 4.1 Partner app — 21 screens (`12` §4.2)

| ID | Screen | States | Assets | Workflow / data |
|---|---|---|---|---|
| SCR-PAR-01 | Onboarding (OTP → KYC → skills → areas → bank → agreement) | L, F, A | **onboarding illustration set lives here, not in `03-customer-app`** (`31` §6) | `23` §8; KYC via presigned URL, `24` §11 (5-min expiry) |
| SCR-PAR-02 | Verification pending | L | none | `23` §8; "what's missing" must come from `technician_documents.verification_state` (`09` §4.4) |
| SCR-PAR-03 | Job feed (offers) | E, F | `AMM-PARTNER-EMPTY-JOBS-480` | `23` §3 `AWAITING_PARTNER` (5 min direct / 10 min feed) |
| SCR-PAR-04 | Accept timer | A | none | countdown ring — `12` §4.3; `23` §3.2 concurrency |
| SCR-PAR-05 | Job detail | L, F | none | checklist, parts, evidence (`06` §3.1, `09` §4.7) |
| SCR-PAR-06 | Navigate | F | markers | deep link to maps (`13` §5.2 hosts) |
| SCR-PAR-07 | Arrival & OTP | F, A | none | `23` §6 `ARRIVED` 10-min SLA |
| SCR-PAR-08 | Execute job (checklist) | L, F, A | none | **offline-first** (`12` §4.3); photo evidence min 1 (`06` §3.1, `01` FR-JOB-04) |
| SCR-PAR-09 | Parts entry | E, F | none | margin-bounded price (`07` §3); 4 catalogue entities missing tables — `OD-DOC-17` |
| SCR-PAR-10 | Complete | A | none | warranty + evidence + invoice generation |
| SCR-PAR-11 | Invoice & collect | L, F, A | none | `09` §4.10; payment link/QR; cash entry if enabled (`07`) |
| SCR-PAR-12 | Earnings | E | `AMM-PARTNER-EMPTY-EARNINGS-480` | `07` §7.6 money flow; commission is partner → platform |
| SCR-PAR-13 | Earnings detail | E | none | plain-language derivation required (`12` §4.3) |
| SCR-PAR-14 | Settlement statement | E, F | `AMM-PARTNER-EMPTY-SETTLEMENT-480` | `07` §7.6 `STL-<YYYY>-W<WW>-<BRANCH>-<NNNN>`; `23` §12 |
| SCR-PAR-15 | Dispute | A | none | `23` §12; dispute edges in `07` §7.6 |
| SCR-PAR-16 | Calendar / availability | E | `AMM-PARTNER-EMPTY-CALENDAR-480` | `12` §4.2 (weekly grid, time off, max jobs/day) — no capacity rule exists elsewhere in the suite |
| SCR-PAR-17 | Service areas | S, F | `AMM-CONTROL-MARKER-ZONE-32` | `02` hierarchy; PostGIS polygons (`09`) — **synthetic demo data only** (`30` §9) |
| SCR-PAR-18 | Profile & documents | E, F | `AMM-WEB-PLACEHOLDER-PARTNER-512` | expiry warnings; `SENSITIVE` class (`09` §8) |
| SCR-PAR-19 | Ratings & score | E | none | anomaly-limited ratings (`13` §5.3) |
| SCR-PAR-20 | Support | E, F | none | `05` §6 ticket model |
| SCR-PAR-21 | Notifications | E | none | `11` §3 |

## 4.2 Control Center — 12 key screens (`12` §5.2), reachable per role via §5.1/§5.3

| ID | Screen | States | Assets | Workflow / data |
|---|---|---|---|---|
| SCR-CC-01 | Role-based dashboard | L, P | `AMM-CONTROL-ICON-OVERVIEW-24` + 42 further nav icons | KPI set per role from `12` §5.3; chart rules `30` §8 |
| SCR-CC-02 | Live job feed | L, E, F | `AMM-CONTROL-ICON-JOB-FEED-24`, markers | `23` §2.4 phases; SLA buckets |
| SCR-CC-03 | SLA monitor | E | `AMM-CONTROL-ICON-SLA-MONITOR-24` | `23` §2.4 default SLAs are the breach source |
| SCR-CC-04 | Approvals queue | E, A | `AMM-CONTROL-ICON-APPROVALS-QUEUE-24` | `23` §9 partner/branch approval; overrides logged (`12` §5.2 audit) |
| SCR-CC-05 | Coverage board | E, S | `AMM-CONTROL-MARKER-ZONE-32` | RED/AMBER/GREEN per `23` §5, always with text (A11Y-4) |
| SCR-CC-06 | Price book editor | L, F, A | `AMM-CONTROL-ICON-PRICE-BOOK-24` | `07`; effective-dated, overlap warnings |
| SCR-CC-07 | Commission rate editor | F, A | `AMM-CONTROL-ICON-COMMISSION-RATES-24` | `07` bps; versioned, impact preview |
| SCR-CC-08 | Settlement workbench | L, E, F, A | `AMM-CONTROL-ICON-SETTLEMENTS-24` | `07` §7.6 + `23` §12; reconciliation assertions before issue |
| SCR-CC-09 | Call console | L, F | `AMM-CONTROL-ICON-CALL-CONSOLE-24` | `05` §3.7 IVR paths; recording player via signed URL (`24` §11) |
| SCR-CC-10 | Ticket queue | L, E | `AMM-CONTROL-ICON-TICKET-QUEUE-24` | `23` §13 ticket machine; `05` escalation |
| SCR-CC-11 | Audit log | L, E, P | `AMM-CONTROL-ICON-AUDIT-LOG-24` | `23` §14 transition audit record |
| SCR-CC-12 | Reports | L, E, F | `AMM-CONTROL-ICON-EXPORTS-24` | scope-aware; CSV/XLSX export; `30` §8 chart rules |

The other 31 navigation destinations in `12` §5.1 are the **same screens reached by a different role**,
so they inherit the states above; the 43 nav icons in `31` cover them all, and none is a new screen.

> **No thirteenth `SCR-CC-*` ID was issued for a storage-configuration screen, and that is deliberate.**
> The owner has asked for a super-admin surface where the active media-storage provider is chosen
> (`OD-DOC-34`). `12` §5.2 lists 12 key Control Center screens and names no such surface, `10` §4 has no
> route for one and `03` §4 has no token for it, so this catalog has nothing to key an ID to. Inventing
> `SCR-CC-13` would create a screen, and a screen in this document is a design requirement — it would look
> like an approved requirement that no owner approved (`DEC-03`). It is registered in `21` as
> `OD-DOC-37` and sequenced **after** `OD-10-06`, whose screen→route→token join is exactly what a new
> admin surface needs before it can be written down here at all.
Any Control Center screen with a DataTable needs `AMM-CONTROL-EMPTY-TABLE-480` and, when the row set is
scope-filtered, the "not found" reading in P (`30` §3).

---

## 5. Component state coverage — what `12` §6.2 names, and what it does not

`12` §6.2 is the canonical component list; this table records only whether the **visual states** the
design phase needs are covered. "Missing" rows are candidates for a `12` amendment — they are named
here because the screens in §3–§4 require them, not to justify inventing a feature.

| Component | Named in `12` §6.2 | States to design | Gap |
|---|---|---|---|
| Button / IconButton | yes | default, hover, pressed, focus, disabled, loading, error | — |
| Input / Select / DatePicker / TimePicker | yes | + boundary at 4.76:1 (`color.border-strong`, `30` §3), label, error via `aria-describedby` (A11Y-3) | — |
| LocationSearch / MapPicker | yes | + **S** no-serviceable-area | serviceability state not specified |
| Card / ListTile | yes | service card content, availability badge, "from ₹X" | **no `ServiceCard`** though `12` §2.1 Category listing requires service cards |
| BookingStatusTimeline / Timeline | yes | 15 canonical statuses (`30` §6), text+icon+colour | **no compact status chip/indicator** |
| PriceBreakdown / PriceBreakdownSheet | yes | collapsible with always-visible total (`12` §3.3) | — |
| **BookingSummary** | no | 7-step review, address, slot, technician, total | missing |
| CouponField | yes | eligible, rejected-with-reason | — |
| **EstimateApproval / PartEntry approval** | `PartEntry` only | approve, reject per line, signature | **no approval component**; `OD-DOC-13`/`17` still open on parts entities |
| **PaymentSummary** | no | method, amount, advance vs balance, failure | missing |
| **InvoiceView** | no | itemised lines, tax, download/share | missing (`09` §4.10 `document_url`) |
| DataTable | yes | sort, filter, paginate, export, overflow on 390 px | — |
| EmptyState | yes | `E` per screen (`31` §5) | — |
| **ErrorState / PermissionDenied** | no | `F`, `P` (must read "not found" — `03` §5) | missing |
| Skeleton | yes | `L`; shimmer only while in flight (`30` §7) | — |
| Sidebar / BottomNav / TabBar / AppBar / Drawer | yes | active/focus, role-filtered | — |
| TechnicianCard | yes | photo placeholder, badge row, ranking reason | — |
| SlotGrid | yes | sold-out, urgent (`OD-UX-04` open) | — |
| OTPInput | yes | resend timer, paste/autofill (A11Y-5), validity per `OD-DOC-24` | — |
| ChecklistBuilder / EvidenceUploader | yes | offline queue, min-1-photo gate | — |
| EarningBreakdown / SettlementTable | yes | plain-language derivation, dispute entry | — |
| CallPanel / TicketDrawer | yes | screen-pop, recording player | — |
| ScopeBadge | yes | `GLOBAL`/`STATE`/`BRANCH` switcher (`12` §5.1) | — |
| Rating | yes | attribute sliders, photo, moderation badge | — |

Eight named gaps: **ServiceCard, BookingSummary, compact status indicator, EstimateApproval,
PaymentSummary, InvoiceView, ErrorState, PermissionDeniedState.** They are design work the existing
screens already demand; recording them here keeps `12` §6.2 as the single place a component is added
once the owner accepts it.

---

## 6. Screen → asset roll-up

| Surface | Screens | Distinct asset IDs required | BLOCKED rows |
|---|---|---|---|
| Website | 9 | 24 | 6 category images |
| Customer app | 26 | 9 | 0 |
| Partner app | 21 | 5 | 0 |
| Control Center | 12 (+31 nav destinations) | 49 | 0 |
| Brand / store | — | 12 | 0 |
| Reference only | — | 4 | 0 |

**Total 105 rows in `design-assets/manifests/asset-inventory.csv`; 6 are `BLOCKED` on a registered
decision, 18 are `GENERATED`, and 0 are `APPROVED`.** No screen has a completed design and no asset has
been accepted, so the phase gate in `31` §7 (batches 1–4) is still the whole of the work available to do —
what changed on 2026-10-22 is that eighteen of those rows now have a file to argue about instead of a
sentence, and the website column went 12 → 24 with the twelve section-artwork rows of `34` §4.7.

**Read the roll-up by production route as well as by surface** — the same 105 rows split **36 generatable
raster / 68 vector-or-authored / 1 real-capture** (`34` §1, measured from this file's inputs). By `surface`
column the Control Center holds 49 rows, of which **43 nav icons and 4 map markers are vector-authored**
and only the empty-state and error-state illustrations belong to the generatable 36; the website's 24
referenced IDs include the 6 `BLOCKED` category images, which cannot be prompted until the launch
categories close, and the 12 rows registered for `39` §3's slots, which can. Under placeholder-first
(`30` §5.3) every one of these asset references currently resolves in review to an SVG glyph or an empty
container, which is why the Assets column is a **schedule of work**, not a list of files.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.3 | 2026-10-22 | Product Design Lead + Frontend Lead (website-design pass) | §3's website rows now name the artwork the `39` §3 slot table reserves: **SCR-WEB-01 Home** lists the eight sections' files (5 appliance tiles, 3 step cards, pricing, trust, serviceability, support, pattern at 6 %), **SCR-WEB-02** the appliance tile family beside its still-`BLOCKED` category images, **SCR-WEB-08** the `/partner` hero and **SCR-WEB-09** the support drawing. The paragraph that dismissed `/pricing` and `/partner` as routes with no asset is corrected: they have registered rows now, which is **artwork, not an approved page** — copy remains the owner's, price stays a server computation in integer paise, and no earning/payout/partner-count claim may be drawn into a file. §6 re-measured from the regenerated CSV: register **93 → 105 rows**, website column **12 → 24** distinct IDs, production route **24 → 36** generatable (68 vector and 1 real-capture unchanged), and the sentence "no asset has been produced" replaced with what is now true — **18 `GENERATED`, 0 `APPROVED`**, so the phase gate still has the work. **Every screen stays `UNDESIGNED`; no status, gate, state list or `BLOCKED` classification was softened.** | §3, §6, Revision History, header |
| 1.2 | 2026-10-21 | Product Design Lead + QA Lead (design-engineering structure pass) | Depends On gained `35` (which directory a screen’s code lives in), `36` (what it may be built from) and `37` (the contract each component named here must satisfy). **Every one of the 68 screens is still `UNDESIGNED`**, the API and permission columns are still empty on purpose (`OD-10-06`, `OD-DOC-29`), and the eight components §5 records as required-but-unnamed — ServiceCard, BookingSummary, the compact status indicator, EstimateApproval, PaymentSummary, InvoiceView, ErrorState, PermissionDeniedState — are **still not added**, because `12` §6.2 is their only home and `CA-00` forbids coining a name in this document. What `37` changes is that once a name is added, its contract, variant axes and states have a specified form rather than an implied one. | Depends On, Revision History, header |
| 1.1 | 2026-10-21 | Product Design Lead + Frontend Lead (palette, storage and prompt-pack pass) | §1 gained the rule that **placeholder-first does not change a row's status**: under `30` §5.3 a screen's layout, states and asset slots can be reviewed against empty containers, which is a layout review and not a design approval — `OD-DOC-36` still asks whether a layout-only approval can be the event `26` §4.1 pays on (the same money trigger `19` `R-45` scores), and **all 68 rows stay `UNDESIGNED`**. §4.2 gained the note that **no `SCR-CC-13` was issued** for the super-admin storage-provider surface the owner asked for: `12` §5.2 names no such screen, `10` §4 has no route and `03` §4 no token, so an ID here would fabricate a requirement (`DEC-03`); registered as `OD-DOC-37` and sequenced after `OD-10-06`. §6 gained the **production-route reading** of the same 93 rows (24 generatable / 68 vector-or-authored / 1 real-capture, `34` §1) with the Control Center's 49 broken down honestly as 43 nav icons + 4 map markers vector-authored and only its empty-state and error-state illustrations generatable. `34` added to Depends On. **No screen row, state legend, asset reference, permission citation or component gap in §2–§5 changed.** | §1, §4.2, §6, header, Revision History |
| 1.0 | 2026-10-21 | Product Design Lead + Frontend Lead (documentation pass) | First issue. 68 screens indexed by ID against `12` §2.1/§3.2/§4.2/§5.2 without restating it; per-screen required states, asset IDs from `31` and workflow/data citations to `04`/`05`/`06`/`07`/`09`/`23`; API and permission columns left unpopulated with the reason registered (`OD-DOC-29`, extending `OD-10-06`); eight component-state gaps named against `12` §6.2; partner-dashboard IDs not issued because `ADR-021` leaves the surface conditional. | All |
