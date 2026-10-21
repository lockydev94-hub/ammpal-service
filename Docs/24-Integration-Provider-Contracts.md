# 24 — Integration Provider Contracts

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-24 |
| Version | 1.3 |
| Status | Approved for Design & Development |
| Owner | Engineering Lead |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `08`, `10`, `11`, `19` |

## §1 Purpose and Scope

### 1.1 Purpose

`[CONFIRMED]` This document defines the **integration contract surface** AmmPal Service will implement against every third-party provider: business purpose, data exchanged, authentication, the API surface AmmPal depends on, the webhook/event contract, failure handling, degradation behaviour, a conformance checklist, and open dependencies. `[CONFIRMED]` It specifies **AmmPal's own obligations**, not a reproduction of any vendor's public documentation; the vendor's public contract remains the source of truth and this document is its projection into the AmmPal modular monolith.

### 1.2 In scope

`[CONFIRMED]` Nine provider integrations: Google Maps Platform; Razorpay; Indian cloud-telephony provider + IVR; WhatsApp Business Platform; Indian SMS provider; transactional email provider; Firebase Cloud Messaging; S3-compatible object storage; OIDC identity provider.

`[CONFIRMED]` These integrations serve the Public Website (Next.js + React + TypeScript), the Customer App (Flutter), the Partner App (Flutter), the AmmPal Control Center (React + Vite + TypeScript) and the Partner web dashboard (React + Vite + TypeScript). `[PROPOSED]` The Partner web dashboard is **conditional scope**: it is a proposed surface only, so no provider contract in this document may be designed to depend on it exclusively — the Partner App and the Control Center are the baseline partner-facing surfaces, and every partner-bound provider flow must work without the web dashboard.

### 1.3 Out of scope

`[CONFIRMED]` Internal service-to-service contracts between AmmPal modules (in `10`, `11`, `19`); the booking lifecycle and domain model (in `08`); vendor selection criteria and commercial negotiation; data encryption-at-rest and key-management policy for the platform datastore (in `14`).

### 1.4 Platform context

`[CONFIRMED]` AmmPal Service is a modular monolith on NestJS + TypeScript with modules `identity`, `rbac`, `organization`, `catalog`, `workflow`, `partner`, `booking`, `pricing`, `billing`, `commission`, `support`, `notification`, `realtime`, `reporting`, `audit`, `integration`. The `integration` module is the **sole owner** of all outbound third-party calls; no other module may call a provider SDK or HTTP endpoint directly, and `[PROPOSED]` this is enforced by a lint rule and a module-boundary test. `[CONFIRMED]` Persistence is PostgreSQL 16 + PostGIS with Redis 7 + BullMQ, and S3-compatible object storage for binaries; `[PROPOSED]` provider webhooks are received by dedicated controllers in the `integration` module, normalised into internal events, and enqueued to BullMQ. `[CONFIRMED]` The deployment target is a Linux VPS with 4 vCPU, 16 GB RAM, 200 GB NVMe and 16 TB monthly bandwidth; `[DEPENDENT]` provider-side capacity, throttling and regional availability must be validated against that single-node topology.

### 1.5 Non-implementation notice

`[CONFIRMED]` **Nothing in this document is implemented.** There is no application source code in the AmmPal Service repository — only documentation and four PNG diagrams. No provider account, commercial contract, template approval, SLA, price, credential or endpoint exists. `[CONFIRMED]` Every conformance checklist in §4–§12 therefore starts at **Not tested**, and every provider in the §3 register carries a contract status of **NOT YET PROCURED**.

## §2 How to Read This Document

### 2.1 Status taxonomy

`[CONFIRMED]` Every material statement carries exactly one status tag. `[CONFIRMED]` An untagged statement is structural (heading, table header, cross-reference) and carries no normative weight.

| Tag | Meaning | Reader's obligation |
|---|---|---|
| `[CONFIRMED]` | Established in project context or an approved project document. | Rely on it as the working baseline. |
| `[PROPOSED]` | Recommended design awaiting approval. | Expect change; treat as intended design. |
| `[OPEN]` | Requires a business-owner decision. | Escalate via the open-decision register (§18). |
| `[DEPENDENT]` | Requires an external provider, legal/tax review, or operational readiness. | Never treat as a commitment. |
| `[IMPLEMENTED]` | Verified in source code or deployment configuration. | **Unused here — no integration is implemented.** |

### 2.2 The provider is an external system, never a source of truth

`[CONFIRMED]` **AmmPal treats every provider as an external system, never as a source of truth.** These rules bind every engineer in the `integration` module.

| # | Rule | Status |
|---|---|---|
| TR-1 | The AmmPal PostgreSQL database is the system of record for bookings, pricing, commissions, invoices, settlements and KYC state. | `[CONFIRMED]` |
| TR-2 | A provider response is never persisted verbatim as a domain fact; it is transformed, validated, then projected into AmmPal domain state. | `[CONFIRMED]` |
| TR-3 | If provider and AmmPal disagree on a completed transaction, AmmPal's ledger wins; the provider report is a reconciliation input only. | `[CONFIRMED]` |
| TR-4 | Provider availability, rate limits and schema changes are never load-bearing for AmmPal availability; every provider call sits behind a timeout, a circuit breaker and a queue. | `[PROPOSED]` |
| TR-5 | No AmmPal module polls a provider API on a hot path; provider state is mirrored into AmmPal tables on a schedule or by event. | `[PROPOSED]` |
| TR-6 | Credentials are referenced by alias only; secret material lives in a secrets manager and is never committed, logged, or written to a document. | `[CONFIRMED]` |

### 2.3 Evidence rule

`[CONFIRMED]` **No credential, endpoint URL, contract, SLA, template, or price may be recorded here without evidence.** `[CONFIRMED]` No secret values, API keys, tokens, webhook secrets, merchant identifiers, account identifiers or real phone numbers appear anywhere in this file. `[CONFIRMED]` Endpoint references use path-style notation against an abstracted `PROVIDER_HOST`, because the concrete base URL is a deployment secret. `[CONFIRMED]` The toll-free number is a **placeholder** `1800-XXX-XXXX` until a real number is procured and verified, and no other number may be substituted. `[DEPENDENT]` Monetary rates, per-message charges and per-minute charges are **not established** and must come from current vendor pricing at procurement. `[DEPENDENT]` Any statement that a template is approved, a service level is agreed, or a vendor will meet a target requires a signed document reference.

### 2.4 Reading paths

`[PROPOSED]` Backend engineers: §2, §3, the relevant §4–§12 section, §13, §14. QA: §3, each §4.6 and §4.8, §14, §19. Platform and DevOps: §3, §11, §15, §16, §19. Security: §2.2, §2.3, each §4.3, §13, §14, §15. Product: §3, each §4.1, §15, §18.

## §3 Provider Register

`[CONFIRMED]` One row per provider integration. **Contract status for every provider is `NOT YET PROCURED` / `[DEPENDENT]`.** No provider account, agreement, SLA, price or approval exists as of the Last Updated date.

| # | Provider | Purpose | Direction | Criticality | Contract status | Fallback | Adapter interface | Owning module |
|---|---|---|---|---|---|---|---|---|
| P-01 | Google Maps Platform | Geocoding, address normalisation, service-area distance and duration matrix, directions, place autocomplete, static map tiles | Outbound (read) | High — booking pricing, serviceability, ETA | **NOT YET PROCURED** `[DEPENDENT]` | Manual pin-centre plus haversine estimate; pre-rendered district map; operator-entered serviceability | `MapsPort` | `catalog` consumes, `integration` owns |
| P-02 | Razorpay | Payment collection, refunds, partial refunds, payment webhooks, settlement reconciliation | Outbound (write) plus inbound (webhook) | Critical — customer payment capture | **NOT YET PROCURED** `[DEPENDENT]` | Manual UPI/NEFT reference payment with operator confirmation; cash-on-completion where policy permits | `PaymentsPort` | `billing` consumes, `integration` owns |
| P-03 | Indian cloud-telephony provider + IVR | Outbound call origination, IVR flow, call recordings, click-to-call, voice OTP fallback, call status callbacks | Outbound (write) plus inbound (callback) | High — dispatch reach-out, voice OTP | **NOT YET PROCURED** `[DEPENDENT]` | SMS OTP primary fallback; manual operator-initiated call; defer to the next attempt window | `TelephonyPort` | `notification` consumes, `integration` owns |
| P-04 | WhatsApp Business Platform | Transactional and service messaging: booking confirmations, dispatch updates, invoice and receipt delivery, reschedule, OTP | Outbound (write) plus inbound (webhook) | High — customer-facing status updates | **NOT YET PROCURED** `[DEPENDENT]` | SMS (P-05), then email (P-06), then an operator phone call (P-03) | `MessagingPort` | `notification` consumes, `integration` owns |
| P-05 | Indian SMS provider | Transactional SMS, OTP delivery, delivery-receipt callbacks, sender ID and DLT registration | Outbound (write) plus inbound (callback) | High — OTP and fallback channel | **NOT YET PROCURED** `[DEPENDENT]` | Voice OTP (P-03), then in-app OTP for authenticated surfaces, then an operator call | `MessagingPort` (SMS channel) | `notification` consumes, `integration` owns |
| P-06 | Transactional email provider | Invoice, statement, receipt, digest and system-notice delivery | Outbound (write) plus inbound (bounce, complaint) | Medium-High — financial document distribution | **NOT YET PROCURED** `[DEPENDENT]` | Object-storage link (P-08) with a manual notification; WhatsApp (P-04) document link | `EmailPort` | `notification` consumes, `integration` owns |
| P-07 | Firebase Cloud Messaging | Push delivery to AmmPal app installs, background kill and collapse events, topic subscriptions | Outbound (write) plus inbound (delivery report) | Medium — engagement, not transactional truth | **NOT YET PROCURED** `[DEPENDENT]` | WhatsApp (P-04), then SMS (P-05), then email (P-06), then the in-app inbox | `PushPort` | `notification` consumes, `integration` owns |
| P-08 | S3-compatible object storage | Invoices, statements, KYC documents, call recordings, job media, exports, backups | Outbound (write) | Critical — durable store for generated artefacts | **NOT YET PROCURED** `[DEPENDENT]` | Local encrypted volume with off-host replication; regenerate deterministic artefacts | `ObjectStoragePort` | `integration` owns; `billing` and `partner` consume |
| P-09 | OIDC identity provider | Staff, partner and customer authentication, authorisation-code with PKCE, refresh rotation, JWKS validation, Control Center SSO | Outbound (read) plus inbound (redirect, callback) | Critical — all access control depends on it | **NOT YET PROCURED** `[DEPENDENT]` | Local credential authentication with mandatory TOTP for staff; break-glass admin with dual control | `IdentityPort` | `identity` consumes, `integration` owns |

`[PROPOSED]` Register order mirrors build sequencing: `MapsPort` and `IdentityPort` are foundational; `PaymentsPort` and `ObjectStoragePort` are revenue-bearing; the notification ports proceed in parallel once the §14 baseline exists. `[DEPENDENT]` Because the deployment is a single VPS, no provider can be treated as a redundant component of another; redundancy must be built inside AmmPal through queueing, retry and alternate channels. `[OPEN]` Whether a second SMS provider is contracted (OD-INT-03) determines whether the P-05 fallback is "different channel" or "different vendor" — see §18.

## §4 Google Maps Platform

### 4.1 Purpose and business use cases

| Use case | Business rule | Status |
|---|---|---|
| U-1.1 Address normalisation for customer and booking addresses | Canonical form stored by `organization`; raw input retained verbatim alongside | `[PROPOSED]` |
| U-1.2 Service-area eligibility (is a pin inside a defined service area?) | Determines whether a booking may be accepted for a branch | `[PROPOSED]` |
| U-1.3 Technician travel-time estimate feeding pricing and ETA | Advisory estimate, never a guaranteed ETA | `[PROPOSED]` |
| U-1.4 Distance matrix between branch hub, service area and job site | Feeds dispatch sequencing and partner travel-cost inputs | `[PROPOSED]` |
| U-1.5 Directions polyline, place autocomplete, and static map tiles for invoices and job reports | Deep links to the Customer App and Partner App; rendered tiles stored in P-08 | `[PROPOSED]` |

`[PROPOSED]` All map-derived values are cached in AmmPal with a request fingerprint and TTL; `pricing` must never call a map provider on the hot path of a quote and reads the cached estimate instead.

### 4.2 Data exchanged

| Direction | Data | PII class | Retention |
|---|---|---|---|
| Outbound | Geocoding query: free-text address, city, state, postal code | Indirect location PII | AmmPal retains the request fingerprint and result only — `[PROPOSED]` 90 days; provider-side retention per vendor policy |
| Outbound | Lat/long of job site, branch hub and service-area polygon vertices; autocomplete keystrokes | Precise location — sensitive | `[PROPOSED]` Life of the booking then 12 months in the audit trail; keystrokes are not stored, only logged as a redacted fingerprint |
| Inbound | Normalised address components, place ID, geometry, confidence score | Indirect location PII | `[PROPOSED]` Persisted on the address record for the life of the entity |
| Inbound | Duration and distance matrix values; rendered static map image bytes | None | `[PROPOSED]` Matrix values cached 24 hours then refreshed; map images stored in P-08 for the life of the artefact |

`[DEPENDENT]` Provider-side retention of request payloads is governed by vendor terms not yet under an executed agreement, so AmmPal minimises request content until terms are confirmed.

### 4.3 Authentication and authorisation

| Item | Contract | Status |
|---|---|---|
| Authentication method | API key passed as a request parameter or header | `[PROPOSED]` |
| Key scope and restrictions | Separate key per environment and per consuming surface; per-key restriction by API and, where supported, by referrer or IP | `[PROPOSED]` / `[DEPENDENT]` — requires the billing project to exist |
| Server-side only | The API key **must never** be embedded in the Customer App, Partner App, or any client bundle | `[CONFIRMED]` |
| Client-side use, rotation and storage | Client-restricted keys only where the provider issues them; rotation every 180 days with a dual-key overlap window; secrets-manager entry referenced by alias, with no key value in a repository, log, or this document | `[DEPENDENT]` / `[PROPOSED]` / `[CONFIRMED]` |

`[PROPOSED]` All map calls originate server-side from `catalog` and `integration`; client apps receive tiles via a short-lived signed URL or a server-side proxy endpoint.

### 4.4 API surface AmmPal depends on

`[PROPOSED]` Path-style references against `PROVIDER_HOST`; the concrete host and version pin are deployment configuration.

| Operation | Path style | Use | Notes |
|---|---|---|---|
| Geocode and reverse geocode | `GET /maps/geocode`, `GET /maps/geocode/reverse` | U-1.1, U-1.2 | Structured query form preferred over free text; reverse only where the customer pins a location |
| Place autocomplete and details | `GET /maps/places/autocomplete`, `GET /maps/places/details` | U-1.5 | Session-token grouping to bound billed sessions |
| Distance matrix and directions | `GET /maps/distancematrix`, `GET /maps/directions` | U-1.3, U-1.4, U-1.5 | Matrix up to 25 elements per call; travel mode and departure time supplied |
| Static map render | `GET /maps/staticmap` | U-1.5 | Rendered to P-08 |

`[PROPOSED]` AmmPal pins the provider API version in configuration so a version migration is a configuration change plus a conformance re-run, not an emergency code change. `[PROPOSED]` `ZERO_RESULTS` and `NOT_FOUND` are **domain outcomes, not errors**: the booking enters an address-correction flow rather than a technical failure path.

### 4.5 Webhook/event contract

`[PROPOSED]` Google Maps Platform does not push webhooks into AmmPal; AmmPal polls nothing and is called by nothing in normal operation.

| Event name | Payload fields | Delivery guarantee | Signature scheme | Idempotency key | Duplicate handling | Retry policy AmmPal implements |
|---|---|---|---|---|---|---|
| (none) | n/a | n/a | n/a | n/a | n/a | n/a |

`[PROPOSED]` Should a billable usage-alert push be introduced, the §14 baseline applies unchanged: HMAC over the raw body, 5-minute timestamp window, constant-time comparison, dedupe on `(provider, provider_event_id)`, persist-then-acknowledge, dead-letter replay after the retry ceiling. `[PROPOSED]` Map usage reconciliation is a scheduled job in `reporting` comparing AmmPal's own call counters to the provider's usage report, not a webhook consumer.

### 4.6 Failure modes and AmmPal's handling

| Failure | Detection | AmmPal behaviour | Fallback | Alert |
|---|---|---|---|---|
| Timeout or 5xx | HTTP timeout, retry budget exhausted | Retry with exponential backoff and jitter; queue the task; never fail the booking transaction | Haversine distance times a default speed factor as a provisional estimate | P2 if failure rate > 5% over 5 min |
| Quota exceeded | 429 or quota error code | Quota-degraded mode: cached values only; optional calls (static map, autocomplete) disabled | Cached matrix; operator-set serviceability | P1 if core calls are exhausted |
| Invalid address (`ZERO_RESULTS`) or partial matrix | 200 with an empty result; per-element status | Return a structured "address needs correction" outcome; use resolvable elements and mark the rest unknown | Operator-assisted correction; haversine for the unresolved pair | P4, aggregated daily |
| API key invalid | 401 or 403 key error | Fail closed; do not retry, because retry cannot help | None — block new address-dependent bookings | P1, immediate |
| Rate limit or provider outage | 429 with a retry-after hint; 5xx spike across independent checks | Honour `Retry-After` and shed non-essential traffic; open the circuit breaker so map calls become advisory-only | Queue and retry; haversine estimate, with an operator confirming serviceability | P3 / P2 |
| Response schema drift | Contract-test failure in the nightly run | Quarantine the adapter; keep the previous cached response shape | Cache-only mode | P1 on contract-test failure |

### 4.7 Degradation and fallback path

`[PROPOSED]` Ordered degradation ladder for geospatial intelligence: **0 — Full** (geocode, matrix, directions and static maps all permitted); **1 — Core only** (geocode and matrix permitted; autocomplete, static maps and directions disabled); **2 — Cache-only** (serve cached values; new addresses require operator entry); **3 — Geometric** (haversine distance with a configurable average speed factor, eligibility by point-in-polygon against stored service-area geometry); **4 — Manual** (an operator sets serviceability in the Control Center, logged with `source=MANUAL`).

`[PROPOSED]` Every degraded response carries `degraded: true` and a `degradation_level` so downstream consumers can adjust and reconciliation can later correct the affected records. `[PROPOSED]` The provider is never a hard dependency for **creating** a booking: AmmPal accepts an address without coordinates and queues geocoding, and an address that cannot be geocoded within 24 hours is escalated to `OPERATOR`.

### 4.8 Conformance checklist

`[CONFIRMED]` All items start at **Not tested** — no provider account or code exists.

| # | Check | Method | Result |
|---|---|---|---|
| 1.1 | Geocode resolves a curated set of Indian addresses to the expected locality and state, and its components map cleanly to AmmPal address fields | Fixture set of at least 200 addresses plus schema mapping test | Not tested |
| 1.2 | Service-area point-in-polygon agrees with provider-derived eligibility | Parallel computation test | Not tested |
| 1.3 | Distance matrix duration is within plus or minus 15% of the prior cached value on re-query | Repeatability test | Not tested |
| 1.4 | Autocomplete session tokens are reused correctly and billed sessions behave as expected | Billing-observation test | Not tested |
| 1.5 | The API key is absent from all client bundles and from logs, and per-key API restrictions reject a disallowed call | Secret-scanning CI check plus negative test | Not tested |
| 1.6 | Quota exhaustion produces the documented Level-2 and Level-3 degradation | Failure-injection drill | Not tested |
| 1.7 | Provider error codes map to the correct AmmPal failure taxonomy | Contract test | Not tested |
| 1.8 | Response schema drift fails the nightly contract test, and cached values expire per the stated TTL | Schema-snapshot and time-controlled test | Not tested |

### 4.9 Open items and dependencies

| ID | Item | Blocking | Status |
|---|---|---|---|
| OD-MAP-01 | Select which Google Maps Platform APIs to license, each of which is separately billed | Budget approval before account creation | `[OPEN]` |
| OD-MAP-02 | Confirm each candidate API is available and appropriately licensed for the deployment region and VPS IP | Provider confirmation | `[DEPENDENT]` |
| OD-MAP-03 | Establish the monthly usage envelope from projected booking volume | Business forecast | `[OPEN]` |
| OD-MAP-04 | Decide whether customer-facing map tiles are served directly by the provider or proxied through AmmPal | Security and cost | `[OPEN]` |
| OD-MAP-05 | Define the cache TTL and the authoritative-source rule when a cached and a live value differ | Pricing correctness | `[OPEN]` |
| OD-INT-04 | Third-party fleet tracking is undecided; if selected it adds a further positioning provider and contract | Fleet-tracking decision | `[OPEN]` |

## §5 Razorpay

### 5.1 Purpose and business use cases

| Use case | Business rule | Status |
|---|---|---|
| U-2.1 Customer pays a booking invoice online | Amount computed by `pricing` and `billing`; never accepted from the client | `[PROPOSED]` |
| U-2.2 Prepaid versus pay-on-completion selection | Policy per service and per service area | `[OPEN]` |
| U-2.3 Full refund on cancellation, and partial refund for example of a visit fee only | Refunds executed against the original payment; the ledger records the remaining liability | `[PROPOSED]` |
| U-2.4 Settlement reconciliation | Provider settlement reports reconciled against the `billing` and `commission` ledgers | `[PROPOSED]` |
| U-2.5 Payment failure handling and retry | Idempotent retry with the same key; no double capture | `[PROPOSED]` |

`[CONFIRMED]` Money is stored as **integer paise**; the provider amount is transmitted in the smallest currency unit, and AmmPal never converts through a floating-point decimal in transit.

### 5.2 Data exchanged

| Direction | Data | PII class | Retention |
|---|---|---|---|
| Outbound | Payment intent: amount in paise, currency, order reference, customer name, email, contact | Direct PII (name, email, phone) | AmmPal stores the intent reference and status only — `[PROPOSED]` 8 years as a financial record (`09` §6) |
| Outbound | Refund request: payment reference, amount, reason, notes | Indirect PII | `[PROPOSED]` 8 years (`09` §6) |
| Inbound | Payment status, method, gateway reference, fee breakdown, verification outcome | Indirect PII (method fingerprint) | `[PROPOSED]` 8 years (`09` §6) |
| Inbound | Refund status and reason code; dispute and chargeback notices with evidence deadlines | None or indirect PII | `[PROPOSED]` 8 years (`09` §6) |
| Inbound | Settlement payload: gross, fees, tax, net, payout reference, cycle | None | `[PROPOSED]` 8 years (`09` §6) |

Payment, refund and settlement records are financial records, so they take the single financial
retention period from `09` §6 rather than a separate integration-local number. The period itself is
`[PROPOSED]` pending `OD-NFR-06`; a provider that cannot retain for the decided period is a
selection criterion, not a reason to shorten the policy.

`[CONFIRMED]` Card numbers, CVV and full track data **never transit the AmmPal platform** and never enter a log, database column or queue payload. `[PROPOSED]` AmmPal stores at most the tokenised instrument reference, the last four digits where supplied, and the network code.

### 5.3 Authentication and authorisation

| Item | Contract | Status |
|---|---|---|
| Authentication method | Provider-issued key pair: a secret key for server-side calls and a separate public key for webhook signature verification | `[PROPOSED]` |
| Server-side only | The secret key is used only by the `integration` module and is never exposed to clients | `[CONFIRMED]` |
| Webhook signature | HMAC-SHA512 over the raw request body, compared in constant time, with a 5-minute timestamp window consistent with §14 | `[PROPOSED]` |
| Least privilege and rotation | The webhook secret is write-only for AmmPal purposes; a key-rotation procedure is defined | `[PROPOSED]` |
| Secret storage | Secrets-manager entries by alias; values never in a repository, ticket, or this document | `[CONFIRMED]` |
| Order creation and replay protection | Amount and description are set server-side and the client supplies only an intent to pay; webhook events are deduped on `(provider, provider_event_id)` and API calls carry an idempotency key | `[PROPOSED]` |

`[DEPENDENT]` Exact header names, signature encoding and key-rotation mechanics are governed by the provider's public documentation, which AmmPal follows as the source of truth; the contract above is the AmmPal-side obligation.

### 5.4 API surface AmmPal depends on

`[PROPOSED]` Path-style references against `PROVIDER_HOST`.

| Operation | Path style | Use | Notes |
|---|---|---|---|
| Create and get order | `POST /v1/orders`, `GET /v1/orders/{order_id}` | U-2.1 | Idempotency key = the AmmPal invoice reference; the read is the poll fallback when a webhook is missed |
| Create, get and capture payment | `POST /v1/payments`, `GET /v1/payments/{payment_id}`, `POST /v1/payments/{payment_id}/capture` | U-2.1, U-2.5 | Idempotency key derived from the order reference; capture supports a pre-authorisation flow |
| Refund payment and fetch refunds | `POST /v1/payments/{payment_id}/refund`, `GET /v1/payments/{payment_id}/refunds` | U-2.3 | The payment reference is the refund idempotency key; refunds feed the partial-refund ledger check |
| Fetch settlements and disputes | `GET /v1/settlements`, `GET /v1/disputes` | U-2.4 | Nightly reconciliation job and daily dispute sweep |
| Verify signature | Library operation over the raw body | U-2.1 | Local verification, no network call |

`[PROPOSED]` AmmPal does not expose a raw provider checkout page inside the Customer App: the app requests a payment session token from AmmPal and uses the provider's client-side SDK or modal. `[PROPOSED]` The client never sees the secret key and never sets the amount.

### 5.5 Webhook/event contract

`[PROPOSED]` Payment webhooks are the authoritative trigger for payment state; a missed webhook is a reconciliation problem, not a state problem.

| Event name | Payload fields | Delivery guarantee | Signature scheme | Idempotency key | Duplicate handling | Retry policy AmmPal implements |
|---|---|---|---|---|---|---|
| `payment.authorized` | event id, order ref, payment ref, amount, currency, method, captured flag, fee, created at | At-least-once; may duplicate | HMAC-SHA512 over the raw body plus a timestamp header | `provider_event_id` | Dedupe on `(provider, provider_event_id)`; a second delivery is a no-op | Provider retries; AmmPal returns 2xx after a durable persist |
| `payment.captured` and `payment.failed` | event id, order ref, payment ref, amount, method, bank reference or failure code and reason | At-least-once | as above | `provider_event_id` | as above | as above |
| `refund.processed` and `refund.failed` | event id, refund ref, payment ref, amount, status, reason | At-least-once | as above | `provider_event_id` | as above | as above |
| `settlement.paid`, `dispute.created` and `order.paid` | event id, settlement/dispute/order ref, amount, bank account token, cycle, reason code, evidence due date | At-least-once | as above | `provider_event_id` | as above | as above |

`[PROPOSED]` Signature detail: computed over the **exact raw request bytes** before JSON parsing, including the timestamp value, compared in constant time with no partial match; a request outside the 5-minute window is rejected even when otherwise valid. `[PROPOSED]` Duplicate handling: the raw event is written to `integration.webhook_inbox` (Rule `09` DB-24) with a unique constraint on `(provider, provider_event_id)` **before** any business mutation; business handling is guarded by a processed flag; a duplicate hits the constraint, is recognised, and is acknowledged with 2xx without re-running the mutation. `[PROPOSED]` Retry: AmmPal acknowledges after durable persistence, not after business processing; business failures are retried by the queue with exponential backoff (base 5 s, factor 2, jitter, max 24 attempts) and then routed to a dead-letter store; dead-letter events are replayable from the Control Center using the original event id.

### 5.6 Failure modes and AmmPal's handling

| Failure | Detection | AmmPal behaviour | Fallback | Alert |
|---|---|---|---|---|
| Webhook signature mismatch, or a replay with a stale timestamp | HMAC comparison fails; timestamp outside the 5-minute window | Reject 4xx; log a redacted reason; increment the security counter | None — never process unsigned events | P1 if the rate exceeds 1 per minute, otherwise P2 |
| Duplicate webhook | Unique-constraint violation on the provider event | Acknowledge 2xx with no state change | n/a | P4, aggregated |
| Event for an unknown order | Referential check against `billing` | Persist, mark `unmatched`, raise to the reconciliation queue | Periodic lookup by reference | P2 |
| Payment captured but webhook lost | Reconciliation job finds a captured payment with no AmmPal record | Align the record from the provider's authoritative fetch, tagged `source=RECONCILED` | This is the repair path | P2 |
| Capture or refund timeout (unknown outcome) | Client timeout | Do not retry blindly; read the status first, then decide | Retry only after confirming no capture | P2 |
| Refund rejected (insufficient balance) | Provider error code | Mark the refund failed with a reason; route to `ACCOUNTANT` | Manual bank transfer with approval | P2 |
| Provider outage during checkout | 5xx or an open circuit | Present "payment temporarily unavailable, pay on completion" per policy | Pay-on-completion; manual reference payment | P1 if longer than 5 minutes |
| Amount or currency mismatch | Comparison on capture | Do not mark paid; hold for reconciliation | None | P1 |
| Dispute or chargeback received | `dispute.created` webhook or the daily sweep | Freeze the disputed amount in the `billing` ledger; open a `support` ticket | Manual evidence workflow | P2 |
| Idempotency key reused with a different payload, or provider schema drift | Provider rejects the request; nightly contract test | Log and raise as an AmmPal defect; quarantine the adapter and keep the last known good shape | Reconcile from provider exports | P1 |

### 5.7 Degradation and fallback path

`[PROPOSED]` Ordered degradation ladder for payment collection: **0 — Full** (online payment enabled, webhook-driven state); **1 — Deferred confirmation** (webhooks unreliable, so mark `PENDING_CONFIRMATION`, confirm by polling `GET /v1/payments/{payment_id}` on a bounded schedule, and reconcile nightly); **2 — Offline instruction** (online payment unavailable, so issue a UPI or NEFT payment instruction and keep the booking `REQUESTED` until an operator matches a payment or records a manual reference); **3 — Pay on completion** (the booking proceeds and payment is collected at job completion, subject to the pay-on-completion policy, which is `[OPEN]`); **4 — Manual collection** (`ACCOUNTANT` records an offline receipt against the invoice and a reconciliation exception is raised).

`[PROPOSED]` Refunds require Level 0 or 1 to execute automatically; at Level 2 and above refunds are executed manually by `ACCOUNTANT` with dual approval and recorded against the same ledger entry so reconciliation still balances. `[CONFIRMED]` Refund and settlement states align with the booking exception statuses `REFUND_PENDING(13)`, `REFUNDED(14)` and `DISPUTED(15)`.

### 5.8 Conformance checklist

| # | Check | Method | Result |
|---|---|---|---|
| 2.1 | Order creation is idempotent for the same idempotency key, and the amount in paise is transmitted without rounding drift | Repeat-call and value-equality test | Not tested |
| 2.2 | A tampered webhook body is rejected, and a valid webhook outside the 5-minute window is rejected | Negative signature and timestamp-window test | Not tested |
| 2.3 | A replayed valid webhook does not double-apply, and duplicate delivery of the same event id is a no-op | Replay and duplicate-delivery test | Not tested |
| 2.4 | The 2xx acknowledgement is returned only after durable persistence | Crash-injection test | Not tested |
| 2.5 | Refund idempotency prevents a double refund on retry, and a client-supplied amount is ignored | Retry and tampering test | Not tested |
| 2.6 | An unknown-order event is parked in reconciliation, not dropped | Unmatched-event test | Not tested |
| 2.7 | A captured payment with no webhook is recovered by reconciliation | Webhook-loss simulation | Not tested |
| 2.8 | Settlement reconciles to gross minus fees with a computed residual | Fixture reconciliation | Not tested |
| 2.9 | A provider outage triggers the documented degradation ladder | Failure-injection drill | Not tested |
| 2.10 | No card data appears in logs, the database, or queue payloads | PAN-scanning CI check | Not tested |

### 5.9 Open items and dependencies

| ID | Item | Blocking | Status |
|---|---|---|---|
| OD-PAY-01 | Select the legal entity that becomes the merchant account holder and confirm settlement bank account ownership | Legal and banking | `[OPEN]` |
| OD-PAY-02 | Confirm the settlement cycle (T+1, T+2, weekly) against the weekly commission model `CINV-YYYY-W<WW>-<BRANCH>-<NNNN>` | Finance | `[OPEN]` |
| OD-PAY-03 | Define the fee and tax treatment so that 15% commission on eligible labour is computed on the correct base | Finance and tax | `[OPEN]` |
| OD-PAY-04 | Confirm a compliant online payment flow is available for the merchant category; some categories need additional documentation | Provider and legal | `[DEPENDENT]` |
| OD-PAY-05 | Define the refund SLA, the partial-refund ceiling, and who may authorise a refund | Business | `[OPEN]` |
| OD-PAY-06 | Decide whether pay-on-completion applies to all services and areas | Business | `[OPEN]` |
| OD-PAY-07 | Confirm the fee breakdown present in the settlement payload for automated reconciliation | Provider | `[DEPENDENT]` |
| OD-DEV-08 | Adapter work depends on the agreed service-layer boundaries and the `integration` module contract | Engineering | `[OPEN]` |

## §6 Cloud Telephony & IVR

### 6.1 Purpose and business use cases

| Use case | Business rule | Status |
|---|---|---|
| U-3.1 Outbound call for dispatch and arrival notification | Call recorded and linked to the booking | `[PROPOSED]` |
| U-3.2 IVR for booking confirmation, reschedule and cancellation self-service | Outcome written back to the booking | `[PROPOSED]` |
| U-3.3 Click-to-call from the Control Center and Partner App | Call logged against the customer | `[PROPOSED]` |
| U-3.4 Voice OTP fallback when SMS delivery fails | Read-aloud OTP with a validity window and attempt cap | `[PROPOSED]` |
| U-3.5 Technician-to-customer call via masked or bridged telephony | Masking rules and recording consent handled by the provider | `[PROPOSED]` |
| U-3.6 Call recording retrieval for dispute and quality review, and missed-call detection to trigger the SMS fallback | Recording stored in P-08 under a controlled access policy; detection from the provider status callback | `[PROPOSED]` |

`[OPEN]` The IVR script, language set and escalation path are content decisions requiring product sign-off. `[PROPOSED]` The IVR is never the only path to a legally significant action; a refund request always escalates to a human.

### 6.2 Data exchanged

| Direction | Data | PII class | Retention |
|---|---|---|---|
| Outbound | Destination number, caller ID, IVR flow id, call purpose, callback URL, correlation id, agent extension | Direct PII (phone number) | AmmPal stores correlation metadata only — `[PROPOSED]` 12 months; provider-side retention per vendor policy |
| Inbound | Call status: initiated, ringing, answered, completed, busy, no-answer, failed, cancelled | Indirect PII (number) | `[PROPOSED]` 12 months |
| Inbound | DTMF keypress sequence, IVR navigation path | Indirect PII | `[PROPOSED]` 90 days |
| Inbound | Call recording audio, duration, timestamps, recording URL | Direct PII — voice is biometric-adjacent | `[PROPOSED]` Copied to P-08, provider copy released, access restricted to `PARTNER_SUPPORT`, `ACCOUNTANT` and auditors; 180 days |
| Inbound | Transcript, if transcription is ever enabled | Direct PII | `[PROPOSED]` 180 days; the feature is disabled by default |

`[CONFIRMED]` The toll-free number is a **placeholder** `1800-XXX-XXXX` until a real number is procured and verified; `[PROPOSED]` it must not be dialled in any test, because pre-production verification uses provider test credentials. `[OPEN]` Consent for call recording and for automated voice calls, including DND and telemarketing registry handling, must be confirmed by legal before any outbound campaign usage; transactional service calls are treated separately from promotional calls.

### 6.3 Authentication and authorisation

| Item | Contract | Status |
|---|---|---|
| Authentication method | Provider-issued API credentials (key or token) presented per request | `[PROPOSED]` |
| Callback authentication | HMAC over the raw callback body plus a timestamp, constant-time comparison | `[PROPOSED]` |
| Source restriction | Provider IP ranges allow-listed at the network edge, in addition to signature verification | `[PROPOSED]` |
| Number provisioning | The toll-free number and any other caller IDs are provisioned with the provider and never configured in code | `[DEPENDENT]` |
| Sub-accounting | Partner-branch cost attribution may require sub-accounts; support is not yet confirmed | `[DEPENDENT]` |
| Least privilege and storage | Credential scopes limited to call origination and callback management; secrets-manager entries by alias only; provider sandbox credentials used for all pre-production verification | `[PROPOSED]` / `[CONFIRMED]` |

`[DEPENDENT]` Availability of a dedicated Indian voice and IVR product with the required regulatory compliance (TRAI DND handling, STD/ISD restrictions) is a selection criterion, not a given.

### 6.4 API surface AmmPal depends on

`[PROPOSED]` Path-style references against `PROVIDER_HOST`.

| Operation | Path style | Use | Notes |
|---|---|---|---|
| Originate call | `POST /v2/calls` | U-3.1, U-3.4 | Idempotency key = the AmmPal correlation id |
| Hang up and get call | `POST /v2/calls/{call_id}/hangup`, `GET /v2/calls/{call_id}` | U-3.6 | Hang up is used when a booking is cancelled mid-call; the read is the status reconciliation path |
| Click-to-call request | `POST /v2/calls/click2call` | U-3.3 | Two-party bridge |
| IVR flow definition and execution | `POST /v2/ivr/flows`, `POST /v2/ivr/executions`, `GET /v2/ivr/executions/{execution_id}` | U-3.2 | The flow body is versioned in AmmPal and the provider-side deployment is a release step; the execution read is the fallback for missed callbacks |
| Fetch recording and list sub-accounts | `GET /v2/calls/{call_id}/recording`, `GET /v2/subaccounts` | U-3.6 | The recording is copied into P-08 and the provider copy released; sub-accounts are used only for cost attribution |

`[PROPOSED]` The provider's IVR authoring UI is not AmmPal's source of truth: the decision tree is authored in AmmPal, versioned, and pushed to the provider as a deployment artefact.

### 6.5 Webhook/event contract

`[PROPOSED]` Provider status and recording callbacks are the trigger for AmmPal's call records; polling is a reconciliation fallback only.

| Event name | Payload fields | Delivery guarantee | Signature scheme | Idempotency key | Duplicate handling | Retry policy AmmPal implements |
|---|---|---|---|---|---|---|
| `call.initiated` | event id, call ref, correlation id, to and from number masks, created at | At-least-once | HMAC over the raw body plus a timestamp | `provider_event_id` | Dedupe on `(provider, provider_event_id)` | Provider retries; AmmPal returns 2xx after the persist |
| `call.ringing` and `call.answered` | event id, call ref, answering party mask, timestamp | At-least-once | as above | `provider_event_id` | as above | as above |
| `call.completed` | event id, call ref, duration seconds, disposition code, recording availability | At-least-once | as above | `provider_event_id` | as above | as above |
| `call.no_answer` and `call.failed` | event id, call ref, retry hint or reason code | At-least-once | as above | `provider_event_id` | as above | as above |
| `call.recording_ready` | event id, call ref, recording reference, duration, expiry timestamp | At-least-once | as above | `provider_event_id` | as above | as above |
| `ivr.execution.completed` and `ivr.execution.failed` | event id, execution ref, correlation id, DTMF path, outcome code or reason | At-least-once | as above | `provider_event_id` | as above | as above |

`[PROPOSED]` Beyond the §14 baseline: callbacks land on a dedicated route and are acknowledged immediately after persistence, with no IVR navigation logic in the request path; DTMF payloads are validated against the expected IVR flow version and an unknown version is parked in the reconciliation queue rather than dropped; recording fetch runs asynchronously from the queue so callback latency stays low.

### 6.6 Failure modes and AmmPal's handling

| Failure | Detection | AmmPal behaviour | Fallback | Alert |
|---|---|---|---|---|
| Callback signature invalid, or a callback from a non-allow-listed source | HMAC comparison fails; edge IP check | Reject 4xx before any processing; count the security event | None | P1 if sustained |
| Origination returns 4xx (invalid number, DND block) | Response status and error code | Record a `call.failed` outcome; do not retry a DND block | Switch to SMS (P-05) for the same notification | P3 |
| Origination timeout (unknown outcome) | Client timeout | Read `GET /v2/calls/{call_id}` before any retry | As above | P3 |
| Busy or no answer | Status callback | Bounded retry per policy, then escalate | SMS, then an operator task | P3 |
| Provider outage during origination or callback delivery | 5xx or an open circuit; provider retries while AmmPal sees a gap | No calls originated and notifications route to SMS; periodic reconciliation pull for calls still `initiated` beyond a threshold | SMS, then email; reconciliation job | P2 |
| Recording unavailable or expired, or a storage failure on download | Fetch returns 404; storage error | Mark `recording_unavailable` with bounded retry; keep the provider reference and retry the storage write | No recording, noted on the ticket; discard after the retention window | P4 / P3 |
| IVR script error, or DTMF and voice input not understood | `ivr.execution.failed`; IVR outcome code | Quarantine the flow version and fall back to a direct agent call; offer an agent callback and never loop indefinitely | Direct call, then an operator task | P2 / P4 |
| Answer latency, congestion, or origination rate limit | Status callback timings; 429 with a retry-after hint | Reduce AmmPal-side concurrency; honour `Retry-After`; queue the excess | Queue | P3 |

### 6.7 Degradation and fallback path

`[PROPOSED]` Channel ladder for voice-dependent notifications and OTP: **0 — Full** (voice calls and IVR enabled); **1 — No IVR** (direct agent calls permitted, with the IVR flow withdrawn to avoid misrouting); **2 — SMS primary** (all voice notifications route to SMS, and voice OTP is disabled); **3 — No automated voice OTP** (OTP delivered by SMS and, on authenticated surfaces, in-app); **4 — Operator task** (a `support` ticket is raised for `OPERATOR` or `CCO` to contact the customer).

`[PROPOSED]` Every voice notification records the `channel_attempted` chain so the customer-contact audit trail shows the real escalation path. `[OPEN]` The retry policy for unanswered service calls — attempt count, spacing and permitted hours — is a business decision and is not yet fixed.

### 6.8 Conformance checklist

| # | Check | Method | Result |
|---|---|---|---|
| 3.1 | A test call originates and reaches an IVR execution, and the flow versioning rejects an unknown flow version gracefully | Sandbox call and version-mismatch test | Not tested |
| 3.2 | Callback signature verification rejects a tampered body, and a callback from a disallowed source IP is rejected | Negative and edge test | Not tested |
| 3.3 | A duplicate status callback does not create a second call record, and call status maps correctly to AmmPal call record states | Duplicate-delivery and contract test | Not tested |
| 3.4 | The recording is fetched, stored in P-08, and access-controlled | Storage and ACL test | Not tested |
| 3.5 | Voice OTP is read correctly and expires per policy | Functional test | Not tested |
| 3.6 | A DND or regulatory block surfaces as a non-retryable failure, and an origination timeout results in a status read rather than a blind retry | Failure-injection and timeout test | Not tested |
| 3.7 | An unanswered call escalates to SMS after the retry ceiling | Ladder test | Not tested |
| 3.8 | The placeholder toll-free number is never dialled in test runs, and cost attribution per sub-account reconciles | Configuration scan and cost report test | Not tested |

### 6.9 Open items and dependencies

| ID | Item | Blocking | Status |
|---|---|---|---|
| OD-INT-01 | Select the Indian cloud-telephony provider on voice and IVR capability, DND and TRAI compliance handling, recording availability, sub-accounting, and per-minute pricing | Procurement | `[OPEN]` |
| OD-TEL-01 | Procure and verify the real toll-free number to replace `1800-XXX-XXXX` | Procurement | `[OPEN]` |
| OD-TEL-02 | Confirm whether a dedicated transactional or non-telemarketing caller ID is required | Legal and provider | `[DEPENDENT]` |
| OD-TEL-03 | Authorise the IVR script set, language coverage and escalation rules | Product | `[OPEN]` |
| OD-TEL-04 | Confirm recording retention and consent requirements under applicable law | Legal | `[DEPENDENT]` |
| OD-TEL-05 | Decide whether transcription is ever enabled; it is off by default | Legal and cost | `[OPEN]` |
| OD-TEL-06 | Define the voice-OTP attempt cap, validity window and lockout behaviour | Security | `[OPEN]` |
| OD-TEL-07 | Confirm sub-account availability for partner-branch cost attribution | Provider | `[DEPENDENT]` |

## §7 WhatsApp Business Platform

### 7.1 Purpose and business use cases

`[CONFIRMED]` WhatsApp is a candidate customer-facing service channel for transactional messaging. Whether AmmPal uses the official WhatsApp Business Platform directly or through a Business Solution Provider is an open decision (OD-INT-02).

| Use case | Business rule | Status |
|---|---|---|
| U-4.1 Booking confirmation | Sent after the booking is accepted | `[PROPOSED]` |
| U-4.2 Technician assignment and arrival updates | Driven by booking statuses `EN_ROUTE(3)` and `STARTED(4)` | `[PROPOSED]` |
| U-4.3 Reschedule and cancellation notice | Driven by `RESCHEDULED(12)`, `CANCELLED_BY_CUSTOMER(7)` and `CANCELLED_BY_TECHNICIAN(8)` | `[PROPOSED]` |
| U-4.4 Invoice, receipt and weekly partner statement delivery | With a document link into P-08, matching the settlement cycle | `[PROPOSED]` |
| U-4.5 Customer-initiated inbound message, and a reminder for an upcoming visit | Opt-in service window routed to `support`; the reminder uses a template that must be pre-approved by the platform | `[PROPOSED]` / `[DEPENDENT]` |
| U-4.6 OTP delivery | Only if WhatsApp is the chosen OTP channel, since SMS is the default | `[OPEN]` |

`[CONFIRMED]` No WhatsApp template is submitted, approved or in use. `[PROPOSED]` AmmPal maintains a template registry mapping internal message keys to platform template names and languages, and a template must be pre-approved by the platform before it carries production traffic.

### 7.2 Data exchanged

| Direction | Data | PII class | Retention |
|---|---|---|---|
| Outbound | Template name and language, recipient number, substitution parameters (booking ref, technician first name, window, amount) | Direct PII (number) plus indirect (booking data) | AmmPal retains the message envelope and status — `[PROPOSED]` 12 months; provider-side retention per policy |
| Outbound | Media or document link (invoice PDF, receipt); session message text within an approved service window | Indirect PII; direct PII for text | `[PROPOSED]` The link is short-lived and signed and the artefact lives in P-08; message text 12 months |
| Inbound | Inbound message body, media, profile identifier, timestamp | Direct PII | `[PROPOSED]` Stored on the `support` ticket; 12 months |
| Inbound | Message status: sent, delivered, read, failed with reason | Indirect PII | `[PROPOSED]` 12 months |
| Inbound | Template status and quality rating from the platform | None | `[PROPOSED]` Indefinite operational metadata |

`[CONFIRMED]` Payment card data, live OTPs and government identifiers **must never** appear in a WhatsApp message body. `[PROPOSED]` Financial artefacts are sent as a link to a short-lived, single-purpose, authenticated AmmPal URL — never a public object-storage URL. `[OPEN]` Retention of message content in the provider's own cloud is governed by platform or BSP terms not yet under an executed agreement.

### 7.3 Authentication and authorisation

| Item | Contract | Status |
|---|---|---|
| Authentication method | Provider-issued business account credentials: a permanent access token obtained through a business-setup flow | `[PROPOSED]` |
| Token lifecycle | Treated as a long-lived secret with an explicit rotation procedure and a replacement overlap window | `[PROPOSED]` |
| Phone number registration | The sending number must be registered and verified with the platform; the number is a deployment secret | `[DEPENDENT]` |
| Webhook verification | Provider-issued app secret; HMAC over the raw body, constant-time comparison, 5-minute window | `[PROPOSED]` |
| Inbound authenticity | A verification token is sent once to the app endpoint and stored; later callbacks are accepted only from the verified app | `[PROPOSED]` |
| Least privilege and storage | Token scoped to message sending only with no management scopes at runtime; secrets-manager entries by alias only, never in a repository or this document | `[PROPOSED]` / `[CONFIRMED]` |
| Service window | AmmPal sends free-form content only inside an approved customer-service window | `[PROPOSED]` |

`[DEPENDENT]` If a BSP is chosen instead of a direct platform relationship, the authentication model, webhook signature scheme and failure semantics all change. §13 `MessagingPort` is the abstraction that isolates the difference: the concrete adapter changes, the caller does not.

### 7.4 API surface AmmPal depends on

`[PROPOSED]` Path-style references against `PROVIDER_HOST`. Path shapes differ between a direct platform relationship and a BSP, and the adapter normalises them.

| Operation | Path style | Use | Notes |
|---|---|---|---|
| Send template message | `POST /messages` | U-4.1 … U-4.4 | Uses a pre-approved template |
| Send service-window message | `POST /messages` | U-4.5 | Only inside the approved window |
| Send media or document | `POST /messages` with a media reference | U-4.4 | Media uploaded to the provider media store or linked |
| Get message status | `GET /messages/{message_id}` | Reconciliation | Polled only when the status webhook is missing |
| Mark inbound message read, and download inbound media | `POST /messages/{message_id}/read`, `GET /media/{media_id}` | U-4.5 | Optional; inbound media is copied to P-08 and the provider reference released |
| List templates and register a template | `GET /message_templates`, `POST /message_templates` | Template registry sync | The daily sync job lists templates; registration is operated by a product owner, never at runtime |

### 7.5 Webhook/event contract

`[PROPOSED]` Inbound message and status events are delivered to a single webhook route.

| Event name | Payload fields | Delivery guarantee | Signature scheme | Idempotency key | Duplicate handling | Retry policy AmmPal implements |
|---|---|---|---|---|---|---|
| `message.received` | event id, message id, from number mask, type, body or media id, timestamp, context | At-least-once | HMAC over the raw body plus a timestamp, using the app secret | `provider_event_id` | Dedupe on `(provider, provider_event_id)`; a repeat from the same customer in a short window is additionally collapsed by content hash so no duplicate ticket is raised | Provider retries on non-2xx; AmmPal returns 2xx after the persist |
| `message.sent`, `message.delivered`, `message.read` | event id, message id, number mask, timestamp | At-least-once | as above | `provider_event_id` | as above | as above |
| `message.failed` | event id, message id, reason code, provider text, timestamp | At-least-once | as above | `provider_event_id` | as above | as above |
| `message.template.status` and `account.quality.update` | event id, template name, status, reason, quality rating, restrictions | At-least-once | as above | `provider_event_id` | as above | as above |

`[PROPOSED]` Outbound idempotency: AmmPal generates a `client_message_id` per send attempt and stores it with the request, so a retry reuses the same id and the provider does not deliver twice. `[PROPOSED]` Template enforcement: the `notification` module rejects any send whose template key is absent from the approved registry and fails with a template-not-approved error rather than sending free text. `[PROPOSED]` Number normalisation: recipients are normalised to E.164 before sending, and a number that fails normalisation is a hard failure routed to the operator task queue.

### 7.6 Failure modes and AmmPal's handling

| Failure | Detection | AmmPal behaviour | Fallback | Alert |
|---|---|---|---|---|
| Message failed (invalid number) | `message.failed` reason code | Mark the recipient unreachable; suppress further sends for that booking | Escalate to an operator task | P4 |
| Message failed (template not approved) | `message.failed` reason code | Hard failure; quarantine the template key; retry only after approval | None — never substitute free text | P1 |
| Message failed (quality restriction or account limit) | `message.failed` plus `account.quality.update` | Stop all WhatsApp sends for the affected entity; move the channel ladder to SMS | SMS (P-05), then email (P-06) | P1 |
| Message failed (throttle or policy block) | The reason code indicates throttling | Back off, queue, and retry inside the provider's window | Queue; SMS if the wait exceeds the business deadline | P3 |
| Callback signature invalid, or a duplicate inbound message | HMAC comparison fails; dedupe on event id plus content hash | Reject 4xx; the second instance of a duplicate is a no-op with no duplicate ticket | None | P1 if sustained / P4 |
| Unsupported inbound message type, or media download failure | Payload inspection; download error | Store as an unsupported-attachment ticket with the raw reference; bounded retry on the media | The ticket shows the reference | P4 / P3 |
| Provider outage (send) | 5xx or an open circuit | The channel ladder advances to SMS | SMS, then email | P2 |
| Provider outage (callback) | Missing events | Reconciliation poll of sent messages with pending status | Periodic poll job | P2 |
| Template registry drift | Daily sync diff against the platform | Fail closed for a drifted template | SMS | P2 |
| Inbound message containing prompt-injection-like content | Content heuristics plus operator review | The message is stored and **never** interpreted as an instruction to any AmmPal component; the ticket is flagged for human review | Human review | P2 |
| No delivery receipt for a critical message | No status within the SLA | Treat as undelivered and escalate to the next channel | SMS | P3 |

### 7.7 Degradation and fallback path

`[PROPOSED]` Channel ladder for a customer-facing message: **0 — WhatsApp primary** (a WhatsApp template message is sent); **1 — WhatsApp pending** (the send is queued, and if it is not sent within the message's business deadline the ladder advances); **2 — SMS** (the same content is sent via SMS using the registered sender ID and DLT template); **3 — Email** (email to the registered address, with a link back to the in-app message centre); **4 — In-app only** (the message is written to the in-app inbox and read on the next app open); **5 — Operator task** (a `support` task is created for a human call).

`[PROPOSED]` The ladder is per-message, not global: one failing template does not degrade all channels, while a global provider outage raises the ladder's starting point for all messages until provider health recovers. `[PROPOSED]` Every message records the intended channel, actual channel, ladder level and degradation reason — the basis of message-delivery reporting in `reporting`.

### 7.8 Conformance checklist

| # | Check | Method | Result |
|---|---|---|---|
| 4.1 | A pre-approved template sends successfully and produces `message.sent`, and an unapproved template is rejected by AmmPal before the provider is called | Sandbox send and registry-guard unit test | Not tested |
| 4.2 | Substitution parameters render correctly for all supported languages | Snapshot test | Not tested |
| 4.3 | Callback signature verification rejects a tampered body, and a duplicate inbound event does not create a duplicate ticket | Negative and duplicate-delivery test | Not tested |
| 4.4 | `client_message_id` prevents double delivery on retry, and number normalisation rejects an invalid recipient | Retry and unit test | Not tested |
| 4.5 | A quality restriction triggers the ladder move to SMS | Failure-injection drill | Not tested |
| 4.6 | A missing delivery receipt escalates to the next channel within the deadline | Timer test | Not tested |
| 4.7 | Template registry sync detects drift and fails closed | Drift test | Not tested |
| 4.8 | Document links are short-lived, signed and single-purpose, and inbound media is copied to P-08 with the provider reference released | Security and storage test | Not tested |

### 7.9 Open items and dependencies

| ID | Item | Blocking | Status |
|---|---|---|---|
| OD-INT-02 | Decide between a direct official WhatsApp Business Platform relationship and a BSP; it drives cost, template control and the adapter shape | Procurement | `[OPEN]` |
| OD-WA-01 | Confirm the sending number type (toll-free or dedicated) and link it to the telephony provider | Procurement | `[DEPENDENT]` |
| OD-WA-02 | Author the template set for every message key and language, then submit for platform approval | Product and legal | `[OPEN]` |
| OD-WA-03 | Confirm the customer-service window definition and the rules for free-form replies | Legal and product | `[OPEN]` |
| OD-WA-04 | Define the opt-in and opt-out mechanism for WhatsApp conversations | Legal | `[OPEN]` |
| OD-WA-05 | Confirm whether inbound message handling requires a human-in-the-loop agent console in the Control Center | Product | `[OPEN]` |
| OD-WA-06 | Confirm the per-conversation pricing model and how it is billed | Provider | `[DEPENDENT]` |
| OD-WA-07 | Decide whether WhatsApp is used for OTP; the default is no | Security | `[OPEN]` |

## §8 SMS Provider

### 8.1 Purpose and business use cases

`[CONFIRMED]` An Indian SMS provider is required for transactional messaging and OTP delivery. DLT registration and a registered sender ID are statutory prerequisites.

| Use case | Business rule | Status |
|---|---|---|
| U-5.1 Customer OTP for authentication and booking verification | Attempt-capped, time-boxed, single-use | `[PROPOSED]` |
| U-5.2 Booking status notification, and technician assignment notification | Transactional, driven by booking statuses | `[PROPOSED]` |
| U-5.3 Invoice availability notice and link, and payment reminder with link | An authenticated link, not full financial content | `[PROPOSED]` |
| U-5.4 Support ticket updates, and partner and branch operational alerts | Transactional | `[PROPOSED]` |
| U-5.5 DLT template-based content | All commercial templates registered on DLT with approved content | `[DEPENDENT]` |

`[CONFIRMED]` Indian DLT registration, sender-ID registration and route-specific commercial templates are statutory requirements for business SMS in India; AmmPal cannot send a business SMS without them.

### 8.2 Data exchanged

| Direction | Data | PII class | Retention |
|---|---|---|---|
| Outbound | Recipient MSISDN, sender ID, message body, DLT template id, unicode flag, entity reference | Direct PII (phone) | AmmPal retains the message envelope and delivery status — `[PROPOSED]` 12 months; provider-side retention per policy |
| Outbound | OTP content | Direct PII plus secret | `[PROPOSED]` The OTP value is never persisted — only a salted hash, expiry, attempt counter and consumed flag; the body is not archived |
| Inbound | Delivery receipt: message id, MSISDN mask, status, error code, timestamp | Indirect PII | `[PROPOSED]` 12 months |
| Inbound | Inbound SMS reply from a customer, and DLT and sender registration status | Direct PII; none | `[PROPOSED]` Replies route to `support` and are kept 12 months; registration status is kept indefinitely |

`[PROPOSED]` Message bodies containing an OTP are never written to application logs; the log records the message id, template key and outcome only.

### 8.3 Authentication and authorisation

| Item | Contract | Status |
|---|---|---|
| Authentication method | Provider-issued API credentials presented per request (header or query parameter) | `[PROPOSED]` |
| DLT account linkage | The provider account must be linked to an approved DLT entity before traffic is accepted | `[DEPENDENT]` |
| Sender ID ownership | Sender IDs must be owned by the AmmPal legal entity | `[DEPENDENT]` |
| Callback authentication | HMAC over the raw body plus a timestamp, constant-time comparison | `[PROPOSED]` |
| Source restriction | Provider IP ranges allow-listed at the edge in addition to signature verification | `[PROPOSED]` |
| Least privilege and storage | Credentials scoped to sending and delivery-receipt subscription only; secrets-manager entries by alias only; provider test routes and sandbox numbers for all pre-production verification, with no real recipient numbers in test | `[PROPOSED]` / `[CONFIRMED]` |

### 8.4 API surface AmmPal depends on

`[PROPOSED]` Path-style references against `PROVIDER_HOST`.

| Operation | Path style | Use | Notes |
|---|---|---|---|
| Send SMS | `POST /v2/sms` | U-5.1 … U-5.5 | A content id / DLT template id is required |
| Send bulk SMS | `POST /v2/sms/bulk` | U-5.4 | Partitioned; per-message status retained |
| Query message status | `GET /v2/sms/{message_id}` | Reconciliation | Fallback for missing receipts |
| Delivery receipt callback, and inbound SMS webhook | `POST /{app}/dlr`, `POST /{app}/inbound` (provider → AmmPal) | U-5.x | Both signed |
| Registration status and health query | `GET /v2/registrations`, `GET /v2/health` | Startup validation and the health panel | Registration status is a readiness check; health is not a business call |

`[PROPOSED]` Every commercial message carries an explicit DLT content-template reference; a message with no registered template is rejected by AmmPal before it reaches the provider, mirroring the WhatsApp template guard.

### 8.5 Webhook/event contract

| Event name | Payload fields | Delivery guarantee | Signature scheme | Idempotency key | Duplicate handling | Retry policy AmmPal implements |
|---|---|---|---|---|---|---|
| `sms.delivered` | event id, message id, MSISDN mask, status, timestamp | At-least-once | HMAC over the raw body plus a timestamp | `provider_event_id` | Dedupe on `(provider, provider_event_id)` | Provider retries on non-2xx; AmmPal returns 2xx after the persist |
| `sms.failed` | event id, message id, error code, error text, timestamp | At-least-once | as above | `provider_event_id` | as above | as above |
| `sms.queued` | event id, message id, route, timestamp | At-least-once | as above | `provider_event_id` | as above | as above |
| `sms.inbound` | event id, message id, from MSISDN mask, body, timestamp | At-least-once | as above | `provider_event_id` | as above | as above |
| `sms.template.rejected` | event id, content id, reason | At-least-once | as above | `provider_event_id` | as above | as above |
| `sms.balance.low` | event id, account balance, threshold | At-least-once | as above | `provider_event_id` | as above | as above |

`[PROPOSED]` Outbound idempotency: AmmPal generates a `client_message_id` per logical send, and AmmPal's own id is authoritative for dedupe. `[PROPOSED]` Inbound replies correlate to the most recent outbound message to the same MSISDN within a defined window, and an unmatched reply opens a generic enquiry ticket. `[PROPOSED]` `sms.balance.low` triggers an internal alert to `ACCOUNTANT` and is never surfaced to customers.

### 8.6 Failure modes and AmmPal's handling

| Failure | Detection | AmmPal behaviour | Fallback | Alert |
|---|---|---|---|---|
| Callback signature invalid | HMAC comparison fails | Reject 4xx | None | P1 if sustained |
| Send rejected (invalid number, DND) | Response error code | Record as undeliverable; suppress further sends to that number | Voice OTP (P-03) or an operator task | P4 |
| Send rejected (template not registered) | Response error code | Hard failure; quarantine the content template | None — never substitute unregistered content | P1 |
| Send timeout (unknown outcome) | Client timeout | Query `GET /v2/sms/{message_id}` before retrying | Escalate to voice OTP | P3 |
| Route congestion, or provider outage | Error code or failure-rate spike; 5xx or an open circuit | Back off, queue, and re-route if the provider exposes an alternate route; the channel ladder advances to WhatsApp or voice | Queue, then voice OTP, then in-app | P3 / P2 |
| Account balance exhausted | Send error or `sms.balance.low` | Stop sends; notify `ACCOUNTANT`; resend pending messages after the top-up | Queue | P1 |
| Delivery receipt missing | No receipt within the SLA | Treat as undelivered and escalate the ladder | WhatsApp (P-04) | P3 |
| DLT registration rejected or lapsed | Startup validation or send error | Fail closed for commercial templates | No commercial SMS until re-registered | P1 |
| Provider schema drift | Nightly contract test | Quarantine the adapter; keep the last known good mapping | Reconciliation pull | P1 |
| Inbound reply that cannot be correlated | No matching outbound context | Generic enquiry ticket; no automatic state change | Operator | P4 |

### 8.7 Degradation and fallback path

`[PROPOSED]` Channel ladder for SMS-dependent flows: **0 — SMS primary** (the SMS is sent and confirmed); **1 — SMS queued** (the send is accepted but unconfirmed, so proceed only for non-blocking notifications); **2 — Voice** (the telephony provider is used for OTP and time-critical notices); **3 — WhatsApp** (the message is sent through WhatsApp where an approved template exists); **4 — In-app** (the message is written to the in-app notification centre); **5 — Operator task** (a `support` task is raised for human contact).

`[PROPOSED]` For OTP specifically the ladder is SMS, then voice OTP, then an in-app challenge for a customer already authenticated in a prior session subject to a step-up policy, then operator-assisted verification. `[PROPOSED]` Every ladder move is recorded as an authentication event in the `audit` module.

### 8.8 Conformance checklist

| # | Check | Method | Result |
|---|---|---|---|
| 8.1 | A test SMS is accepted and a delivery receipt is received | Sandbox send | Not tested |
| 8.2 | A tampered receipt body is rejected, and a duplicate receipt does not double-update delivery state | Negative and duplicate-delivery test | Not tested |
| 8.3 | An unregistered content template is rejected by AmmPal before send | Registry-guard test | Not tested |
| 8.4 | The OTP is stored only as a hash with expiry and an attempt cap, and the OTP body never appears in logs | Storage inspection and log-scanning CI check | Not tested |
| 8.5 | An invalid MSISDN is rejected before dispatch | Validation test | Not tested |
| 8.6 | A send timeout results in a status query, not a blind retry | Timeout test | Not tested |
| 8.7 | Balance exhaustion stops sends and alerts the accountant | Failure-injection test | Not tested |
| 8.8 | A missing receipt escalates to the next channel within the deadline | Timer test | Not tested |
| 8.9 | An inbound reply correlates to the correct outbound message | Correlation test | Not tested |
| 8.10 | DLT registration is validated at startup and fails closed | Readiness test | Not tested |

### 8.9 Open items and dependencies

| ID | Item | Blocking | Status |
|---|---|---|---|
| OD-INT-03 | Decide whether a second SMS provider is contracted for redundancy; a single-vendor SMS dependency is an availability risk on a single-VPS deployment | Procurement and risk | `[OPEN]` |
| OD-SMS-01 | Complete entity-level DLT registration, sender-ID registration and content-template registration | Legal and provider | `[DEPENDENT]` |
| OD-SMS-02 | Select the provider on route coverage, DLT integration depth, delivery-report quality and per-message pricing | Procurement | `[OPEN]` |
| OD-SMS-03 | Define the OTP policy: length, validity, attempt cap, lockout and fallback trigger | Security | `[OPEN]` |
| OD-SMS-04 | Decide the handling of international numbers, if any, and the suppression list for DND categories | Legal | `[OPEN]` |
| OD-SMS-05 | Establish the daily and transactional volume split to size the messaging budget | Business | `[OPEN]` |
| OD-SMS-06 | Confirm the provider supports the required Unicode and regional-script rendering, including Indic scripts | Provider | `[DEPENDENT]` |

## §9 Transactional Email

### 9.1 Purpose and business use cases

| Use case | Business rule | Status |
|---|---|---|
| U-6.1 Customer invoice and receipt | The AmmPal reference `INV-YYYYMMDD-XXXXXX` always appears in the body | `[PROPOSED]` |
| U-6.2 Weekly partner commission statement, and weekly settlement advice | References `CINV-YYYY-W<WW>-<BRANCH>-<NNNN>` and `STL-YYYY-W<WW>-<BRANCH>-<NNNN>` | `[PROPOSED]` |
| U-6.3 Booking confirmation and status digest | Text-first with a link back to the app | `[PROPOSED]` |
| U-6.4 KYC status communication to partners | Status only, with a portal link; no document attached | `[PROPOSED]` |
| U-6.5 System and policy notices to staff and operators | Internal, low sensitivity | `[PROPOSED]` |
| U-6.6 Password reset and account action links, and data-export delivery for audit, support and reporting | Single-use and time-boxed links; exports use a secure, time-limited link into P-08 | `[PROPOSED]` |

### 9.2 Data exchanged

| Direction | Data | PII class | Retention |
|---|---|---|---|
| Outbound | Recipient address, display name, subject, body, headers | Direct PII (email) | AmmPal retains the message envelope and status — `[PROPOSED]` 12 months; provider-side retention per policy |
| Outbound | Attachment bytes or a signed link to an artefact in P-08 | Contains financial or personal data | `[PROPOSED]` The artefact follows its own schedule; the link is short-lived |
| Inbound | Delivery, bounce, complaint, and (if tracked) open events | Indirect PII | `[PROPOSED]` 12 months |
| Inbound | Spam-complaint feedback | Indirect PII | `[PROPOSED]` 12 months; drives suppression |

`[CONFIRMED]` Government identifiers, KYC document images and full card data **must never** be sent as email attachments**;** KYC is handled through an authenticated portal link only. `[OPEN]` Whether *any* attachment is permitted remains a live question (OD-INT-05).

### 9.3 Authentication and authorisation

| Item | Contract | Status |
|---|---|---|
| Authentication method | Provider-issued API key presented per request | `[PROPOSED]` |
| Domain authentication | SPF, DKIM and DMARC configured for the sending domain before production sending | `[DEPENDENT]` |
| Webhook authentication | HMAC over the raw body plus a timestamp, constant-time comparison | `[PROPOSED]` |
| Source restriction | Provider IP ranges allow-listed at the edge | `[PROPOSED]` |
| Sender identity | The sending domain must be owned by the AmmPal legal entity | `[DEPENDENT]` |
| Least privilege and storage | Key scoped to sending and event subscription only; secrets-manager entries by alias only | `[PROPOSED]` / `[CONFIRMED]` |
| Bounce and complaint handling | A permanent-failure list is maintained in AmmPal and mirrored to the provider; suppressed addresses are excluded from later sends | `[PROPOSED]` |

### 9.4 API surface AmmPal depends on

`[PROPOSED]` Path-style references against `PROVIDER_HOST`.

| Operation | Path style | Use | Notes |
|---|---|---|---|
| Send transactional email | `POST /v3/mail/send` | U-6.1 … U-6.6 | One recipient per request so the suppression list stays per-address |
| Send bulk email | `POST /v3/mail/batch` | U-6.5 | Per-recipient status retained |
| Get send status | `GET /v3/mail/{message_id}` | Reconciliation | Fallback for missing events |
| Event subscription | `POST /v3/webhooks` | U-6.x | Configured at setup, never at runtime |
| Domain verification status | `GET /v3/domains/{domain}/verify` | Readiness check | Startup readiness probe |
| Suppression list management | `GET/DELETE /v3/suppressions` | U-6.x | AmmPal's own list is the source of truth and is mirrored |

`[PROPOSED]` AmmPal never sends a bulk message with recipients visible to each other, except where a per-recipient copy is required for personalisation.

### 9.5 Webhook/event contract

| Event name | Payload fields | Delivery guarantee | Signature scheme | Idempotency key | Duplicate handling | Retry policy AmmPal implements |
|---|---|---|---|---|---|---|
| `email.sent` and `email.delivered` | event id, message id, recipient mask, timestamp | At-least-once | HMAC over the raw body plus a timestamp | `provider_event_id` | Dedupe on `(provider, provider_event_id)` | Provider retries on non-2xx; AmmPal returns 2xx after the persist |
| `email.bounced` | event id, message id, recipient mask, bounce type, timestamp | At-least-once | as above | `provider_event_id` | as above | as above |
| `email.complained` | event id, message id, recipient mask, complaint category | At-least-once | as above | `provider_event_id` | as above | as above |
| `email.opened` | event id, message id, recipient mask, timestamp, if tracking is enabled | At-least-once | as above | `provider_event_id` | as above | as above |
| `email.deferred` and `email.suppressed` | event id, message id, reason, retry count or suppression reason | At-least-once | as above | `provider_event_id` | as above | as above |

`[PROPOSED]` Open tracking is **disabled by default** because artefact content can include financial information, and `[OPEN]` whether it is enabled for non-sensitive categories is a business decision. `[PROPOSED]` A permanent `email.bounced` adds the address to AmmPal's suppression list, skips later sends, and records the reason on the customer record. `[PROPOSED]` `email.complained` adds a global suppression and raises a P2 alert.

### 9.6 Failure modes and AmmPal's handling

| Failure | Detection | AmmPal behaviour | Fallback | Alert |
|---|---|---|---|---|
| Callback signature invalid | HMAC comparison fails | Reject 4xx | None | P1 if sustained |
| Send rejected (invalid address) | Response error code | Record undeliverable; update the customer contact record | WhatsApp (P-04) or SMS (P-05) using the contact phone | P4 |
| Send rejected (domain not verified) | Response error code | Fail closed for all email | WhatsApp and SMS | P1 |
| Attachment too large, or attachment type rejected | Response error code | Switch to a signed link into P-08 and set a text notice | Link | P3 |
| Hard bounce | `email.bounced` | Suppress the address; mark the customer contact unverified | Channel ladder to WhatsApp or SMS | P4 |
| Spam complaint | `email.complained` | Global suppression and alert | Channel ladder | P2 |
| Transient deferral | `email.deferred` | Queue and retry inside the provider's window | Queue | P3 |
| Provider outage (send) | 5xx or an open circuit | The channel ladder advances to WhatsApp or SMS | WhatsApp, then SMS | P2 |
| Provider outage (callback) | Missing events | Reconciliation pull of sent messages with pending state | Poll job | P2 |
| No delivery event for a financial document | No event within the SLA | Treat as undelivered; expose the artefact in the app and via P-08 | In-app and operator | P3 |
| Rate limit | 429 with a retry-after hint | Honour `Retry-After`; queue | Queue | P3 |
| Accidental content disclosure to a wrong recipient | Incident process | Immediate suppression, notification to the privacy owner, breach assessment | n/a | P1 and incident |

### 9.7 Degradation and fallback path

`[PROPOSED]` Channel ladder for email-dependent notifications: **0 — Email primary** (the email is sent and confirmed); **1 — Email queued** (accepted but unconfirmed, and for financial documents the artefact is also published to the in-app message centre immediately); **2 — In-app first** (the artefact and its reference are published in-app while email is still attempted); **3 — WhatsApp or SMS** (the customer is notified through WhatsApp or SMS with a link to the app); **4 — Operator task** (a `support` task is raised to deliver the document manually).

`[PROPOSED]` For partner financial documents (statement, settlement) AmmPal **always** publishes the artefact in the Partner App and in P-08 regardless of email status; email is a convenience channel, never the sole delivery path.

### 9.8 Conformance checklist

| # | Check | Method | Result |
|---|---|---|---|
| 9.1 | A test email is accepted and a delivery event is received | Sandbox send | Not tested |
| 9.2 | A tampered callback body is rejected, and a duplicate callback is a no-op | Negative and duplicate-delivery test | Not tested |
| 9.3 | A hard bounce adds the address to the suppression list, and a spam complaint adds a global suppression and raises an alert | Bounce and complaint simulation | Not tested |
| 9.4 | An attachment failure falls back to a signed link | Size and type test | Not tested |
| 9.5 | Domain verification is checked at startup and fails closed | Readiness test | Not tested |
| 9.6 | KYC documents are never sent as attachments | Content-guard test | Not tested |
| 9.7 | Open tracking is disabled for financial templates | Configuration check | Not tested |
| 9.8 | The statement artefact is available in-app even when email fails, and sending respects the suppression list | Fault-injection test and unit test | Not tested |

### 9.9 Open items and dependencies

| ID | Item | Blocking | Status |
|---|---|---|---|
| OD-INT-05 | Decide whether attachments are permitted at all; a signed-link-only model is simpler and safer | Security and product | `[OPEN]` |
| OD-MAIL-01 | Select the provider on deliverability to Indian inboxes, transactional throughput, bounce and feedback API quality, and price | Procurement | `[OPEN]` |
| OD-MAIL-02 | Register and verify the sending domain; configure SPF, DKIM and DMARC | DNS and provider | `[DEPENDENT]` |
| OD-MAIL-03 | Confirm the provider throughput limit against projected weekly statement volume | Provider | `[DEPENDENT]` |
| OD-MAIL-04 | Decide the unsubscribe policy for non-transactional categories, if any | Legal | `[OPEN]` |
| OD-MAIL-05 | Confirm whether email is used for customer authentication at all, or whether the OIDC provider (P-09) covers it | Architecture | `[OPEN]` |

## §10 Firebase Cloud Messaging

### 10.1 Purpose and business use cases

| Use case | Business rule | Status |
|---|---|---|
| U-7.1 Push a booking status change to the customer app | Token-based; message content minimal and non-sensitive | `[PROPOSED]` |
| U-7.2 Notify the Partner App of an assignment | Token-based per technician device | `[PROPOSED]` |
| U-7.3 Notify the Control Center web clients | FCM web push, if adopted | `[OPEN]` |
| U-7.4 Silent or background push to refresh cached state | Data-only message; the app fetches state from the API | `[PROPOSED]` |
| U-7.5 Device token lifecycle management, and topic subscription for broadcast service alerts | Tokens registered, refreshed and invalidated on uninstall; opt-in topics only | `[PROPOSED]` |

`[PROPOSED]` Push is **never** the transport for a financially or legally significant message; the source of truth for a message is the in-app notification centre in the `notification` module.

### 10.2 Data exchanged

| Direction | Data | PII class | Retention |
|---|---|---|---|
| Outbound | Device registration token, title and short body, data payload of references only | Indirect PII (device) | `[PROPOSED]` Token records retained until invalidated, then pruned after 180 days of inactivity |
| Outbound | Notification name, collapse key, TTL, priority | None | n/a |
| Inbound | Delivery metrics: accepted, delivered, opened or clicked, dropped with reason | Indirect PII | `[PROPOSED]` 90 days |
| Inbound | Invalid or expired token signal | Indirect PII | `[PROPOSED]` The token is invalidated immediately and the record is kept 90 days |
| Inbound | Device and OS metadata, app version | Indirect PII | `[PROPOSED]` 180 days |

`[CONFIRMED]` No document, credential, OTP or full customer contact record may appear in a push payload. `[PROPOSED]` Payloads carry identifiers only and the app resolves content through the authenticated API.

### 10.3 Authentication and authorisation

| Item | Contract | Status |
|---|---|---|
| Authentication method | Service-account credentials with the narrowest role that can send to the project | `[PROPOSED]` |
| Token handling | The service-account private key is a long-lived secret; the adapter exchanges it internally for a short-lived access token | `[PROPOSED]` |
| Least privilege | The service account cannot read user data, only send | `[PROPOSED]` |
| Event authentication | Delivery metrics are read through the metrics API, not pushed; if a push-notification extension is adopted, the §14 baseline applies | `[PROPOSED]` |
| Secret storage and client registration | Secrets-manager entries by alias, with the private key never in the repository; app instances register their FCM token with AmmPal over an authenticated API | `[CONFIRMED]` / `[PROPOSED]` |
| User consent | Push is opt-in at first use; a declined permission is respected immediately and permanently | `[PROPOSED]` |

### 10.4 API surface AmmPal depends on

`[PROPOSED]` Path-style references against `PROVIDER_HOST`.

| Operation | Path style | Use | Notes |
|---|---|---|---|
| Send to device token | `POST /v1/projects/{project_id}/messages:send` | U-7.1, U-7.2 | One token per call for precise invalidation |
| Send to topic | `POST /v1/projects/{project_id}/messages:send` with a topic name | U-7.5 | Opt-in topics only |
| Batch send | `POST /v1/projects/{project_id}/messages:batchSend` | Burst traffic | Per-token results retained |
| Validate token | `POST /v1/projects/{project_id}/messages:send` with a dry run | Token hygiene | Scheduled cleanup job |
| Fetch delivery metrics | `GET /v1/projects/{project_id}/messagingMetrics` | Reporting | Not a webhook |

`[PROPOSED]` AmmPal uses **per-token sends** rather than fan-out topics for transactional notifications so an invalid token is invalidated precisely.

### 10.5 Webhook/event contract

`[PROPOSED]` FCM does not push delivery events to AmmPal in the base configuration; delivery outcomes are read through the metrics API. If a push extension or third-party wrapper is adopted, the §14 baseline applies with the mapping below.

| Event name | Payload fields | Delivery guarantee | Signature scheme | Idempotency key | Duplicate handling | Retry policy AmmPal implements |
|---|---|---|---|---|---|---|
| `push.delivered` | event id, message id, token hash, timestamp | At-least-once | HMAC over the raw body plus a timestamp | `provider_event_id` | Dedupe on `(provider, provider_event_id)` | Provider retries; AmmPal returns 2xx after the persist |
| `push.opened` | event id, message id, token hash, timestamp | At-least-once | as above | `provider_event_id` | as above | as above |
| `push.dropped` | event id, message id, reason, token hash | At-least-once | as above | `provider_event_id` | as above | as above |
| `push.invalid_token` | event id, token hash, reason | At-least-once | as above | `provider_event_id` | as above | as above |

`[PROPOSED]` Outbound idempotency: AmmPal assigns a `collapse_key` derived from the domain event so repeated sends for the same event collapse in the device tray instead of stacking notifications.

### 10.6 Failure modes and AmmPal's handling

| Failure | Detection | AmmPal behaviour | Fallback | Alert |
|---|---|---|---|---|
| Service-account credential invalid | 401 or 403 response | Fail closed; no push sent | WhatsApp or SMS ladder | P1 |
| Device token invalid or expired | 404 or an invalid-registration error | Invalidate the token; never retry to it | In-app only | P4 |
| Quota exhausted | 429 quota error | Queue and batch; reduce non-essential push | In-app only | P3 |
| Provider outage (send) | 5xx or an open circuit | No push; the message remains in the in-app centre | WhatsApp or SMS for critical messages | P2 |
| Message dropped by the platform | Metrics show a high drop ratio | Record the drop reason; escalate critical messages to the next channel | WhatsApp or SMS | P3 |
| App not installed or permission denied | The token was never registered | No push; the customer relies on other channels | WhatsApp or SMS | P4 |
| Payload exceeds size limits | 400 size error | Truncate the body, keep the identifier | In-app only | P3 |
| Schema drift in the response | Nightly contract test | Quarantine the adapter | n/a | P1 |
| One device token registered to two users | Registration conflict | Reject the registration and require re-authentication | n/a | P2 |
| Stale content shown on a locked device | Platform behaviour | All push payloads are non-sensitive; state is fetched by the app after unlock | n/a | P4 |

### 10.7 Degradation and fallback path

`[PROPOSED]` Push is a **best-effort** channel with no blocked state. At **Level 0** a push is sent only when the message class is `ENGAGEMENT` or `NUDGE`. At **Level 1** transactional-class messages are never sent by push and instead use WhatsApp or SMS per the ladder. At **Level 2** a push failure never blocks a business transaction and never triggers a retry storm: the message is still written to the in-app notification centre and is read on the next app open.

### 10.8 Conformance checklist

| # | Check | Method | Result |
|---|---|---|---|
| 10.1 | A test device receives a push notification, and an invalid token is invalidated and not retried | Sandbox device and token-hygiene test | Not tested |
| 10.2 | The payload contains identifiers only, with no financial or document content | Payload-assertion test | Not tested |
| 10.3 | The service-account credential is absent from client bundles | Secret-scanning CI check | Not tested |
| 10.4 | The collapse key prevents duplicate tray entries | Repeat-send test | Not tested |
| 10.5 | A push failure does not block the business transaction, and the in-app centre still holds the message | Fault-injection test | Not tested |
| 10.6 | A declined notification permission is respected permanently | Client contract test | Not tested |
| 10.7 | Quota exhaustion causes batching, not unbounded retries | Quota simulation | Not tested |

### 10.9 Open items and dependencies

| ID | Item | Blocking | Status |
|---|---|---|---|
| OD-FCM-01 | Confirm the messaging provider identity for FCM delivery and its interaction with Flutter platform registration (APNs, Play) | Architecture | `[OPEN]` |
| OD-FCM-02 | Define the push message taxonomy and which events are engagement-class versus transactional-class | Product | `[OPEN]` |
| OD-FCM-03 | Decide whether the Control Center uses FCM web push or an in-app plus email model | Product | `[OPEN]` |
| OD-FCM-04 | Confirm the Firebase project will sit under the AmmPal legal entity with the required agreements | Legal | `[DEPENDENT]` |
| OD-FCM-05 | Establish the free-tier or quota envelope and the alerting threshold for quota exhaustion | Cost | `[OPEN]` |

## §11 Object Storage (S3-compatible)

### 11.1 Purpose and business use cases

| Use case | Business rule | Status |
|---|---|---|
| U-8.1 Customer invoice and receipt PDFs | Retained on the financial record schedule | `[PROPOSED]` |
| U-8.2 Weekly partner commission statements and settlement files | One artefact per statement, immutable once issued | `[PROPOSED]` |
| U-8.3 KYC document images (partner business proof, technician identity) | Highest sensitivity; encrypted under a dedicated key prefix | `[PROPOSED]` |
| U-8.4 Call recordings and IVR transcripts, and job media (before and after photos, job evidence) | Access-controlled, short-lived download links; job media attached to the booking and customer-visible where policy allows | `[PROPOSED]` |
| U-8.5 Data exports for audit, support and reporting | Time-limited signed links, download-logged | `[PROPOSED]` |
| U-8.6 Application backups and database dumps, and static assets | Encrypted, separate prefix, restore-tested; assets are read-mostly | `[PROPOSED]` |

### 11.2 Data exchanged

| Direction | Data | PII class | Retention |
|---|---|---|---|
| Outbound | Object key, content type, content length, checksum, encryption flag, storage class, metadata | Classified by object content | Object lifetime is set by the owning artefact type |
| Outbound | Object bytes: invoices, statements, KYC images, recordings, media, exports | Up to **high PII** (KYC, voice) | `[PROPOSED]` Invoices and statements 8 years; KYC life of relationship plus 3 years; recordings 180 days; job media 12 months; exports 30 days |
| Inbound | Object version id, etag and checksum, storage class, creation time | None | `[PROPOSED]` Indefinite |
| Inbound | Access-denied and throttling errors | None | n/a |

`[CONFIRMED]` Object keys are namespaced by domain and never embed a customer name, phone number, email or any other PII; keys are opaque identifiers such as `invoices/{yyyy}/{mm}/{invoice_ref}.pdf`, `kyc/{partner_org_ref}/{doc_id}` and `recordings/{yyyy}/{mm}/{call_ref}.wav`. `[PROPOSED]` Every object carries metadata — the AmmPal entity reference, artefact type, retention class, generating module and creation timestamp — which is the basis of lifecycle deletion.

### 11.3 Authentication and authorisation

| Item | Contract | Status |
|---|---|---|
| Authentication method | Provider-issued access key and secret key, or a workload identity exchanging for short-lived scoped credentials | `[PROPOSED]` |
| Least privilege | Bucket policy grants write to owned artefact prefixes and read only where needed; no cross-module wildcard read | `[PROPOSED]` |
| Public access | **No** bucket, prefix or object is publicly readable | `[CONFIRMED]` |
| KYC access | A dedicated prefix with a separate key and role; the general `integration` credential cannot read it | `[PROPOSED]` |
| Download links | Pre-signed, short expiry (proposed 15 minutes for financial documents, 5 minutes for KYC), single-purpose | `[PROPOSED]` |
| Encryption | Server-side encryption on all buckets with a customer-managed key proposed for the KYC prefix; TLS required for all operations, with plaintext rejected | `[PROPOSED]` |
| Secret storage and audit | Secrets-manager entries by alias only; access logging enabled and shipped to the `audit` module sink | `[CONFIRMED]` / `[PROPOSED]` |

> **`[OPEN]` — `OD-DOC-34` `[BLOCKER]`, and this row is the mirror side of it.** The public-access row
> above says no bucket, prefix or object is publicly readable, and it is left exactly as issued. The
> owner has since asked for **Cloudinary as the primary media store**, several storage platforms
> supported, the active one chosen by a super admin in the admin dashboard — and a CDN delivery URL for
> catalogue or marketing imagery *is* a publicly readable object, however the URL is signed. Those two
> statements cannot both hold as written. `DEC-07` applies, so this document is annotated rather than
> rewritten: the annotation on the other side is `13` §5.2, whose `img-src 'self'` does not name any such
> host either. The recommendation registered in `21` splits the question **by data class** rather than
> answering it for the whole platform — the classes in §11.2 above (KYC images, call recordings, job
> media, invoices) stay under the no-public-read rule with short-lived pre-signed links, and only
> non-personal catalogue and marketing imagery could ever be an exception. Whether *any* exception exists,
> which provider holds it, and what that costs are all unanswered, and no provider's pricing has been
> read for this suite (`OD-COM-12` remains open on the IP position of generated assets). Nothing here
> changes a contract, a threshold or a control.

### 11.4 API surface AmmPal depends on

`[PROPOSED]` Path-style references against `PROVIDER_HOST`; the S3 API is path-style by definition.

| Operation | Path style | Use | Notes |
|---|---|---|---|
| Put and get object | `PUT /{bucket}/{key}`, `GET /{bucket}/{key}` | U-8.1 … U-8.6 | A checksum header is required for integrity verification; a server-side copy is preferred for re-encryption |
| Head object | `HEAD /{bucket}/{key}` | Existence and size check | Cheap reconciliation check |
| Delete object | `DELETE /{bucket}/{key}` | Retention expiry | Lifecycle policy governs residual copies |
| List objects | `GET /{bucket}?list-type=2&prefix={prefix}` | Lifecycle sweep and reconciliation | Paginated and prefix-scoped |
| Copy object | `PUT /{bucket}/{key}` with a copy source | Re-encryption and template change | Server-side copy |
| Presign URL | `GET /{bucket}/{key}?X-Amz-Signature=…` | U-8.3, U-8.5 | Short expiry; no stored client credential |
| Multipart upload | `POST /{bucket}/{key}?uploads` | Large media | Used above a size threshold |
| Bucket versioning and lifecycle | `PUT /{bucket}?versioning`, `PUT /{bucket}?lifecycle` | Immutability and retention enforcement | Versioning on financial prefixes; provider-side defence in depth |

`[PROPOSED]` AmmPal depends on no provider-specific extension beyond the S3 baseline, so the storage provider stays swappable (see §17).

### 11.5 Webhook/event contract

`[PROPOSED]` S3-compatible storage does not push webhooks in the base configuration; AmmPal owns lifecycle and does not rely on provider notifications.

| Event name | Payload fields | Delivery guarantee | Signature scheme | Idempotency key | Duplicate handling | Retry policy AmmPal implements |
|---|---|---|---|---|---|---|
| `object.created` (if event notifications are enabled) | event id, bucket, key, size, etag, version id | At-least-once | Provider-specific signature over the raw body | `provider_event_id` | Dedupe on `(provider, provider_event_id)` | Provider retries; AmmPal returns 2xx after the persist |
| `object.deleted` (if enabled) | event id, bucket, key, version id | At-least-once | as above | `provider_event_id` | as above | as above |

`[PROPOSED]` Even where event notifications are enabled, AmmPal's authoritative lifecycle is a **daily sweep job** that lists objects and enforces the retention class from AmmPal's own metadata; provider events are advisory only.

### 11.6 Failure modes and AmmPal's handling

| Failure | Detection | AmmPal behaviour | Fallback | Alert |
|---|---|---|---|---|
| Credential invalid or expired, or bucket missing or wrong region | 403 access-key error; 404 on the startup probe | Fail closed; no write; fail the readiness check and refuse to start the module | None | P1 |
| Write timeout (unknown outcome) | Client timeout | Head the key; if present with a matching checksum treat it as success, otherwise retry with the same key (a write is idempotent by key) | None needed | P3 |
| Checksum mismatch on read | Response checksum versus the stored value | Re-fetch once, then mark the artefact corrupt and regenerate if deterministic | Regenerate the artefact | P1 for financial artefacts |
| Read throttling | 503 with a retry-after hint | Back off and queue reads | Serve a cached copy for display | P3 |
| Pre-signed URL generated with too long an expiry | Policy guard | The adapter refuses and clamps to the maximum allowed expiry | None | P2 (security) |
| Cross-prefix read attempted by the wrong role | 403 AccessDenied | Log a security event and deny | None | P1 |
| Lifecycle deletion removes an artefact early | Lifecycle audit | Regenerate from source data if deterministic, otherwise flag a compliance exception | Compliance exception workflow | P1 |
| Object list fails during the sweep | 5xx | Retry the sweep; a failed sweep deletes nothing | No deletion this cycle | P3 |
| Provider outage on write | 5xx or an open circuit | Artefact generation is deferred; the business record is created with `artefact_status=PENDING` and a queued retry | Regenerate later from source data | P2 |
| Provider outage on read | 5xx | Serve the last cached copy; for KYC this blocks the flow | Block the KYC step | P2 |
| Concurrent write to the same key | The put returns a different etag | A later write wins only for explicitly mutable artefact types; issued financial artefacts are immutable and the write is rejected | None | P2 |
| Bandwidth saturation on the VPS | Host monitoring | Artefact downloads are proxied with caching; large exports are scheduled off-peak | Cache | P3 |

### 11.7 Degradation and fallback path

`[PROPOSED]`

| Level | Behaviour |
|---|---|
| 0 — Full | Read and write available; pre-signed links issued. |
| 1 — Read-only | Writes are queued; the module serves reads. |
| 2 — Cache-only | Reads are served from the local encrypted cache; no pre-signed links are issued; KYC flows are blocked. |
| 3 — Local spill | New artefacts are written to a locally encrypted volume, marked `SPILLED`, and uploaded by a background job after recovery. |
| 4 — Regenerate only | Artefacts are not persisted; each is regenerated on demand from AmmPal's own data where deterministic (invoices, statements). Non-deterministic artefacts (KYC images, recordings) are unavailable and a compliance exception is raised. |

`[PROPOSED]` Spilled objects are never treated as durable; any artefact read while spilled is flagged in the audit trail.

### 11.8 Conformance checklist

| # | Check | Method | Result |
|---|---|---|---|
| 11.1 | Put, get, head and delete round-trip against the configured endpoint, and checksums are verified on every write and read | Smoke and integrity test | Not tested |
| 11.2 | No object key embeds PII | Key-pattern scan | Not tested |
| 11.3 | The pre-signed URL expiry is clamped to the policy maximum | Policy test | Not tested |
| 11.4 | A pre-signed URL for a KYC object cannot be used to access a different key | Tampering test | Not tested |
| 11.5 | The general credential cannot read the KYC prefix | IAM policy test | Not tested |
| 11.6 | Public access is disabled on every bucket, and encryption at rest is enabled on all buckets | Provider config check | Not tested |
| 11.7 | Versioning protects issued financial artefacts from overwrite | Overwrite-attempt test | Not tested |
| 11.8 | The retention sweep deletes only artefacts past their class | Sweep test | Not tested |
| 11.9 | A write timeout is resolved by a Head check, not a blind rewrite | Timeout test | Not tested |
| 11.10 | Spill mode recovers and re-uploads artefacts after the provider returns | Recovery drill | Not tested |

### 11.9 Open items and dependencies

| ID | Item | Blocking | Status |
|---|---|---|---|
| OD-INT-06 | Select the object storage provider: region, durability, egress, data residency, and fit with the 200 GB NVMe and 16 TB bandwidth envelope | Procurement and legal | `[OPEN]` |
| OD-INT-08 | (cross-ref `05`) Define the data classification and retention matrix that this document's retention column implements | Governance | `[OPEN]` |
| OD-STOR-01 | Confirm whether a customer-managed encryption key is required for the KYC prefix, and who holds it | Security | `[OPEN]` |
| OD-STOR-02 | Decide the data residency requirement (in-country versus any) for personal and KYC data | Legal | `[OPEN]` |
| OD-STOR-03 | Confirm whether the provider offers object-lock immutability for issued statements | Provider | `[DEPENDENT]` |
| OD-STOR-04 | Define the backup and restore-test cadence for the bucket and its relationship to the database backup | Platform | `[OPEN]` |
| OD-STOR-05 | Decide the egress-reduction lever: pre-signed link caching versus an AmmPal proxy for hot artefacts | Cost and platform | `[OPEN]` |

## §12 OIDC Identity Provider

### 12.1 Purpose and business use cases

| Use case | Business rule | Status |
|---|---|---|
| U-9.1 Staff (SUPER_ADMIN, ADMIN, OPERATOR, CCO, ACCOUNTANT, PARTNER_SUPPORT, MARKETING_OPS) sign in to the Control Center | OIDC authorisation-code flow with PKCE | `[PROPOSED]` |
| U-9.2 Partner users (PARTNER_BRANCH_ADMIN, BRANCH_MANAGER, BRANCH_COORDINATOR, BRANCH_FINANCE) sign in to the Partner App and partner dashboard | Same flow, with partner-org scoping applied by AmmPal's `rbac` module | `[PROPOSED]` |
| U-9.3 Customer sign-in to the Customer App | Same flow via the system browser or native app-link | `[PROPOSED]` |
| U-9.4 Token refresh and rotation | Refresh-token rotation with reuse detection | `[PROPOSED]` |
| U-9.5 Single sign-on for internal tooling, and local credential fallback for break-glass access | SSO is optional, subject to the provider's application catalogue; break-glass requires a second factor, dual control and audit | `[OPEN]` / `[PROPOSED]` |

`[CONFIRMED]` The OIDC provider is the **authentication** authority. **Authorisation** — mapping an authenticated identity to an AmmPal role (SUPER_ADMIN, ADMIN, OPERATOR, CCO, ACCOUNTANT, PARTNER_SUPPORT, MARKETING_OPS, PARTNER_BRANCH_ADMIN, BRANCH_MANAGER, BRANCH_COORDINATOR, BRANCH_FINANCE, CUSTOMER, TECHNICIAN, TECHNICIAN_CREW) and to a partner organisation or branch scope — stays entirely inside AmmPal's `rbac` and `organization` modules.

### 12.2 Data exchanged

| Direction | Data | PII class | Retention |
|---|---|---|---|
| Outbound | Authorisation request: client id, redirect URI, scope, state, nonce, PKCE challenge | None until the user authenticates | `[PROPOSED]` Logged without the code |
| Inbound | Claims: subject, email, email_verified, phone, name, groups, tenant | Direct PII | `[PROPOSED]` Stored on the AmmPal user record for the life of the account |
| Inbound | Access, refresh and id tokens | Contains PII in claims | `[PROPOSED]` The access token is held in memory only; the refresh token is stored encrypted at rest and rotated |
| Inbound | JWKS document | Public keys only | Cached in memory with a refresh interval; stale keys are not persisted beyond the TTL |
| Inbound | Token introspection or revocation signal | Indirect PII | `[PROPOSED]` 12 months |

`[CONFIRMED]` AmmPal does **not** create accounts in the identity provider as its source of user truth: a user exists in AmmPal first, or is provisioned through a partner onboarding flow, and is linked to an identity-provider subject. `[PROPOSED]` The `identity` module stores the `sub` claim as the external link and owns all profile and role data.

### 12.3 Authentication and authorisation

| Item | Contract | Status |
|---|---|---|
| Flow | Authorisation code + PKCE for all public clients (Flutter apps, web) | `[PROPOSED]` |
| Confidential clients | A server-side client secret is used only by the Control Center backend for token exchange and refresh, if the provider supports it | `[PROPOSED]` |
| Redirect URIs | Exact-match allow-list; no wildcards | `[PROPOSED]` |
| `state` and `nonce` | Generated per request, stored server-side, verified on callback | `[PROPOSED]` |
| Token validation | Signature verified against the provider JWKS; `iss`, `aud`, `exp`, `nbf` and `azp` all validated; `nonce` checked on the id token | `[PROPOSED]` |
| JWKS caching and rotation | Cached in memory with a short TTL and refreshed on an unknown `kid`; refresh-token rotation on every refresh, with reuse of a rotated token revoking the family | `[PROPOSED]` |
| Logout and MFA | RP-initiated logout plus local session invalidation; MFA required for staff roles, with the provider's MFA capability preferred — `[OPEN]`: "staff roles" is a wider scope than `13` §5.1's "internal staff with financial or administrative permission", and neither wording covers `branch:settlement:*` holders (`OD-DOC-20`) | `[PROPOSED]` |
| Break-glass | A local credential path with TOTP and dual approval for elevation | `[PROPOSED]` |
| Secret storage | Client secrets in the secrets manager by alias; never in the repository or this document | `[CONFIRMED]` |
| Session tokens | AmmPal issues its **own** short-lived session token after the OIDC callback; provider tokens are never handed to the client | `[PROPOSED]` |

### 12.4 API surface AmmPal depends on

`[PROPOSED]` Path-style references against `PROVIDER_HOST`.

| Operation | Path style | Use | Notes |
|---|---|---|---|
| Authorisation endpoint | `GET /authorize` | U-9.1 … U-9.3 | Browser redirect; PKCE, state, nonce |
| Token endpoint | `POST /oauth/token` | Token exchange, refresh, revocation | Form-encoded per the standard |
| JWKS endpoint | `GET /.well-known/jwks.json` | Token validation | Cached in memory |
| Userinfo endpoint | `GET /userinfo` | Optional claim enrichment | Only when claims are absent from the id token |
| End-session endpoint | `GET /end-session` | Logout | RP-initiated |
| Introspection and revocation endpoints | `POST /oauth/introspect`, `POST /oauth/revoke` | Refresh-token validation, logout and session kill | Optional, provider-dependent |
| Discovery document | `GET /.well-known/openid-configuration` | Runtime discovery | Cached; AmmPal may pin the values instead |

`[PROPOSED]` AmmPal pins the exact `iss` value and never accepts a discovery-supplied issuer that differs from the configured one, so a substituted discovery document cannot redirect validation.

### 12.5 Webhook/event contract

`[PROPOSED]` The OIDC provider is not a push-event source in the configuration AmmPal uses. The relevant inbound event is the **redirect callback** carrying the authorisation code, which is a front-channel request, not a webhook. If back-channel logout or security-event push is offered, the §14 baseline applies.

| Event name | Payload fields | Delivery guarantee | Signature scheme | Idempotency key | Duplicate handling | Retry policy AmmPal implements |
|---|---|---|---|---|---|---|
| `callback.code` (front-channel) | `code`, `state`, optional `error`, optional `error_description` | Single delivery, browser-navigated | Not webhook-signed; protected by `state` plus PKCE | `state` (one-time) | A reused `state` is rejected | n/a — a user-agent retry is a new authorisation request |
| `logout.push` (if back-channel logout is enabled) | event id, `sid` or `sub`, timestamp | At-least-once | Provider-specific signed token validated against the provider JWKS | `provider_event_id` | Dedupe on `(provider, provider_event_id)` | Provider retries; AmmPal returns 2xx after the persist |
| `security.event` (if enabled) | event id, type, subject, timestamp | At-least-once | as above | `provider_event_id` | as above | as above |

`[PROPOSED]` Callback handling: the `state` value is single-use, server-stored, bound to the initiating session, and expires in 10 minutes; a callback with an unknown, expired or mismatched `state` is rejected and the session discarded; a callback carrying an `error` is recorded as a failed sign-in attempt in `audit`; the authorisation code is exchanged exactly once, and a second exchange attempt is logged as an anomaly.

### 12.6 Failure modes and AmmPal's handling

| Failure | Detection | AmmPal behaviour | Fallback | Alert |
|---|---|---|---|---|
| JWKS unavailable at startup | Fetch failure | Do not accept sessions; the readiness check fails | Local break-glass path | P1 |
| Unknown `kid` in a presented token | Signature verification fails with an unrecognised key id | Refresh JWKS once and retry validation; if still unknown, reject the token | Re-authentication | P2 |
| Token validation failure (expired, bad audience, bad issuer) | Claim validation | Reject and force re-authentication | None | P4 |
| Refresh-token reuse detection | Provider signal | Revoke the whole token family and force re-authentication for that subject | Local break-glass for elevated roles | P1 |
| Provider outage during sign-in | 5xx or a timeout on the authorisation redirect | Show an error state; never present a half-authenticated session | Local credential sign-in for staff | P2 |
| Provider outage during refresh | Refresh failure | Do not extend the session; force re-authentication | Local credential sign-in for staff | P2 |
| Clock skew on token validation | `exp` or `nbf` outside the allowed skew | Apply a bounded skew tolerance (proposed 60 seconds) and log | None | P4 |
| Unverified email claim | `email_verified` absent or false | Do not auto-link to a customer record | Manual linking by an operator | P3 |
| Subject reused across tenants | `sub` already bound to another AmmPal tenant | Reject the link and raise a security event | None | P1 |
| Callback replay (reused `code`) | The exchange returns an invalid-grant error | Reject and log the anomaly | Re-authentication | P2 |
| Group or role claim drift | The claim set differs from the last seen set | Never auto-apply role changes from the provider; re-resolve roles from AmmPal's `rbac` at the next sign-in | None | P3 |
| Break-glass account misuse | Audit alerting on the local credential path | Automatic session limit, dual approval for elevation, immediate review | None | P1 |
| Provider metadata inconsistent with AmmPal's record | Field comparison | AmmPal's own record wins for display; the provider value is not authoritative | None | P4 |

### 12.7 Degradation and fallback path

`[PROPOSED]`

| Level | Behaviour |
|---|---|
| 0 — Full | OIDC sign-in and refresh available. |
| 1 — JWKS cached | Validation continues from the cached key set, refreshed opportunistically. |
| 2 — No new sign-ins | Existing sessions continue until expiry; refresh is suspended. |
| 3 — Local credential fallback (staff only) | Designated staff roles (SUPER_ADMIN, ADMIN) sign in with a local credential plus TOTP; partner and customer sign-in is **not** available at this level. |
| 4 — Read-only operations | The Control Center runs read-only with no transactional mutations, pending identity restoration. |

`[CONFIRMED]` Role assignment is never taken from the provider at any level: AmmPal's `rbac` module remains the authority, and local fallback accounts are explicitly scoped, time-boxed and audited.

### 12.8 Conformance checklist

| # | Check | Method | Result |
|---|---|---|---|
| 12.1 | The authorisation-code + PKCE flow completes end to end | Sandbox sign-in | Not tested |
| 12.2 | A mismatched or reused `state` is rejected, and a tampered `nonce` is rejected | Negative test | Not tested |
| 12.3 | A token with a bad audience is rejected, and a token with a pinned but unexpected `iss` is rejected | Negative and issuer-pinning test | Not tested |
| 12.4 | A token signed by an unknown key triggers a JWKS refresh then rejection | Unknown-`kid` test | Not tested |
| 12.5 | Refresh-token rotation works and reuse revokes the family | Rotation and reuse test | Not tested |
| 12.6 | Redirect URIs are exact-match and a tampered redirect is rejected | Redirect test | Not tested |
| 12.7 | Provider access and refresh tokens never reach the client | Token-leak test | Not tested |
| 12.8 | Provider group claims do not change AmmPal roles | Role-isolation test | Not tested |
| 12.9 | Local break-glass sign-in requires TOTP and is audited | Break-glass drill | Not tested |
| 12.10 | Client secrets are absent from the repository | Secret-scanning CI check | Not tested |
| 12.11 | Sign-in and refresh failures during a provider outage follow the documented ladder | Failure-injection drill | Not tested |

### 12.9 Open items and dependencies

| ID | Item | Blocking | Status |
|---|---|---|---|
| OD-IDP-01 | Select the identity provider on OIDC conformance, MFA capability, regional data residency, and the ability to map to the AmmPal role model | Procurement | `[OPEN]` |
| OD-IDP-02 | Decide whether partner and customer identities live in the same provider tenant or in separate ones | Security and product | `[OPEN]` |
| OD-IDP-03 | Define the break-glass account policy: count, approvers and audit review cadence | Security | `[OPEN]` |
| OD-IDP-04 | Confirm the required session lifetime and idle timeout for each role class | Security | `[OPEN]` |
| OD-IDP-05 | Confirm whether the provider supports the provisioning AmmPal needs for the staff lifecycle, or whether AmmPal must provision manually | Architecture | `[OPEN]` |
| OD-INT-07 | The KYC vendor, if selected, needs its own identity and document verification contract and may need linking to the OIDC subject | KYC selection | `[OPEN]` |

## §13 Adapter Interface Contracts

`[CONFIRMED]` The following are **interface sketches only — implementation does not exist.** They define the seam between AmmPal's `integration` module and each provider, and they are the contract a provider swap must satisfy (see §17).

`[PROPOSED]` All adapters share a common envelope: correlation id, timeout, idempotency key, and a typed result or a typed error drawn from a common `ProviderError` taxonomy.

```typescript
// contract only — implementation does not exist
export type ProviderErrorCode =
  | 'AUTH_FAILED' | 'RATE_LIMITED' | 'TIMEOUT' | 'UNAVAILABLE'
  | 'VALIDATION_FAILED' | 'NOT_FOUND'
  | 'DOMAIN_REJECTED'   // provider understood the request and refused it (DND block, unregistered template)
  | 'SCHEMA_DRIFT' | 'UNKNOWN';

export interface ProviderError {
  readonly code: ProviderErrorCode;
  readonly provider: string;
  readonly retryable: boolean;
  readonly message: string;          // redacted, safe for logs
  readonly providerCode?: string;    // vendor-side code, mapped via a per-provider table
  readonly retryAfterMs?: number;
  readonly correlationId: string;
}

export interface ProviderResult<T> {
  readonly value: T;
  readonly providerReference: string;
  readonly rawResponseRef?: string;  // pointer to a stored payload, never inline secrets
  readonly degraded: boolean;
  readonly degradationLevel?: number;
}

export interface ProviderCallOptions {
  readonly correlationId: string;
  readonly idempotencyKey?: string;
  readonly timeoutMs: number;
  readonly attempts: number;
}
```

### 13.1 Payments

```typescript
// contract only — implementation does not exist
export interface PaymentsPort {
  createOrder(input: CreateOrderInput, opts: ProviderCallOptions): Promise<ProviderResult<PaymentOrder>>;
  capturePayment(paymentRef: string, amountPaise: number, opts: ProviderCallOptions): Promise<ProviderResult<PaymentResult>>;
  getPayment(paymentRef: string, opts: ProviderCallOptions): Promise<ProviderResult<PaymentResult | null>>;
  refundPayment(input: RefundInput, opts: ProviderCallOptions): Promise<ProviderResult<RefundResult>>;
  listRefunds(paymentRef: string, opts: ProviderCallOptions): Promise<ProviderResult<RefundResult[]>>;
  fetchSettlements(from: string, to: string, opts: ProviderCallOptions): Promise<ProviderResult<SettlementRecord[]>>;
  listDisputes(opts: ProviderCallOptions): Promise<ProviderResult<DisputeRecord[]>>;
  verifyWebhookSignature(rawBody: Buffer, headers: Record<string, string>): boolean;
}

export interface CreateOrderInput {
  readonly ammallInvoiceRef: string;      // INV-YYYYMMDD-XXXXXX
  readonly amountPaise: number;           // integer paise
  readonly currency: 'INR';
  readonly customer: { readonly name: string; readonly email: string; readonly contact: string };
  readonly description: string;
}

export interface RefundInput {
  readonly paymentRef: string;
  readonly amountPaise: number;
  readonly reason: string;
  readonly initiatedBy: string;          // AmmPal user id
}

export interface PaymentResult {
  readonly providerPaymentRef: string;
  readonly status: 'CREATED' | 'AUTHORIZED' | 'CAPTURED' | 'FAILED' | 'REFUNDED' | 'PARTIALLY_REFUNDED';
  readonly amountPaise: number;
  readonly capturedAmountPaise: number;
  readonly refundedAmountPaise: number;
  readonly method?: string;
  readonly feePaise?: number;
  readonly failureCode?: string;
}

export interface SettlementRecord {
  readonly providerSettlementRef: string;
  readonly grossPaise: number;
  readonly feePaise: number;
  readonly taxPaise: number;
  readonly netPaise: number;
  readonly periodStart: string;
  readonly periodEnd: string;
}
```

`[PROPOSED]` `PaymentResult.status` is the **adapter-normalised provider status**, not the domain
column. `09` §4.9 `payments.status` (`CREATED|PENDING|SUCCESS|FAILED|REFUNDED`) is the domain state and
is the only one any other module may read — Rule `11` IN-6. The translation happens once, in the
adapter, and is total:

| Adapter status | Domain `payments.status` | Booking effect |
|---|---|---|
| `CREATED` | `CREATED` | none |
| `AUTHORIZED` | `PENDING` | none — an authorisation is not a payment (`PAY-03`) |
| `CAPTURED` | `SUCCESS` | `advance.paid` / `payment.captured` (`23` T-02, T-19) |
| `FAILED` | `FAILED` | `advance.failed` (`23` T-03) |
| `REFUNDED` | `REFUNDED` | `refund.completed` (`23` T-24) |
| `PARTIALLY_REFUNDED` | `SUCCESS` + a partial `refunds` row | the **invoice** moves to `PARTIALLY_REFUNDED` (`09` §4.9, `23` FP-03); the payment stays captured |

A partial refund is the reason the two enums differ: the domain models one captured payment plus
refund records, while the provider reports a composite status on the payment itself. The invoice
status, not the payment status, is what carries `PARTIALLY_REFUNDED`.

### 13.2 Maps

```typescript
// contract only — implementation does not exist
export interface MapsPort {
  geocode(query: GeocodeQuery, opts: ProviderCallOptions): Promise<ProviderResult<GeocodeResult | null>>;
  reverseGeocode(point: GeoPoint, opts: ProviderCallOptions): Promise<ProviderResult<GeocodeResult | null>>;
  autocomplete(input: string, sessionToken: string, opts: ProviderCallOptions): Promise<ProviderResult<AutocompleteResult[]>>;
  distanceMatrix(origins: GeoPoint[], destinations: GeoPoint[], mode: TravelMode, opts: ProviderCallOptions): Promise<ProviderResult<MatrixRow[]>>;
  directions(origin: GeoPoint, destination: GeoPoint, mode: TravelMode, opts: ProviderCallOptions): Promise<ProviderResult<DirectionsResult | null>>;
  staticMap(spec: StaticMapSpec, opts: ProviderCallOptions): Promise<ProviderResult<StoredArtefact>>;
}

export interface GeoPoint { readonly lat: number; readonly lng: number; }

export interface GeocodeQuery {
  readonly addressLine: string;
  readonly locality?: string;
  readonly region?: string;
  readonly postalCode?: string;
  readonly country: 'IN';
}

export interface GeocodeResult {
  readonly formattedAddress: string;
  readonly locality?: string;
  readonly region?: string;
  readonly postalCode?: string;
  readonly point: GeoPoint;
  readonly placeId?: string;
  readonly confidence: 'HIGH' | 'MEDIUM' | 'LOW' | 'NONE';
  readonly components: Readonly<Record<string, string>>;
}

export interface MatrixRow {
  readonly originIndex: number;
  readonly destinationIndex: number;
  readonly distanceMeters?: number;
  readonly durationSeconds?: number;
  readonly status: 'OK' | 'ZERO_RESULTS' | 'UNRESOLVED';
}
```

### 13.3 Telephony

```typescript
// contract only — implementation does not exist
export interface TelephonyPort {
  originateCall(input: OriginateCallInput, opts: ProviderCallOptions): Promise<ProviderResult<CallHandle>>;
  hangup(callRef: string, opts: ProviderCallOptions): Promise<ProviderResult<void>>;
  getCall(callRef: string, opts: ProviderCallOptions): Promise<ProviderResult<CallStatus | null>>;
  clickToCall(input: ClickToCallInput, opts: ProviderCallOptions): Promise<ProviderResult<CallHandle>>;
  executeIvr(flowRef: string, input: IvrInput, opts: ProviderCallOptions): Promise<ProviderResult<IvrExecution>>;
  getIvrExecution(executionRef: string, opts: ProviderCallOptions): Promise<ProviderResult<IvrExecution | null>>;
  fetchRecording(callRef: string, opts: ProviderCallOptions): Promise<ProviderResult<StoredArtefact | null>>;
  verifyWebhookSignature(rawBody: Buffer, headers: Record<string, string>): boolean;
}

export interface OriginateCallInput {
  readonly correlationId: string;
  readonly toNumber: string;              // E.164
  readonly purpose: 'DISPATCH_NOTIFY' | 'ARRIVAL_NOTIFY' | 'OTP_VOICE' | 'SERVICE_OUTREACH' | 'IVR_SELF_SERVICE';
  readonly reference: string;            // booking ref or ticket ref
  readonly ivrFlowRef?: string;
  readonly maxDurationSeconds?: number;
  readonly recordCall: boolean;
}

export interface CallStatus {
  readonly providerCallRef: string;
  readonly status: 'INITIATED' | 'RINGING' | 'ANSWERED' | 'COMPLETED' | 'NO_ANSWER' | 'BUSY' | 'FAILED' | 'CANCELLED';
  readonly durationSeconds?: number;
  readonly failureCode?: string;
  readonly recordingAvailable: boolean;
}
```

### 13.4 Messaging (WhatsApp + SMS)

```typescript
// contract only — implementation does not exist
export type MessageChannel = 'WHATSAPP' | 'SMS';

export interface MessagingPort {
  send(input: OutboundMessage, opts: ProviderCallOptions): Promise<ProviderResult<MessageReceipt>>;
  sendBulk(inputs: OutboundMessage[], opts: ProviderCallOptions): Promise<ProviderResult<MessageReceipt[]>>;
  getStatus(providerMessageRef: string, opts: ProviderCallOptions): Promise<ProviderResult<MessageReceipt | null>>;
  fetchInbound(cursor: string, opts: ProviderCallOptions): Promise<ProviderResult<InboundMessage[]>>;
  listTemplates(opts: ProviderCallOptions): Promise<ProviderResult<TemplateDescriptor[]>>;
  verifyWebhookSignature(rawBody: Buffer, headers: Record<string, string>): boolean;
}

export interface OutboundMessage {
  readonly channel: MessageChannel;
  readonly recipient: string;                       // E.164 / MSISDN
  readonly templateKey: string;                    // must exist in AmmPal's approved registry
  readonly locale: string;
  readonly parameters: Readonly<Record<string, string>>;
  readonly clientMessageId: string;                // AmmPal-generated idempotency id
  readonly reference?: string;                     // booking ref / invoice ref / ticket ref
  readonly attachment?: { readonly artefactRef: string; readonly signedUrl: string; readonly mimeType: string };
  readonly priority: 'CRITICAL' | 'NORMAL' | 'LOW';
}

export interface MessageReceipt {
  readonly providerMessageRef: string;
  readonly clientMessageId: string;
  readonly channel: MessageChannel;
  readonly status: 'QUEUED' | 'SENT' | 'DELIVERED' | 'READ' | 'FAILED' | 'UNKNOWN';
  readonly failureCode?: string;
  readonly sentAt?: string;
  readonly deliveredAt?: string;
}

export interface InboundMessage {
  readonly providerEventId: string;
  readonly providerMessageRef: string;
  readonly sender: string;
  readonly body?: string;
  readonly mediaRef?: string;
  readonly receivedAt: string;
}
```

### 13.5 Push

```typescript
// contract only — implementation does not exist
export interface PushPort {
  sendToDevice(deviceToken: string, input: PushMessage, opts: ProviderCallOptions): Promise<ProviderResult<PushReceipt>>;
  sendToTopic(topic: string, input: PushMessage, opts: ProviderCallOptions): Promise<ProviderResult<PushReceipt>>;
  sendBatch(inputs: BatchPushMessage[], opts: ProviderCallOptions): Promise<ProviderResult<PushReceipt[]>>;
  invalidateToken(deviceToken: string): Promise<void>;
}

export interface PushMessage {
  readonly title: string;
  readonly body: string;                 // short, non-sensitive
  readonly data: Readonly<Record<string, string>>;  // identifiers only
  readonly collapseKey: string;
  readonly ttlSeconds: number;
  readonly priority: 'HIGH' | 'NORMAL';
}
```

### 13.6 Email

```typescript
// contract only — implementation does not exist
export interface EmailPort {
  send(input: OutboundEmail, opts: ProviderCallOptions): Promise<ProviderResult<EmailReceipt>>;
  sendBulk(inputs: OutboundEmail[], opts: ProviderCallOptions): Promise<ProviderResult<EmailReceipt[]>>;
  getStatus(providerMessageRef: string, opts: ProviderCallOptions): Promise<ProviderResult<EmailReceipt | null>>;
  isSuppressed(address: string): Promise<boolean>;
  verifyWebhookSignature(rawBody: Buffer, headers: Record<string, string>): boolean;
}

export interface OutboundEmail {
  readonly to: string;
  readonly templateKey: string;
  readonly locale: string;
  readonly subject?: string;
  readonly parameters: Readonly<Record<string, string>>;
  readonly clientMessageId: string;
  readonly reference?: string;
  readonly attachment?: { readonly artefactRef: string; readonly signedUrl: string; readonly mimeType: string };
  readonly trackOpens: boolean;   // default false; must be false for financial templates
}
```

### 13.7 Storage

```typescript
// contract only — implementation does not exist
export interface ObjectStoragePort {
  put(input: PutObjectInput, opts: ProviderCallOptions): Promise<ProviderResult<StoredArtefact>>;
  get(key: string, opts: ProviderCallOptions): Promise<ProviderResult<Buffer>>;
  head(key: string, opts: ProviderCallOptions): Promise<ProviderResult<ObjectMetadata | null>>;
  delete(key: string, opts: ProviderCallOptions): Promise<ProviderResult<void>>;
  list(prefix: string, opts: ProviderCallOptions): Promise<ProviderResult<ObjectMetadata[]>>;
  copy(fromKey: string, toKey: string, opts: ProviderCallOptions): Promise<ProviderResult<StoredArtefact>>;
  presign(input: PresignInput): Promise<ProviderResult<{ readonly url: string; readonly expiresAt: string }>>;
}

export interface PutObjectInput {
  readonly key: string;                 // opaque; must not embed PII
  readonly body: Buffer;
  readonly contentType: string;
  readonly checksumSha256: string;
  readonly metadata: Readonly<Record<string, string>>;  // entity ref, artefact type, retention class
  readonly retentionClass: 'TRANSIENT' | 'FINANCIAL' | 'KYC' | 'MEDIA' | 'BACKUP';
  readonly encrypted: boolean;
}

export interface PresignInput {
  readonly key: string;
  readonly method: 'GET' | 'PUT';
  readonly expiresInSeconds: number;    // clamped by adapter policy
}
```

### 13.8 Identity

```typescript
// contract only — implementation does not exist
export interface IdentityPort {
  buildAuthorizationUrl(input: AuthorizationRequest): Promise<ProviderResult<string>>;
  exchangeCode(input: TokenExchangeRequest): Promise<ProviderResult<IdentityTokenSet>>;
  refresh(refreshToken: string, opts: ProviderCallOptions): Promise<ProviderResult<IdentityTokenSet>>;
  validateAccessToken(accessToken: string): Promise<ProviderResult<IdentityClaims>>;
  revoke(token: string, opts: ProviderCallOptions): Promise<ProviderResult<void>>;
  jwks(): Promise<ProviderResult<JwksDocument>>;
}

export interface AuthorizationRequest {
  readonly redirectUri: string;
  readonly scopes: readonly string[];
  readonly state: string;               // one-time, server-stored
  readonly nonce: string;
  readonly codeChallenge: string;
  readonly codeChallengeMethod: 'S256';
  readonly loginHint?: string;
}

export interface IdentityTokenSet {
  readonly accessToken: string;
  readonly refreshToken?: string;
  readonly idToken: string;
  readonly expiresInSeconds: number;
  readonly refreshExpiresInSeconds?: number;
}

export interface IdentityClaims {
  readonly subject: string;
  readonly issuer: string;              // must equal the pinned issuer
  readonly audience: readonly string[];
  readonly email?: string;
  readonly emailVerified?: boolean;
  readonly phone?: string;
  readonly name?: string;
  readonly groups: readonly string[];
  readonly expiresAt: string;
  readonly issuedAt: string;
}
```

### 13.9 Cross-adapter rules

`[PROPOSED]`

| Rule | Statement |
|---|---|
| AR-1 | No adapter exposes a raw provider DTO above its port; every DTO is mapped to an AmmPal type. |
| AR-2 | No adapter returns a raw provider error string; errors map to `ProviderErrorCode` with a redacted message. |
| AR-3 | Every adapter exposes `verifyWebhookSignature` (or a platform-specific equivalent) that operates on the **raw** body. |
| AR-4 | Every adapter implements a timeout, a bounded retry with jitter, and a circuit breaker. |
| AR-5 | Every adapter is behind an interface registered in the DI container, so a replacement is a provider-only change. |
| AR-6 | Every adapter logs a structured record — provider, operation, outcome, latency, correlation id — and no secret, token, card, OTP, or full PII. |
| AR-7 | Every adapter exposes a `health()` probe that the readiness check can call without side effects. |

## §14 Webhook Security Baseline

`[CONFIRMED]` This baseline applies to **every** provider webhook, callback and inbound event route. Deviations require an ADR (see §17.3).

### 14.1 Requirements

| ID | Requirement | Status |
|---|---|---|
| WS-1 | The signature is computed over the **raw request body bytes**, before JSON parsing, decompression or charset normalisation; the bytes are captured by a raw-body mechanism and never re-serialised. | `[PROPOSED]` |
| WS-2 | The scheme is HMAC (SHA-256 or stronger) with a per-provider, per-environment secret, unless the provider mandates an asymmetric signature over a signed token, in which case the asymmetric scheme governs. | `[PROPOSED]` |
| WS-3 | The signature input includes the timestamp and, where supplied, the endpoint path or a nonce, so a captured signature cannot be replayed against a different route. | `[PROPOSED]` |
| WS-4 | The request timestamp must fall within a **5-minute window** of AmmPal's server clock; a request outside the window is rejected even when the signature is valid. | `[PROPOSED]` |
| WS-5 | Comparison is **constant-time** across the full expected value; a mismatch is a hard rejection with no partial match and no tolerance. | `[PROPOSED]` |
| WS-6 | Clock skew is handled by a bounded tolerance (proposed 60 seconds) applied **on top of** the 5-minute window, on NTP-synchronised hosts; the two are distinct controls. | `[PROPOSED]` |
| WS-7 | Every event is deduplicated on `(provider, provider_event_id)` with a unique constraint, so a duplicate delivery can never re-apply a business mutation. | `[PROPOSED]` |
| WS-8 | The event is **persisted before acknowledgement**: AmmPal responds 2xx only after the raw event is durably written to `integration.webhook_inbox` (Rule `09` DB-24). | `[PROPOSED]` |
| WS-9 | Business processing happens **after** acknowledgement, in the `integration` module's queue, with bounded exponential backoff and jitter, and a dead-letter store beyond the retry ceiling. | `[PROPOSED]` |
| WS-10 | Dead-letter events are replayable from the Control Center by an operator action that re-enqueues the **same** event id, preserving idempotency. | `[PROPOSED]` |
| WS-11 | Rejected requests are logged with a redacted reason, the provider, the route and the correlation id — but never the body of a request that failed signature verification, since it may be attacker-controlled. | `[PROPOSED]` |
| WS-12 | Rate limiting is applied per provider route with a burst allowance; an IP allow-list is an additional control, never a replacement for signature verification. | `[PROPOSED]` |
| WS-13 | A replay attack is detected when a valid, in-window signature arrives with an event id already seen: the event is acknowledged as a duplicate and a security counter is incremented. | `[PROPOSED]` |
| WS-14 | The webhook secret is rotatable without downtime: a verification window accepts the previous secret for a bounded period, and the rotation is recorded as an operational event. | `[PROPOSED]` |
| WS-15 | Webhook routes are exempt from the standard CSRF protection (they are not session-authenticated) and are instead protected by WS-1 … WS-7. | `[PROPOSED]` |

### 14.2 Processing sequence

`[PROPOSED]`

1. Receive the request on a dedicated route and capture the raw body bytes and the relevant headers.
2. Reject if the source IP is outside the provider's allow-list (edge control).
3. Read the timestamp; reject if outside the 5-minute window.
4. Compute the expected signature over the raw body; compare in constant time; reject on mismatch.
5. Begin a transaction and insert the event row with a `(provider, provider_event_id)` unique constraint. On conflict, treat it as a duplicate, commit, and return 2xx.
6. Store the raw event, the headers, and a redacted payload preview; commit the transaction; return 2xx.
7. A queue worker picks up the event, performs the business mutation inside a transaction guarded by the event's processed flag, and marks the event processed.
8. On failure the worker retries with exponential backoff and jitter (base 5 s, factor 2, jitter, max 24 attempts, roughly 24 h spread).
9. Beyond the ceiling the event moves to the dead-letter store and a P2 alert is raised.

### 14.3 Dead-letter and replay

`[PROPOSED]`

| Aspect | Contract |
|---|---|
| Storage | `integration.dead_letter_event` with the full raw payload and the provider reference |
| Replay trigger | An operator action in the Control Center, restricted to `SUPER_ADMIN` and `ADMIN` |
| Replay semantics | The original `provider_event_id` is reused; the event is marked `REPLAYED` with a replay counter |
| Idempotency | A replayed event already applied is a no-op; the replayed status is reported back to the operator |
| Retention | `[PROPOSED]` 90 days, then a manual purge |

### 14.4 Per-provider deviations

`[PROPOSED]` No provider is known to deviate from this baseline; the table records the expected mechanism where a provider's shape differs.

| Provider | Mechanism | Deviation | Note |
|---|---|---|---|
| Razorpay | HMAC over the raw body with a timestamp carried in a signature header | None expected | Verify the exact header encoding during contract testing |
| Google Maps Platform | No inbound webhook in the base configuration | n/a | If event push is enabled, the baseline applies |
| Telephony | HMAC over the raw callback body plus timestamp, plus an IP allow-list | None expected | The IP allow-list is additive, not substitutive |
| WhatsApp | HMAC over the raw body using the app secret | Possible variation in which fields are signed | The contract test must assert the exact field set |
| SMS | HMAC over the raw body plus timestamp | None expected | Some providers sign a flattened parameter set rather than the body; the contract test must pin the actual mechanism |
| Email | HMAC over the raw body plus timestamp | None expected | Bounce and complaint payloads are small; validate the signature before parsing |
| FCM | No inbound webhook in the base configuration | n/a | A push extension inherits the baseline |
| Object storage | No inbound webhook in the base configuration | n/a | Optional event notifications inherit the baseline |
| OIDC | Front-channel callback, not a webhook | n/a | Protected by `state` and PKCE; back-channel logout inherits the baseline |

### 14.5 Inbound route map `[OPEN]`

`10` §4.5 names six receiving routes. This document names the events that arrive on them. Until this
table existed the two lists had nothing joining them, so there was no way to check that every inbound
route has an owning provider contract, or that every provider event has somewhere to land.

| AmmPal route (`10` §4.5) | Owning provider | Events | `24` section |
|---|---|---|---|
| `/webhooks/payments/{provider}` | P-02 Razorpay | payment captured / failed, refund, dispute | §5.5 |
| `/webhooks/telephony/{provider}` | P-03 cloud telephony | call status, DTMF, recording available | §6.5 |
| `/webhooks/whatsapp/{provider}` | P-04 | delivery status, inbound message, template status | §7.5 |
| `/webhooks/sms/{provider}` | P-05 | `sms.delivered`, `sms.failed`, `sms.queued`, `sms.inbound`, `sms.template.rejected`, `sms.balance.low` | §8.5 |
| `/webhooks/email/{provider}` | P-06 | bounce, complaint, delivery | §9.5 |
| `/webhooks/otp/{provider}` | **none** | — | — |

**The OTP route has no contract, because there is no OTP provider.** OTP arrives over P-05 (SMS) and
P-03 (voice); §8.5 already carries the delivery events. So `/webhooks/otp/{provider}` is either a
second name for events P-05 already posts to `/webhooks/sms/{provider}` — in which case the same
`provider_event_id` can arrive on two routes, and the §14.1 WS-7 dedupe, keyed on
`(provider, provider_event_id)`, will not catch it across routes — or it is a genuinely separate
provider, which no document names. The recommendation is to **delete the route** and treat OTP status as
an SMS event distinguished by message purpose. Registered as `OD-DOC-18`; it removes a
duplicate-delivery risk on the one flow where a duplicate grants access.

**One inbound path this document depends on is absent from `10` §4.5:** the OIDC front-channel redirect
callback (P-09, §12.5). It is not a provider webhook in the §4.5 sense, which is why it is missing — but
`10` §3 lists `/auth/sso/{provider}` as a public endpoint and never names the route that receives the
provider's response, so `29` has no path to test. Object storage (P-08) and FCM (P-07) are
outbound-only in the base configuration and appear in §14.4 for completeness, not as missing routes.

## §15 Vendor Account Procurement Checklist

`[CONFIRMED]` **Every account below is `NOT STARTED`.** No provider account, agreement, SLA, price or approval exists. Lead times are **estimates only**, marked as such, and must be replaced with confirmed dates during procurement.

### 15.1 Account register

| # | Account to open | Purpose | Owner | Status | Lead time (estimate) | Blocking phase | Dependencies |
|---|---|---|---|---|---|---|---|
| A-01 | Razorpay merchant account | Payment collection, refunds, settlement reports | Finance Lead and Founder | **NOT STARTED** | `[PROPOSED]` 1–3 weeks plus legal-entity KYC | Revenue-bearing build (booking to payment) | Legal entity, settlement bank account, business categories, website and app presence |
| A-02 | Google Maps Platform billing account, project and API keys | Geocoding, places, routes, static maps | Engineering Lead | **NOT STARTED** | `[PROPOSED]` 1–5 business days, extended by billing verification | Core services (address capture, pricing, ETA) | Legal entity billing details, API selection (OD-MAP-01) |
| A-03 | WhatsApp Business account (official or via BSP) | Customer messaging on the WhatsApp channel | Product Lead | **NOT STARTED** | `[PROPOSED]` 2–6 weeks including display-name review, number registration and template approvals | Notification phase | OD-INT-02 decision, sending number, business verification documents, template authoring |
| A-04 | Cloud telephony account (Indian provider) | Voice calls, IVR, call recording, click-to-call | Engineering Lead | **NOT STARTED** | `[PROPOSED]` 1–3 weeks plus DND and registration formalities | Notification and dispatch phase | OD-INT-01 selection, toll-free number procurement (OD-TEL-01), compliance documents |
| A-05 | SMS provider account with DLT entity registration | Transactional SMS and OTP | Engineering Lead | **NOT STARTED** | `[PROPOSED]` 2–4 weeks including DLT entity, sender ID and content-template approvals | Notification and authentication phase | Legal entity proof, GST and PAN, template registry, OD-SMS-02 selection |
| A-06 | Transactional email provider account | Invoice, statement and notification email | Engineering Lead | **NOT STARTED** | `[PROPOSED]` 1–2 weeks plus domain verification | Notification phase | Sending domain ownership, SPF/DKIM/DMARC DNS changes, OD-MAIL-01 selection |
| A-07 | Firebase project with service account | Push notifications | Engineering Lead | **NOT STARTED** | `[PROPOSED]` 3–10 business days plus store and app registration | Engagement phase | Mobile app identifiers, bundle and package IDs, legal entity for the project, OD-FCM-04 |
| A-08 | S3-compatible object storage buckets and access keys | Artefact storage | Platform Lead | **NOT STARTED** | `[PROPOSED]` 1–5 business days | Core services (artefact generation) | OD-INT-06 provider selection, data residency decision (OD-STOR-02), key policy |
| A-09 | OIDC identity provider application registration | Authentication for every surface | Engineering Lead | **NOT STARTED** | `[PROPOSED]` 1–3 weeks including tenant, app and redirect URIs | Authentication phase (blocks every surface) | OD-IDP-01 selection, redirect URI inventory, role model freeze, MFA policy |

### 15.2 Procurement prerequisites common to all accounts

`[PROPOSED]`

| Prerequisite | Owner | Notes |
|---|---|---|
| Legal entity documentation (incorporation certificate, GST and PAN, bank proof) | Founder and Finance | Required by A-01, A-03, A-05, A-07, A-08 |
| A business address and a live website or domain | Product | Required by A-01, A-03, A-06; the website must be reachable |
| A data-processing position with each vendor | Legal | Not yet negotiated; each vendor's terms must be reviewed per account |
| A named technical owner per account | Engineering | A single accountable owner per account; the register updates on change |
| A budget line per provider | Finance | Amounts to be established from current vendor pricing at procurement (§16) |
| A readiness checklist per account | Engineering | Built from the §4.8 conformance checklist of the relevant provider |

### 15.3 Account lifecycle rules

`[PROPOSED]`

1. An account is **not** opened until the corresponding selection decision in §18 is closed, except where a sandbox or trial account is explicitly required to run a conformance test.
2. Credentials are issued into the secrets manager at account creation; they are never communicated over chat, email, or a ticket, and never written to this document.
3. Every account carries an owner, a renewal date, and a cost-monitored spend alert.
4. An account unused for 90 consecutive days is reviewed for closure to avoid dormant spend.
5. Production traffic is switched on only after the provider's §4.8 conformance checklist reaches **Pass** on the critical rows and the relevant §19 tests are green.

## §16 Cost Model and Third-Party Expense Envelope

`[CONFIRMED]` **Actual rates are not established.** No rate card, quote, negotiated price, free-tier allowance or credit is confirmed for any provider. Every figure below must be sourced from **current vendor pricing at the time of procurement** and recorded in the cost model register owned by Finance — not in this document.

`[PROPOSED]` The table below defines the **metering dimension** for each cost driver (the unit the provider bills against) and the optimisation lever AmmPal controls. These are procedural facts about how such providers generally meter; the actual unit price must be confirmed per provider.

| # | Cost driver | Metering dimension | Optimisation lever | Rate status | Notes |
|---|---|---|---|---|---|
| C-01 | Transactional SMS | Per message, segmented by route and category (transactional, promotional, OTP) | Template consolidation; batch notifications; per-event dedupe before send; quiet-hours batching | **Not established** — current vendor pricing required at procurement | The DLT template registry must match the provider's content categories or sends are rejected or reclassified |
| C-02 | WhatsApp conversations | Per conversation (a window and its messages), with per-category rates and possible per-message charges inside a window | Minimise distinct conversations by batching related updates; notify inside an open window where possible; suppress redundant updates | **Not established** — current platform or BSP pricing required | The cost model differs fundamentally between a direct platform relationship and a BSP; OD-INT-02 drives this line |
| C-03 | Google Maps Platform calls | Per API call, by product (Geocoding, Places, Routes/Distance Matrix, Static Maps) with tiered volume pricing | Caching; batch matrix elements up to the request limit; serve static maps from P-08; disable autocomplete and static maps in degraded mode | **Not established** — current Google Maps Platform pricing required | Maps cost scales with bookings; the cache TTL is the primary lever (OD-MAP-05) |
| C-04 | Telephony | Per connected minute, with separate rates for inbound, outbound, IVR and click-to-call, and a possible minimum-billed duration | Cap IVR length; enforce the retry ceiling and spacing; route simple notifications to SMS; record only calls that need it | **Not established** — current vendor pricing required | Recording and transcription, if ever enabled, are separate cost lines (OD-TEL-05) |
| C-05 | Transactional email | Per message, often tiered, plus a bandwidth or attachment-size charge | One message per recipient (never a shared `to` array) for personalisation and suppression accuracy; use signed links instead of attachments | **Not established** — current vendor pricing required | The attachment policy is a cost *and* a security lever (OD-INT-05) |
| C-06 | Object storage | Per GB-month stored, plus per-GB egress, plus per-request charges | Enforce retention classes through lifecycle; cache hot artefacts; use signed links with a short TTL; archive rather than store indefinitely | **Not established** — current vendor pricing required | Egress is the risk line against a 16 TB bandwidth envelope; VPS bandwidth and provider egress are separate budgets |
| C-07 | Push notifications | Per message, commonly within a free monthly allowance | Send per-token rather than by topic only where invalid-token hygiene matters; send engagement-class pushes only | **Not established** — current pricing and allowance must be confirmed | A free allowance, if any, must be confirmed at procurement, not assumed (OD-FCM-05) |
| C-08 | Identity provider | Per monthly active user or per authentication, depending on the plan | Use refresh-token rotation rather than repeated interactive sign-ins; use local break-glass for emergencies | **Not established** — current vendor pricing required | Depends entirely on the selected provider's plan (OD-IDP-01) |
| C-09 | Map tiles and static map rendering | Per request, plus a bandwidth component for tile delivery | Render server-side into P-08; never proxy tiles through the VPS | **Not established** — current pricing required | See OD-MAP-04 (direct versus proxied) |

### 16.1 Envelope discipline

`[PROPOSED]`

| Rule | Statement |
|---|---|
| CM-1 | No provider is activated in production without a Finance-approved spend envelope, expressed as a monthly ceiling and a per-unit assumption. |
| CM-2 | Each provider's actual spend is tracked monthly against its assumption; a variance above 20% triggers a review, not an automatic throttle. |
| CM-3 | A hard spend alert is configured at the provider where supported, and a soft alert is raised in AmmPal's own reporting when the assumption is exceeded. |
| CM-4 | Free tiers and promotional allowances are **not** relied upon for capacity planning until confirmed in writing by the provider. |
| CM-5 | A cost-model assumption is a `[PROPOSED]` estimate until the provider's current pricing page or a written quote is recorded in the cost register. |
| CM-6 | If a provider introduces a new billable unit, §16 is updated and the change is recorded in §20. |

### 16.2 Cost drivers not yet quantifiable

`[OPEN]` The following cannot be estimated until the volume forecast and the selection decisions close: total bookings per month, notification volume per booking, WhatsApp conversation rate, technician call minutes per booking, and KYC document volume. The forecast is a business deliverable tracked in `05` and `11`.

## §17 Change Management

### 17.1 Provider swap procedure

`[PROPOSED]` A provider change is a **seam change, not a business-logic change**.

1. **Impact assessment.** Identify every AmmPal module that consumes the affected port, the data fields it relies on, and the fallback levels defined in the relevant §4–§12 section.
2. **Contract definition.** Extend or amend the port interface in §13 to express the new provider's capabilities. Any port change is an interface change and requires a new ADR.
3. **New adapter implementation.** Implement the new provider behind the port. The adapter is the **only** code family that may know provider-specific details.
4. **Parallel run.** Run the new adapter in shadow mode against a sanitised production sample and compare its normalised output with the current adapter's output.
5. **Conformance re-run.** Re-run the full §4.8 conformance checklist for that provider against the new provider, plus the §19 contract tests. Nothing advances on a partial pass.
6. **Failure-injection drill.** Run the degradation-ladder drill for the new provider.
7. **Cost re-baseline.** Re-derive the §16 cost lines from the new provider's current pricing and obtain Finance approval.
8. **Data migration.** Migrate retained artefacts (invoice PDFs, KYC images) from the old storage provider to the new one under a dedicated migration plan with checksum verification.
9. **Cutover.** Switch the DI binding, keep the previous adapter available behind a feature flag for a defined rollback window, and monitor error and latency metrics closely.
10. **Decommission.** Remove the old credentials, close the old account, and archive the old provider's data per the retention schedule.

### 17.2 What a provider change must never do

`[PROPOSED]`

| Prohibition | Reason |
|---|---|
| Must not change a domain rule, a booking status, a status mapping, or the commission calculation. | The provider is not a source of truth (§2.2). |
| Must not require a schema migration of a historical business record. | Historical records are AmmPal's; the provider reference is a stored attribute. |
| Must not silently change money values. | Money is integer paise; a swap may not alter a stored amount. |
| Must not change a customer-visible identifier format. | Booking `AMM-YYYYMMDD-XXXXXX`, invoice `INV-YYYYMMDD-XXXXXX`, commission invoice `CINV-YYYY-W<WW>-<BRANCH>-<NNNN>`, settlement `STL-YYYY-W<WW>-<BRANCH>-<NNNN>`, ticket `TCK-YYYYMMDD-XXXXXX`, coupon `AMM-<PFUND\|DFUND\|SHARED>-<RANDOM5>`, branch `<STATE2>-<CITY3>-<NNN>`, zone `<BRANCH>-Z<NN>`, service area `<ZONE>-A<NN>`, partner org `PT-OD-<NNNN>` and technician `TECH-<BRANCH>-<NNNN>` are platform invariants. |
| Must not change the 15%-on-eligible-labour commission basis or the weekly settlement cadence. | Those are business rules, not integration details. |

### 17.3 ADR requirement

`[CONFIRMED]` **A provider change requires a new ADR.** An ADR is mandatory for: adding a provider; removing a provider; changing a port interface in §13; changing a webhook signature scheme or the §14 baseline; changing a money-affecting provider; changing a data-residency position; changing the fallback ladder for a critical channel; or changing a retention class.

`[PROPOSED]` The ADR must state the driver, the options considered, the §16 cost impact, the data-migration plan, the conformance plan, the rollback plan, and the affected downstream modules.

### 17.4 Routine (non-ADR) changes

`[PROPOSED]` The following do **not** require an ADR but do require a §20 revision-history entry: adding an optional provider response field that AmmPal ignores; a provider-side pricing change with no functional effect; a new API version on an unchanged capability; a new outbound message template; adjusting a cache TTL within the agreed envelope.

## §18 Unresolved Items

`[CONFIRMED]` The items below are open decisions and dependencies that this document cannot resolve, cross-referenced with the open-decision register used across the project set.

| ID | Item | Affected provider | Owner | Blocking | Status |
|---|---|---|---|---|---|
| OD-INT-01 | Select the Indian cloud-telephony provider (voice, IVR, DND and TRAI compliance, recording, sub-accounting, per-minute price) | P-03 | Engineering and Procurement | Notification and dispatch build | `[OPEN]` |
| OD-INT-02 | Decide an official WhatsApp Business Platform relationship versus a Business Solution Provider | P-04 | Product and Procurement | Notification build | `[OPEN]` |
| OD-INT-03 | Decide whether a second SMS provider is contracted for redundancy | P-05 | Engineering and Risk | Reliability posture | `[OPEN]` |
| OD-INT-04 | Decide whether third-party fleet and vehicle tracking is adopted; if so it introduces a further positioning provider and contract | P-01 (adjacent) | Product | Fleet features scope | `[OPEN]` |
| OD-INT-05 | Decide whether email attachments are permitted at all, or signed-link only | P-06 | Security and Product | Email build and cost model | `[OPEN]` |
| OD-INT-06 | Select the S3-compatible object storage provider (region, durability, egress, residency, cost envelope) | P-08 | Platform and Procurement | Core services build | `[OPEN]` |
| OD-INT-07 | Select the KYC vendor for partner and technician verification; it may link to the OIDC subject | P-09, P-08 | Compliance and Product | Partner onboarding | `[OPEN]` |
| OD-INT-08 | (cross-ref `05`) Finalise the data classification and retention matrix that this document's retention columns implement | All | Governance | Retention correctness | `[OPEN]` |
| OD-DEV-08 | Confirm the agreed service-layer boundaries and the `integration` module contract that the §13 adapters implement | All | Engineering Lead | Adapter implementation | `[OPEN]` |
| OD-MAP-01 | Select which Google Maps Platform APIs to license; each is separately billed | P-01 | Engineering and Finance | Account creation | `[OPEN]` |
| OD-MAP-03 | Establish the projected monthly map call volume for the cost envelope | P-01 | Business | Budget | `[OPEN]` |
| OD-PAY-01 | Confirm the merchant legal entity and settlement bank account ownership | P-02 | Finance and Legal | Payment build | `[OPEN]` |
| OD-PAY-02 | Align the provider settlement cycle with the weekly Mon–Sun commission cycle | P-02 | Finance | Reconciliation design | `[OPEN]` |
| OD-PAY-05 | Define the refund authorisation matrix and the refund SLA | P-02 | Business | Refund implementation | `[OPEN]` |
| OD-TEL-01 | Procure and verify the real toll-free number to replace `1800-XXX-XXXX` | P-03 | Procurement | Caller identity | `[OPEN]` |
| OD-SMS-01 | Complete DLT entity, sender ID and content-template registration | P-05 | Legal and Provider | Any SMS traffic | `[OPEN]` |
| OD-SMS-03 | Define the OTP policy (length, validity, attempt cap, lockout) | P-05 | Security | Authentication implementation | `[OPEN]` |
| OD-MAIL-01 | Select the transactional email provider | P-06 | Engineering and Procurement | Notification build | `[OPEN]` |
| OD-IDP-01 | Select the OIDC identity provider | P-09 | Engineering and Security | Authentication build (blocks all surfaces) | `[OPEN]` |
| OD-FCM-01 | Confirm the FCM delivery path and its interaction with app platform registration | P-07 | Architecture | Engagement build | `[OPEN]` |
| OD-STOR-02 | Confirm the data residency requirement for personal and KYC data | P-08 | Legal | Provider selection | `[OPEN]` |

`[PROPOSED]` The open-decision register remains the single source of truth for these items; this table is a **view** of it scoped to integrations, updated when the register changes.

## §19 Validation and Conformance Testing

### 19.1 Test layers

`[PROPOSED]`

| Layer | Purpose | Trigger | Owner |
|---|---|---|---|
| L1 — Unit | DTO mapping, error-code mapping, template-registry guards, policy clamps | On every commit | Engineering |
| L2 — Contract test | The provider's actual response shape against the adapter's expected schema, using a recorded sanitised fixture | Nightly, and on provider API version change | Engineering |
| L3 — Sandbox integration | A real call against the provider's sandbox or test environment, asserting the §4.8 checklist | Nightly, scheduled | Engineering and QA |
| L4 — Webhook security | Signature, window, replay, duplicate and persist-then-ack behaviour | Nightly and pre-release | Engineering and Security |
| L5 — Failure injection | Simulated timeouts, 5xx, 429, signature failures, partial outages, schema drift | Weekly, rotating per provider | Engineering |
| L6 — Degradation drill | The full §4.7 ladder is exercised and the observable behaviour verified | Monthly, per critical provider | Engineering and Ops |
| L7 — Reconciliation rehearsal | Provider settlement and invoice data reconciled against AmmPal's ledgers on a sample | Weekly | Finance and Engineering |
| L8 — Load and soak | Sustained call volume against a sandbox to validate timeouts, queue behaviour and VPS resource headroom | Pre-release and quarterly | Engineering |

### 19.2 Sandbox-mode nightly runs

`[PROPOSED]`

| Rule | Statement |
|---|---|
| CN-1 | Every nightly run executes against the provider's **sandbox or test mode** where one exists; production credentials are never used in an automated nightly run. |
| CN-2 | The nightly run covers, per provider: one successful call, one validation rejection, one simulated timeout, and one signature-failure case. |
| CN-3 | A nightly failure raises a build-breaking alert for the affected adapter and marks the corresponding conformance checklist row **Fail** until the failure is triaged. |
| CN-4 | Nightly runs never call a real customer-facing number, address, or payment instrument; recipients and destinations come from a test corpus. |
| CN-5 | Sanitised response fixtures are stored in the repository **without** secrets, tokens, real identifiers, or personal data; a leak in a fixture is a security defect. |
| CN-6 | The nightly run records provider latency and error rate into the same metrics pipeline used in production, so trends are comparable. |

### 19.3 Contract-test focus per provider

`[PROPOSED]`

| Provider | Contract-test focus | Failure-injection scenarios |
|---|---|---|
| P-01 Maps | Geocode component mapping, matrix element statuses, error codes | Timeout, quota exhaustion, `ZERO_RESULTS`, partial matrix, schema drift |
| P-02 Payments | Order, payment and refund DTOs, signature verification, settlement breakdown | Signature mismatch, replay, capture timeout, refund rejection, provider outage, amount mismatch |
| P-03 Telephony | Call status mapping, DTMF payloads, recording reference | Callback from a disallowed IP, origination timeout, DND block, IVR failure, recording 404 |
| P-04 WhatsApp | Template rendering, status mapping, inbound payloads | Template unapproved, quality restriction, throttle, duplicate inbound, missing receipt |
| P-05 SMS | DLR mapping, error codes, DLT template enforcement | DLT rejection, balance exhaustion, send timeout, missing DLR, route congestion |
| P-06 Email | Send DTO mapping, bounce and complaint events | Hard bounce, spam complaint, attachment rejection, provider outage, domain not verified |
| P-07 Push | Token handling, payload shape, drop reasons | Invalid token, quota exhaustion, provider outage, payload size |
| P-08 Storage | Checksum integrity, key policy, presign policy | Credential failure, write timeout, read throttle, cross-prefix access, lifecycle deletion |
| P-09 Identity | JWKS validation, claim validation, PKCE flow, refresh rotation | JWKS unavailable, unknown `kid`, token replay, provider outage, subject collision |

### 19.4 Acceptance criteria for go-live

`[PROPOSED]` A provider may be enabled in production only when:

1. Its §4.8 conformance checklist shows **Pass** on every critical row, and each non-critical row is either Pass or has a recorded, accepted exception.
2. Its nightly sandbox run has been green for 14 consecutive days.
3. Its failure-injection drill has been executed and the observed behaviour matches the §4.6 table.
4. Its degradation ladder has been exercised end to end at least once.
5. The §14 baseline tests are green for that provider's routes.
6. A cost envelope (§16) is approved by Finance and a spend alert is configured.
7. A support runbook exists covering the top five failure modes for that provider, with the escalation path and operator actions.
8. A rollback switch exists to disable the provider without a deployment.

### 19.5 Test data rules

`[PROPOSED]`

| Rule | Statement |
|---|---|
| TD-1 | Test data uses synthetic records only; no production customer record, phone number, address, or instrument is copied into a test environment. |
| TD-2 | The placeholder toll-free number `1800-XXX-XXXX` is never dialled. |
| TD-3 | Recorded provider payloads are sanitised before storage, and the sanitiser is covered by its own unit test. |
| TD-4 | Test keys and sandbox credentials live in the same secrets manager as production keys, in a separate namespace. |

## §20 Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.3 | 2026-10-21 | Engineering Lead + Security Owner (palette and storage pass) | §11.3's **Public access** row annotated, not edited: "**No** bucket, prefix or object is publicly readable" is now one side of `OD-DOC-34` (`[BLOCKER]`), because the owner has asked for Cloudinary as primary media storage with a super-admin-selectable provider, and a CDN delivery URL for catalogue imagery is a publicly readable object. The annotation names `13` §5.2 as the mirror side (`img-src 'self'` lists no such host), records the registered recommendation to split **by data class** — §11.2's KYC, recordings, job media and invoice classes keep pre-signed short-expiry access under `09` §8's `PERSONAL` classification — and states that no provider plan or price has been read for this suite. Also fixes the document's closing trailer, which still said **v1.1** after v1.2 was issued. **No contract term, provider requirement, retention period, key rule or SLA was changed, and no `[CONFIRMED]` row was relaxed.** | §11.3, header, trailer, Revision History |
| 1.2 | 2026-10-21 | Engineering Lead (documentation audit pass 3, continued) | §12.3's "Logout and MFA" cell annotated: the MFA **scope** in this document ("staff roles") is one of four incompatible statements across `13` §5.1, `README` §11 and `28` §3.7, and the narrowest of them exempts every partner-side account that can approve or dispute a settlement. Registered as `OD-DOC-20` (`[BLOCKER]`, before the auth module is built); the provider-side factor question stays with `OD-SEC-01`. No contract term, provider requirement or SLA was changed. | §12.3, header, Revision History |
| 1.1 | 2026-10-21 | Engineering Lead (documentation audit pass 3) | Aligned integration retention to the single financial period in `09` §6 (7 → **8 years**, `[PROPOSED]` pending `OD-NFR-06`) instead of an integration-local number. Renamed the inbound event store to `integration.webhook_inbox` and cited Rule `09` DB-24 (§5.6 and §14.1 WS-8) — the document had called it `integration.provider_event`, a table that does not exist. Added the **`PaymentResult.status` → domain `payments.status` total mapping** (§13.1), including why a partial refund leaves the payment `SUCCESS` and moves the **invoice** instead. Added §14.5, the inbound route map, which found that `/webhooks/otp/{provider}` has no owning provider contract (`OD-DOC-18`) and that the OIDC redirect callback is depended on here but named by no route in `10` §4.5. Renumbered the duplicated `OD-DEV-05` reference to `OD-DEV-08`. | §5.2, §5.6, §5.9, §13.1, §14.1, §14.5, header, Revision History |
| 1.0 | 2026-10-21 | Engineering Lead | Initial issue. Establishes the provider contract specification for the AmmPal Service platform: the provider register; per-provider contract sections for Google Maps Platform, Razorpay, cloud telephony and IVR, WhatsApp Business Platform, the SMS provider, transactional email, Firebase Cloud Messaging, S3-compatible object storage, and the OIDC identity provider; the §13 adapter port sketches; the §14 webhook security baseline; the §15 vendor account procurement checklist; the §16 cost-model structure; the §17 change-management procedure; and the §18 integration-scoped view of the open-decision register. | All (§1–§20) — new document |

`[CONFIRMED]` **End of document AMM-SVC-DOC-24 v1.3.** Nothing described in this document is implemented, and no provider account, agreement, SLA, price, template approval, or credential exists as of 2026-10-21.
