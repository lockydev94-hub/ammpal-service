# 03 — Roles, RBAC & Permission Matrix

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-03 |
| Version | 1.3 |
| Status | Approved for Design & Development |
| Owner | Engineering Lead + Security Owner |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `01` §4.1, `02` §4 |

---

## 1. Model Overview

AmmPal uses a **hybrid authorisation model**:

```
Effective Access  =  Role Permissions  ∩  Account Scope  ∩  Resource Ownership
```

| Layer | Question it answers | Mechanism |
|---|---|---|
| **Identity** | Who are you? | OTP/JWT for customers & technicians; SSO/OIDC for central staff |
| **Role** | What may you do? | Named role → set of `(resource, action)` permissions |
| **Scope** | Where may you do it? | `GLOBAL` / `STATE` / `BRANCH` / `SERVICE_AREA` / `SELF` |
| **Ownership** | On whose data? | Ownership predicates (own bookings, own tickets, own earnings) |
| **State** | Is it allowed *now*? | Account status, document validity, branch status, booking state |

All five are enforced **server-side**. The client never decides access.

---

## 2. Role Catalogue

### 2.1 Family A — Platform Admin (Central)

These roles operate the **AmmPal Control Center** across the platform.

| Role | Code | Purpose | Scope | Approves |
|---|---|---|---|---|
| **Super Admin** | `SUPER_ADMIN` | Master administrator. Owns master data, role/permission definition, global configuration, and has all permissions. | `GLOBAL` | Partner branches, technicians, roles, master data |
| **Admin (Manager)** | `ADMIN` | Platform manager. Supervises Operators and Accountants, monitors cross-functional KPIs, handles escalations above Operator level. | `GLOBAL` (or `STATE`) | Operators' escalations, coupons (shared), price band overrides |
| **Operator** | `OPERATOR` | Booking & partner operations. Onboards/approves partners, technicians and branches, allocates territories, monitors the job feed, resolves operational issues. | `GLOBAL` (or `STATE`) | Partner orgs, branches, technicians, territory allocation |
| **CCO** | `CCO` | Customer Care Officer. Handles toll-free calls and support tickets, supports customers, partners and technicians, logs complaints, coordinates with branch and technician. | `GLOBAL` (or `STATE`) | Ticket resolution, callback scheduling |
| **Accountant** | `ACCOUNTANT` | Finance. Commission accrual review, settlement generation and reconciliation, GST/tax treatment, dispute handling, partner payment tracking. | `GLOBAL` (or `STATE` / `BRANCH`) | Settlement issuance, credit/debit notes, tax configuration review |
| **Partner Support** | `PARTNER_SUPPORT` | Partner enablement. Assists partner branches and technicians with KYC, wallet/earnings queries, app usage, document updates, and escalates to Operator. | `GLOBAL` (or `STATE`) | Partner KYC updates, wallet query resolution |
| **Marketing & Operations** | `MARKETING_OPS` | Growth and content. Campaigns, platform-funded coupons, service listings and content, content analytics. | `GLOBAL` (or `STATE`) | Platform-funded coupon creation, content publishing |

> **Separation of duties.** A single account must not hold both `SUPER_ADMIN` and `ACCOUNTANT`.
> Settlement issuance (`settlement.issue`) and settlement approval (`settlement.approve`) must be held
> by **different** accounts. See `19` §4 (SoD controls).

### 2.2 Family B — Partner of Platform (Branch)

These roles operate a **branch** — either a company-owned branch or an authorised platform-partner branch.
Their entire view is location-bound.

| Role | Code | Purpose | Scope |
|---|---|---|---|
| **Branch Admin (Partner of Platform)** | `PARTNER_BRANCH_ADMIN` | Owner/manager of a partner branch. Manages its technician team, sets local price within band, manages partner-funded coupons, approves technicians, tracks local P&L. | `BRANCH` |
| **Branch Manager** | `BRANCH_MANAGER` | Manager of a **company-owned** branch. Same operational capability as above, but within AmmPal's own branch and reporting to the Admin. | `BRANCH` |
| **Branch Coordinator** | `BRANCH_COORDINATOR` | Front-desk/dispatch for a branch. Creates bookings on behalf of customers, monitors SLA, coordinates technicians, handles first-line issues. | `BRANCH` |
| **Branch Finance** | `BRANCH_FINANCE` | Branch-level view of commission, settlements and payouts for that branch. Read-mostly. | `BRANCH` |

> **Partner branch onboarding.** A `PARTNER_BRANCH_ADMIN` account cannot be self-activated. The
> partner organisation and branch are approved by `OPERATOR` or `SUPER_ADMIN` (`02` §5, TA-02), and
> only then is a scoped account provisioned.

### 2.3 Family C — Customer

| Role | Code | Purpose | Scope |
|---|---|---|---|
| **Customer** | `CUSTOMER` | Books and tracks services, pays, rates, raises support requests. | `SELF` (own data only) |

### 2.4 Family D — Service Technician (Partner)

| Role | Code | Purpose | Scope |
|---|---|---|---|
| **Technician** | `TECHNICIAN` | Platform technician. Executes jobs, captures parts and evidence, generates invoices, earns commission-based settlements. | `SELF` + pinned service areas |
| **Technician Crew (Assistant)** | `TECHNICIAN_CREW` | Helper assisting a lead technician. Cannot accept jobs or invoice independently. | `SELF` + attached to a job |

> The founder's model places **technicians** under the platform ("technician register at main
> platform") while **jobs work location-based**. This is modelled as: a technician has exactly one
> **home branch** (registration authority) and zero or more **pinned service areas** (job
> distribution scope). `02` §4.2, SR-06.

---

## 3. Permission Model

### 3.1 Permission Format

```
<domain>:<resource>:<action>
```

| Segment | Values |
|---|---|
| `domain` | `platform` · `branch` · `customer` · `technician` · `catalog` · `booking` · `job` · `finance` · `support` · `report` · `platformOps` |
| `resource` | e.g. `technician`, `partnerOrg`, `booking`, `priceBook`, `coupon`, `settlement` |
| `action` | `list` · `read` · `create` · `update` · `delete` · `approve` · `reject` · `issue` · `export` · `assign` · `override` |

### 3.2 Action Semantics

| Action | Meaning | Notes |
|---|---|---|
| `list` | Retrieve collection (scoped) | Paged, max page size 100 |
| `read` | Retrieve single entity (scoped) | Ownership + scope checks |
| `create` | Create new | |
| `update` | Modify existing | Field-level restrictions may apply (see `03` §5) |
| `delete` | Soft delete only | Hard delete restricted to `SUPER_ADMIN` for master data, and **refused entirely while the platform is in `PRODUCTION` mode** (`38` §6, Rule `FL-09`). Soft delete is unaffected — the row survives, so the protection holds. |
| `approve` | Approve a pending workflow item | Partner, technician, branch, coupon approval |
| `reject` | Reject a pending workflow item | Reason mandatory, audited |
| `issue` | Emit an immutable financial/operational document | Invoice, settlement statement, commission invoice |
| `export` | Bulk download | Always audited, rate-limited, watermarked |
| `assign` | Assign work to a person/queue | Technician, ticket, branch |
| `override` | Bypass a configurable rule | Requires a reason; separately audited; subject to penalty rules |

### 3.3 Super Admin Statement

`SUPER_ADMIN` holds **all** permissions, including `override`. However:
- Super Admin **cannot** approve their own actions; an approval requires a second account.
- Super Admin **cannot** unilaterally delete financial records.
- Super Admin **cannot** change the platform mode without passing the step-up ceremony of `38` §5,
  and cannot change it alone: `FL-03`'s self-approval block plus `FL-09`'s second-account
  acknowledgement apply to the transition itself.
- Super Admin **cannot** turn the `PRODUCTION` delete guard off. There is no off-switch state (§4 of
  `38`); the legitimate paths are the code-defined retention purge and, if `OD-DOC-40` is decided that
  way, the statutory-erasure routine.
- Every Super Admin action is audited identically to others.

---

## 4. Permission Matrix

**Legend** — `✔` full · `◐` limited/own-scope or read-only subset · `○` conditional (see note) · `—` none

### 4.1 Platform Roles (Family A)

| Permission | SUPER_ADMIN | ADMIN | OPERATOR | CCO | ACCOUNTANT | PARTNER_SUPPORT | MARKETING_OPS |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| `platform:masterData:*` | ✔ | ◐ | ◐ | — | — | — | ◐ |
| `platform:role:*` | ✔ | ◐ | — | — | — | — | — |
| `platform:permission:*` | ✔ | — | — | — | — | — | — |
| `platform:user:create` | ✔ | ✔ | ○ | — | — | — | — |
| `platform:user:update` | ✔ | ✔ | ○ | — | — | — | — |
| `platform:audit:read` | ✔ | ✔ | ◐ | ◐ | ✔ | ◐ | — |
| `platform:config:*` | ✔ | ◐ | — | — | ◐ | — | — |
| `platformOps:partnerOrg:*` | ✔ | ✔ | ✔ | ◐ | ◐ | ✔ | — |
| `platformOps:partnerOrg:approve` | ✔ | ✔ | ✔ | — | — | — | — |
| `platformOps:branch:*` | ✔ | ✔ | ✔ | — | — | ◐ | — |
| `platformOps:branch:approve` | ✔ | ✔ | ✔ | — | — | — | — |
| `platformOps:technician:*` | ✔ | ✔ | ✔ | ◐ | — | ✔ | — |
| `platformOps:technician:approve` | ✔ | ✔ | ✔ | — | — | ◐ | — |
| `platformOps:territory:*` | ✔ | ✔ | ✔ | — | — | — | — |
| `booking:*` | ✔ | ✔ | ✔ | ◐ | ◐ | — | ◐ |
| `booking:create` (on behalf) | ✔ | ✔ | ✔ | ✔ | — | — | — |
| `booking:override` | ✔ | ✔ | ○ | — | — | — | — |
| `job:complete` | — | — | — | — | — | — | — |
| `job:verify` | ✔ | ✔ | ✔ | — | — | — | — |
| `support:queue:read` | ✔ | ✔ | ✔ | ✔ | — | ◐ | — |
| `support:ticket:*` | ✔ | ✔ | ✔ | ✔ | ◐ | ✔ | — |
| `support:ticket:assign` | ✔ | ✔ | ✔ | ✔ | — | — | — |
| `support:call:read` | ✔ | ✔ | ◐ | ✔ | — | ◐ | — |
| `support:complaint:escalate` | ✔ | ✔ | ✔ | ✔ | — | — | — |
| `finance:commission:*` | ✔ | ◐ | — | — | ✔ | — | — |
| `finance:settlement:generate` | ✔ | — | — | — | ✔ | — | — |
| `finance:settlement:issue` | ✔ | — | — | — | ✔ | — | — |
| `finance:settlement:approve` | ✔ | — | — | — | ○ | — | — |
| `finance:invoice:read` | ✔ | ◐ | — | — | ✔ | ◐ | — |
| `finance:tax:config` | ✔ | — | — | — | ◐ | — | — |
| `finance:reconciliation:*` | ✔ | ◐ | — | — | ✔ | — | — |
| `finance:adjustment:create` | ✔ | — | — | — | ✔ | — | — |
| `catalog:service:*` | ✔ | ✔ | ◐ | — | — | — | ✔ |
| `catalog:priceBook:*` | ✔ | ✔ | — | — | ◐ | — | — |
| `catalog:priceBook:local` | ✔ | ◐ | — | — | — | ◐ | — |
| `catalog:coupon:platform` | ✔ | ✔ | — | — | — | — | ✔ |
| `catalog:coupon:partner` | ✔ | ✔ | ◐ | — | — | ◐ | — |
| `report:export` | ✔ | ✔ | ◐ | ◐ | ✔ | ◐ | ◐ |
| `report:finance` | ✔ | ◐ | — | — | ✔ | — | — |
| `report:operations` | ✔ | ✔ | ✔ | ✔ | — | ✔ | ✔ |

**Notes**
- `○ platformOps:technician:approve` for `PARTNER_SUPPORT` = may approve **document** updates only, not the technician account itself.
- `○ finance:settlement:approve` for `ACCOUNTANT` = may approve only if `settlement.issue` is not also held by that account (SoD).
- `○ booking:override` for `OPERATOR` = may override within state scope; overrides above a threshold require `ADMIN`.

### 4.2 Branch Roles (Family B)

| Permission | PARTNER_BRANCH_ADMIN | BRANCH_MANAGER | BRANCH_COORDINATOR | BRANCH_FINANCE |
|---|:--:|:--:|:--:|:--:|
| `branch:profile:read/update` | ✔ | ✔ | ◐ | — |
| `branch:technician:list/read` | ✔ | ✔ | ✔ | — |
| `branch:technician:create` | ✔ | ✔ | — | — |
| `branch:technician:approve` | ✔ | ✔ | — | — |
| `branch:technician:deactivate` | ✔ | ✔ | — | — |
| `branch:serviceArea:*` | ✔ | ✔ | ◐ | — |
| `branch:availability:*` | ✔ | ✔ | ✔ | — |
| `branch:booking:list/read` | ✔ | ✔ | ✔ | — |
| `branch:booking:create` | ✔ | ✔ | ✔ | — |
| `branch:booking:assign` | ✔ | ✔ | ✔ | — |
| `branch:booking:reschedule` | ✔ | ✔ | ✔ | — |
| `branch:booking:cancel` | ✔ | ✔ | ◐ | — |
| `branch:priceBook:local` | ✔ | ✔ | — | — |
| `branch:coupon:partner` | ✔ | ✔ | — | — |
| `branch:coupon:shared` | ○ | ○ | — | — |
| `branch:complaint:*` | ✔ | ✔ | ✔ | — |
| `branch:report:operations` | ✔ | ✔ | ◐ | ◐ |
| `branch:finance:read` | ✔ | ✔ | — | ✔ |
| `branch:settlement:read` | ✔ | ✔ | — | ✔ |
| `branch:settlement:dispute` | ✔ | ✔ | — | ✔ |
| `branch:settlement:approve` | ○ | — | — | ○ |
| `branch:priceBook:setOutOfBand` | ○ | — | — | — |

**Notes**
- `○ branch:coupon:shared` = shared coupons require `ADMIN` approval at creation.
- `○ branch:settlement:approve` = requires the account to not hold `finance:settlement:issue` (SoD).
- `○ branch:priceBook:setOutOfBand` = always requires an override reason, is fully audited, and triggers a finance alert. Reserved for exceptional circumstances.

### 4.3 Customer Role (Family C)

| Permission | CUSTOMER |
|---|:--:|
| `customer:profile:read/update` | ✔ |
| `customer:address:*` | ✔ |
| `customer:favoriteTechnician:*` | ✔ |
| `booking:search` | ✔ |
| `booking:create` | ✔ |
| `booking:read` (own) | ✔ |
| `booking:reschedule` | ✔ |
| `booking:cancel` | ✔ |
| `booking:changeTechnician` (request) | ✔ |
| `payment:pay` | ✔ |
| `payment:history` | ✔ |
| `invoice:read` (own) | ✔ |
| `rating:create` | ✔ |
| `review:create` | ✔ |
| `support:ticket:create` | ✔ |
| `support:ticket:read` (own) | ✔ |
| `support:call` (toll-free) | ✔ |
| `notification:preference` | ✔ |

### 4.4 Technician Role (Family D)

| Permission | TECHNICIAN | TECHNICIAN_CREW |
|---|:--:|:--:|
| `technician:profile:read/update` | ✔ | ◐ |
| `technician:skills:update` | ✔ | — |
| `technician:serviceArea:pin` | ✔ | — |
| `technician:availability:set` | ✔ | — |
| `technician:documents:upload` | ✔ | — |
| `booking:offer:read` | ✔ | ◐ |
| `booking:offer:accept` | ✔ | — |
| `booking:offer:reject` | ✔ | — |
| `booking:read` (assigned) | ✔ | ◐ |
| `job:start` (OTP verified) | ✔ | — |
| `job:checklist:complete` | ✔ | ✔ |
| `job:parts:add` | ✔ | — |
| `job:evidence:upload` | ✔ | ✔ |
| `job:complete` | ✔ | — |
| `job:invoice:generate` | ✔ | — |
| `payment:collect` | ✔ | — |
| `earnings:read` | ✔ | — |
| `settlement:read` | ✔ | — |
| `rating:read` (own) | ✔ | ◐ |
| `support:ticket:create` | ✔ | ✔ |
| `penalty:read` | ✔ | — |

---

## 5. Field-Level & Conditional Restrictions

| # | Restriction |
|---|---|
| FL-01 | `platform:user:update` cannot change a user's **role** or **scope**. Role/scope changes require `platform:role:assign` (Super Admin) and a reason. |
| FL-02 | A user cannot grant a permission they do not hold ("no privilege escalation"). |
| FL-03 | A user cannot act on their **own** approval request — self-approval is blocked at the service layer. |
| FL-04 | `finance:*` write operations cannot be performed by an account holding `booking:*` write in the same scope for the same branch (segregation of duties). |
| FL-05 | `platform:masterData:delete` on `state`, `city`, `branch` is soft-delete only, and blocked when any booking references the entity. |
| FL-06 | Technician price fields are read-only from the technician surface. Local price customisation is a **branch** action. |
| FL-07 | A CCO can modify a booking's *service details* but never its *price* or *commission*. |
| FL-08 | Overrides (`*:override`) require a non-empty reason, are written to a separate `audit_override` stream, and are reported monthly to `ADMIN`. |
| FL-09 | A platform-mode transition (`38`) is requestable by `SUPER_ADMIN` only, requires a step-up verification and a second-account acknowledgement, and writes both a `platform_mode_transitions` row and a hash-chained `audit_events` row in the same transaction. **It is deliberately given no permission token in §4**: `10` §4.6 counts 92 tokens and a token invented here would be a guard nobody approved — the allocation waits on `OD-10-06` and `OD-DOC-44`. |
| FL-10 | No role, including `SUPER_ADMIN`, may add a table or a job to the destructive-operation allow-list at runtime. That list is code-reviewed (`38` §6.2), because an operator-editable purge list is a delete button with a schedule attached. |

---

## 6. Scope Enforcement Pattern

Implemented as a shared guard in the API layer:

```ts
// Contract only — implementation detail
interface ScopeContext {
  userId: string;
  role: RoleCode;
  scope: { type: 'GLOBAL' | 'STATE' | 'BRANCH' | 'SERVICE_AREA' | 'SELF';
           stateId?: string; branchId?: string; serviceAreaId?: string };
  technicianId?: string;   // present when acting as a technician
  customerId?: string;     // present when acting as a customer
}
```

**Enforcement order**

```
1. Permission check        → 403 PERMISSION_DENIED
2. Scope check             → 403 SCOPE_VIOLATION   (logged as a security event)
3. Ownership check         → 404 NOT_FOUND         (resource existence is not leaked)
4. State/tenant check      → 409 INVALID_STATE
5. Field-level check       → 422 FIELD_NOT_MODIFIABLE
```

**Rule SEC-01** — A user whose scope is `BRANCH:X` may never read a row with `branch_id ≠ X`,
regardless of permission. `GLOBAL` bypasses step 2 only.

**Rule SEC-02** — List endpoints apply the scope predicate in the SQL query (never in application
code after fetch) to guarantee correctness and pagination integrity.

**Rule SEC-03** — Report endpoints accept a `branch_id` filter only within the caller's scope;
out-of-scope filters are ignored with a warning header, not an error.

---

## 7. Account Lifecycle

### 7.1 State Machine (All Internal Users)

```
PENDING_INVITE → ACTIVE ⇄ SUSPENDED
      │             │
      │             ├──→ PASSWORD_RESET_REQUIRED → ACTIVE
      │             ├──→ LOCKED (failed attempts) → ACTIVE (admin unlock)
      │             └──→ DEACTIVATED (offboarded, preserved for audit)
      └──→ EXPIRED (invitation timeout)
```

### 7.2 Technician State Machine

```
DRAFT → PENDING_VERIFICATION → APPROVED → ACTIVE ⇄ INACTIVE
                        │          │         │
                        │          │         └──→ SUSPENDED (policy breach)
                        │          └──→ REJECTED (re-submission allowed)
                        └──→ REJECTED
```

| Transition | Trigger | Actor | SLA |
|---|---|---|---|
| `DRAFT → PENDING_VERIFICATION` | KYC + documents + skills submitted | Technician | — |
| `PENDING_VERIFICATION → APPROVED` | KYC and documents validated | Operator / Super Admin | 48 h |
| `APPROVED → ACTIVE` | Account opened, first login | System | — |
| `ACTIVE → INACTIVE` | Technician paused | Technician / Branch | — |
| `ACTIVE → SUSPENDED` | Score below threshold, policy breach, fraud | Operator / Super Admin | — |
| Any → auto `INACTIVE` | A required document expired beyond grace | System | Daily job |

### 7.3 Customer State Machine

`REGISTERED → VERIFIED (OTP) → ACTIVE` · `ACTIVE ⇄ DELETED (DPDP erasure, after statutory retention)`

---

## 8. Service Level Objectives for Access Operations

| Operation | SLA | Escalation |
|---|---|---|
| Partner branch approval | 48 h | Operator → Admin at 72 h |
| Technician KYC approval | 48 h | Operator → Admin at 72 h |
| Role/scope assignment (internal) | 4 h | Super Admin |
| Account unlock | 2 h | Super Admin |
| Document expiry re-approval | 24 h | Partner Support |

---

## 9. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| OD-RBAC-01 | Should `BRANCH_COORDINATOR` be able to collect payment offline (cash) and record it? | Finance + Product | Before Phase 2 |
| OD-RBAC-02 | Is `MARKETING_OPS` allowed to create partner-funded coupons, or only platform-funded? | Product | Phase 2 |
| OD-RBAC-03 | Should field supervisors exist as a `SERVICE_AREA` scope in v1.0? | Operations | Phase 3 |
| OD-RBAC-04 | Who can reverse a `settlement:issue` action — only Super Admin, or also a two-person Finance team? | Finance | Before Phase 2 |
| OD-RBAC-05 | Does the CCO role require native telephony integration in the Control Center, or is it link-based to the provider console? | Support + Engineering | Phase 2 |

> **A gap that belongs to this document but is registered elsewhere.** `OD-10-06` (`21` §2,
> `[BLOCKER]`) is about §4 above: nothing in this suite joins the **92 distinct permission tokens** in
> these matrices (96 cells) to the **117 endpoint rows** in `10` §4; **29 action segments used here are
> not among the eleven actions §3.2 declares** (`complete`, `cancel`, `collect`, `dispute`, `escalate`,
> `generate`, `pay`, `pin`, `reschedule`, `search`, `set`, `start`, `upload`, `verify` among them) while
> the declared `delete` appears **nowhere**; and nine cells state their scope as prose beside the token
> (`booking:read` (own) in §4.3, `booking:read` (assigned) in §4.4, `job:start` (OTP verified),
> `support:call` (toll-free), `booking:create` (on behalf)). The same token therefore carries two
> different scopes in two role families, which an enforcement layer cannot read. Per `DEC-01` the
> decision lives in `21`, not here; when it closes, §4.5 (endpoint → permission), a readable scope
> column and the corrected §3.2 vocabulary land in this document, and `10` §4.6 is deleted.

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.3 | 2026-10-21 | Security Owner + Product Lead (platform-mode pass) | `38` decided what `delete` means in this platform, so the permission vocabulary changed rather than grew. §3.2's `delete` **verb row** now states that an operator-initiated hard delete is refused entirely in `PRODUCTION` and that **soft delete is unaffected** — the existing contract is preserved, not rewritten. §3.3 gained two Super-Admin limits that did not exist before: the account **cannot bypass** the promotion ceremony, **cannot act alone** in it, and **cannot turn the guard off**. Two flow rules added — **`FL-09`** (a mode transition is `SUPER_ADMIN` only, requires step-up verification and a second account, is audited twice, and **allocates no permission token**, which is why §4 stays at **92 tokens** while `OD-10-06` is open) and **`FL-10`** (nothing may be added to the retention purge allow-list at runtime — a list a dashboard can edit is not an allow-list). **No token, role or permission cell was invented, and the 96-cell / 92-token inventory is unchanged.** | §3.2, §3.3, §7 flow rules |
| 1.2 | 2026-10-21 | Engineering Lead + Security Owner (documentation audit pass 3, continued) | §9 gained the pointer to `OD-10-06` that this document was missing: the matrices in §4 were counted here at **96 cells / 92 distinct tokens** (66 three-part, 26 two-part, 19 wildcards), 29 of their action segments are outside §3.2's declared eleven, `delete` is declared and used nowhere, and nine cells write their scope as prose inside the cell. No permission, role or matrix row was changed — the vocabulary decision belongs to `21` (`DEC-01`), and editing §4 here would have resolved a conflict by choosing one side (`DEC-07`). | §9, Revision History |
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Cross-referenced the audit additions: bounded support financial permissions (ADR-016), the service-area scope for technicians, and the callback and waitlist permissions implied by the support console. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
