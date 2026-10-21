# 38 — Platform Mode (`TESTING` / `PRODUCTION`) and the Data-Lifecycle Guard

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-38 |
| Version | 1.0 |
| Status | **PROPOSED** — not approved; five owner decisions open (§13) |
| Owner | Engineering Lead (mechanism) + Founder (the decision to adopt it) |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `01` §4.11, `03` §3.2/§3.3/§5, `08` §6.1/§7, `09` §4.15/§6, `10` §4.3/§6.1/§11, `13` §5, `15` §16, `16` §5, `20` §8/§9, `21` §7, `22` ADR-026, `24` §9, `25` §5/§9, `27` §4, `29` §4/§17 |

---

## 1. Why This Document Exists

The platform owner gave the following direction on 2026-10-21, recorded here as `[REPORTED]` and
quoted as issued:

> "another think need that mode of platform like 'Testing' and 'Production'. if have Testing or Test
> mode then will be all data save in database, default mode is Test, when make production then will be
> need super admin email OTP verification. This feature why need ?. This feture data delete protect
> like test model all data will be deleted but production mode data not able to delete from database.
> so add this instruction in docs then will be move phase 1 of implements."

Read as an engineering requirement, that paragraph contains **five** distinct assertions, and this
document treats each of them separately because they are not equally safe:

| # | Assertion in the instruction | Status here |
|---|---|---|
| 1 | The platform has two modes, `TESTING` and `PRODUCTION`. | Specified — §2, §3 |
| 2 | Test-mode data is saved in the **same database**, not a scratch store. | Specified, with the consequences spelled out — §8. **This is the part that needs the most engineering care**, because the rest of the suite assumes one schema, one numbering series and one statutory record set. |
| 3 | The default mode is `TESTING`. | Specified — §3 PM-03. **It is also the riskiest word in the instruction** (§10): a default that is safe for a developer machine is unsafe for a live deployment. |
| 4 | Promotion to `PRODUCTION` requires super-admin **email OTP** verification. | Specified — §5. Registered as dependent on an **unprocured provider** and against an undecided MFA factor (`OD-DOC-42`). |
| 5 | `TESTING` data may be deleted; `PRODUCTION` data may **not** be deleted from the database. | Specified as a *taxonomy*, not as a blanket rule — §6. Taken literally this collides with three existing requirements, and §13 registers that collision rather than resolving it. |

**What this document decides:** the vocabulary, the state machine, the transition ceremony, the
definition of "delete", the enforcement layers, the marking of test-origin data, and the rules a
first implementation must satisfy so that the protection is real rather than decorative.

**What this document does not decide:** it does not approve the feature. Per `22` ADR-026 it is
`Proposed`; per `01` §8 a new Must requirement in v1.0 needs a charter amendment; per `26` §3.2 an
item outside §3.1's scope list needs a written change to the executed agreement. It also creates no
code, no directory, no table in a live database and no claim that anything is implemented
(`22` ADR-025-02 — no application source code exists in this workspace).

---

## 2. The Name, and the Four Things It Is Not

The instruction uses the word "mode", which the suite already uses for four other things. Every one
of them is a plausible misreading of this feature, and three of them would be implemented instead of
it. §2 of `20` carries the disambiguation into the glossary; this table is the canonical statement.

| Concept | Where it lives | What it controls | Is it this feature? |
|---|---|---|---|
| **Deployment environment** — `local`, `dev`, `staging`, `prod` | `08` §6.1, `16` §1/§2, `15` §16 | Which **machine and database instance** the code runs against, and whose data is in it | **No.** An environment is infrastructure. A mode is a row in a database. `prod` can in principle be running `TESTING` mode — that is precisely the hazard in §10 |
| **Feature flag** — `feature_flag` table, server-side targeting | `08` §7, `16` §4.4, `20` §8 | Whether an unfinished or risky behaviour is switched on for a subset of users, branches or percentages | **No.** A flag targets *who gets a behaviour*; the mode targets *what may be destroyed*. A mode implemented as a flag is a flag an operator can flip in the dashboard without a ceremony |
| **Provider sandbox / test credentials** — Razorpay test mode, SMS/WhatsApp test numbers | `24` §5/§8/§7, `11` §10 `INT-01`, `15` `TE-03` | Whether an outbound call reaches a real vendor with real money | **No, but it is coupled** — §8.4 (PM-15). A mode that does not bind the provider credentials leaves a test deployment able to charge a real customer |
| **Tenant / branch scope** | `ADR-019`, `02`, `03` §6 | Which rows a given actor may see inside one shared schema | **No.** The mode is **platform-global and exactly one per database**. There is no such thing as a branch in `PRODUCTION` mode while another branch is in `TESTING` (PM-06) |
| **Platform mode** — this document | `09` §4.15 (`platform.platform_mode`), `10` §4.3, `03` §3.2/§5 | Whether destructive data operations are permitted, how data origin is stamped, and which ceremony an actor must pass to change it | **Yes** |

> **Why the distinction is load-bearing, not pedantic.** `15` `TE-02` says "a nightly job resets `dev`
> and reseeds `staging`", `15` `TD-03` gives each test a truncated-and-reset schema, and `15` `TD-04`
> forbids production data in tests. If the new mode is read as "the `dev`/`staging` environment", then
> those existing rules already implement it and this document is redundant. The owner's stated purpose —
> *"data delete protect"* — is a **runtime, server-enforced guard on one database**, which none of the
> environment rules provide. §3 therefore states the mode as a first-class, database-resident fact.

---

## 3. Rules

Rules `PM-01`…`PM-24`. They are written to be implementable and testable; a rule that cannot be
asserted in `15` is marked as guidance.

| # | Rule |
|---|---|
| PM-01 | **Two modes, exhaustive.** `TESTING` and `PRODUCTION`. There is no third mode, no per-request override and no per-branch mode. |
| PM-02 | **The mode is a row in the database, not an environment variable.** The single row `platform.platform_mode` is the only authority. An `APP_MODE`-style variable may *seed* the row on first boot; the moment it exists, the variable is ignored. Reason: two surfaces disagreeing about the mode is worse than no mode, and a variable is invisible in an audit. |
| PM-03 | **Default is `TESTING`.** If no row exists, the effective mode is `TESTING` — the owner's "default mode is Test". This default is safe on a developer machine and **unsafe on a live deployment**, which is why PM-04 exists; `README` §12.5's rule that a check must be observable applies here. |
| PM-04 | **A deployment may not accept staff or customer traffic while `prod` infrastructure runs `TESTING` mode** without a recorded, time-boxed bootstrap exception that itself carries the §5 ceremony. The check belongs in the `16` §5 pipeline and the `29` §4 gate, not in a person's memory (§10). |
| PM-05 | **Only `SUPER_ADMIN` may request a transition** — no `ADMIN`, no `OPERATOR`, no support role, no API key, no service account. Requested by the owner; consistent with `03` §3.3. |
| PM-06 | **Exactly one mode per database.** `ADR-019` puts every tenant in one shared schema discriminated by `branch_id`; the mode sits **above** that discrimination and is never a scope filter. |
| PM-07 | **Every transition writes two durable records in the same transaction**: an append-only row in `platform.platform_mode_transitions` (`09` §4.15) and a hash-chained `audit_events` row (`09` §4.14, `13` §5 Audit). A transition that is not audited did not happen. |
| PM-08 | **A request reads the mode once, at entry**, and carries it for its whole unit of work. A transaction may never straddle two modes; a mid-transaction flip is not allowed to produce half-guarded writes. |
| PM-09 | **`PRODUCTION` blocks destructive data operations** initiated by an operator or the application: hard `DELETE` on business/financial rows, `TRUNCATE`, `DROP` of a table or a data-bearing column, and the Redis flush commands `25` §12 already forbids. The full taxonomy is §6. |
| PM-10 | **The scheduled-retention purge allow-list runs in both modes.** It is defined **in code as a named job list**, never assembled in a dashboard, because a purge list an operator can edit is a delete button with a schedule attached. |
| PM-11 | **Statutory erasure is neither silently allowed nor silently blocked.** The suite already promises DPDP erasure (`09` §6, `03` §7.3 customer state `ACTIVE ⇄ DELETED`, `01` §5 "consent, purpose limitation, retention, erasure"). PM-09's prohibition and that promise cannot both be absolute. §6.3 names the two lawful readings; `OD-DOC-40` decides between them. **No implementation may pick one on its own.** |
| PM-12 | **Origin is stamped on write.** Every row inserted while mode = `TESTING` carries `record_origin = 'TEST'`; while `PRODUCTION`, `'LIVE'`. Column definition in `09` §4.15; the write is in the repository layer so no module can forget it. |
| PM-13 | **`record_origin` is write-once.** It is never updated to launder a test row into a live one, and it is excluded from every unique-key business constraint so that synthetic and real rows can coexist without colliding. |
| PM-14 | **`TESTING` must not consume a live statutory document sequence.** `FR-CMP-05` requires gapless invoice/statement numbering per entity and fiscal year, and `ADR-015` makes those records immutable; a test invoice written into the production series cannot be removed without breaking the gap the tax review looks for. §8.3 gives the two implementations; `OD-DOC-41` chooses. |
| PM-15 | **The mode binds provider credentials at boot.** In `TESTING`, adapters must present **test/sandbox credentials and refuse a live capture**; in `PRODUCTION`, an adapter configured with sandbox credentials must fail to start. Extends `11` `INT-01` (adapters declare `isConfigured()`). Symmetric, because "test mode" that can move real money and "production" that silently runs on mocks are the same incident viewed from two directions. |
| PM-16 | **The effective mode is displayed on every staff surface and in every export header**, and while the mode is `TESTING` a persistent, non-dismissible indicator is shown on customer and technician surfaces too. This document states the requirement only; the component that renders it is named in `12` §6.2 and placed by `37` `CA-00`, **not here**. |
| PM-17 | **Reports, settlements and dashboards read `LIVE` origin only** unless an operator explicitly opts into `TEST` rows for a named diagnostic run — and that run is labelled and audited. A settlement statement computed over test bookings would be issued to a partner as real. |
| PM-18 | **Promotion (`TESTING` → `PRODUCTION`) requires a freshly verified email OTP** sent to the super-admin address of record, plus a non-empty reason (`03` `FL-08` pattern). The ceremony is §5. |
| PM-19 | **Demotion (`PRODUCTION` → `TESTING`) requires at least the same ceremony.** The owner's instruction names a gate for going *into* `PRODUCTION` but not for coming *out of* it; since `PRODUCTION` is the protected state, an ungated demotion deletes the protection (§13, `OD-DOC-42`). Until that row is decided, PM-09's guard is advisory. |
| PM-20 | **Self-approval is blocked and dual control applies where the suite already requires it.** `03` §3.3: Super Admin cannot approve their own action. A transition therefore needs a second `SUPER_ADMIN`/`ADMIN` account to acknowledge the pending change inside its validity window, matching `24` §12's break-glass dual-control pattern. |
| PM-21 | **OTP mechanics:** single-use, stored only as a hash (`13` §5 already lists OTP among values redacted from logs), short TTL, attempt-capped, rate-limited per identity and per IP (`10` §8), lockout on exhaustion (the `13` §5 five-failed-attempt lockout pattern), and re-send cooldown. |
| PM-22 | **A transition is a planned operational act:** taken in the deployment window of `29` §7 under the release authority of `29` §2, with a verified backup and a current restore
drill (`13` §10, `16` §5.6, `19` `R-05`) **before** promotion, and with the on-call roster aware. The mode is the highest-consequence configuration value in the platform and should not be reachable from a phone in a corridor. |
| PM-23 | **The guard fails closed.** An unreadable mode row, a missing row under `prod` infrastructure, or an unresolvable origin stamp on a row a delete targets all resolve to `block` + alert, never to `allow`. A guard that fails open is a guard that is off, discovered at the worst possible moment. |
| PM-24 | **The `platform_mode` row is not deletable and its UPDATE path is a stored procedure**, restricted to the transition service — the same mechanism `09` `DB-03` uses to keep `commission_ledger` append-only. Nothing else, including a migration, may delete it. |

---

## 4. State Machine

The mode has exactly two states and two guarded transitions. "Guarded" means the §5 ceremony must
complete; the guard is not a UI confirmation.

```mermaid
stateDiagram-v2
    [*] --> TESTING: PM-03 default when no row exists
    TESTING --> PRODUCTION: promote (PM-18 email OTP + PM-20 dual control + PM-22 window)
    PRODUCTION --> TESTING: demote (PM-19 same or stronger ceremony)
    note right of PRODUCTION: PM-09 guard active: no operator hard delete
    note right of TESTING: guard inert, data may be purged, reseeded, truncated
```

| From | To | Event | Pre-conditions (all must hold) | Effects |
|---|---|---|---|---|
| — | `TESTING` | bootstrap / no row | none | Guard inert. `13` §5 audit still runs |
| `TESTING` | `PRODUCTION` | `promote` | valid unexpired OTP verified against the super-admin address of record; second-account acknowledgement; non-empty reason; current verified backup; zero pending `TEST`-origin rows **or** the §8.3 disposition recorded; provider credentials verified live-mode (`PM-15`); `OD-DOC-40`/`OD-DOC-41` closed | Guard armed; subsequent inserts stamped `LIVE`; mode change effective for new requests (`PM-08`) |
| `PRODUCTION` | `TESTING` | `demote` | **`[OPEN]`** — `OD-DOC-42`: same OTP ceremony, plus (recommended) a second reason field naming the incident that justifies un-protecting live data | Guard disarmed. **This is the most dangerous transition in the platform** and the one the instruction did not cover |

> **There is no `PRODUCTION` → `PRODUCTION` edit and no "pause the guard" state.** If a maintenance
> task needs a destructive operation, it runs the named purge job (`PM-10`) or it follows the
> exception path in `25` §5/§9, which is audited and time-boxed. A guard with a quiet off-switch is
> not a guard, and the suite already refuses quiet off-switches elsewhere: `19` `R-05` and `13` §10 make a **restore drill**, not a backup,
the thing that is verified, and `25` §12 states flatly that `FLUSHDB` is never the answer.

---

## 5. The Transition Ceremony

The owner specified the control: *"when make production then will be need super admin email OTP
verification."* This is the specification of that control, in the shape the rest of the suite's
authentication material expects (`10` §3, `13` §5, `24` §9).

| Step | Action | Rule | Failure handling |
|---|---|---|---|
| 1 | `SUPER_ADMIN` requests the transition from the Control Center and supplies a **reason** | `PM-05`, `PM-22`; mirrors `03` `FL-08` | `403 PERMISSION_DENIED` for any other role; `400 VALIDATION_ERROR` on empty reason |
| 2 | Server checks the **pre-conditions** table in §4 and returns a consequence summary | `13` `US-05` — no destructive action is a single unlabelled tap | `409 MODE_PRECONDITION_FAILED`, listing which condition failed |
| 3 | A **second account** acknowledges the pending transition | `PM-20`, `03` §3.3 | The request expires unacknowledged; audited as an attempt |
| 4 | The OTP is dispatched to the super-admin address of record — the address stored in the platform's own configuration, **not** typed into the request | Accepting a caller-supplied destination turns the ceremony into a forwarding service. Address-of-record is set by the same guarded path | `424 EMAIL_CHANNEL_UNAVAILABLE` — see §5.1 |
| 5 | The actor enters the code within its TTL | `PM-21` | `OTP_EXPIRED` / `OTP_INVALID`; 5 failures → lockout (`13` §5 pattern); each attempt is an authentication event (`FR-ID-09`) |
| 6 | The transition commits: mode row updated, `platform_mode_transitions` appended, `audit_events` chained, cache invalidated | `PM-07`, `PM-24`, `08` §10 caching rule | Any step failing rolls the whole transaction back; the mode does not half-change |
| 7 | The new mode is **re-read from the database** and displayed back, and the surfaces' indicator updates | `PM-16`, `PM-23` | A mismatch between the write and the read is a P1 incident, not a retry |

### 5.1 What the ceremony depends on, and what is not yet bought

The control is email, and **this suite has no email provider.** `24` §3 registers P-06
(transactional email) as **NOT YET PROCURED**, `24` §15 row **A-06** records the account as **NOT
STARTED** with domain verification, SPF/DKIM/DMARC outstanding, and `OD-MAIL-01` (`24` §18) is the
unmade selection. Two consequences that must be decided rather than discovered:

1. **A hard dependency on an unpurchased service.** If email is the only way to promote, the platform
   cannot go live until A-06 completes — and cannot *leave* live if it is also the demotion gate.
2. **Deliverability on a domain with no reputation yet.** An OTP that never arrives is not a security
   control; it is an outage with a lockout attached.

`24` §9's own delivery ladder and `24` §8.7's OTP ladder (SMS → voice → in-app challenge) exist for
*customer* OTP. Whether a staff **step-up** may use the same ladder, must use email only, or should use
the TOTP that `24` §12 already assumes for break-glass, is the factor half of `OD-DOC-42` — and it
intersects `OD-SEC-01`, which is this suite's still-open decision about **which factor type staff with
administrative permission use at all** (`13` §5.1). Documenting "email OTP" here does not settle
`OD-SEC-01`; it adds a second, narrower question about the highest-privilege action in the platform.

### 5.2 A step-up is not a login

`13` §5 requires multi-factor for internal staff holding financial or administrative permission, and
`OD-DOC-20` records that the *scope* of that rule is stated four different ways across `13`, `README`,
`24` and `28`. The mode ceremony is deliberately **not** delegated to that undecided scope: it is a
per-action step-up that applies to whoever holds `SUPER_ADMIN`, whatever the MFA policy eventually
says. That keeps this feature shippable even while `OD-DOC-20` stays open — and it is the only part of
the authentication surface in this document that does not depend on an unmade decision.

---

## 6. What "Delete" Means

*"production mode data not able to delete from database"* — the intent is **irreversible loss is
prevented**. A literal `BEFORE DELETE` trigger cannot express that intent, because the platform must
also delete things the law and its own retention schedule require it to delete, and because some
deletions are already load-bearing for correctness. The four classes are distinct and get distinct
rules. **This taxonomy is the actual engineering content of the feature.**

### 6.1 The taxonomy

| Class | Example | `TESTING` | `PRODUCTION` | Basis |
|---|---|---|---|---|
| **A. Operator hard delete** | `DELETE FROM bookings WHERE …`; the `delete` verb's hard-delete path; bulk "clear demo data"; `TRUNCATE`; dropping a data-bearing column in a migration `down()`; Redis `FLUSHDB` (`25` §12) | **Allowed** — this is what the mode is for | **Blocked** (`PM-09`) → `403 MODE_PROTECTED` | The owner's requirement, stated precisely |
| **B. Soft delete** | `deleted_at` set on a business entity; `is_active = false` on configuration | Allowed | **Allowed** — unchanged | `03` §3.2 already defines the `delete` verb as *soft delete only*; `09` §2 defines the `deleted_at` / `is_active` pattern. The row survives, so the protection holds. **A soft delete in `PRODUCTION` is not a violation of this feature; treating it as one would break the existing UI/API contract** |
| **C. Obligation-driven erasure** | DPDP Act 2023 erasure of a data principal's PII after the statutory window; a court or regulator instruction | Allowed | **`[OPEN]` — `OD-DOC-40`** | `09` §6 retention row "Customer PII on erasure request — Deleted after statutory retention — DPDP Act 2023"; `01` §5 privacy line; `03` §7.3 customer state `ACTIVE ⇄ DELETED (DPDP erasure, after statutory retention)`; `ADR-024` requires professional review before production on exactly this class |
| **D. Scheduled retention purge** | `notification_deliveries` 90 days; `webhook_inbox` 30 days; technician location history 90 days; call-recording references; `audit_events` payload 24 months with partition archiving | Allowed | **Allowed, via the code-defined allow-list only** (`PM-10`) | `09` §6 partitioning and retention tables — these purges *are* the documented design, and `09` §6 is explicit that purging the webhook inbox never deletes a payment |

### 6.2 Why class D is not a loophole

Class D looks like class A wearing a schedule. It is not, and the difference is what makes the guard
implementable:

| | Class A (blocked in production) | Class D (permitted) |
|---|---|---|
| Who chooses the rows | An operator, in the moment, by a filter they typed | Code, by a predicate reviewed in a pull request and versioned |
| Scope | Arbitrary tables, arbitrary `WHERE` | A **named job**, an allow-listed table, an age predicate it cannot exceed |
| Reversibility | The operator can undo it (backup, WAL) | Not intended to be undone; it is the policy executing |
| Auditability | Explained by a reason string | Explained by a job identity, a row count and the policy version |

So: **the guard is not "no deletes in production"; the guard is "no delete that was not written in
code and reviewed before it ran."** That sentence belongs in `14` §11 and `27` §4 as a coding rule,
and it is the reason a `DELETE` arriving over the wire from a dashboard is categorically different
from the same SQL issued by `purge_notification_deliveries()`.

### 6.3 The class C conflict, stated without a hidden answer

PM-11 refuses to resolve this, and the refusal is deliberate. The two lawful readings:

| Reading | What it means | What it costs |
|---|---|---|
| **(i) Protection yields to statute** | Erasure runs in `PRODUCTION` through the same allow-list mechanism as class D, gated by the DPDP routine, dual-controlled and audited | "Production data can never be deleted" becomes false as written; the guard's promise must be restated as "no *arbitrary* deletion" |
| **(ii) Protection is absolute** | Nothing deletes in `PRODUCTION`; erasure requests are queued for a future state (archive-and-exclude, or a controlled off-platform process) | The platform carries a stated inability to satisfy a statutory erasure request, which `ADR-024` says is a legal question this suite must not answer, and `01` §5 promises erasure as an NFR |

Neither reading may be coded by an implementer as a compromise (`27` §4). `OD-DOC-40` asks the Founder
and the compliance owner to pick, with counsel (`24` §16's professional-review boundary), **before** any
`09` guard trigger or `13` §5 control is written.

---

## 7. Where Enforcement Lives

A mode that is only checked by a screen is not a control: the same operator can reach the database
with a console, and an AI agent or a script can reach it with a query. This is the point where
`22` `ADR-013` (the backend is the only source of truth) and `19` `R-42`-family concerns about
access held by the development partner are supposed to bite. The guard therefore has four layers,
and **the lower layers are the control; the upper layers are ergonomics.**

| Layer | Mechanism | Catches | Weakness |
|---|---|---|---|
| **L1 UI** | The destructive action is not offered; consequence summary shown (`13` `US-05`) | Honest mistakes | Trivially bypassed. **Never the only layer** |
| **L2 API / service** | The transition-guarded command handlers reject with `403 MODE_PROTECTED`; every mutation reads the mode once (`PM-08`) | Any client, any generated client, any script going through the API | Bypassed by direct database access |
| **L3 database role and trigger** | The application connects as a role **without** `DELETE`/`TRUNCATE` on guarded tables; guarded purge jobs connect as a separate role with `DELETE` on their allow-listed tables only; a trigger refuses data-destructive DDL from the migration role in `PRODUCTION` | Direct SQL, psql, a leaked credential, an agent with a connection string | Requires the role split, which is **new**: the suite currently implies one application role (`14` §11, `16` §5). Registered as part of `OD-DOC-43` |
| **L4 CI and pipeline** | A migration whose `down()` drops a data-bearing object fails review unless annotated and paired with an exception recorded through `25` §11 (`14` `DB-05` already demands two deprecation releases before a destructive schema change); `16` §5 blocks a `prod` deploy that would boot in `TESTING` without a bootstrap exception | Silent schema loss, wrong-environment deploys | Only as good as the reviewer |

> **The role split is the honest answer to "why is this hard."** Read `PM-09` as "no `DELETE`
> privilege" rather than "an `if` statement", and the feature becomes a database design question with
> four connection identities instead of one — which touches `14` §11 (secrets), `16` §5 (deploy),
> `13` §5 (least privilege), `24` §12 (credential custody) and every runbook in `25`. `OD-DOC-43`
> records that a mode guard implemented at L2 alone gives the owner a protection that exists on paper
> and disappears at `psql`, and asks which layer the Founder is actually paying for.

---

## 8. Test Data in the Same Database

*"if have Testing or Test mode then will be all data save in database"* — accepted as a requirement,
with its consequences made explicit. Storing test data in the live schema is a legitimate and common
choice (it exercises real constraints, real indexes and the `09` §7 index catalogue rather than a
toy schema), **and** it imports four problems that the mode flag does not solve by itself.

### 8.1 Origin marking

`record_origin` (`'TEST'` | `'LIVE'`, `PM-12`/`PM-13`) is stamped in the repository layer at insert.
Without it, a promotion to `PRODUCTION` cannot tell a seeded demo booking from a customer's real one —
and `17` P0-08/P0-09 and `29` §14's city-activation checklist both **require** seed data: the initial
catalogue, price book, zones, service areas and a technician pool. Some of that seed content is
legitimately live configuration (`09` §8's `INTERNAL` class — `roles`, `permissions`,
`workflow_templates`, catalogues), and some of it is fake *transactions*. They must not be marked the
same way, so:

| Data created while `TESTING` | Mark | Why |
|---|---|---|
| Synthetic bookings, jobs, tickets, ratings, reviews, call logs | `TEST` | Fake transactions must never enter a real report or settlement (`PM-17`) |
| Test customers / technicians / partner orgs created for rehearsal | `TEST` | They would otherwise appear in a partner's roster and, worse, in a commission accrual |
| Master data (states, cities, branches, zones, service areas), catalogue, price book, workflow templates | **Live configuration, not `TEST`** — `09` §8's `INTERNAL` class already covers this | It is the intended production content, entered early. Excluding it from `PM-17` is what makes the marker usable |
| Uploaded media produced during testing | `TEST` origin on the referencing row | Interacts with `OD-DOC-26`/`OD-DOC-34`: media storage and its columns are undecided, and a test upload routed to a production CDN is a real cost and a real leak |

### 8.2 Contamination, which is what the marker buys

`PM-17` excludes `TEST` rows from dashboards, `FR-RPT` reports, commission accrual (`07` §7), settlement
statements (`09` `DB-03`/`DB-04`), reconciliation and every `15` golden-path assertion made in a live
database. The failure it prevents is concrete and expensive: **a weekly settlement statement computed
over test bookings is issued to a partner as a real invoice** (`07` `STL-01` makes it immutable once
issued, and `FR-CMP-05` numbers it as a GST document). Without origin marking there is no way to
detect that after the fact except by reading every row's story.

### 8.3 The numbering hazard

`FR-CMP-05`: every invoice, statement and credit note is **gapless per entity and fiscal year**.
`ADR-015`: those records are append-only. Put those two together with "all data saved in the same
database in Test mode" and the conflict is arithmetic: a test invoice consumes a number in the live
FY series, and deleting the test invoice later — which is the entire purpose of `TESTING` mode — leaves
a hole in a series the tax review is designed to inspect. Options, with `OD-DOC-41` as the decision:

| Option | Mechanism | Cost |
|---|---|---|
| **(a) Do not issue in `TESTING`** | The `issue` verb (`03` §3.2) is refused in `TESTING`; completion flows stop before the invoice step and evidence is generated as unsigned drafts | Test mode stops exercising the money path — the most-tested part of this platform (`15` §5) |
| **(b) A separate test series** | A physically distinct sequence and a visibly non-statutory prefix (`T-INV-…`) that can never be mistaken for `INV-<FY>-…`; test rows purged freely | Needs `09` sequence definitions, a `12`/`13` label rule so a `T-` document cannot be emailed as an invoice, and a §4 promote-time check |
| **(c) Issue for real and never purge financials** | Test documents become permanent members of the series; purge is allowed only for non-financial tables | Contradicts the feature's stated purpose, and `19` `R-45`-adjacent: statutory documents that prove nothing |

Recommendation is **(b)**: it preserves the gapless property for live documents, keeps the money path
testable, and keeps the purge usable. It is **not** adopted here; it is a Founder + Accountant + tax
advisor decision (`ADR-024`).

### 8.4 Money and providers

`PM-15` binds the mode to provider credentials: sandbox credentials under `TESTING` and a refusal to
capture a live payment there; a refusal to boot `PRODUCTION` on sandbox credentials. `24` §19 `CN-1`
already states that every nightly run hits the provider's sandbox or test mode and that production
credentials are never used in an automated run, and `15` `TE-03` mandates deterministic mock mode for
vendor adapters in test environments. What is *new* here is the guarantee that a credential set is
bound to a runtime mode rather than to a deploy target, because no rule in `24` currently links the
two. The failure without it is a test run charging a real customer's UPI handle, or a
live deployment quietly not taking money.

### 8.5 What happens to test rows at promotion

§4's promote pre-condition requires either zero `TEST`-origin transaction rows or an explicit recorded
disposition. In practice the safe order is: rehearse in `TESTING`, **purge `TEST` rows** while still in
`TESTING` (where purging is permitted and easy), verify counts, then promote. Promoting with test rows
still present and relying on `PM-17` exclusion is a standing correctness tax on every future report.

---

## 9. The Indicator

Requirement only, deliberately minimal:

| Rule | Statement |
|---|---|
| PM-16 | The effective mode is visible wherever a staff user can act, on every screen, in every export header, and in every generated document's metadata. While `TESTING`, customer and technician surfaces carry a persistent, non-dismissible indicator. |
| — | **No component is named here.** `37` `CA-00` forbids adding a component name outside `12` §6.2, and `OD-DOC-29`/`OD-DOC-37` record that this suite still has no screen → route → permission join (`OD-10-06`), so a new admin surface cannot be expressed properly yet. The indicator is therefore specified as a requirement in `01` §4.11 and `13` §5, and the Control Center screen that hosts the transition control is **not** invented here. |
| — | The indicator must be legible in the palette that exists (`30` §3) and must not depend on colour alone `12` §6.3 accessibility rules — a badge that reads "TEST" in text, not merely an amber dot. |

---

## 10. The Default Hazard

`PM-03` implements "default mode is Test". Consider what happens on a real deployment: the application
is deployed to the production VPS (`17` P0-05, `16` §5), the database is migrated and seeded (`17`
P0-06), **and nobody has run the §5 ceremony yet — because there is nothing to promote from.** The row
does not exist, so the effective mode is `TESTING`, so the guard is off, so the freshly provisioned
system holding the first real customer data is the one thing this feature exists to prevent.

The default is still correct — it is the right default for `local` and `dev`, and it is what the owner
asked for. What has to accompany it is `PM-04`: a **machine-checkable boot precondition**, not a
remembered step.

| Check | Where | Outcome |
|---|---|---|
| Is this `prod` infrastructure? | `16` §5 deploy target inventory; the `08` §6.1 environment label | Decides which rule applies |
| Does `platform.platform_mode` exist, and what does it say? | Read at startup, before traffic | Absent or `TESTING` on `prod` → refuse to serve staff mutations and page on-call (`PM-23` fail-closed) |
| Is there a recorded bootstrap exception? | `25` §11 runbook style, time-boxed, dual-controlled | The only lawful way for `prod` infrastructure to run `TESTING` during initial load; it expires |
| Pipeline assertion | `16` §5, `29` §4 gate item (§12) | A deploy that would leave `prod` in `TESTING` without an exception fails the build rather than the day |

---

## 11. Canonical Homes

`DEC-01` — one copy of each fact. This document owns the **behaviour**; it points at the owners of
everything else. Nothing below is a duplicate specification, and if two of these ever disagree,
`22` §1 rule `ADR-07` says the ADR wins and the document is corrected.

| Fact | Owner | What `38` contributes |
|---|---|---|
| Whether the feature is required at all, and its Must/Should priority | `01` §4.11 (`FR-MODE-01`…`08`) | The wording of each requirement; `01` §8's charter-amendment route |
| Columns, constraints, the mode table and the transition history | `09` §4.15 + rule `DB-25` | The semantics the columns must express, and the `record_origin` addition |
| Which roles and verbs are affected; what `delete` means | `03` §3.2/§3.3 + `FL-09` | The reason the existing soft-delete contract is preserved (§6.1 class B) |
| Routes, payloads, error codes | `10` §4.3, §6.1 | The pre-conditions each route must enforce; the reason a route-only guard is insufficient (§7 L2 vs L3) |
| The security control and its test | `13` §5.1 | The failure-closed and displayed-mode rules |
| Deployment order, boot precondition, role split | `16` §5 | The `PM-04` assertion |
| Test data rules | `15` §16 (`TE-06`) | Origin marking as a test-data requirement |
| Who runs a transition, and what to do when the guard blocks something legitimate | `25` §2, §11, §12 | The ceremony as a runbook |
| What an AI agent may and may not write | `27` §7, §9, §12 | The rule that an agent must implement the guard at L2 **and** L3, and must not invent a class-C exception |
| Release evidence | `29` §4, §17 | The gate items that make "protected" a checked claim |
| Whether this is inside the fee | `26` §3.1/§3.2 | The statement that it is an addition, not an inclusion |

---

## 12. Cost of Delay and Sequencing

| Order | Act | Owner | Gate it blocks |
|---|---|---|---|
| 1 | Close `OD-DOC-40` (statute vs absolute protection) | Founder + compliance owner (`ADR-024`) | Any `09` trigger or `13` §5 control |
| 2 | Close `OD-DOC-41` (test rows vs statutory numbering) | Founder + Accountant + tax advisor | The first invoice-sequence migration |
| 3 | Close `OD-DOC-42` (demotion path + factor, incl. the email-provider dependency) | Founder + Security Owner (`OD-SEC-01`, `OD-MAIL-01`) | The transition service and any `git init` that scaffolds it |
| 4 | Close `OD-DOC-43` (enforcement layer and DB role split) | Eng Lead + DevOps | `14` §11, `16` §5, the connection configuration |
| 5 | Close `OD-DOC-44` (indicator placement, pending `OD-10-06`) | Product + Design | The Control Center surface |
| 6 | Adopt or reject `ADR-026`, and amend `00` §14 / `26` §3 | Founder | The whole feature |

**Sequencing against the delivery plan (`17`).** `OD-DOC-38` (`[BLOCKER]`, the backend framework) still
gates any repository scaffold and any `git init` — `38` cannot be implemented before that is decided,
because the guard lives in the backend and its migration tool. Beyond that, `PM-12`/`PM-13`
(`record_origin`) must exist **before the first seeded booking**, or every pre-existing row is
origin-unknown and `PM-17` cannot exclude it. `17` places the repo, environments and seed data in
Phase 0, so the honest reading is: this feature is **Phase 0 work with Phase 1 consequences**, not a
Phase 1 feature. A "move to Phase 1" that starts by scaffolding a backend without `OD-DOC-38` closed
and without the origin column in the first migration buys two repairs instead of one.

---

## 13. Open Decisions Created by This Document

Registered in `21` §7 as `OD-DOC-40`…`44` (two `[BLOCKER]`, two `[IMPORTANT]`, one `[NICE]`). In one
line each, with the fuller statement in `21`:

| ID | Sev | Question |
|---|---|---|
| `OD-DOC-40` | **BLOCKER** | Does the production delete-protection yield to DPDP statutory erasure, or is it absolute? §6.3's two readings cannot both be coded |
| `OD-DOC-41` | **BLOCKER** | How do `TESTING`-origin transactions coexist with gapless statutory document numbering, and what is purged, frozen or issued before promotion? §8.3 |
| `OD-DOC-42` | IMPORTANT | Is demotion gated as hard as promotion, and by which factor — email OTP (an **unprocured** provider, `24` P-06/A-06) or the TOTP `24` §12 and `OD-SEC-01` already contemplate? §5.1 |
| `OD-DOC-43` | IMPORTANT | At which layer is the guard enforced, and does the owner accept the database **role split** L3 requires (§7) or is L2 the paid scope? |
| `OD-DOC-44` | NICE | Where does the mode indicator and the transition control live, given no screen → route → token join exists (`OD-10-06`, `OD-DOC-29`, `OD-DOC-37`)? §9 |

Two risks are registered in `19`: **`R-49`** (the protection is illusory — default-`TESTING` on live
infrastructure, or a guard enforced only where it can be bypassed) and **`R-50`** (the absolute
prohibition makes statutory erasure and scheduled retention purges impossible, i.e. the compliance
cost of the feature as literally stated).

---

## 14. What This Document Is Not

| It is not | Statement |
|---|---|
| Implemented | No source code, migration, table, endpoint or dependency exists (`22` `ADR-025-02`). Nothing here is `[IMPLEMENTED]` |
| Scaffolded | No directory named in §11 or in `35` has been created |
| Approved | Status is `PROPOSED`; `ADR-026` is `Proposed`, not `Accepted`; `01` §8 and `26` §3.2 both require an owner act |
| Priced | No cost, effort or timeline figure is asserted for this feature. `26` §4.5 item 1 and item 7 require scope and change-management terms that do not exist yet |
| A legal conclusion | §6.3 describes a conflict between two obligations the suite already carries. Resolving it needs counsel (`ADR-024`); this document names the question and stops |
| A substitute for `OD-DOC-38` | The backend framework decision still gates everything above |

---

## 15. Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.0 | 2026-10-21 | Engineering Lead (documenting an owner instruction) | First issue. Records the owner's 2026-10-21 `[REPORTED]` instruction verbatim and specifies it as `PM-01`…`PM-24`: the two-state machine with guarded promote/demote, the email-OTP ceremony (with its dependency on the **unprocured** transactional-email provider P-06/A-06 and its intersection with `OD-SEC-01`), a four-class deletion taxonomy that preserves `03` §3.2's existing soft-delete contract and separates operator deletion from statutory erasure and scheduled retention purge, four enforcement layers with the database role split named as the real cost, `record_origin` marking for test data held in the same database, the gapless-statutory-numbering hazard, the fail-closed boot precondition for the "default is Test" rule, and the mode-indicator requirement without naming a component (`CA-00`). Registered `OD-DOC-40`…`44` in `21` (2 blockers), `R-49`/`R-50` in `19`, `FR-MODE-01`…`08` in `01`, `platform_mode`/`platform_mode_transitions` and the `record_origin` column in `09`, routes and two error codes in `10`, the control in `13`, `FL-09` and the `delete`-verb note in `03`, `ADR-026` in `22`, glossary terms in `20`, and pointers in `08`, `14`, `15`, `16`, `17`, `25`, `26`, `27`, `28`, `29`, `35` and `README`. **No code, directory, dependency, table in a live database, cost or legal answer was created; nothing is approved; `OD-DOC-38` still gates any scaffold or `git init`.** | All |
