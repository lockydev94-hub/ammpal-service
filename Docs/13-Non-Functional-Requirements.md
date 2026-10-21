# 13 — Non-Functional Requirements

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-13 |
| Version | 1.7 |
| Status | Approved for Design & Development |
| Owner | Engineering Lead + Security Owner |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `08`, `09`, `13` |

---

## 1. Availability

| Surface / Capability | Target | Measurement | Notes |
|---|---:|---|---|
| Public API | 99.5% monthly | Successful non-5xx / total requests | Excludes planned maintenance (announced ≥ 48 h in advance, capped at 2 h/month) |
| Customer App & Web core flows | 99.5% | Synthetic journey checks every 5 min | Booking, tracking, payment |
| Partner App core flows | 99.0% | Synthetic checks | Degraded to queue-based offers if the realtime gateway is down |
| Control Center | 99.0% | Synthetic checks | Internal surface |
| Payment callbacks | 99.9% | Webhook acceptance rate | Webhooks are acknowledged even if downstream processing is delayed |
| Notification dispatch | 99.0% | Queue drain within SLA | At-least-once delivery |
| Realtime tracking | 99.0% | Connection success | **Polling fallback** guarantees the customer still sees the location |

**Rule AV-01** — No single component failure may make the platform unusable. The realtime gateway, the notification worker and the reporting module are all degradable.

---

## 2. Performance

### 2.1 API Latency (server-side, excluding client and third-party time)

| Endpoint | p50 | p95 | p99 | Note |
|---|---:|---:|---:|---|
| `GET /catalog/categories` | 30 ms | 80 ms | 150 ms | — |
| `GET /catalog/services` | 60 ms | 150 ms | 300 ms | — |
| `POST /quotes` | 90 ms | 250 ms | 500 ms | — |
| `GET /search/technicians` | 180 ms | 600 ms | 1200 ms | — |
| `POST /bookings` | 140 ms | 350 ms | 700 ms | — |
| `GET /bookings/{id}` | 40 ms | 100 ms | 200 ms | — |
| `GET /bookings/{id}/track` | 25 ms | 80 ms | 150 ms | — |
| `POST /bookings/{id}/complete` | 200 ms | 500 ms | 1000 ms | — |
| `POST /admin/settlements/generate` (dry run) | 1.5 s | 4 s | 8 s | For ~5,000 jobs |
| `GET /admin/reports/*` (paged) | 300 ms | 900 ms | 2 s | Cached aggregates |
| `POST /webhooks/*` (ack) | 20 ms | 60 ms | 120 ms | Persist + enqueue only |

**Rule PF-01** — The booking search path (location → candidates → ranked results) must complete in **under 800 ms p95** including the PostGIS query and the ranking.

### 2.2 Client Performance

| Metric | Target |
|---|---|
| Website LCP (4G, mid-range Android) | < 2.5 s |
| Website INP | < 200 ms |
| Website CLS | < 0.1 |
| Customer App cold start | < 2.5 s |
| Partner App cold start | < 2.5 s (2.0 s warm) |
| Partner App offline job open | < 500 ms |
| Control Center table interaction | < 100 ms perceived |

> **These budgets are what constrains the asset plan, and nothing here has been measured against a real
> device.** `32` §4 derives every raster weight ceiling in the workspace from the LCP and APK figures
> above and labels them as derived, not measured. Two consequences in §5.2 are load-bearing and are not
> design preferences: `font-src 'self'` means both Inter and the Noto families must be self-hosted and
> subset — nobody has produced that pipeline, and Odia cannot render without it (`FR-CAT-08`, `OD-DOC-32`)
> — and `img-src 'self'` plus `24` §11's rule that no object is publicly readable means asset imagery
> is same-origin, not served from a public bucket (`OD-DOC-26`, and the CDN question itself is
> `OD-DOC-34` `[BLOCKER]`). Motion does not relax any figure in this
> table: `30` §7 prohibits an animation from being used as evidence of server-side progress.

### 2.3 Throughput & Capacity Targets

| Dimension | Phase 1 | Phase 3 (target) | Phase 4 (target) |
|---|---:|---:|---:|
| Registered customers | 5,000 | 50,000 | 250,000 |
| Active technicians | 150 | 2,000 | 8,000 |
| Bookings / day | 200 | 2,500 | 12,000 |
| Bookings / month | 6,000 | 75,000 | 360,000 |
| Peak requests / minute | 120 | 800 | 3,000 |
| Concurrent WebSocket connections | 50 | 400 | 2,000 |
| Staff users (Control Center) | 20 | 80 | 250 |
| Bookings retained | 8 years | 8 years | 8 years |

### 2.4 Scale Test Profile

The Phase 3 exit test (`17` §5) executes:
- **Baseline**: 2,500 bookings/day spread over 12 hours with a 3× evening peak.
- **Spike**: 5× baseline for 15 minutes (a festival/heatwave demand spike).
- **Soak**: 24 hours at 1.5× baseline to detect leaks.
- **Failover**: kill the primary API instance; the second must absorb traffic with < 5 s of errors.

---

## 3. Scalability

| Layer | Scaling approach | Trigger |
|---|---|---|
| Front ends (web, Control Center, apps) | CDN + static hosting | From Day 1 |
| API | Horizontal (PM2/Nginx upstream) | p95 CPU > 60% or latency breach |
| Worker | Horizontal with per-queue concurrency | Queue depth > 10,000 |
| Realtime | Horizontal with the Redis adapter | Connection count > 2,000 |
| PostgreSQL | Managed instance with read replicas + connection pooling (PgBouncer) | Phase 3 |
| Redis | Managed, with `maxmemory-policy` split (cache LRU + queue noeviction) | Phase 3 |
| Object storage | Managed S3-compatible | Phase 2 |

**Rule SC-01** — The API must be **stateless**; all session and state data lives in PostgreSQL or Redis, never in process memory.

---

## 4. Reliability & Data Integrity

| # | Requirement |
|---|---|
| RI-01 | **No silent data loss.** Every write path is transactional. |
| RI-02 | The booking → price snapshot → coupon redemption write is atomic (`08` §5.1). |
| RI-03 | Commission accrual is uniquely keyed per booking — double accrual is impossible. |
| RI-04 | Settlement generation is uniquely keyed per (partner, branch, period). |
| RI-05 | Invoice numbers are gapless per entity + financial year. A gap is a P1 incident. |
| RI-06 | The audit chain is hash-linked and verified daily; a break is a P1 incident. |
| RI-07 | Every job runs **at-least-once** with idempotent handlers. |
| RI-08 | Outbox pattern guarantees an event is published **iff** its transaction committed. |
| RI-09 | Nightly reconciliation asserts: Σ invoice lines = invoice totals; Σ settlement lines + adjustments = net; Σ ledger entries balance. |
| RI-10 | Money is never stored or computed in floating point. |

### 4.1 Recovery Objectives

| Metric | Target |
|---|---|
| RPO (data loss window) | ≤ 15 minutes |
| RTO (service restoration) | ≤ 2 hours |
| Backup frequency | Continuous WAL archiving + nightly full snapshot |
| Backup retention | 30 days rolling + 1 monthly archive |
| Restore test cadence | Monthly (automated), quarterly (documented full drill) |
| Payment webhook replay window | 7 days (provider-supported) |

---

## 5. Security

### 5.1 Controls

| Layer | Control |
|---|---|
| **Transport** | TLS 1.2+ everywhere; HSTS with `max-age=31536000; includeSubDomains`; HTTP→HTTPS redirect |
| **Authentication** | OTP (rate-limited) for customers/technicians; OIDC SSO + password for staff; **multi-factor authentication required for every internal staff account holding a financial or administrative permission** (`ADMIN`, `ACCOUNTANT`, `SUPER_ADMIN`, and any account with `finance:*` write). JWT RS256, 15-min access, rotating refresh tokens. `[OPEN]` — this scope excludes partner-side settlement approvers (`branch:settlement:*` holders are not internal staff and are not `finance:*`), while `README` §11, `24` §12.3 and `28` §3.7 state three different scopes for the same control (`OD-DOC-20`) |
| **Authorisation** | Role + scope + ownership, enforced server-side in SQL (`03` §6) |
| **Destructive-operation guard** | The platform mode (`38`) decides whether a hard delete, `TRUNCATE` or data-destructive DDL is permitted; in `PRODUCTION` it is refused. Enforced at the service layer **and** by bound database privilege (`38` §7 L2/L3) — a check that lives only in a screen is not this control. Soft delete (`03` §3.2) and the code-defined retention purge (`09` §6) continue to run. `[OPEN]` — the guard as literally stated collides with the DPDP erasure this same suite promises; `OD-DOC-40` decides, and it is scored as `19` `R-50` |
| **Password storage** | Argon2id, cost ≥ 19, per-user salt |
| **Secrets** | Environment/secret manager; rotated; never in code, logs or the repository |
| **Encryption at rest** | Database volume encryption; app-level encryption for bank details and document numbers (`pgcrypto` or KMS envelope) |
| **Encryption in transit** | TLS to all vendors, including webhook endpoints |
| **Payment data** | Never touches AmmPal servers (hosted gateway checkout) — PCI-DSS SAQ-A scope |
| **PII in logs** | Redacted: OTP, passwords, full card data, full bank account numbers, document numbers |
| **File uploads** | Presigned upload; MIME + extension allow-list; size cap; content sniffing; AV scan; served from a separate bucket with a short-lived signed URL and `Content-Disposition: attachment` |
| **SQL injection** | Parameterised queries only; ORM/query-builder; no string concatenation |
| **XSS** | No `dangerouslySetInnerHTML` with untrusted data; output encoding; CSP |
| **CSRF** | Not applicable to Bearer-token APIs; enforced for cookie-based web sessions (double-submit token) |
| **Rate limiting** | Per identity and per IP (`10` §8) |
| **Brute force** | 5 failed OTP verifications → 15-minute lockout; exponential backoff on login |
| **Multi-factor authentication** | Required for internal staff holding financial or administrative permissions. `[PROPOSED]` — the factor type (TOTP app, hardware key, or provider-hosted) is `OD-SEC-01`. `[OPEN]` — the **scope** is the other half of the decision: `README` §11, `24` §12.3 and `28` §3.7 each state it differently, and the test as written exempts every partner-side account that approves or disputes a settlement (`OD-DOC-20`) |
| **Session** | Refresh rotation with reuse detection — a reused refresh token revokes the whole family |
| **Dependency** | Automated SCA scanning; critical advisories block the pipeline |
| **SAST/DAST** | In CI for the API and web surfaces |
| **Audit** | Every sensitive mutation → `audit_events`; overrides → `audit_override_log` |
| **Least privilege** | Role review quarterly; scope assigned explicitly, never inherited implicitly. `[OPEN]` — `19` §4.2 IC-03 sets this review at **monthly** and `26` §6.2 cites IC-03 for the auditability promise; the cadence is undecided (`OD-DOC-21`) |

> **A control `26` says lives here, and this table does not contain:** `26` §4.5 item 9 assigns
> "production access approval, audit, confidentiality" to `13` §5. Nothing above or below §5 governs a
> **human** obtaining a shell on the production host — who may hold it, who approves it, for how long,
> where the session is recorded, or whether IC-03's review covers infrastructure accounts at all (it
> reviews "internal accounts, roles and scopes", and `03` §4 defines no infrastructure role). `25`'s
> runbooks assume that shell exists. Registered as `OD-DOC-22` `[BLOCKER]`; this note is the placeholder,
> not the rule. `[OPEN]`

### 5.2 Content Security Policy (baseline)

```
default-src 'self';
script-src 'self' 'nonce-<random>';
style-src 'self' 'nonce-<random>';
img-src 'self' data: blob: https://maps.googleapis.com https://maps.gstatic.com https://*.googleusercontent.com;
connect-src 'self' https://api.ammpalservice.com wss://api.ammpalservice.com https://*.googleapis.com https://fcm.googleapis.com;
font-src 'self';
frame-src https://api.razorpay.com;
object-src 'none'; base-uri 'self'; form-action 'self';
```

> **`[OPEN]` — `OD-DOC-34` `[BLOCKER]`, and this policy is one side of it.** As written, `img-src`
> names no media host of ours: `res.cloudinary.com` — or any other object-storage or CDN origin — is
> **not** in the list, so imagery served from one is blocked at render time in production while working
> in development. The owner has since asked for Cloudinary as **primary** media storage, several storage
> platforms supported, the active one selected by a super admin in the admin dashboard. Neither side has
> been edited into the other (`DEC-07`): this baseline stays exactly as issued until the decision closes,
> and the mirror annotation lives in `24` §11, whose rule that no bucket, prefix or object is publicly
> readable is the other half of the contradiction. The recommendation registered in `21` is to decide
> **per data class**, not per platform — catalogue and marketing imagery from a CDN origin named here,
> job evidence and anything derived from a `PERSONAL` class (`09` §8) from the platform's own storage
> behind short-lived signed URLs. `16` §5.2's same-origin static-bundle assumption and `09` §4.3's
> missing media columns are the other two things that have to change if this is decided the other way.

> **What may be loaded under these directives is `36` §3, and it is not a taste question.** An
> animation runtime that injects un-nonce'd `style` elements fails `style-src` here; an icon font or a
> component kit fetched from a CDN fails `font-src` and `script-src`; a remote web font fails `font-src
> 'self'`; and any media origin not named above is blocked at render time while `OD-DOC-34` is open. `13`
> states the policy, `36` states what can be built inside it, and a library that cannot pass the gate is
> not a candidate (`LB-02`).

### 5.3 Threat Model — Top Threats & Controls

| Threat | Controls |
|---|---|
| Credential stuffing | Rate limits, lockout, OTP-only for consumer accounts, device fingerprinting |
| IDOR on bookings | Ownership + scope checks; `404` (not `403`) on cross-owner access to avoid existence leaks |
| Price manipulation | Server-computed pricing only; band enforcement in the DB via trigger; provenance chain recorded |
| Coupon abuse | Server-side validation, usage caps, unique redemption per booking, anomaly detection on redemption velocity |
| Coupon farming | New-account and min-order rules; velocity limits per customer/device/IP |
| Technician collusion on ratings | Rating weight limited to verified completed bookings; anomaly detection on mutual rating clusters |
| PII exposure in the Control Center | Role-based masking; exports audited and watermarked |
| Webhook forgery | HMAC verification over the raw body; timestamp window; constant-time comparison |
| Partner branch data leak | `branch_id` scope predicate in every query; RLS as defence-in-depth (OD-09-01) |
| Financial tampering | Append-only ledgers, hash-chained audit, immutable invoices and settlements |
| Insider misuse | SoD on settlement issue/approve, override logging, quarterly access review (`OD-DOC-21` — `19` §4.2 IC-03 says monthly) |
| Location data exposure | 90-day retention for location history; encryption; DPDP consent |

---

## 6. Privacy & Regulatory Compliance (India)

### 6.1 DPDP Act, 2023

| Requirement | Implementation |
|---|---|
| Lawful purpose | Every purpose is declared in the consent record; no collection beyond it |
| Consent | Explicit, granular, per-purpose consent captured at registration and at marketing opt-in; a versioned consent table (`OD-09-03`) |
| Notice | Privacy policy + in-app notice at first launch, in the local language |
| Data minimisation | Only the data needed for service delivery, billing and compliance is collected |
| Purpose limitation | Data used only for the declared purpose |
| Storage limitation | Retention schedule enforced (`09` §6); automated purge jobs |
| Data subject rights | Access, correction, erasure, nomination, grievance redressal — implemented via the Account screen and a support request |
| Erasure | Erasure request → anonymisation of non-statutory data; financial records retained for the statutory period and de-linked from the customer profile. `[OPEN]` — anonymisation is defined against the **live database only**; `16` §5.6 keeps WAL plus nightly copies for 30 days and a monthly archive, and object storage is versioned for 30 days, so a restored copy can resurrect data the subject asked to erase. Nobody has said who may read those copies either (`OD-DOC-23`) |
| Security safeguards | Encryption, RBAC, audit, backups |
| Breach notification | Incident runbook with a 72-hour notification path to the Data Protection Board |
| Data fiduciary obligations | Grievance officer designated; grievance channel published |

### 6.2 Other Regulatory Requirements

| Area | Requirement |
|---|---|
| **GST** | Registration per operating state; correct place of supply; invoice numbering; e-invoicing/e-way bill if thresholds are crossed (`OD-07-01`) |
| **TDS (Sec. 194C)** | If applicable to commissions, deduct at source, issue TDS certificates and Form 16A (`OD-07-02`) |
| **Professional tax / labour welfare** | State-level, per branch — tracked as a configurable compliance item |
| **TRAI / DND** | Commercial voice respects DND registries; transactional messages exempt; template registration for WhatsApp |
| **IT Act, 2000** | Reasonable security safeguards; intermediary rules as applicable to the platform's role |
| **Consumer Protection (E-Commerce) Rules** | Clear pricing, no dark patterns, grievance officer, no misleading claims, cancellation policy displayed |
| **Payment security** | PCI-DSS SAQ-A via the gateway; no card storage |
| **Records** | Statutory retention of books (8 years) |

---

## 7. Usability

| # | Requirement |
|---|---|
| US-01 | A first-time customer completes a booking in ≤ 3 minutes on a mid-range Android, with no prior registration beyond OTP. |
| US-02 | A first-time technician completes onboarding in ≤ 10 minutes (excluding KYC verification time). |
| US-03 | All task flows are usable with one hand and in outdoor bright light (technician app). |
| US-04 | Every error message states **what happened and what to do next**. |
| US-05 | No destructive action is a single unlabelled tap; destructive actions require a confirm with a consequence summary. |
| US-06 | The price breakdown is visible at every stage where a price is shown. |
| US-07 | Localisation is complete — no untranslated English strings in Odia mode. |

> `US-07` is not achievable by translation alone. Odia has to **render**, which under §5.2's
> `font-src 'self'` requires a self-hosted, subset Odia face; `30` §4 records that no document says who
> produces that pipeline, and that the shaping behaviour of Noto Sans Odia in the Flutter text stack has
> never been verified here (`OD-DOC-32`). Colour-contrast usability is specified in `30` §3 with measured
> WCAG 2.1 AA ratios and satisfies `12` §6.3 `A11Y-1`; it is a token concern, not a duplicate NFR.

---

## 8. Compatibility & Interoperability

| Surface | Minimum supported |
|---|---|
| Website browsers | Chrome/Edge 110+, Firefox 105+, Safari 15.5+ (Android WebView 110+) |
| Customer App | Android 8.0 (API 26)+, iOS 14+ |
| Partner App | Android 8.0 (API 26)+; iOS 14+ from Phase 3 |
| API clients | OpenAPI 3.1; generated clients pinned to a released version |

**Rule CP-01** — The API is versioned and additive within a major. Clients must ignore unknown fields.
**Rule CP-02** — The website must degrade to a functional (if slower) booking flow on a 3G connection.

---

## 9. Observability & Maintainability

| # | Requirement |
|---|---|
| OB-01 | Structured JSON logs with `requestId`, `traceId`, `userId`, `role`, `branchId`. |
| OB-02 | OpenTelemetry traces across API → worker → vendor calls. |
| OB-03 | Prometheus metrics: RED for every service, USE for the infrastructure. |
| OB-04 | Grafana dashboards: API health, booking funnel, SLA breaches, notification delivery, settlement readiness, vendor health, coverage. |
| OB-05 | Centralised logs (Loki) with 30-day hot retention. |
| OB-06 | **Alerting** on: error rate > 2% (5 min), p95 latency breach (10 min), queue depth > 10,000, settlement job failure, reconciliation mismatch, payment webhook failure rate > 5%, disk > 80%, backup failure. |
| OB-07 | Every alert links to a runbook. |
| OB-08 | Health endpoints: `/health/live`, `/health/ready` (checks DB + Redis), `/health/ready?deep=1` (checks vendors). |
| OB-09 | Dependency health is surfaced on the Control Center dashboard. |
| OB-10 | Mean time to detect (MTTD) < 5 min for user-impacting failures. |
| OB-11 | Mean time to restore (MTTR) < 30 min for P1 incidents. |

### 9.1 Maintainability

| # | Requirement |
|---|---|
| MT-01 | Modular boundaries enforced by an architecture test in CI (`08` §2.3, MB-03). |
| MT-02 | No module may exceed 40 modules-equivalent in complexity; a module over 5,000 lines triggers a review. |
| MT-03 | Every module has a README, an owner and a public contract. |
| MT-04 | OpenAPI drift fails CI. |
| MT-05 | Coverage: ≥ 80% line coverage on domain modules; ≥ 95% on `pricing`, `commission` and `billing`. |
| MT-06 | Every public function in a domain module has a doc comment describing preconditions and invariants. |

---

## 10. Backup, DR & Continuity

| Scenario | Response | RTO |
|---|---|---|
| Single API instance failure | Load balancer routes to the healthy instance | < 30 s |
| Postgres primary failure | Failover to the replica (managed) or restore + WAL replay (self-hosted) | < 60 min |
| Redis failure | Cache rebuilds; queues resume from Postgres-backed outbox | < 30 min |
| Object storage failure | Restore from the provider's versioning; critical documents also stored in DB metadata | < 2 h |
| Full VPS loss | Provision a new VPS, restore from the backup, replay the WAL | < 2 h |
| Payment provider outage | Booking continues with `paymentMode = PAY_AFTER`; advance collection deferred | No outage |
| Maps provider outage | Pincode fallback; PostGIS still resolves service areas | Degraded |
| Telephony outage | In-app and web booking unaffected; callback queue | Degraded |
| SMS provider outage | Voice OTP fallback; WhatsApp fallback | Degraded |

**Rule DR-01** — A restore drill is executed monthly and its result recorded. A failed drill is a P1 engineering issue.
**Rule DR-02** — The disaster runbook is documented, rehearsed, and owned by a named engineer.

---

## 11. Capacity & Cost Envelopes

| Item | Monthly ceiling (Phase 2) | Lever |
|---|---:|---|
| Hosting (VPS + backups + storage) | ₹12,000 | Right-size after the load test |
| SMS | ₹4,000 | OTP + critical only |
| WhatsApp conversations | ₹2,500 | Template-first |
| Google Maps | ₹3,000 | Geocode caching, Distance Matrix batching |
| Push (FCM) | ₹0 | Free tier covers launch volume |
| Telephony | ₹6,000 | Includes toll-free minutes + recording |
| Email | ₹500 | Transactional + statements |
| **Total third-party** | **₹28,000** | Tracked as `integration_cost_estimate` |

**Rule CO-01** — Third-party spend is tracked per provider against this envelope and reviewed monthly. A provider exceeding 120% of its envelope for two consecutive months triggers a review.

---

## 12. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| OD-NFR-01 | Is the availability target 99.5% or 99.9% for the payment path specifically? | Engineering + Finance | Phase 1 |
| OD-NFR-02 | Which data residency commitment will we publish — India only? | Legal | Phase 1 |
| OD-NFR-03 | Do we need a formal SOC 2 or ISO 27001 readiness programme, and when? | Leadership | Phase 4 |
| OD-NFR-04 | What is the retention period for technician location history — 90 days proposed, or shorter? | Privacy | Phase 1 |
| OD-NFR-05 | Do we need a dedicated data protection officer / grievance officer from Day 1? | Legal | Phase 1 |
| OD-NFR-06 | Is 8-year retention of booking and financial records confirmed by the tax advisor? | Finance + Tax advisor | Before Phase 2 |

**Decisions registered elsewhere that bind this document.** None of the five below is an `OD-NFR-*` row
— they are owner decisions in `21` §7, listed here because §2.2 and §5.2 are where they bite:
`OD-DOC-32` (self-hosted, subset fonts under §5.2's `font-src 'self'`, with no named producer),
`OD-DOC-26` (no media column in `09` §4.3 and no public serving path, against §5.2's `img-src 'self'`),
`OD-DOC-34` (a third-party media host the owner has asked for that §5.2's `img-src` does not list —
annotated on the §5.2 side above, `DEC-07`),
`OD-DOC-30` (the colour palette, which is what §7's contrast-bearing usability claims rest on) and
`OD-DOC-31` (no documented dark-mode position, so US-03's "outdoor bright light" has no specified theme
answer). This table stays at six rows; the register total is `21` §1's, currently **231**.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.7 | 2026-10-21 | Security Owner + Eng Lead (platform-mode pass) | §5.1 gained the **Destructive-operation guard** control row: the platform mode decides whether a hard delete, `TRUNCATE` or data-destructive DDL is permitted; it is required at the **service layer and by bound database privilege**, because a check that lives only in a screen is not this control; soft delete and the code-defined retention purge continue to run. It is marked `[OPEN]` on both sides of the collision `38` §6.3 documents — an absolute production ban contradicts the erasure right §6.1 of this same document promises, which is `OD-DOC-40` scored as `19` `R-50`. **No existing target, threshold or control was weakened, and no legal conclusion is drawn here** (`00` §11). | §5.1 |
| 1.6 | 2026-10-21 | Security Owner + Engineering Lead (design-engineering structure pass) | **No target, threshold, period, control, limit or CSP directive was changed.** §5.2 gained one sentence and it is a security sentence: what may be **loaded** under these directives is decided by `36` §3, not by taste — a runtime injecting un-nonce’d styles fails `style-src`, an icon font or CDN component kit fails `font-src`/`script-src`, and any media origin not named above is blocked while `OD-DOC-34` stays open, which makes a CSP-failing library a production-time failure rather than a review comment (`LB-02`). §12’s register figure was re-measured from `21` rather than incremented: **224 → 231 rows, 45 blockers**. The six-row open-points table is unchanged, because the seven new rows belong to `14`, `35` and `36`, not to this document. | §5.2, §12, Revision History, header |
| 1.5 | 2026-10-21 | Security Owner + Engineering Lead (palette and storage pass) | **No target, threshold, period, control or CSP directive was changed.** §5.2 gained an `[OPEN]` annotation under the policy block recording that it is one side of `OD-DOC-34` `[BLOCKER]`: the owner has asked for Cloudinary as primary media storage with multiple providers and a super-admin selector, and `img-src 'self' data: blob: …` lists no such host, so third-party-served imagery renders in development and is blocked in production. The annotation names `24` §11 ("no bucket, prefix or object is publicly readable") as the mirror side, `16` §5.2 and `09` §4.3 as the other two things a CDN decision would move, and the registered recommendation — decide **per data class**, with `PERSONAL` job evidence off any public object store (`09` §8). Per `DEC-07` neither document was rewritten to fit the new instruction; the policy above stays as issued until the decision closes. §2.2's constraining-budgets note now cites `OD-DOC-34` next to `OD-DOC-26`, and §12's "decisions registered elsewhere" list grew from four rows to five. The register figure this document quotes moved with `21` §1: **220 → 224 rows, 43 → 44 blockers**. | §2.2, §5.2, §12, Revision History |
| 1.4 | 2026-10-21 | Engineering Lead + Security Owner (design-system and asset pass) | No target, threshold or control changed. Three notes added where the visual layer meets an NFR: §2.2 now states that **none of the client budgets has been measured on a real device**, that `32` §4's raster weight ceilings are *derived from* those budgets rather than verified against them, and that §5.2's `font-src 'self'` and `img-src 'self'` are what force self-hosted subset fonts and same-origin imagery (`OD-DOC-32`, `OD-DOC-26`); §7 now records that `US-07` cannot be satisfied by translation alone, because Odia has to render, and points at `30` §3 for the measured WCAG 2.1 AA evidence behind `12` §6.3 `A11Y-1`; §12 lists the four `21` §7 rows that bind this document without pretending to be new `OD-NFR-*` rows. `US-03`'s bright-light claim is flagged as having no theme answer while `OD-DOC-31` is open. | §2.2, §7, §12, Revision History |
| 1.3 | 2026-10-21 | Engineering Lead + QA Lead | Audit pass 3 (continued). Four `[OPEN]` annotations added where this document is one side of a registered conflict: the MFA **scope** in §5.1 (`OD-DOC-20`, which accounts must use a factor — `OD-SEC-01` decides only which factor), the access-review cadence in §5.3 and the erasure definition in §6.1 (`OD-DOC-21`, `OD-DOC-23`), and a pointer before §5.2 to the production-access rule §5 does **not** contain (`OD-DOC-22`). §2.1's latency table gained the Note column its three longest rows were already writing into, which had been splitting those cells. No target, threshold, period or control changed; none of the four conflicts is decided and §5.1's internal-staff scope is explicitly not treated as the answer for partner-side money approvers. | §2.1, §5.1, §5.2, §5.3, §6.1, Revision History |
| 1.2 | 2026-10-21 | Security Owner + Engineering Lead | Audit pass 3 (continued). This document had never been re-audited after pass 2, and three gaps in §5/§6 turned out to be **cross-document conflicts rather than local omissions**, so they are annotated and registered rather than silently fixed here: the MFA **scope** in §5.1 is stated four different ways across `README` §11, `24` §12.3 and `28` §3.7 and exempts every partner-side settlement approver, because those tokens are `branch:settlement:*` and their holders are not internal staff (`OD-DOC-20`); the access review is quarterly in §5.1/§5.3 and monthly in `19` §4.2 IC-03, which `26` §6.2 cites for the auditability promise (`OD-DOC-21`); and `26` §4.5 item 9 assigns **production access approval** to `13` §5, which contains no such rule — a placeholder note now says so out loud instead of the citation pointing at nothing (`OD-DOC-22`). §6.1's erasure row now states that anonymisation is defined only against the live database while `16` §5.6 retains WAL and monthly copies (`OD-DOC-23`). **No control's substance was changed**, and none of the four is decided. | §5.1, §5.3, §6.1, Revision History |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Added the MFA requirement for staff with financial or administrative permissions, the MFA factor open decision, and the full VPS planning envelope with the backup-storage separation note. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
