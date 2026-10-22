# 12 — UI/UX & Information Architecture

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-12 |
| Version | 1.6 |
| Status | Approved for Design & Development |
| Owner | Product Design Lead + Frontend Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-22 |
| Depends On | `01`, `04`, `06`, `10` |

---

## 1. Surfaces

| Surface | Audience | Platform | Stack | Primary goal | Status |
|---|---|---|---|---|---|
| **Website** | Customers, prospective partners | Mobile web + desktop | Next.js + React + TS | Booking funnel, SEO, partner registration, public pages | Confirmed |
| **Customer App** | Customers | Android + iOS | Flutter | Repeat booking, tracking, payment, rating | Confirmed |
| **Partner App** | Technicians | Android (+ iOS later) | Flutter | Job feed, execution, earnings | Confirmed |
| **Control Center** | Platform staff, branch staff | Desktop web | React + Vite + TS | Operations, finance, support, configuration | Confirmed |
| **Partner dashboard** | Partner organisation owners | Desktop web | React + Vite + TS | Partner-side earnings, settlement, technician roster, local coupons | **Conditional — `ADR-021`; scope open in `21`** |

> **Partner dashboard.** The master project requirements list it as a separate web dashboard "where
> included in the approved scope". It is modelled here so the information architecture is complete,
> but it is **not assumed in the initial delivery**. When included, it reuses the Control Center's
> component library, design tokens and RBAC model, with a distinct permission set scoped to the
> partner organisation's own branches and technicians (`partner:self` rather than staff scope).
> It never exposes platform pricing bands, commission rates, or another partner's data.
> `33` issues **no `SCR-PD-*` IDs** for it and `31` keeps `design-assets/06-partner-dashboard/`
> deliberately empty: an unapproved surface gets no screen catalog and no artwork.

### 1.1 Surfaces by Role

| Role | Website | Customer App | Partner App | Control Center |
|---|:--:|:--:|:--:|:--:|
| Customer | ✔ | ✔ | — | — |
| Technician | ✔ (registration) | — | ✔ | — |
| Super Admin / Admin / Operator / CCO / Accountant / Partner Support / Marketing Ops | — | — | — | ✔ |
| Branch Manager / Partner Branch Admin / Coordinator / Branch Finance | — | — | — | ✔ (branch-scoped) |

### 1.2 Design Principles

| # | Principle |
|---|---|
| DX-1 | **One source of truth for the API.** All clients are generated from OpenAPI. |
| DX-2 | **Offline-tolerant.** The Partner App must let a technician work in a basement with no signal: checklist state, photos and notes are queued locally and synced. |
| DX-3 | **Price transparency.** Every price shown to a customer is the server-computed quote, with the breakdown visible — never a single opaque number. |
| DX-4 | **Design tokens are shared.** One token set (`packages/design-tokens`) drives web, Control Center and both Flutter apps. |
| DX-5 | **Localise everything.** Every user-facing string is externalised. `en` / `or` / `hi`. |
| DX-6 | **Accessible by default.** WCAG 2.1 AA on web; minimum touch target 48 dp on mobile. |
| DX-7 | **Progressive disclosure.** Complex admin screens expose power features progressively; the common path stays short. |

---

## 2. Information Architecture — Website

```
/                                   Home (search entry, city picker, popular services, offers)
/services                           Category listing (location-aware)
/services/{categorySlug}            Services in a category
/services/{categorySlug}/{slug}     Service detail (variants, price range, what's included, FAQs)
/technicians                        Technician discovery (location-aware)
/technicians/{id}                   Technician profile (skills, rating, reviews, completed jobs)
/book/{serviceVariantId}            Booking flow (see §3.2)
/bookings                           Customer booking history (web)
/bookings/{code}                    Booking detail + tracking
/partner                            Partner programme landing page
/partner/register                   Technician / partner registration
/partner/login                      Partner portal entry
/support                            Support, FAQs, policies
/toll-free                          Toll-free call landing page (click-to-call)
/offers                              Coupons and campaigns
/pricing                            How our pricing works (transparency page)
/terms  /privacy  /refund-policy    Legal
```

> **No screen in §2–§5 is joined to an endpoint or a permission token, because no such mapping exists anywhere in this suite.** `10` §4 lists 117 route rows and `03` §4 declares 92 permission tokens; nothing connects them to each other (`OD-10-06`, `[BLOCKER]`) or to the screens here (`OD-DOC-29`). `33` indexes these screens by `SCR-*` ID and leaves its API and permission columns empty **on purpose** — a permission-denied state cannot be drawn against a mapping that has not been published.

### 2.1 Website Pages — Detail

> **The Key Elements column below is the page list, not the layout.** Which sections a page renders, in
> what order, and what image box each section reserves is `39` §2/§3 — a document derived *from* this
> table, which adds no route and removes none (`35` PS-06 keeps the route list's only home here). Where
> the two disagree: this column wins on **what a page must contain**, `39` wins on **how those contents are
> arranged and sized**. Nothing in `39` changes a row below, including the `OD-DOC-25` tile/icon
> annotation, which stays unresolved.

| Page | Key Elements | Notes |
|---|---|---|
| **Home** | City picker, service search, category tiles, "book now" CTA, active offer strip, trust signals | Search-first, not marketing-first. "Tiles" here and "Icons, names" on §3.2 screen 4 are the same unresolved question, twice in one document (`OD-DOC-25`) |
| **Category listing** | Service cards with "from ₹X", availability badge, rating | Availability badge only when ≥ 1 technician |
| **Service detail** | Variant picker, price range, inclusions, exclusions, process steps, warranty, reviews, FAQ | Price range is location-specific |
| **Technician list** | Cards with rating, jobs, distance, price range, verified badges | Sort/filter by rating, price, distance, availability |
| **Technician profile** | Bio, skills, service areas, rating breakdown, review list, completed-job count | Review moderation badge shown |
| **Booking flow** | Stepper (Address → Service → Slot → Technician → Price → Payment → Confirm) | Address first — everything depends on it |
| **Booking detail** | Status timeline, technician card, live map, price breakdown, invoice, actions | The single most important customer screen |
| **Partner registration** | Multi-step: identity → KYC docs → skills → service areas → bank details → review | Progress saved; resumable |
| **Support** | FAQ search, category cards, click-to-call, ticket form | Toll-free number displayed prominently |

---

## 3. Customer App (Flutter)

### 3.1 Navigation

Bottom navigation (5 tabs) + a stack-based flow layer.

```
Bottom tabs:  Home  │  Services  │  Bookings  │  Wallet  │  Account
                   │
                   ├── push/deep-link targets open a modal stack over the tabs
                   └── Tracking opens as a full-screen route from Bookings
```

### 3.2 Screen Inventory

| # | Screen | Purpose | Key Elements |
|---|---|---|---|
| 1 | **Splash / Auth** | OTP login, social login, language pick | Language selector on first launch (defaults by state) |
| 2 | **Home** | Entry point | Location chip (tap to change), search bar, category rail, "Book again" for past services, offer carousel, active booking card |
| 3 | **Location picker** | Choose/enter address | Map + search + saved addresses + pincode fallback + service availability check |
| 4 | **Category list** | Browse categories | Icons, names (localised) `[OPEN]` — the design brief asks for a **photographic tile per category**, which is not what this row specifies; neither text has been edited into the other (`OD-DOC-25`). The screen also presumes imagery the data model cannot reference yet (`OD-DOC-26`) |
| 5 | **Service list** | Services in a category | Price "from", availability, rating, sort/filter |
| 6 | **Service detail** | Decide | Variant picker, inclusions, process, warranty, reviews, price range, "Check availability" CTA |
| 7 | **Technician list** | Compare | Sort (rating/distance/price/soonest), filter chips, "First available" toggle |
| 8 | **Technician profile** | Vet | Photo, skills, rating breakdown, reviews, jobs, service areas, badge row |
| 9 | **Slot picker** | Schedule | Date strip + slot grid (from live availability), "urgent" slot if enabled |
| 10 | **Booking summary** | Review | Address, service, slot, technician, **full price breakdown**, coupon field, cancellation policy |
| 11 | **Coupon apply** | Discount | Eligibility list, rejection reason on failure |
| 12 | **Payment** | Pay advance | Gateway-hosted sheet (UPI/card/netbanking), or "pay after service" |
| 13 | **Booking confirmation** | Reassure | Booking code, technician, timeline preview, WhatsApp/SMS note, track CTA |
| 14 | **Booking list** | History | Tabs: Active / Upcoming / Completed / Cancelled |
| 15 | **Booking detail** | Track | Status timeline, technician card, live map, price breakdown, invoice, actions (cancel/reschedule/change technician/rate/contact support) |
| 16 | **Live tracking** | Watch | Map with technician marker + ETA, call/chat buttons, safety note |
| 17 | **Job start OTP** | Verify | 4-digit entry, resend timer, "share with technician" assist |
| 18 | **Approve work & parts** | Consent | Parts list with prices, approve / reject, signature of approval |
| 19 | **Invoice** | Receipt | Itemised lines, tax breakdown, download / share |
| 20 | **Payment success** | Confirm | Amount paid, method, reference |
| 21 | **Rating & review** | Feedback | Stars, attribute sliders, text, photo |
| 22 | **Wallet** | Money | Upcoming settlement, lifetime earnings, transaction list, payout info |
| 23 | **Notifications** | Inbox | Grouped by booking, deep links |
| 24 | **Support** | Help | Call (click-to-call), ticket list, create ticket, FAQ |
| 25 | **Account** | Settings | Profile, addresses, language, notifications preference, privacy & consent, help, logout |
| 26 | **Cancellation sheet** | Decide | Policy, refund amount, penalty, confirm |

### 3.3 Key Interaction Notes

| Flow | Note |
|---|---|
| Home → Book | Target ≤ 3 minutes. The "Book again" path (previous service + same technician) reaches confirmation in ~45 s. |
| Address | The map is the primary control; a pincode fallback handles low-data networks. |
| Technician comparison | Show at most 3 cards above the fold; a "see all" list expands. Show *why* a technician ranks first ("Closest · 4.8★ · 320 jobs"). |
| Price | The breakdown is collapsible but its **total is always visible**. A "what's included" explainer sits next to it. |
| Tracking | Works with the socket; falls back to polling and shows "updated 30 s ago" honestly. |
| OTP | Large numeric keypad, auto-submit on 4 digits, generous resend window, and a voice-call fallback for the OTP itself. |
| Offline | Bookings list and job details are cached; the technician can open a job offline and sync later. |

---

## 4. Partner App (Flutter)

### 4.1 Navigation

Bottom tabs: **Jobs  │  Earnings  │  Calendar  │  Profile** (+ a **Notifications** icon in the app bar).

### 4.2 Screen Inventory

| # | Screen | Purpose | Key Elements |
|---|---|---|---|
| 1 | **Onboarding** | Register | Mobile OTP → identity → KYC doc upload → skills & levels → service areas (map pin) → bank details → agreement → submit |
| 2 | **Verification pending** | Wait | Status, what's missing, support contact |
| 3 | **Job feed (Offers)** | Accept work | Offer cards: service, distance, slot, payout estimate, accept/reject + reason |
| 4 | **Accept timer** | Urgency | Countdown ring on the offer card |
| 5 | **Job detail** | Execute | Full brief: address + map, customer note, service checklist, parts, photos, price breakdown, contact |
| 6 | **Navigate** | Travel | Directions deep link, ETA, "Start route" |
| 7 | **Arrival & OTP** | Verify | Enter the customer's OTP; request a new one if expired |
| 8 | **Execute job** | Work | Checklist items (tap to complete), text notes, photo capture, parts add, customer approval gate |
| 9 | **Parts entry** | Record | Part name (searchable catalogue), qty, unit price (bounded by the margin rule), MRP vs margin indicator |
| 10 | **Complete** | Finish | Confirmation, warranty selection, photo evidence, "Generate invoice" |
| 11 | **Invoice & collect** | Get paid | Invoice preview, "Collect balance" → payment link / QR, cash entry (if enabled) |
| 12 | **Earnings** | Money | Today / this week / lifetime; commission vs gross; pending settlement |
| 13 | **Earnings detail** | Transparency | Booking-wise: labour, commission rate, platform fee, net, GST note, penalties |
| 14 | **Settlement statement** | Statement | Weekly statement list + detail + PDF download |
| 15 | **Dispute** | Raise | Select a settlement line, reason, attach evidence |
| 16 | **Calendar / availability** | Capacity | Weekly availability grid, time off, "accepting jobs" toggle, max jobs/day |
| 17 | **Service areas** | Coverage | Map with pinned polygons/radii, add/edit, coverage status |
| 18 | **Profile & documents** | Compliance | Photo, bio, skills, document list with expiry warnings, support |
| 19 | **Ratings & score** | Reputation | Score breakdown by component, recent reviews, penalty history |
| 20 | **Support** | Help | Call support, raise a ticket, FAQ |
| 21 | **Notifications** | Inbox | Grouped by job |

### 4.3 Key Interaction Notes

| Flow | Note |
|---|---|
| Offer → Accept | The countdown is visible without opening anything. The payout estimate is shown on the card, not behind a tap. |
| Reject | A reason sheet with 6 options + a note. Rejecting is one thumb-tap and never penalising (unless abuse). |
| Job execution | One-handed operation. The checklist is the screen. Photo capture is inline, not a separate flow. |
| Parts | Search a small catalogue first; free text only if no match. The unit price shows the allowed range inline. |
| Offline | **The most important design constraint.** Checklist completion, notes, photos and parts are stored locally (SQLite/Drift) and synced with a conflict-safe queue. A clear "offline — will sync" banner is always shown. |
| Earnings | Every number has a plain-language explanation. "You earned ₹510 because the job's labour was ₹600 and the platform commission is 15%." |

---

## 5. Control Center (React + Vite)

### 5.1 Navigation

Sidebar navigation, role-filtered, scope-aware. A **global scope switcher** is present for `GLOBAL` and `STATE` users.

```
Overview
Operations
  ├ Bookings            ├ Job Feed (live)      ├ Assignments
  ├ Technicians         ├ Coverage             ├ SLA Monitor
Partners & Branches
  ├ Partner Orgs        ├ Branches             ├ Territory / Service Areas
  ├ Technicians (KYC)   └ Approvals Queue
Catalogue & Pricing
  ├ Categories          ├ Services & Variants   ├ Workflow Templates
  ├ Price Book          ├ Branch Prices         ├ Coupons
Finance
  ├ Commission Rates    ├ Commission Ledger     ├ Settlements
  ├ Invoices            ├ Reconciliation        ├ Adjustments & Disputes
  ├ Tax Registrations   └ Partner Payouts
Support
  ├ Call Console        ├ Ticket Queue          ├ Escalations
  ├ Complaints          └ CSAT & QA
Growth
  ├ Campaigns           ├ Offers                └ Content
Reports
  ├ Funnel & Conversion ├ Revenue & Margin      ├ Technician Performance
  ├ Branch P&L          └ Exports
Administration
  ├ Users & Roles       ├ Audit Log             ├ Feature Flags
  └ Master Data
```

### 5.2 Key Screens

| Screen | Purpose | Notable Features |
|---|---|---|
| **Role-based dashboard** | Home | The KPI set differs per role. Super Admin sees platform health; CCO sees queue health; Accountant sees settlement readiness |
| **Live job feed** | Ops | A real-time board of open bookings by SLA state; drag-free, click-to-act (assign, escalate) |
| **SLA monitor** | Ops | Buckets by elapsed time; breached items surfaced first |
| **Approvals queue** | Ops | A single inbox for partner/branch/technician/coupon/price-overband approvals |
| **Coverage board** | Ops | A service-area × service matrix with RED/AMBER/GREEN health |
| **Price book editor** | Finance | Band editing with live validation; effective-dated; overlap warnings |
| **Commission rate editor** | Finance | Versioned; shows the impact of a rate change before it is saved |
| **Settlement workbench** | Finance | Generation → preview (with reconciliation assertions) → issue → track payment → close |
| **Call console** | Support | Screen-pop panel, ticket drawer, in-app actions, one-click payment link, recording player (signed URL) |
| **Ticket queue** | Support | Saved views per category, SLA countdown, bulk assign, escalation |
| **Audit log** | Admin | Filter by actor, action, entity, date; shows override entries prominently |
| **Reports** | All | Parameterised, scope-aware, CSV/XLSX export, scheduled email |

### 5.3 Role → Dashboard KPI Mapping

| Role | Default dashboard KPIs |
|---|---|
| Super Admin | Active branches · active technicians · bookings today · GMV · commission MTD · settlement accuracy · SLA breach % · coverage RED count |
| Admin | Operator workload · unassigned bookings · overdue approvals · complaint backlog · revenue by branch |
| Operator | Pending partner/branch/technician approvals · unassigned bookings · technician coverage by area · new technician applications |
| CCO | Queue size · avg handle time · FCR · CSAT · open P1 tickets · callbacks pending · missed calls |
| Accountant | Unsettled accruals · statements to issue · unmatched payments · disputes · GST summary · DSO |
| Partner Support | Pending KYC · expiring documents · wallet queries · partner issues |
| Marketing Ops | Coupon performance · booking conversion by campaign · category demand · content gaps |
| Branch Manager | Today's bookings · fill rate · avg accept time · technician utilisation · local rating · complaints · local revenue |
| Partner Branch Admin | Same as Branch Manager, plus **earnings preview** and **settlement status** |
| Branch Finance | Branch accruals · statement status · payout due · disputes |
| Branch Coordinator | Today · live feed · unassigned · reschedules due |

---

## 6. Design System

> **Token values are not in this section.** §6.1 names the token *groups*; the values, the measured
> WCAG 2.1 AA contrast evidence, the status→colour binding to `23` §2.3 and the motion curves live in
> `30` §3–§7. Where the two disagree — §6.1's "brand blue / accent orange" against `30` §3's teal and
> green — neither has been edited into the other: that is `OD-DOC-30` and it is an owner decision
> (`DEC-01`, `DEC-07`). Component *names* stay here; the state matrix and the eight components the
> screens in §2–§5 require but §6.2 does not name are in `33` §5. On 2026-10-21 the owner chose a
> **direction** — Deep Teal + Gold, `30` §2/§3 — and a direction is an input to `OD-DOC-30`, not its
> output: this section's wording is unchanged, `30` §3's values are unapproved, and both sides stay on
> file until the Founder and Product Design Lead decide.
>
> **This section names; it does not specify how to build.** The values live in `30`, the screen×state×
> asset matrix in `33` §5, **the component contract, the variant axes, the colour-as-role mechanism, the
> motion recipes and the review checklist live in `37`**, and the libraries that may be used to build any
> of it are admitted by `36` §4/§5 against `13` §5.2's policy. Four documents, four jobs, one copy of
> each fact (`DEC-01`).

### 6.1 Foundations

| Token group | Values |
|---|---|
| **Colour** | Primary (brand blue), Secondary (accent orange), Success, Warning, Danger, Info, plus neutral scale 50–900, plus semantic surface/ink pairs. `[OPEN]` — `30` §3 originally proposed teal `#087F8C` + green `#20A675` against this wording; the measured corrections in `30` §3.5 keep `#20A675` as **decoration only** and the chosen direction now runs action teal `#0A6E77` with a gold detail (`30` §3.2/§3.4). The owner selected that direction (Scheme A, Deep Teal + Gold) on 2026-10-21, which is **not** an approval: `OD-DOC-30` stays open with this row as its other side, and `30` §10's **light only** proposal is `OD-DOC-31`. |
| **Typography** | Inter (UI) / Noto Sans (localised scripts, incl. Odia) / tabular numerals for money. `[OPEN]` — `13` §5.2 sets `font-src 'self'`, so both families must be self-hosted and subset; no document says who produces that pipeline (`OD-DOC-32`). Scale in `30` §4. The owner has also directed **English-first at design time**, with Odia and Hindi after design and programming — which defers translation but cannot defer the §8 expansion tolerance (`OD-DOC-35`; `30` §4.1). |
| **Spacing** | 4 px base scale: `4 8 12 16 24 32 48 64` |
| **Radius** | `4 / 8 / 12 / 16 / 999` |
| **Elevation** | 3 shadow levels + a border-first approach |
| **Iconography** | One outline set, 20/24 px, consistent stroke |
| **Motion** | 150 ms (micro) / 250 ms (transition) / 400 ms (page); respect `prefers-reduced-motion` |

### 6.2 Component Inventory

> Canonical list. `33` §5 records which of these have their visual states designed and names eight
> components that §2–§5 screens require but this table does not contain — ServiceCard, BookingSummary,
> a compact status indicator, EstimateApproval, PaymentSummary, InvoiceView, ErrorState and
> PermissionDeniedState. Any addition lands **here**, once, not in a second list.
>
> **`CA-00`, restated because it is the rule most often broken:** adding a component is adding a row
> here, and only here. `37` describes how every component in this list must be *built* and may gain a
> rule, never a name; `33` §5 tracks which of them have designed states; `34` may reference one by name
> in an asset prompt. A name coined in any of those three is an inconsistency, not a design decision.

| Category | Components |
|---|---|
| **Foundation** | Button (primary/secondary/ghost/danger, loading), IconButton, Input, Select, DatePicker, TimePicker, Checkbox, Radio, Switch, Slider, Stepper, Chip, Tag/Badge, Avatar, Tooltip, Toast, Snackbar, **Field** (label + hint + error wrapper that owns `aria-describedby`), **Icon** (the one place a glyph is drawn, so size and stroke come from `30` §5's scale), **ImageSlot** (`30` §5.3's reserved container, `37` §7.1's five props) |
| **Navigation** | BottomNav, TabBar, Sidebar, Breadcrumb, AppBar, Drawer, Stepper header, Deep-link router |
| **Data display** | DataTable (sort/filter/paginate/export), Card, ListTile, Accordion, Timeline, StatCard, ProgressBar, Rating, PriceBreakdown, EmptyState, Skeleton |
| **Domain** | BookingStatusTimeline, TechnicianCard, PriceBreakdownSheet, CouponField, MapPicker, LocationSearch, SlotGrid, OTPInput, ChecklistBuilder, PartEntry, EvidenceUploader, EarningBreakdown, SettlementTable, CallPanel, TicketDrawer, ScopeBadge |
| **Feedback** | ConfirmDialog, Sheet, Snackbar, ProgressOverlay, OfflineBanner, SyncIndicator |

> **Three rows were added on 2026-10-22, and the addition is the point of `CA-00`.** `Field`, `Icon` and
> `ImageSlot` are the first component names this repository ever *built* (`packages/ui`, `apps/web`) while
> having no row here: `37` §4 and §7.1 described how all three must behave, `30` §5.3 described the slot's
> reserved state, and none of them may add a name. Code was therefore ahead of the canonical list by three
> components, which is the failure mode `CA-00` exists to catch rather than a decision anyone made. The rows
> **name** the components only — the values stay in `30`, the state matrix in `33` §5, the build contract in
> `37`. `33` §5's eight unnamed components in the note above are still unnamed there, and `33` §5's matrix
> still owes these three their state columns.

### 6.3 Accessibility

| Rule | Detail |
|---|---|
| A11Y-1 | WCAG 2.1 AA contrast for all text and interactive elements |
| A11Y-2 | Minimum touch target 48 × 48 dp on mobile; 44 × 44 px on web |
| A11Y-3 | All inputs have programmatic labels; errors are associated via `aria-describedby` |
| A11Y-4 | The status timeline conveys state with **text + icon + colour**, never colour alone |
| A11Y-5 | The OTP input supports paste and autofill |
| A11Y-6 | Every screen has a semantic heading structure and a skip link (web) |
| A11Y-7 | Screen-reader announcements for live status changes on the tracking screen |

---

## 7. Cross-Surface Consistency Rules

| ID | Rule |
|---|---|
| XS-01 | A **booking code** has the same visual treatment and format everywhere. |
| XS-02 | **Money is always** `₹1,119.82` with tabular numerals; never abbreviated in a breakdown. |
| XS-03 | The **status timeline** component is identical across web, app and Control Center. |
| XS-04 | The **price breakdown** component is identical across all surfaces and shows the same line order: Labour → Visiting/Diagnostic → Parts → Discounts → Tax → Total → Advance → Balance. |
| XS-05 | The **cancellation policy** text is identical everywhere and is versioned centrally. |
| XS-06 | Status labels come from one shared enum → one i18n file → no per-surface drift. |

---

## 8. Localisation

| Locale | Code | Coverage |
|---|---|---|
| English | `en` | 100% |
| Odia | `or` | 100% — primary for Odisha |
| Hindi | `hi` | 100% |

**Rules**
- i18n-01 — No hard-coded user-facing strings in any client. CI fails on a lint rule that flags them.
- i18n-02 — Pluralisation and currency formatting use locale-aware formatters (`Intl` on web; `intl` in Flutter).
- i18n-03 — Layout must tolerate 30% text expansion (Odia and German-style expansion are common causes of clipping).
- i18n-04 — Right-to-left is not required for the launch locales, but the layout system must not block it.

> **`[OPEN]` — `OD-DOC-35`, and the coverage table above is left as issued.** The owner has directed
> English-first at design time ("currently design time focus in English … after design and programing ok
> then will be make multi language supported"), which is a sequencing decision about *translation
> production*, not a relaxation of this section: no row above has been re-marked, and `DEC-07` keeps both
> sides visible until `17` names the phase and `29` §4 gains the check that would verify it. Two things
> follow and neither is deferrable. **i18n-03's 30 % expansion tolerance is a layout rule and applies from
> the first English screen** — a fixed-height label, a width-fitted button or a single-line table header
> that survives Latin script becomes rework in three files once Odia renders at its own length. And
> `13` §7 `US-07` cannot be met by translation alone: Odia has to *render*, which needs the self-hosted
> subset Indic face of `OD-DOC-32` and the shaping verification in `30` §4.2. Designing English-only
> screens that satisfy i18n-03 is cheap; retrofitting the tolerance is not. See `30` §4.1 for what the
> pass did and did not treat as deferred.

---

## 9. Performance Budgets

| Surface | Budget |
|---|---|
| Website (LCP / INP / CLS) | LCP < 2.5 s · INP < 200 ms · CLS < 0.1 on a mid-range Android over 4G |
| Customer app | Cold start < 2.5 s · screen transition < 300 ms · APK ≤ 25 MB (AAB ≤ 40 MB) |
| Partner app | Cold start < 2.5 s · offline mode fully functional · APK ≤ 30 MB |
| Control Center | First contentful paint < 1.5 s on a corporate LAN · table interactions < 100 ms perceived |

> **Budgets, not measurements** — nothing has been built, so no figure here has been observed; `13` §2.2
> says the same about the client budgets behind these, and `32` §4's per-file byte ceilings are *derived*
> from this table rather than measured against it. **What may be installed to meet them is `36` §4/§5**
> (`OD-14-09`…`13` are the undecided cells of that table), **how the component that meets them is shaped
> is `37`**, and **which directory its files sit in is `35`**. A library that cannot fit a budget here, or
> cannot pass `13` §5.2's CSP, is not a candidate (`LB-03`, `LB-02`).

---

## 10. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| OD-UX-01 | Design tool of record — Figma with a token-sync pipeline, or tokens-first in code? | Design Lead | Phase 0 |
| OD-UX-02 | Is a customer **wallet** (stored balance) in scope for v1.0, or is it display-only settlement information? | Product + Finance | Phase 1 |
| OD-UX-03 | Should the Control Center be a separate SPA or a route inside the Next.js app? | Engineering + Design | Phase 0 |
| OD-UX-04 | Do we need a "Urgent / same-day" slot concept with a premium, or is a standard SLA enough? | Product | Phase 2 |
| OD-UX-05 | Is the Partner App required on iOS at launch, or Android-only with iOS later? | Product | Phase 1 |
| OD-UX-06 | Does the customer app need an in-app chat with the technician, or is phone/call + WhatsApp sufficient? | Product | Phase 2 |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.6 | 2026-10-22 | Product Design Lead + Frontend Lead (first components built) | **Three names added to §6.2, and only here (`CA-00`)**: `Field`, `Icon` and `ImageSlot` join the Foundation row. They are the components `packages/ui` and `apps/web` now implement and the only three this repository has ever *built* without a row in the canonical list — `37` §4/§7.1 and `30` §5.3 describe their behaviour but may not name them, so code had moved ahead of the list and the list is where it belongs. A note under the table records exactly that, keeps the parenthetical to a *definition* (values stay in `30`, states in `33` §5, contract in `37`), and states plainly that `33` §5 still owes all three their state columns and its own eight unnamed components remain unnamed. **No screen, route, page element, rule, token or ID changed**: §1–§5, §6.1, §6.3, §7–§10, §2.1's `OD-DOC-25` annotation and 1.5's §2.1 lead-in are untouched, and the `33` §5 gap count is unchanged at eight. | §6.2, Revision History, header |
| 1.5 | 2026-10-22 | Product Design Lead (website-design pass) | **One annotation added, no page, route, element or screen changed.** §2.1 gained a lead-in stating the boundary the website-design pass created: the Key Elements column is *what a page must contain*, while the section breakdown and the image boxes are `39` §2/§3 — derived from this table, adding no route and removing none (`35` PS-06 keeps the route list's home here). `OD-DOC-25`'s tile-versus-icon ambiguity in the Home row is **left unresolved on purpose**; `39` §2.1-H3 answers it for the marketing surface only and says so, and the catalogue pages keep the question open. §2's existing `OD-10-06`/`OD-DOC-29` note about screens having no endpoint or permission join stands untouched. | §2.1 lead-in, Revision History, header |
| 1.4 | 2026-10-21 | Product Design Lead + Engineering Lead (design-engineering structure pass) | Three pointers added, no content re-listed. §6’s lead now states the four-way split of jobs explicitly — this document **names**, `30` holds values, `33` §5 holds the screen×state matrix, `37` holds the component contract and review checklist, `36` holds the admitted libraries (`DEC-01`). §6.2’s blockquote gained **`CA-00` restated in this document’s own words**: a component is added by a row **here** and nowhere else, so a name coined in `33`, `34`, `36` or `37` is an inconsistency rather than a design decision. §9’s budget table gained the sentence it lacked — these are **budgets, not measurements**, nothing has been built, and `32` §4’s byte ceilings are derived from them rather than measured against them — plus the rule that a library which cannot fit a budget here or pass `13` §5.2’s CSP is not a candidate (`LB-02`, `LB-03`). **No screen, component, route or rule was added, removed or renamed** in §1–§5, §6.2 or §10, and the eight components `33` §5 records as unnamed here are still unnamed here. | §6, §6.2, §9, Revision History, header |
| 1.3 | 2026-10-21 | Product Design Lead (palette and i18n pass) | Annotated, **not rewritten** — no value in §6.1's token table, §8's coverage table or any rule below it was changed. §6's blockquote now records that the owner chose Deep Teal + Gold as a *direction* on 2026-10-21 and that a direction is an input to `OD-DOC-30`, not its output, so `12` and `30` remain on file as the two sides of the conflict (`DEC-07`). §6.1's Colour cell carries the corrected hexes (`30` §3.2's `#0A6E77` action, `30` §3.4's gold detail) and states that `#20A675` is decoration-only per `30` §3.5; its Typography cell carries the owner's English-first direction and points at `OD-DOC-35`. §8 gained an `[OPEN]` note under i18n-01…04 saying which half of the deferral is a plan (translation production, until `17` names a phase and `29` §4 gains a check) and which half is not (the 30 % expansion tolerance is a layout rule from the first English screen, and `US-07` needs the subset Indic face of `OD-DOC-32` to *render* Odia). | §6, §6.1, §8, header, Revision History |
| 1.2 | 2026-10-21 | Product Design Lead + Engineering Lead (design-system pass) | Annotated, not rewritten. §6 now names `30` as the home of token **values** and `33` §5 as the component state matrix, with the §6.1 colour row and typography row carrying `[OPEN]` markers for `OD-DOC-30` (blue/orange versus the measured teal/green), `OD-DOC-31` (no documented dark-mode position) and `OD-DOC-32` (`font-src 'self'` against fonts whose loading nobody owns). §1's partner-dashboard note records that no `SCR-PD-*` ID and no asset was produced for a conditional surface. Nothing in §2–§5 or §6.2 was re-listed, and no screen, component or rule was removed. Three further annotations from the same pass: §2 gains the statement that **no screen here is joined to an endpoint or a permission token, because no such mapping exists** (`OD-10-06`, extended as `OD-DOC-29`, which is why `33` leaves those columns empty deliberately); §2.1's Home row and §3.2 screen 4 now carry `OD-DOC-25`, because this document asks for "**Icons, names (localised)**" on screen 4 and "**category tiles**" on Home while the design brief asks for a photograph per category — the question is unanswered twice inside one document. | §1, §2, §2.1, §3.2, §6, §6.1, §6.2, Revision History |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Added the Partner web dashboard as a conditional fifth surface (ADR-021) with its scope boundary; cross-referenced the surface rules. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
