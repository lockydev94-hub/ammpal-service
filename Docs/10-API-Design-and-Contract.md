# 10 — API Design & Contract

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-10 |
| Version | 1.5 |
| Status | Approved for Design & Development |
| Owner | Engineering Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `08`, `09`, `03` |
| Contract Artifact | OpenAPI 3.1 at `/openapi.json`; generated from code; CI fails on drift |

---

## 1. Design Principles

| # | Principle and consequence |
|---|---|
| AP-1 | **The API is the contract.** Front ends are generated from OpenAPI; no hand-written clients. |
| AP-2 | **Resources over actions.** `POST /bookings/{id}/cancel` is acceptable only where the action is a state transition, not a CRUD operation. |
| AP-3 | **Scope is implicit.** The caller's scope is derived from their token. `branch_id` filters are optional narrowing, never widening. |
| AP-4 | **Money is server-computed.** No client ever sends a price, a commission or a tax amount. |
| AP-5 | **Idempotent creates.** Every `POST` that creates money or work accepts `Idempotency-Key`. |
| AP-6 | **Errors are stable.** A machine `code` is part of the contract; messages are not. |
| AP-7 | **PII is minimised.** Responses are scoped and paginated; sensitive fields are masked by role. |
| AP-8 | **Additive within a major.** No field removals, no semantic changes, no breaking renames inside `/v1`. |

---

## 2. Conventions

| Aspect | Rule |
|---|---|
| Base URL | `https://api.ammpalservice.com/v1` |
| Content type | `application/json; charset=utf-8` (multipart only for uploads) |
| Auth | `Authorization: Bearer <access_token>` |
| Access token | JWT, RS256, 15-minute TTL, claims: `sub`, `role`, `scope`, `type` |
| Refresh token | Opaque, rotating, httpOnly cookie (web) / secure storage (apps), 30-day sliding |
| Locale | `Accept-Language: en\|or\|hi` |
| Time | All timestamps ISO-8601 UTC (`2026-10-21T09:14:22Z`) |
| Money | Integer paise in JSON, with a `currency` field on the enclosing object |
| Idempotency | `Idempotency-Key: <uuid>` header on create endpoints |
| Correlation | `X-Request-Id` returned on every response; accepted on input for tracing |
| Pagination | Cursor-based: `?cursor=<opaque>&limit=50` → `{ "data": [...], "nextCursor": "...", "hasMore": true }` |
| Sorting | `?sort=-createdAt,name` (field name + optional `-`) |
| Filtering | `?field=value` for scalars; `?field.from=&field.to=` for ranges; `?field[]=a&field[]=b` for `IN` |
| Expansion | `?expand=technician,invoice` (opt-in, capped) |
| Rate limiting | Per identity + per IP; headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` |
| Optimistic locking | `If-Match: <version>` on updates of versioned resources → `412 PRECONDITION_FAILED` |
| Soft delete | `DELETE` sets `deleted_at`; `?includeDeleted=true` for Super Admin only |

---

## 3. Authentication Endpoints

| Method | Path | Purpose | Auth |
|---|---|---|---|
| `POST` | `/auth/otp/request` | Send an OTP to a phone number | Public |
| `POST` | `/auth/otp/verify` | Verify OTP → issue tokens | Public |
| `POST` | `/auth/refresh` | Rotate the refresh token | Refresh token |
| `POST` | `/auth/logout` | Revoke the session | Bearer |
| `GET` | `/auth/me` | Current identity, role, scope, permissions | Bearer |
| `POST` | `/auth/password/forgot` | Central staff password reset | Public |
| `POST` | `/auth/password/reset` | Complete the reset | Token |
| `POST` | `/auth/sso/{provider}` | Social login (Google, Facebook) | Public |

**OTP request — rate limits**

| Rule | Limit |
|---|---|
| Per phone number | 5 per hour, 20 per day |
| Per IP | 20 per hour |
| Failed verifications | 5 attempts, then a 15-minute lockout |
| Minimum resend interval | 45 seconds |

```http
POST /v1/auth/otp/request
{ "phone": "+919876543210", "purpose": "LOGIN" }
```
```json
{
  "status": "OTP_SENT",
  "expiresInSeconds": 300,
  "resendAfterSeconds": 45
}
```

---

## 4. Resource Catalogue

Two columns appear in every table below. They did not exist in the first issue, which is why the
catalogue could not be reviewed for security or for financial reach: a reader could see *what* an
endpoint does but not *who may call it* or *whether it touches money*.

**Auth** — the credential the route accepts. Values are the ones §3 and §2 already use:

| Value | Meaning |
|---|---|
| `Public` | No token. Allowed only where `OD-10-02` keeps catalogue browsing unauthenticated. |
| `Cust` | Customer Bearer token. Ownership guard applies: another customer's resource returns `404`, not `403` (`03` §6). |
| `Tech` | Technician Bearer token; `sub` must be the technician named by the route, or the technician must hold the booking. |
| `Staff` | Control Center Bearer token + permission check + scope (`03` §4, §6). |
| `Sig` | No user token at all — the provider's webhook signature is the only authenticator. |

**Effects** — what one successful call actually changes. A is the shorthand used in `28` test mapping:

| Code | Meaning |
|---|---|
| `R` | Read only. Safe to retry, never audited as a mutation. |
| `W` | Writes or mutates a row. |
| `S` | Advances a state machine — a transition ID in `23` must exist for the call to be legal. |
| `$` | Creates or changes money: a price snapshot, an invoice line, a ledger row, a refund. |
| `M` | Enqueues an outbound message (push / SMS / WhatsApp / email / call). |
| `A` | Writes an `audit_events` row. Mandatory for every `$` and every `override`. |

### 4.1 Public / Customer

| Method | Path | Description | Key Params | Auth | Effects |
|---|---|---|---|---|---|
| `GET` | `/catalog/categories` | Active categories with localised content | `scope`, `lang` | `Public` | `R` |
| `GET` | `/catalog/services` | Services in a category, available at a location | `categoryId`, `lat`, `lng`, `addressId` | `Public` — **but `Public` only while `addressId` is absent** (see note below) | `R` |
| `GET` | `/catalog/services/{id}` | Service detail, variants, price range | `lat`, `lng` | `Public` | `R` |
| `GET` | `/catalog/variants/{id}/price` | Price range for a location | `lat`, `lng` | `Public` | `R` |
| `GET` | `/catalog/service-areas/resolve` | Resolve an address → area/zone/city/state/branch | `lat`, `lng` **or** `addressId` | `Public` for `lat`/`lng`; **`Cust` when `addressId` is supplied** | `R` |
| `GET` | `/catalog/coverage` | Whether a service is available at an address | `serviceId`, `lat`, `lng` | `Public` | `R` |
| `GET` | `/search/technicians` | Ranked eligible technicians | `serviceId`, `lat`, `lng`, `slot`, `page` | `Public` | `R` — response is masked: no phone, no exact home address (`03` §5) |
| `GET` | `/search/availability` | Available slots | `technicianId`, `date`, `serviceId` | `Public` | `R` |
| `POST` | `/quotes` | **Price quote** (no side effects) | see below | `Public` — and it accepts `addressId` (see the note below) | `R` per §7 — but `09` gives quotes a table; the two cannot both be true (`OD-DOC-19`) |
| `POST` | `/waitlist` | Join the waitlist for a non-serviceable location | see §5.6 | `Public` | `W` `M` — **stores a phone number and an address from an unauthenticated caller** |
| `POST` | `/bookings` | Create a booking | see below | `Cust` | `W` `S` `$` `M` `A` |
| `GET` | `/bookings/{id}` | Booking detail (own only) | `expand` | `Cust` | `R` |
| `POST` | `/bookings/{id}/cancel` | Cancel with policy evaluation | | `Cust` | `W` `S` `$` `M` `A` |
| `POST` | `/bookings/{id}/reschedule` | Request a new slot | | `Cust` | `W` `S` `M` `$` if the reschedule fee applies |
| `POST` | `/bookings/{id}/change-technician` | Request a technician change | | `Cust` | `W` `S` `M` |
| `GET` | `/bookings/{id}/track` | Live location + ETA (poll fallback) | | `Cust` | `R` |
| `POST` | `/bookings/{id}/otp` | Customer OTP for job start | | `Cust` | `W` `S` `M` `A` |
| `POST` | `/bookings/{id}/approve` | Customer approval for work/parts | | `Cust` | `W` `S` `$` `M` |
| `POST` | `/bookings/{id}/rate` | Submit a rating + review | | `Cust` | `W` `S` |
| `GET` | `/bookings` | Own bookings (filter by status) | `status`, `from`, `to` | `Cust` | `R` |
| `GET` | `/invoices/{id}` | Own invoice | `expand=lines` | `Cust` | `R` |
| `GET` | `/payments` | Own payment history | | `Cust` | `R` |
| `POST` | `/payments/{id}/refund-request` | Request a refund | | `Cust` | `W` `S` `$` `A` |
| `GET` | `/addresses` · `POST` · `PATCH` · `DELETE` | Address book | | `Cust` | `W` — `DELETE` is soft (§2) |
| `GET` | `/notifications` · `POST` `/notifications/{id}/read` | Notification inbox | | `Cust` | `R` / `W` |
| `PATCH` | `/notification-preferences` | Preferences | | `Cust` | `W` — consent changes are `A` (`WL-02` depends on them) |
| `POST` | `/tickets` | Create a support ticket | | `Cust` | `W` `S` `M` |
| `GET` | `/tickets` · `GET /tickets/{id}` | Own tickets | | `Cust` | `R` |

> **`addressId` on a public route is an IDOR-shaped defect, not a style question.**
> `GET /catalog/services`, `GET /catalog/service-areas/resolve` and `POST /quotes` all accept
> `addressId` — a row in the caller's own address book, which `09` stores as a geocoded address — and
> all three are reachable without a token under `OD-10-02`. Served as written, an enumerated `addressId`
> returns a stored home location belonging to someone else. The reads and the quote must branch:
> coordinates → `Public`; `addressId` → `Cust` with an ownership check, and an `addressId` that is not
> the caller's returns `404`. Until that is built, the `addressId` parameter on those three rows is
> **`[OPEN]` — `OD-DOC-13`**.


### 4.2 Technician

Every route in this table is `Tech`, and every one of them is ownership-bound: `/me/…` resolves from
the token's `sub`, never from a parameter. `GET /bookings/{id}` is the one route whose authority is a
*relationship* rather than an identity — the caller must hold the current assignment.

| Method | Path | Description | Auth | Effects |
|---|---|---|---|---|
| `GET` | `/technicians/me` | Own profile | `Tech` | `R` |
| `PATCH` | `/technicians/me` | Update profile | `Tech` | `W` `A` — name/phone changes are audited; a bank-detail change is `A` and re-verifies |
| `PUT` | `/technicians/me/skills` | Set skills and levels | `Tech` | `W` — eligibility recomputation, so it silently changes *future* routing |
| `PUT` | `/technicians/me/service-areas` | Pin service areas | `Tech` | `W` — same routing effect |
| `PUT` | `/technicians/me/availability` | Weekly availability | `Tech` | `W` |
| `POST` | `/technicians/me/time-off` | Declare time off | `Tech` | `W` `S` `M` — releases assigned jobs, so it moves bookings (`23`) |
| `GET` | `/technicians/me/documents` | Uploaded KYC documents | `Tech` | `R` |
| `POST` | `/technicians/me/documents` | Upload a document (multipart) | `Tech` | `W` `A` |
| `GET` | `/technicians/me/offers` | Open job offers | `Tech` | `R` |
| `POST` | `/technicians/me/offers/{offerId}/accept` | Accept an offer | `Tech` | `W` `S` `M` |
| `POST` | `/technicians/me/offers/{offerId}/reject` | Reject with a reason | `Tech` | `W` `S` `M` |
| `GET` | `/technicians/me/bookings` | Assigned jobs | `Tech` | `R` |
| `GET` | `/bookings/{id}` | Assigned job detail | `Tech` | `R` |
| `POST` | `/bookings/{id}/start-route` | Begin travel | `Tech` | `W` `S` `M` |
| `POST` | `/bookings/{id}/start` | Start work (requires customer OTP) | `Tech` | `W` `S` `A` |
| `POST` | `/bookings/{id}/complete` | Complete (workflow-validated) | `Tech` | `W` `S` `$` `M` `A` |
| `POST` | `/bookings/{id}/parts` | Add a part used | `Tech` | `W` `$` `S` — a part changes the invoice, so it requires the customer approval path (`/approve`) |
| `POST` | `/bookings/{id}/evidence` | Upload evidence photo (multipart) | `Tech` | `W` |
| `POST` | `/bookings/{id}/invoice` | Generate/confirm the invoice | `Tech` | `W` `$` `S` `M` `A` |
| `POST` | `/bookings/{id}/collect-payment` | Create a payment link for the balance | `Tech` | `W` `$` `M` |
| `POST` | `/technicians/me/location` | Push live location (throttled) | `Tech` | `W` — Redis-only unless `OD-08-04` says otherwise; §8 caps it at 1 per 10 s |
| `GET` | `/technicians/me/earnings` | Earnings ledger | `Tech` | `R` |
| `GET` | `/technicians/me/settlements` | Settlement statements | `Tech` | `R` |
| `GET` | `/technicians/me/score` | Performance score breakdown | `Tech` | `R` — see `OD-QA-06`: the score's *uses* are undocumented |
| `GET` | `/technicians/me/penalties` | Penalties | `Tech` | `R` |
| `POST` | `/settlements/{id}/dispute` | Dispute a settlement line | `Tech` | `W` `S` `M` |

> **Two rows change money without a stated authorisation check.** `/bookings/{id}/parts` and
> `/bookings/{id}/invoice` both carry `$`, and both are called by the technician — the person whose
> earnings rise when the invoice rises. `07` requires customer approval before chargeable parts, and
> `ADR-006` freezes the price snapshot, but nothing in this catalogue states that the server rejects a
> part or an invoice line that has no matching `/approve` record. That check is the whole control. It
> must be specified before the job module is built — `OD-DOC-14`.

### 4.3 Control Center — Platform

**Auth for every row: `Staff`** — a Control Center Bearer token, a permission check and a scope filter
(`03` §4, §6). The column is therefore omitted; what varies is the effect, and that is where the risk
is. `A` marks a row that must write `audit_events`; `$` marks money; `S` marks a state machine.

| Method | Path | Description | Effects |
|---|---|---|---|
| `GET` | `/admin/dashboard` | Role-scoped KPI dashboard | `R` |
| `GET` | `/admin/users` · `POST` · `PATCH` | User administration | `W` `A` |
| `POST` | `/admin/users/{id}/roles` | Assign role + scope (reason required) | `W` `A` — the highest-privilege write in the API |
| `GET` | `/admin/roles` · `PATCH /admin/roles/{code}` | Role & permission management | `W` `A` — a permission change authorises *future* calls, so it is audited even though no row of another type moves |
| `GET` | `/admin/platform/mode` | The effective mode, read from `platform.platform_mode` | `R` — display only. It is **never** an input; a client cannot ask for a mode (`38` PM-02/PM-04) |
| `GET` | `/admin/platform/mode/transitions` | Mode history | `R` `A` — read is audited because it shows who attempted to disarm the guard |
| `POST` | `/admin/platform/mode/transitions` | Request `promote` or `demote` with a non-empty reason; returns the pre-condition report | `W` `A` — the highest-consequence write after role assignment (`38` §5 step 1–2) |
| `POST` | `/admin/platform/mode/transitions/{id}/verify` | Submit the step-up OTP for a pending transition | `W` `A` — attempt-capped, locked, single-use (`38` PM-21); every attempt is an authentication event (`FR-ID-09`) |
| `POST` | `/admin/platform/mode/transitions/{id}/acknowledge` | Second-account dual control | `W` `A` — cannot be the requester (`03` §3.3, `FL-03`) |
| `GET` | `/admin/states` · `POST` · `PATCH` | Master data: states | `W` |
| `GET` | `/admin/cities` · `POST` · `PATCH` | Master data: cities | `W` |
| `GET` | `/admin/branches` · `POST` · `PATCH` | Branches | `W` `A` |
| `POST` | `/admin/branches/{id}/approve` | Approve a branch (Operator/Super Admin) | `W` `S` `A` — cannot be self-approved (`03` §3.3) |
| `GET` | `/admin/partner-orgs` · `POST` · `PATCH` | Partner organisations | `W` `A` |
| `POST` | `/admin/partner-orgs/{id}/approve` | Approve a partner | `W` `S` `A` |
| `GET` | `/admin/zones` · `POST` · `PATCH` | Zones | `W` |
| `GET` | `/admin/service-areas` · `POST` · `PATCH` | Service areas | `W` — geometry edits re-route live demand |
| `POST` | `/admin/territories/allocate` | Allocate a service area to a branch | `W` `S` `A` |
| `GET` | `/admin/technicians` · `GET /admin/technicians/{id}` | Technician roster | `R` |
| `POST` | `/admin/technicians/{id}/approve` | Approve a technician (KYC) | `W` `S` `A` |
| `POST` | `/admin/technicians/{id}/suspend` | Suspend | `W` `S` `M` `A` — releases assigned jobs |
| `GET` | `/admin/catalog/categories` · `POST` | Catalogue administration | `W` |
| `GET` | `/admin/catalog/services` · `POST` | Services | `W` |
| `GET` | `/admin/workflows` · `POST` · `POST /admin/workflows/{id}/publish` | Workflow templates | `W` `A` — publish changes the completion path of *every* in-flight job of that category |
| `GET` | `/admin/price-book` · `POST` · `PATCH` | Price book administration | `W` `$` `A` — `ADR-006`: never edits a snapshot already taken |
| `GET` | `/admin/branch-prices` · `POST` | Local price overrides | `W` `$` `A` |
| `GET` | `/admin/coupons` · `POST` · `PATCH` · `POST /admin/coupons/{id}/pause` | Coupons | `W` `$` `A` — reserve/release semantics are `ADR-008` |
| `GET` | `/admin/bookings` | Booking list (scoped) | `R` |
| `GET` | `/admin/bookings/{id}` | Booking detail with full audit trail | `R` |
| `POST` | `/admin/bookings/{id}/assign` | Manual assignment | `W` `S` `M` `A` |
| `POST` | `/admin/bookings/{id}/override` | Override a rule (reason required) | `W` `S` `$` `M` `A` — the only row where `A` is not optional but contractual (`03` §3.2) |
| `GET` | `/admin/commission/rates` · `POST` | Commission rate versions | `W` `$` `A` — versioned, so an edit must not alter a past period |
| `GET` | `/admin/commission/ledger` | Commission ledger (scoped) | `R` |
| `POST` | `/admin/settlements/generate` | Generate weekly statements | `W` `$` `A` — idempotent by natural key (§7) |
| `GET` | `/admin/settlements` · `GET /admin/settlements/{id}` | Settlements | `R` |
| `POST` | `/admin/settlements/{id}/issue` | Issue (immutable) | `W` `$` `S` `M` `A` |
| `POST` | `/admin/settlements/{id}/approve` | Approve (SoD enforced) | `W` `S` `A` — the generator may not be the approver |
| `POST` | `/admin/settlements/{id}/adjustments` | Credit/debit note | `W` `$` `A` — additive only (`ADR-015`) |
| `GET` | `/admin/invoices` · `GET /admin/invoices/{id}` | Invoices | `R` |
| `GET` | `/admin/reconciliation` | Gateway reconciliation view | `R` |
| `GET` | `/admin/tax/registrations` · `POST` | Tax registrations | `W` `A` — the values themselves are `[OPEN]`; no registration is recorded in this suite |
| `GET` | `/admin/tickets` · `GET /admin/tickets/{id}` | Support tickets | `R` |
| `POST` | `/admin/tickets/{id}/assign` | Assign a ticket | `W` `S` `M` |
| `POST` | `/admin/tickets/{id}/status` | Change status / escalate | `W` `S` `M` |
| `GET` | `/admin/calls` · `GET /admin/calls/{id}` | Call logs | `R` — recordings are PII; access is `A` |
| `GET` | `/admin/reports/{reportKey}` | Run a report | `R` |
| `GET` | `/admin/reports/{reportKey}/export` | CSV/XLSX export | `R` `A` — `export` is always audited and watermarked (`03` §3.2) |
| `GET` | `/admin/audit-events` | Audit trail | `R` |
| `GET` | `/admin/coverage` | Service-area coverage health | `R` |
| `GET` | `/admin/webhooks/dead-letters` | Dead-letter queue view (required by the §4.5 replay rule) | `R` |

> **The replay action has no route.** §4.5 states that `GET /admin/webhooks/dead-letters` "allows
> replay", but a `GET` cannot legally change state, and replaying an event — a payment event in
> particular — re-runs money logic. The verb, the path and the permission for replay are unspecified
> anywhere in this suite, and replaying a settlement-bearing event is exactly the operation that
> `03` §3.2 would class as `override` with a mandatory reason. Registered as `OD-DOC-15`.

### 4.4 Control Center — Branch

**Auth for every row: `Staff` with a `BRANCH` scope** — a branch user can never widen it with a
`branch_id` parameter (§2 AP-3). Compared with §4.3 this table is the one that matters most for
`OD-DOC-01`: a partner-operated branch holds price-band and settlement access.

| Method | Path | Description | Effects |
|---|---|---|---|
| `GET` | `/branch/dashboard` | Branch KPIs (branch-scoped) | `R` |
| `GET` | `/branch/technicians` · `POST` | Branch technician roster | `W` `A` |
| `POST` | `/branch/technicians/{id}/approve` | Approve a branch technician | `W` `S` `A` — who may approve is the unresolved half of `OD-DOC-01` |
| `GET` | `/branch/service-areas` · `POST` | Branch service areas | `W` |
| `GET` | `/branch/bookings` | Branch bookings | `R` |
| `POST` | `/branch/bookings` | Create on behalf of a customer | `W` `S` `$` `M` `A` — a staff-created booking is a CCO call written into the same machine; the created-by identity must be retained |
| `POST` | `/branch/bookings/{id}/assign` | Manual assignment | `W` `S` `M` `A` |
| `GET` | `/branch/prices` · `PUT /branch/prices/{variantId}` | Local price within band | `W` `$` `A` |
| `GET` | `/branch/coupons` · `POST` | Partner-funded coupons | `W` `$` `A` — funding party decides who bears the discount (`OD-07-02`) |
| `GET` | `/branch/settlements` | Branch settlements | `R` |
| `POST` | `/branch/settlements/{id}/dispute` | Raise a dispute | `W` `S` `M` |
| `GET` | `/branch/reports/*` | Branch reports | `R` — a wildcard path cannot be permission-checked per resource; see `OD-DOC-16` |

### 4.5 Webhook & Callback Endpoints (Inbound)

**Auth for every row: `Sig`** — there is no user token. The provider signature is the entire
authentication story, which is why an unverified signature is both a `401` and a logged security
event: nothing else in the API rejects a caller before authorisation has been considered.

| Method | Path | Provider | Effects |
|---|---|---|---|
| `POST` | `/webhooks/payments/{provider}` | Gateway payment + refund events | `W` `S` `$` `M` `A` — the only inbound route that moves money |
| `POST` | `/webhooks/telephony/{provider}` | Call events | `W` `S` `M` |
| `POST` | `/webhooks/whatsapp/{provider}` | WhatsApp delivery status + inbound messages | `W` `S` `M` — **inbound** content originates with an unauthenticated third party |
| `POST` | `/webhooks/sms/{provider}` | SMS delivery status | `W` |
| `POST` | `/webhooks/email/{provider}` | Email events (bounce, complaint) | `W` |
| `POST` | `/webhooks/otp/{provider}` | OTP delivery status | `W` — **`[OPEN]`: no provider contract owns this route; see `24` §14.5 and `OD-DOC-18`** |

`GET /admin/webhooks/dead-letters` (required by the replay rule below) is a `Staff` read with `W` on
replay, and it was referenced in this section's rules while being absent from §4.3 — added there.

**Webhook rules**
- The raw body is used for signature verification (no JSON pre-parsing).
- Events are deduped by `(provider, provider_event_id)` (`webhook_inbox`).
- Unverified signatures → `401`, and the request is logged as a security event.
- Handlers are **fast**: they persist the event and enqueue processing, then return `202`.
- A dead-letter queue holds events that fail after N retries; `GET /admin/webhooks/dead-letters` allows replay. `[OPEN]` — a `GET` cannot be a state-changing replay: no route carries the action (`OD-DOC-15`).

### 4.6 Permission Mapping `[OPEN]`

`03` defines **92 distinct permission tokens** (96 matrix cells in §4.1–§4.4; 66 three-part, 26
two-part, 19 wildcards) in the `<domain>:<resource>:<action>` format. `10` §4 listed **117 endpoint
rows** when this was first measured; `38` added **five** mode routes to §4.3, so the figure is restated by
re-measurement rather than arithmetic: a row-anchored scan of §4 for a cell whose first column is exactly one
of `GET`/`POST`/`PATCH`/`PUT`/`DELETE` returns **122 rows / 116 distinct paths** now, and **117 rows / 112
paths** once those five rows are removed — so the inherited 117 reconciles against the file it describes, and
nothing is carried forward on trust. The auth rows in §3 are untouched by `38` (**8** rows, still 8, and
excluded from the §4 count by design — the two are reported separately in `28` §2). **The two are not joined
anywhere in this suite** — `03`
contains no path, and no endpoint above carries a token. Nothing is invented here, because a guessed
token is worse than a missing one: an implementer would code the guess, and the guess would be the
guard.

The mapping rule that §4.3–§4.4 imply is stated below so the RBAC owner can confirm or correct it in
one pass rather than endpoint by endpoint. `[PROPOSED]` in the strict sense — it is a proposal, it is
not approved, and no guard may be written against it until `OD-10-06` closes.

| Shape | Action segment | Basis in `03` §3.2 |
|---|---|---|
| `GET /{collection}` (list) | `list` | "Retrieve collection (scoped)" |
| `GET /{collection}/{id}` | `read` | "Retrieve single entity (scoped)" |
| `POST /{collection}` | `create` | "Create new" |
| `PATCH` / `PUT /{collection}/{id}` | `update` | "Modify existing" |
| `DELETE /{collection}/{id}` | `delete` | "Soft delete only" |
| `POST /{collection}/{id}/approve` | `approve` | named verbatim |
| `POST /{collection}/{id}/reject` | `reject` | named verbatim |
| `POST /{collection}/{id}/assign` | `assign` | named verbatim |
| `POST /{collection}/{id}/override` | `override` | named verbatim |
| `GET /{…}/export` | `export` | named verbatim |
| `POST /{collection}/{id}/issue` | `issue` | named verbatim |
| anything else — `/complete`, `/start-route`, `/rate`, `/dispute`, `/refund-request`, `/pause`, `/publish`, `/allocate`, `/generate` | **no action segment exists** | `03` §3.1 lists eleven actions and none of these is one |

Two consequences to decide together in `OD-10-06`:

1. **The `domain` segment is not derivable from the path.** `/admin/settlements/{id}/approve` could be `finance:settlement:approve`, `platform:settlement:approve` or `branch:settlement:approve` — and the three have different holders in `03` §4.1–§4.2. Separation of duties (`03` §3.3) depends on which is chosen, so this is a control decision, not a naming preference.
2. **Ten transition endpoints have no action.** Either `03` §3.1 gains actions (e.g. `transition`, `submit`, `dispute`), or each of those maps to `update` — in which case a completion, an invoice issue and a profile edit all share one permission, and the RBAC matrix stops constraining the job lifecycle.

A third finding came out of counting the tokens rather than trusting the earlier figure, and it is the
one that will bite an implementer first: **`03` §4 already ignores §3.2's own vocabulary.** Twenty-nine
action segments in the matrix are not among the eleven declared actions (`accept`, `cancel`, `collect`,
`complete`, `deactivate`, `dispute`, `escalate`, `generate`, `pay`, `pin`, `reschedule`, `search`, `set`,
`start`, `upload`, `verify`, and thirteen more), while the declared `delete` appears **nowhere**. Nine
cells also carry their scope as prose beside the token — `booking:read` (own), `booking:read` (assigned),
`job:start` (OTP verified), `support:call` (toll-free), `booking:create` (on behalf) among them. That is
not a style complaint: the same customer role token reads two different scopes in two role families, and
an enforcement layer cannot see the parenthetical. The endpoint→permission table `OD-10-06` asks for must
either adopt the 29 actions as the vocabulary or rewrite the tokens down to eleven, and it must move the
nine parentheticals into a column the guard can read.

`03` §9 should record the outcome, and `28` should add the confirming permission to the row whose
verification is already named `rbac.matrix.spec` (`FR-ID-06`, `ADR-016`). Today those two rows cite a
guard and a test with nothing for the test to assert against.

---

## 5. Key Request / Response Examples

### 5.1 `POST /v1/quotes` — Price Quote

```json
{
  "serviceVariantId": "9f3c…",
  "addressId": "2a71…",
  "couponCode": "AMM-PLAT-8FK2M",
  "slotStart": "2026-10-22T09:00:00Z"
}
```

```json
{
  "quoteId": "q_9b12c4",
  "currency": "INR",
  "lines": [
    { "code": "LABOUR",   "label": "Labour charge",        "amountPaise": 60000, "affectsCommissionBase": true },
    { "code": "VISITING", "label": "Visiting charge",       "amountPaise": 9900,  "affectsCommissionBase": false }
  ],
  "discounts": [
    { "code": "AMM-PLAT-8FK2M", "amountPaise": 5000, "funding": "PLATFORM",
      "affectsCommissionBase": false }
  ],
  "tax": {
    "placeOfSupply": { "stateCode": "OD", "stateName": "Odisha" },
    "lines": [
      { "type": "CGST", "rateBps": 900, "amountPaise": 8504 },
      { "type": "SGST", "rateBps": 900, "amountPaise": 8504 }
    ],
    "totalPaise": 17008
  },
  "totals": {
    "subtotalPaise": 64900, "taxPaise": 17008, "grandTotalPaise": 81908,
    "advancePaise": 9900, "balancePaise": 72008
  },
  "commission": { "rateBps": 1500, "basis": "LABOUR_ONLY", "eligibleLabourPaise": 60000 },
  "provenance": ["DEFAULT", "STATE:OD", "BRANCH:OD-BBI-001"],
  "validUntil": "2026-10-21T09:29:22Z"
}
```

> The quote is advisory and non-binding. The authoritative snapshot is created with the booking.

### 5.2 `POST /v1/bookings`

**Headers:** `Authorization`, `Idempotency-Key: 3f9c…`

```json
{
  "serviceVariantId": "9f3c…",
  "addressId": "2a71…",
  "slotStart": "2026-10-22T09:00:00Z",
  "technicianId": "b71e…",
  "couponCode": "AMM-PLAT-8FK2M",
  "customerNote": "Gate code 4521; please call on arrival",
  "paymentMode": "ADVANCE"
}
```

**Response `201`**
```json
{
  "booking": {
    "id": "5d2a…",
    "code": "AMM-20261021-K7M2QX",
    "status": "REQUESTED",
    "statusCode": 1,
    "branch": { "code": "OD-BBI-001", "name": "Bhubaneswar Branch" },
    "serviceArea": { "code": "OD-BBI-001-Z03-A02", "name": "Patia" },
    "scheduledStart": "2026-10-22T09:00:00Z",
    "price": { /* the frozen snapshot */ },
    "offer": { "type": "DIRECT", "expiresAt": "2026-10-21T09:19:22Z" },
    "payment": { "required": true, "amountPaise": 9900, "link": "https://pay…" }
  }
}
```

### 5.3 `POST /v1/bookings/{id}/complete` — Job Completion

```json
{
  "parts": [
    { "name": "Capacitor 35µF", "quantity": 1, "unitPricePaise": 25000, "marginBasis": "MRP" }
  ],
  "notes": "Replaced capacitor, cleaned condenser, gas refilled",
  "evidenceIds": ["ev_7a…", "ev_7b…"],
  "warrantyDays": 30
}
```

**Response `200`**
```json
{
  "booking": { "id": "5d2a…", "status": "COMPLETED", "statusCode": 5 },
  "invoice": {
    "id": "8f11…", "code": "INV-20261021-K7M2QX", "number": "INV/2026-27/000451",
    "subtotalPaise": 94900, "taxPaise": 17082, "totalPaise": 111982,
    "advancePaidPaise": 9900, "balancePaise": 102082,
    "status": "ISSUED",
    "lines": [ /* itemised */ ]
  },
  "balancePaymentLink": "https://pay…"
}
```

**Error if the workflow is incomplete**
```json
{
  "error": {
    "code": "WORKFLOW_INCOMPLETE",
    "message": "Cannot complete the job while mandatory steps are pending.",
    "details": {
      "pendingSteps": [
        { "key": "repair", "label": "Carry out the repair",
          "blockedItems": [ { "code": "repair.photo_after", "label": "Photo after repair" } ] }
      ]
    },
    "requestId": "req_01J8…"
  }
}
```

### 5.4 `POST /v1/admin/settlements/generate`

```json
{ "period": "2026-W43", "branchIds": ["OD-BBI-001"], "dryRun": true }
```

```json
{
  "dryRun": true,
  "candidates": [
    { "branchId": "OD-BBI-001", "partnerOrgId": "PT-OD-0042", "period": "2026-W43",
      "jobsCount": 84, "eligibleLabourPaise": 4200000, "commissionPaise": 630000,
      "taxPaise": 113400, "netPaise": 743400, "alreadyExists": false }
  ]
}
```

### 5.5 `GET /v1/search/technicians`

```json
{
  "data": [
    {
      "id": "b71e…", "name": "Ramesh Kumar", "photoUrl": "https://…",
      "rating": { "average": 4.8, "count": 320 },
      "jobsCompleted": 320,
      "skills": [ { "code": "AC_REPAIR", "level": 3 } ],
      "distanceKm": 2.5,
      "etaMinutes": 18,
      "priceRange": { "minPaise": 40000, "maxPaise": 70000 },
      "badges": [ "KYC_VERIFIED", "TOP_RATED" ],
      "score": 0.87
    }
  ],
  "nextCursor": "eyJ2IjoxMjM0fQ",
  "hasMore": true
}
```

---

### 5.6 `POST /v1/waitlist` — Join the Waitlist

Used when serviceability fails. The customer is **not** given a confirmed booking.

```json
{
  "serviceVariantId": "9f3c…",
  "addressText": "Plot 42, Patia, Bhubaneswar",
  "lat": 20.2961,
  "lng": 85.8245,
  "phone": "+919876543210"
}
```

```json
{
  "waitlistId": "wl_9c21",
  "status": "WAITING",
  "reasonCode": "NO_ELIGIBLE_TECHNICIAN",
  "message": "We do not have a technician for this service in your area yet. We will contact you as soon as one becomes available.",
  "expiresAt": "2027-01-19T09:14:22Z"
}
```

**Rules**
- WL-01 — A waitlist entry is never a booking. It creates no obligation and no price.
- WL-02 — The customer is notified when coverage becomes available, **only** with a valid marketing or service consent (`customer_consents`).
- WL-03 — The waitlist is demand data. It feeds the coverage dashboard and the city-expansion decision (`ADR-017`).
- WL-04 — Scope: `[PROPOSED]` — see `21` OD-07-12 and `ADR-023`.

---

## 6. Error Model

```json
{
  "error": {
    "code": "PRICE_OUT_OF_RANGE",
    "message": "The requested price is outside the allowed range for this service.",
    "details": { "serviceVariantId": "9f3c…", "minPaise": 40000, "maxPaise": 70000, "requestedPaise": 75000 },
    "requestId": "req_01J8…",
    "timestamp": "2026-10-21T09:14:22Z"
  }
}
```

### 6.1 Error Code Catalogue

| HTTP | Code | Meaning |
|---|---|---|
| 400 | `VALIDATION_ERROR` | Request body/query failed schema validation |
| 400 | `INVALID_STATE` | Operation not allowed in the current state |
| 401 | `UNAUTHENTICATED` | Missing or invalid token |
| 401 | `OTP_EXPIRED` · `OTP_INVALID` · `OTP_LOCKED` | OTP failures |
| 403 | `PERMISSION_DENIED` | Role lacks the permission |
| 403 | `SCOPE_VIOLATION` | Outside the caller's scope (logged as a security event) |
| 403 | `SELF_APPROVAL_BLOCKED` | Cannot approve your own action |
| 403 | `MODE_PROTECTED` | Destructive operation refused because the platform is in `PRODUCTION` mode (`38` §6). The response names the guard and the legitimate path, never a bypass |
| 409 | `MODE_PRECONDITION_FAILED` | A mode transition cannot start; the payload lists which `38` §4 pre-condition failed |
| 424 | `EMAIL_CHANNEL_UNAVAILABLE` | The step-up could not be dispatched — a **dependency** failure (`24` P-06 is not procured), not a permission denial (`38` §5.1) |
| 404 | `NOT_FOUND` | Resource does not exist or is not visible to the caller |
| 409 | `STATE_CONFLICT` | Optimistic lock failure / concurrent update |
| 409 | `DUPLICATE` | Unique constraint (e.g. coupon already redeemed) |
| 409 | `TERRITORY_CONFLICT` | Service area already allocated |
| 409 | `IDEMPOTENCY_MISMATCH` | Same key, different payload |
| 409 | `SETTLEMENT_ALREADY_EXISTS` | Unique on (partner, branch, period) |
| 410 | `GONE` | Resource archived and no longer accessible |
| 412 | `PRECONDITION_FAILED` | `If-Match` version mismatch |
| 422 | `PRICE_OUT_OF_RANGE` | Price outside the band |
| 422 | `COUPON_NOT_APPLICABLE` | Coupon failed a rule (details: which rule) |
| 422 | `COUPON_EXPIRED` · `COUPON_USAGE_LIMIT_REACHED` | Coupon failures |
| 422 | `SERVICE_NOT_AVAILABLE` | **Serviceability failed.** `details.reasonCode` carries one of the six reason codes below |
| 422 | `WORKFLOW_INCOMPLETE` | Mandatory steps pending |
| 422 | `FIELD_NOT_MODIFIABLE` | Field-level restriction |
| 422 | `APPROVAL_REQUIRED` | Needs an approval step to proceed |
| 429 | `RATE_LIMITED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Unexpected failure (requestId included) |
| 502 | `UPSTREAM_UNAVAILABLE` | Third-party provider failed |
| 503 | `SERVICE_UNAVAILABLE` | Maintenance / degraded mode |

### 6.2 Serviceability Reason Codes

Returned in `error.details.reasonCode` when `SERVICE_NOT_AVAILABLE` is raised (`ADR-004`, `23` §5).

| Reason code | Meaning | Customer-facing action |
|---|---|---|
| `ADDRESS_NOT_GEOGRAPHABLE` | The address could not be resolved to a point | Ask for a landmark or a pincode |
| `NO_SERVICE_AREA` | The point is outside every service area | Offer the waitlist and a callback |
| `AREA_INACTIVE` | The area exists but is not currently served | Offer the waitlist |
| `AREA_UNASSIGNED` | The area has no owning branch | Offer the waitlist; escalate to the operator |
| `BRANCH_INACTIVE` | The owning branch is suspended or closed | Offer the waitlist; notify the customer |
| `CATEGORY_NOT_ENABLED` | The branch does not offer this category | Offer a category that is available |
| `NO_TAX_REGISTRATION` | The branch's legal entity cannot invoice this state | Offer the waitlist; **escalate to finance immediately** |
| `SERVICE_NOT_OFFERED` | The service is not published for this area | Offer a related service |
| `NO_PRICE_BAND` | No valid price band for the area | Escalate to the operator |
| `NO_ELIGIBLE_TECHNICIAN` | No technician passes the hard filters | Offer the waitlist and the next available slot |

**Rule ERR-03** — A `SERVICE_NOT_AVAILABLE` response must always be accompanied by at least one
**approved alternative** in `details.alternatives` (a different service, a waitlist entry, a callback,
or an enquiry). The customer is never given a dead end.

**Rule ERR-01** — A `4xx` response never leaks internal identifiers or stack traces.
**Rule ERR-02** — The `requestId` is present on every error and is searchable in the logs.

---

## 7. Idempotency

| Endpoint group | Key | Behaviour |
|---|---|---|
| `POST /bookings` | `Idempotency-Key` | Replays the original `201` for the same key + payload |
| `POST /quotes` | — | **`[OPEN]` — `OD-DOC-19`.** Labelled read-only here and "advisory and non-binding" in §5.1, but `09` gives quotes a `quotes` table with a unique `quote_ref`, and §5.1 returns that reference with a `validUntil`. Until the storage question closes, do not treat this row as settled |
| `POST /bookings/{id}/complete` | `Idempotency-Key` | Replays the original response; never double-invoices |
| `POST /payments/.../collect` | `Idempotency-Key` | One active payment link per booking |
| `POST /admin/settlements/generate` | Natural key | Unique `(partner, branch, period)` |
| `POST /bookings/{id}/rate` | Natural key | Unique `booking_id` in `ratings` |
| Gateway webhooks | `provider_event_id` | `webhook_inbox` unique constraint |

**Rule IDM-01** — Reusing a key with a **different** payload returns `409 IDEMPOTENCY_MISMATCH`.
**Rule IDM-02** — Idempotency records are retained for 24 hours.

---

## 8. Rate Limits

| Scope | Limit |
|---|---|
| Auth / OTP | 5 / hour per number, 20 / hour per IP |
| Public catalog & search | 120 / min per IP |
| **Public unauthenticated writes** — `POST /waitlist` `[PROPOSED]` | 6 / hour per IP, 3 / hour per phone number. `/waitlist` is the only `Public` route that stores a phone number, and `WL-02` makes it the trigger for a later message. The message is billed to the platform owner, not to this engagement (`26` §3.2 item 1), so an unbounded public write is an unbounded cost the owner pays for |
| Customer write endpoints | 60 / min per user |
| Technician endpoints | 120 / min / technician |
| Tracking location | 1 / 10 s per technician (also enforced in-app) |
| Control Center reads | 600 / min per user |
| Control Center writes | 120 / min per user |
| Webhooks | 600 / min per provider IP |

**Rule RL-01** — A `429` includes `Retry-After` in seconds.

---

## 9. WebSocket Protocol

**Endpoint:** `GET /ws?token=<jwt>` → upgrade to WebSocket.

**Client → Server**

```json
{ "type": "subscribe", "channels": ["booking:AMM-20261021-K7M2QX:track", "booking:AMM-20261021-K7M2QX:status"] }
{ "type": "ping", "ts": 1780000000000 }
```

**Server → Client**

```json
{ "type": "location", "channel": "booking:…:track",
  "payload": { "lat": 20.2961, "lng": 85.8245, "heading": 92, "speedKph": 34, "etaMinutes": 8, "ts": "2026-10-21T09:31:00Z" } }

{ "type": "status", "channel": "booking:…:status",
  "payload": { "status": "EN_ROUTE", "statusCode": 3, "changedAt": "2026-10-21T09:28:00Z" } }
```

**Rules**
- WS-01 — The server validates the subscription target against the caller's ownership/scope before subscribing. An unauthorised subscription is refused and logged.
- WS-02 — Location updates are throttled to ≥ 15 s or ≥ 25 m of movement.
- WS-03 — The client must implement a polling fallback (`GET /bookings/{id}/track`).
- WS-04 — Heartbeat every 25 s; the server drops a connection silent for 60 s.
- WS-05 — The Redis adapter enables horizontal scaling of the gateway.

---

## 10. Versioning & Compatibility

| Rule | Statement |
|---|---|
| VER-01 | The major version is in the path (`/v1`). A breaking change requires `/v2`. |
| VER-02 | Within a major version, changes are **additive only**: new optional fields, new endpoints, new enum values in a documented extensible set. |
| VER-03 | New enum values are a breaking change for strict clients → extensible enums are documented in the OpenAPI schema with `x-extensible-enum: true`. |
| VER-04 | Deprecated fields are marked `deprecated: true` and removed only after a 2-release window. |
| VER-05 | The OpenAPI document is generated from code and committed. CI fails on drift. |
| VER-06 | Flutter and web clients are generated from the OpenAPI document and pinned to a released API version. |

---

## 11. Security Controls

| Control | Implementation |
|---|---|
| Authentication | OTP + rotating refresh tokens; JWT RS256; short TTL |
| Authorisation | Role + scope + ownership guards (`03` §6) |
| Mode guard | Destructive operations are refused by the **handler and by database privilege**, not by the UI alone (`38` §7). `403 MODE_PROTECTED` is the API-visible half of a control whose stronger half is a role that has no `DELETE` grant |
| Rate limiting | Per identity and per IP; Redis-backed |
| Input validation | Schema validation at the boundary; parameterised queries only |
| SQL injection | No string-concatenated SQL; ORM/query-builder parameters throughout |
| Data masking | Phone/email/bank masked by role; full values only to Finance/Admin |
| File upload | Presigned direct upload; MIME and size validation; antivirus scan; content-type sniffing |
| Secrets | Environment/secret manager; never in code or logs |
| Logging | Sensitive fields redacted (passwords, OTPs, full card data, bank account numbers) |
| CORS | Explicit allow-list per environment |
| CSRF | Not applicable to Bearer-token APIs; required for cookie-based web sessions |
| Headers | `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy` |
| Audit | Every sensitive mutation writes an `audit_event` (`09` §4.14) |
| Reconcile | `GET /admin/reconciliation` compares gateway settlements to recorded payments |

---

## 12. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| OD-10-01 | Should the Control Center use the same `/v1` API with role-based scoping, or a separate `/admin` API with its own auth? | Engineering | Phase 0 |
| OD-10-02 | Public (unauthenticated) catalog access — allowed for browsing, or login-first? | Product | Phase 1 |
| OD-10-03 | Should quotes be cached server-side (with a `quoteId`) to lock the price at booking, or recomputed at booking? | Product + Finance | Phase 1 |
| OD-10-04 | Do we expose a public webhook for partner systems, or is the integration one-way only? | Engineering | Phase 3 |
| OD-10-05 | Is a GraphQL/REST hybrid needed for the Control Center's complex report screens? | Engineering | Phase 2 |
| OD-10-06 | **Map every endpoint in §4 to a permission token in `03`, and decide the `domain` segment for money routes.** §4.6 shows the mapping is missing entirely, and that ten transition verbs (`complete`, `start-route`, `rate`, `dispute`, `refund-request`, `pause`, `publish`, `allocate`, `generate`, `approve-settlement`) have no `action` in `03` §3.1. | Security Owner + Engineering Lead | Phase 0 — before the first guard is written |
| OD-DOC-13 | `addressId` accepted on two `Public` catalogue routes (`/catalog/services`, `/catalog/service-areas/resolve`) — an ownership check or the parameter removed? | Engineering Lead + Security | Phase 0 |
| OD-DOC-14 | Server-side rejection of a `/parts` or `/invoice` call with no matching customer `/approve` record — who writes that rule? | Product + Finance + Eng | Phase 0 |
| OD-DOC-15 | The dead-letter replay route: verb, path, permission and audit shape (§4.5 promises replay through a `GET`). | Engineering Lead | Phase 1 |
| OD-DOC-16 | `/branch/reports/*` — an enumerated report list with one permission per report, or one wildcard permission? | Security Owner + Product | Phase 3 |
| OD-DOC-18 | `/webhooks/otp/{provider}` — delete the route and carry OTP status as an SMS event, or procure a dedicated OTP vendor and write its contract? | Engineering Lead | Phase 0 |
| OD-DOC-19 | Is a quote persisted (`09` `quotes`) or genuinely read-only (§7)? The two statements cannot both hold. | Finance + Engineering Lead | Phase 0 |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.5 | 2026-10-21 | Eng Lead + Security Owner (platform-mode pass) | §4.3 gained **five mode routes** — read the effective mode, list transition history, request a promote/demote with a non-empty reason, submit the step-up OTP, and record the second-account acknowledgement. Each carries the note that the mode is **never an input**: no header, query parameter or client value may set it. §6.1 gained three codes — `403 MODE_PROTECTED` (refused because the state forbids it), `409 MODE_PRECONDITION_FAILED` (with the machine-readable pre-condition report), `424 EMAIL_CHANNEL_UNAVAILABLE` (the ceremony cannot complete because the OTP channel is not procured — a **dependency failure, not a client error**). §11 gained the mode-guard control row. §4.6 was **re-measured rather than recomputed**: a row-anchored scan returns **122 endpoint rows / 116 distinct paths** where the inherited figure was 117/112, and removing the five new rows reproduces 117 exactly — so an intermediate claim in this pass that the inherited figure was 'one short' was wrong and is corrected here, with the §3 auth rows (8, unchanged) still reported separately. | §4.3, §4.6, §6.1, §11 |
| 1.4 | 2026-10-21 | Engineering Lead | Render-integrity fixes, no contract change: the §1 principle table's header declared a third **Consequence** column that no row supplied, so the table rendered with an empty column on every row — the header now matches the two columns the rows actually carry. One inline code span in §2 (the `Accept-Language` row, whose value lists three locales separated by pipes) contained an unescaped pipe and was splitting its cell in two; escaped. These were found by a suite-wide table-column scan, not by reading. | §1, §2 |
| 1.3 | 2026-10-21 | Engineering Lead (documentation audit pass 3, continued) | §4.6 **re-measured both sides of the gap it describes**: the catalogue is 117 endpoint rows (125 counting §3), not the 123 carried from `28` §2, and `03` §4.1–§4.4 hold 96 permission cells / 92 distinct tokens, not 89. Counting them rather than quoting them produced a new finding, recorded in §4.6 and folded into `OD-10-06`: **29 action segments in the `03` matrix are not among the 11 actions `03` §3.2 declares**, the declared `delete` appears nowhere, and nine cells carry their scope as prose beside the token (`booking:read` (own), `job:start` (OTP verified), `support:call` (toll-free) among them) where an enforcement layer cannot read it. §4.5's dead-letter bullet annotated `[OPEN]` — the sentence "allows replay" is the claim `OD-DOC-15` disputes, and the dispute now sits on the same line as the claim. No route, status code or contract in this document was changed. | §4.5, §4.6, Revision History |
| 1.2 | 2026-10-21 | Engineering Lead (documentation audit pass 3) | Every endpoint row in §4 now carries an **Auth** and **Effects** value — the catalogue previously described what a route returned and nothing about who could call it or what it changed. §4.6 added: no permission token in `03` is joined to any route in this document, and ten verbs here have no `action` in `03` §3.1 (`OD-10-06`). Registered from this section: `OD-DOC-13` (`addressId` accepted on three unauthenticated routes — an ownership-check defect), `OD-DOC-14` (no stated server-side rejection of an unapproved part or invoice line), `OD-DOC-15` (dead-letter replay is documented as a `GET`; `24` §14.3 already requires an operator action), `OD-DOC-16` (`/branch/reports/*` wildcard cannot be permission-checked), `OD-DOC-18` (`/webhooks/otp/{provider}` has no owning contract — mapped against `24` §14.5), `OD-DOC-19` (quotes are "read-only" in §7 and have a table in `09`). §4.3 gained the `dead-letters` route its own §4.5 rule depended on. §8 gained a public-write limit for `POST /waitlist`, the only unauthenticated route that stores a phone number. | §4 (all), §4.6, §7, §8, §12, header, Revision History |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Added the idempotency store entity, the persisted quote resource, ~~the add-on and emergency-charge line codes~~, and the serviceability reason codes to the error catalogue; cross-referenced the audit additions. **(corrected 2026-10-21:** the serviceability reason codes (§6.2) and the idempotency treatment (§7) are present, so those halves of this claim hold. No add-on or emergency-charge **line code** appears anywhere in this document, and §5.1's quote example contains neither — the claim is struck through rather than deleted, so the audit trail of what was asserted is not silently rewritten. The "persisted quote resource" half is now a registered conflict, `OD-DOC-19`**)** | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
