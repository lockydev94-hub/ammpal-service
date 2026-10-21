# 18 — Team Structure & RACI

| Field | Value |
|---|---|
| Document ID | AMM-SVC-DOC-18 |
| Version | 1.1 |
| Status | Approved for Design & Development |
| Owner | Founder / Sponsor |
| Classification | Internal — Confidential |
| Last Updated | 2026-10-21 |
| Depends On | `03`, `17` |

---

## 1. Organisation Model

```
                        ┌───────────────────────────┐
                        │      Sponsor / Founder    │
                        │  Strategy · Funding ·    │
                        │  Major decisions         │
                        └─────────────┬─────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
┌───────▼────────┐          ┌─────────▼─────────┐         ┌─────────▼─────────┐
│  Product &     │          │    Engineering     │         │    Operations     │
│  Design        │          │                    │         │                   │
│  Lead          │          │  Eng Lead          │         │  Ops Lead         │
│                │          │   ├─ Backend       │         │   ├─ Partner Ops   │
│  PM            │          │   ├─ Frontend      │         │   ├─ Support (CCO) │
│  UX Designer   │          │   ├─ Mobile         │         │   ├─ Finance/Acct  │
│  QA Lead       │          │   ├─ QA             │         │   └─ City launch   │
└────────────────┘          │   └─ Infra/DevOps   │         └───────────────────┘
                            └───────────────────┘
```

**Rule ORG-01** — The organisation is deliberately **flat and cross-functional**. The same person
may appear in several cells below; a role is a responsibility, not a headcount.

---

## 2. Roles & Responsibilities

### 2.1 Product & Design

| Role | Responsibilities | Key Deliverables |
|---|---|---|
| **Product Lead** | Owns the roadmap and the requirement set; keeps `Docs/` current; chairs the weekly metric review; owns open decisions | `01`, `17`; requirement sign-off |
| **Product Manager** | Requirements analysis, acceptance criteria, backlog refinement, stakeholder interviews, launch checklists | Backlog, user stories, acceptance criteria |
| **UX/UI Designer** | Design system, flows, prototypes, localisation review, accessibility | `12`; Figma library; design tokens |
| **QA Lead** | Test strategy, test automation, release gates, defect management, exploratory testing | `15`; automation suites; release sign-off |

### 2.2 Engineering

| Role | Responsibilities | Key Deliverables |
|---|---|---|
| **Engineering Lead** | Architecture, code standards, module boundaries, technical decisions, delivery commitments | `08`, `14`; technical decisions |
| **Backend Engineer(s)** | API modules, domain logic, pricing/commission engines, integrations, background jobs | API modules; domain modules |
| **Frontend Engineer (Web)** | Next.js website, public pages, SEO, performance | `apps/web` |
| **Frontend Engineer (Control Center)** | React + Vite admin surfaces, dashboards, tables, forms | `apps/control-center` |
| **Mobile Engineer(s) (Flutter)** | Customer app and Partner app, offline sync, push, store releases | `apps/customer-app`, `apps/partner-app` |
| **QA Automation Engineer** | E2E, integration, performance, security test suites | `15` §2 |
| **DevOps / Infra Engineer** | CI/CD, environments, monitoring, backups, DR, vendor accounts | `16` |

### 2.3 Operations & Finance

| Role | Responsibilities | Key Deliverables |
|---|---|---|
| **Operations Lead** | City launch readiness, branch operations, technician supply, coverage, escalation | Launch checklists; coverage reports |
| **Partner Ops Executive** | Partner & technician onboarding, KYC, enablement, document expiry | Technician pipeline; approval queue |
| **Customer Support Lead (CCO Manager)** | Support staffing, IVR/menu, quality, CSAT, escalation policy | `05`; support playbook; QA sampling |
| **Customer Care Officer (CCO)** | Inbound calls, bookings by phone, complaints, tickets, follow-ups | Call logs; resolved tickets |
| **Accountant / Finance Analyst** | Commission review, settlement generation and reconciliation, GST, dispute handling | Weekly settlements; reconciliation reports |
| **Growth / Marketing Executive** | Campaigns, platform-funded coupons, content, local marketing, analytics | Campaign calendar; coupon performance |
| **Field Supervisor** `[PROPOSED]` | Technician field visits, quality spot-checks, onboarding support | Visit reports |

### 2.4 Indicative Team Shape (Phase 1–2)

| Function | Headcount | Note |
|---|---:|---|
| Product Lead | 1 | Also the founder's chief of staff for product |
| Product Manager | 1 | |
| UX/UI Designer | 1 | Contract if needed |
| QA Lead | 1 | |
| Engineering Lead | 1 | Also reviews money-path code |
| Backend Engineer | 2–3 | 1 dedicated to pricing/commission/billing |
| Frontend (Web) | 1 | |
| Frontend (Control Center) | 1–2 | |
| Mobile (Flutter) | 2 | 1 per app initially |
| QA Automation | 1 | |
| DevOps/Infra | 0.5–1 | Can be fractional early |
| **Engineering total** | **~9–12** | |
| Operations Lead | 1 | |
| Partner Ops | 1–2 | |
| Support Lead | 1 | |
| CCO | 2–4 | Scales with call volume |
| Accountant | 1 | Fractional is viable pre-Phase 3 |
| Growth | 0.5–1 | |
| **Operations total** | **~7–10** | |

**Rule ORG-02** — Every role in `03` §2 must have **at least one named human** before that surface goes
live. A role with no owner is a role nobody can audit.

---

## 3. RACI Matrix

**R** = Responsible (does the work) · **A** = Accountable (owns the outcome, one per row) ·
**C** = Consulted (two-way input) · **I** = Informed (one-way)

### 3.1 Product & Requirements

| Activity | Founder | Product Lead | Eng Lead | Design | QA | Ops Lead | Finance | Support Lead |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Vision & strategy | **A/R** | C | C | C | I | C | C | I |
| Requirement definition | C | **A/R** | C | C | C | C | C | C |
| Acceptance criteria | I | **A/R** | C | I | C | I | C | C |
| Design / UX | C | C | C | **A/R** | C | I | I | C |
| Technical design | I | C | **A/R** | C | C | I | C | I |
| Priority / roadmap | **A** | **R** | C | I | C | C | C | C |
| Documentation currency | I | **A/R** | C | C | I | C | C | C |

### 3.2 Financial & Pricing

| Activity | Founder | Product Lead | Eng Lead | Finance | Ops Lead | QA |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Price band policy | **A** | C | I | **R** | C | I |
| Discount & coupon policy | **A** | C | I | **R** | C | I |
| Commission rate policy | **A** | C | I | **R** | C | I |
| Tax treatment | **A** | I | I | **R** | I | I |
| Pricing implementation | I | C | **A/R** | C | I | C |
| Settlement generation | I | I | C | **A/R** | I | C |
| Settlement approval | I | I | I | **A/R** | I | I |
| Dispute resolution | C | I | I | **R** | C | I |
| Financial reconciliation | I | I | C | **A/R** | I | C |

### 3.3 Operations & Supply

| Activity | Founder | Ops Lead | Partner Ops | Support Lead | Eng Lead | Product Lead |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| City launch plan | **A** | **R** | C | C | C | C |
| Technician onboarding | I | **A** | **R** | I | I | I |
| Technician KYC approval | I | **A** | **R** | I | I | I |
| Partner branch approval | **A/R** | C | C | I | I | I |
| Territory allocation | I | **A/R** | C | I | I | I |
| Coverage management | I | **A/R** | C | I | C | I |
| Branch price localisation | I | **A/R** | C | I | I | I |
| Suspension of a technician | **A** | **R** | C | I | I | I |

### 3.4 Support & Quality

| Activity | Founder | Support Lead | CCO | Ops Lead | Product Lead | Eng Lead | QA |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| IVR menu design | I | **A/R** | C | I | C | I | C |
| Support policies | C | **A/R** | C | C | C | I | I |
| Complaint handling | I | **A** | **R** | C | I | I | I |
| Escalation policy | C | **A/R** | C | C | I | I | I |
| CSAT & QA sampling | I | **A/R** | C | I | I | I | C |
| Rating & penalty rules | C | C | I | C | **A** | C | C |
| Refund approval (above limit) | I | I | C | I | I | I | **A/R** (Finance) |

### 3.5 Engineering & Release

| Activity | Founder | Eng Lead | QA Lead | Product Lead | DevOps |
|---|:--:|:--:|:--:|:--:|:--:|
| Technical decisions | I | **A/R** | C | C | C |
| Sprint commitment | I | **A/R** | C | C | I |
| Release to production | I | **A/R** | C (gate) | I | R |
| Release gate sign-off | I | R | **A** | I | R |
| Incident response | I | **A/R** | C | I | R |
| Post-mortem | I | **A/R** | C | I | C |
| Security remediation | I | **A/R** | C | I | R |

### 3.6 Partner & Customer Communications

| Activity | Founder | Growth | Product Lead | Support Lead | Ops Lead |
|---|:--:|:--:|:--:|:--:|:--:|
| Public pricing policy | **A/R** | C | C | I | I |
| Offers & campaigns | **A** | **R** | C | I | C |
| Policy documents (refund, warranty, terms) | **A** | C | **R** | C | C |
| Partner onboarding kit | I | C | C | I | **A/R** |
| Partner onboarding material | I | **A/R** | C | C | C |
| Public communications during an incident | **A** | C | C | R | C |

### 3.7 Governance

| Activity | Founder | Product Lead | Eng Lead | Finance | Ops Lead |
|---|:--:|:--:|:--:|:--:|:--:|
| Charter amendment | **A/R** | C | C | C | C |
| Business rule change | **A** | **R** | C | C | C |
| Open decision closure | **A** | **R** | C | C | C |
| Risk register review | **A** | R | R | R | R |
| Documentation audit | I | **A/R** | C | C | C |

---

## 4. Decision Rights

| Decision | Decides | Consulted | Cannot be decided by |
|---|---|---|---|
| Business model / pricing policy | Founder | Product, Finance | Engineering, Ops |
| Commission rate | Founder | Finance, Product | Any individual account |
| Tax treatment | Founder | Finance + external tax advisor | Engineering |
| Settlement issue | Accountant | Finance lead | Partner, Technician, CCO |
| Settlement approval | Accountant (≠ issuer) | Finance lead | The issuing account |
| Branch/partner approval | Operator | Super Admin | The applicant |
| Technician KYC approval | Operator | Partner Ops | The technician |
| Price band change | Super Admin | Admin, Finance | Branch (out of band) requires Super Admin + reason |
| Workflow template publish | Super Admin | Product, Ops | Branch, Technician |
| Role/permission change | Super Admin | Admin | Any non-Super-Admin account |
| Territory allocation | Operator | Super Admin | Branch (request only) |
| Suspension of a technician | Operator | Super Admin | CCO, Support |
| Refund above the CCO limit | Accountant | Support lead | CCO |
| Production release | Eng Lead | QA (gate), DevOps | Individual engineers outside the pipeline |
| Incident declaration (P0) | Eng Lead | On-call | — |
| Public pricing change | Founder | Growth, Product | Marketing in isolation |

**Rule DR-01** — Self-approval is blocked everywhere, in the product and in the organisation.
**Rule DR-02** — Every decision in this table is recorded in the audit log or the decision register.

---

## 5. Communication Cadence

| Forum | Cadence | Attendees | Purpose |
|---|---|---|---|
| Daily stand-up | Every working day, 15 min | Engineering + QA + Product | Progress, blockers |
| Sprint planning | Every 2 weeks | Product, Eng, QA, Design | Backlog commitment |
| Sprint review/demo | Every 2 weeks | Whole team + stakeholders | Working software demo |
| Retrospective | Every 2 weeks | Delivery team | Process improvement |
| **Product & metric review** | Weekly | Product, Ops, Finance, Support | Funnel, SLA, quality, finance metrics |
| **Steering review** | Fortnightly | Founder, Product Lead, Eng Lead, Ops Lead, Finance | Strategy, roadmap, risks, decisions |
| **Ops & support review** | Weekly | Ops, Support, Partner Ops | Coverage, ticket backlog, CSAT, technician supply |
| **Finance review** | Weekly (Mon, post-settlement) | Finance, Founder, Eng Lead | Settlement readiness, reconciliation, disputes |
| **Security & access review** | Monthly | Eng Lead, Security Owner | Access, audit, vulnerabilities, overrides |
| **All-hands** | Monthly | Everyone | Progress, demos, announcements |

---

## 6. On-Call & Support

| Tier | Scope | Rotation |
|---|---|---|
| **P0 on-call** | Production incident, financial discrepancy, security event | Engineering Lead + 1 engineer (weekly rotation) |
| **P1 on-call** | Core-flow degradation, degraded vendor | Same rotation |
| **Support hours** | 09:00–21:00 IST, 7 days | CCO team |
| **Out-of-hours** | Callback queue only; P0 escalation | On-call CCO + Eng Lead |

**Rule ORG-03** — A P0 incident declared outside business hours pages the on-call engineer **and** the
founder. There is no "wait until morning" for a financial or security incident.

---

## 7. Onboarding & Growth

### 7.1 New Team Member Ramp (First 30 Days)

| Week | Focus | Output |
|---|---|---|
| 1 | This documentation set; the repo; local setup; the stack | A running local environment; a first merged (trivial) change |
| 2 | The domain: `02`, `03`, `04`, `06`, `07`; pair on a small ticket | A merged domain change with tests |
| 3 | The surfaces: `12`; the API contract (`10`); a small end-to-end feature | A merged feature across at least 2 surfaces |
| 4 | Ownership: on-call shadowing; a release participation; a documentation improvement | A first owned module or ticket |

**Rule ORG-04** — No one touches the money path (`pricing`, `billing`, `commission`) without
completing the financial training in §7.2.

### 7.2 Mandatory Training

| Audience | Training | When |
|---|---|---|
| All engineers | Money handling: paise-only arithmetic, rounding rules, the commission base, the worked example (`07` §4) | Before touching the money path |
| All engineers | GDPR/DPDP basics, PII handling, logging redaction | Week 1 |
| All engineers | The booking state machine and the workflow engine | Week 2 |
| Operations & Support | The full booking lifecycle, the 6 call use cases, cancellation & refund policy | Before going live |
| Finance | The settlement cycle, the reconciliation assertions, the tax treatment | Before Phase 2 |
| All staff | Security awareness, phishing, data handling | On joining + annually |

---

## 8. Performance & Growth

| Level | Basis | Review |
|---|---|---|
| **Individual** | Role-specific goals + the team's engineering quality standards | Fortnightly 1:1 |
| **Team (engineering)** | Delivery predictability, defect escape rate, DORA metrics (deploy frequency, lead time, change failure rate, recovery time) | Monthly |
| **Team (operations)** | Fill rate, SLA, rating, complaint rate, technician supply, settlement accuracy | Monthly |
| **Company** | Contribution margin, GMV, repeat rate, CAC payback, city-level P&L | Monthly steering |

**Rule ORG-05** — No individual's performance is measured by ticket count alone. Quality, documentation
and mentoring count.

---

## 9. Open Points

| ID | Question | Owner | Deadline |
|---|---|---|---|
| ORG-01 | Is a separate **Finance Lead** (above the Accountant) needed from Phase 2? | Founder | Phase 1 |
| ORG-02 | Does the founder take the Product Lead role, or is a dedicated PM hired first? | Founder | Phase 0 |
| ORG-03 | Is a dedicated **QA automation** hire needed before Phase 2? | Eng Lead | Phase 1 |
| ORG-04 | Should field supervisors be hired per city from Phase 2? | Ops Lead | Phase 2 |
| ORG-05 | What is the escalation path when the founder is unavailable? | Founder | Phase 0 |

---

## Revision History

| Version | Date | Author | Summary | Sections changed |
|---|---|---|---|---|
| 1.1 | 2026-10-21 | Product Lead + Engineering Lead | Documentation audit and consolidation. Added the decision-rights rows for the legal entity and city activation decisions, and cross-referenced the RACI ownership of the new documents. | All |
| 1.0 | 2026-10-21 | Product Lead | Initial issue. | All |
