# Final Year Project Prototype Blueprint

## 1) End-to-End Implementation Plan

1. **Provision two logical clouds (CloudA, CloudB)** in the application domain model with independent users, resources, and policies.
2. **Build identity layer** (register/login/session/MFA) and enforce session-bound access evaluation for all actions.
3. **Implement hybrid authorization**: RBAC action permissions + ABAC constraints (department, clearance, cloud assignment, resource sensitivity).
4. **Integrate Zero Trust policy engine** returning `ALLOW`, `STEP-UP`, `DENY` for every request.
5. **Ingest CERT insider-threat raw logs** (`logon`, `device`, `http`, etc.), engineer user behavior features, and produce model-based risk scores.
6. **Connect ML risk into policy engine** to influence final access and sync decisions.
7. **Create secure cross-cloud synchronization flow** with source/target mapping controls, approval logic, and detailed logs.
8. **Expose APIs for dashboard pages** (cloud overview, access request, sync request, ML training, audit logs).
9. **Implement professional React console** with enterprise navigation pages and Zero Trust decision surfaces.
10. **Prepare demo scenarios and testing scripts** for supervisor presentation.

---

## 2) System Architecture (Supervisor-Friendly)

- **Frontend (React + Vite)**
  - Enterprise console pages for auth, cloud view, sync, ML, audits.
- **Backend (Flask API)**
  - Auth Service, Policy Engine, Sync Service, Insider ML Service, Data Store.
- **Security Core**
  - RBAC + ABAC + contextual risk + ML risk + step-up MFA.
- **Data Domain**
  - Two clouds, resource inventory, fake company datasets, user directory.
- **ML Pipeline**
  - CERT parser -> feature engineering -> RandomForest -> risk score.
- **Auditability**
  - Access decisions and sync actions logged with timestamp + reasons.

---

## 3) Frontend Dashboard Structure

Mandatory pages included in implementation:

1. Landing / Overview
2. Login
3. Register fake account
4. MFA page
5. User dashboard
6. Cloud A overview
7. Cloud B overview
8. Synchronization management
9. Dataset / logs
10. ML training
11. Access request
12. Decision results
13. Audit logs
14. Admin management

---

## 4) Backend Modules

- `backend/app.py`: API orchestration.
- `backend/services/auth_service.py`: login + MFA verification.
- `backend/services/policy_engine.py`: Zero Trust decision logic.
- `backend/services/sync_service.py`: secure cross-cloud sync flow.
- `backend/services/insider_ml_service.py`: CERT parsing, feature engineering, model training, risk prediction.
- `backend/services/data_store.py`: in-memory enterprise data model + logs.
- `backend/data/seed_data.py`: fake users/resources/role policies/sync mapping.

---

## 5) Fake Cloud-Company Data Design

Each cloud has scoped enterprise resources with classifications:

- **Cloud A**: employee records, AI training data, SOC logs.
- **Cloud B**: model assets, project files, sync queue.

Resource classes (`internal`, `restricted`, `confidential`) drive ABAC outcomes with clearance checks.

---

## 6) Fake User Account Design

Fields for each account:

- full name
- company email
- username / password
- department
- role
- clearance level
- assigned clouds
- allowed resources
- sync-approval flag

Includes roles requested in your scope (Security Admin, Cloud Administrator, Cloud Analyst, Research User, Intern; extensible for AI Engineer/Internal Staff/External User).

---

## 7) RBAC + ABAC Permission Model

- **RBAC**: Role controls allowed actions (view/upload/modify/sync/train_model/approve_sync).
- **ABAC** checks include:
  - target cloud assignment
  - resource allow-list
  - clearance vs resource classification
  - action criticality
  - device trust & IP reputation context

---

## 8) Secure Synchronization Design

Sync flow:

1. User submits sync request with source/target cloud and target resource.
2. Sync service validates allowed source-target mapping.
3. Zero Trust engine evaluates identity + role + ABAC + risk score.
4. If medium risk -> `STEP-UP` (MFA required).
5. High risk or forbidden mapping -> `DENY`.
6. Approved action logged in sync/audit logs.

---

## 9) CERT Dataset Integration Plan

- Place uploaded CERT CSV files under `data/cert/`.
- Loader automatically reads all CSVs and tags records by source file.
- Supports event streams such as `logon`, `device`, `http` and any additional files.
- Events are transformed from raw logs into aggregated per-user behavior vectors.

---

## 10) Insider-Threat ML Pipeline

Engineered features:

- event count
- odd-hour activity
- device usage frequency
- suspicious web activity
- login activity
- cross-cloud context proxy
- abnormal behavior indicator

Model/evaluation:

- RandomForestClassifier
- Accuracy, Precision, Recall, F1
- Confusion matrix
- output risk probability used by policy engine

---

## 11) Zero Trust Decision Logic

Every request is evaluated with:

- identity/session validity
- role action authorization
- cloud assignment
- resource allow-list
- clearance check
- context risk (cross-cloud, device trust, IP reputation)
- ML risk score from insider behavior

Final outcomes:
- `ALLOW`
- `STEP-UP` (MFA)
- `DENY`

---

## 12) Demo Scenarios for Presentation

1. **Normal Access**: Analyst views CloudA logs -> ALLOW.
2. **Role Difference**: Intern tries modifying confidential dataset -> DENY.
3. **Step-Up MFA**: Research user requests cross-cloud sync with medium risk -> STEP-UP.
4. **Secure Sync Success**: Cloud admin performs approved mapping with MFA -> completed sync log.
5. **Malicious Attempt**: Low-clearance user from bad IP attempts restricted sync -> DENY.
6. **ML Influence**: Increased suspicious activity yields high risk and blocks access.
7. **Auditability**: Show all decisions in `/api/audit/logs` output.

---

## 13) Academic Alignment Statement

This prototype directly supports your report and progress presentation by demonstrating:

- Zero Trust enforcement for every action
- practical multi-cloud architecture (CloudA + CloudB)
- secure cross-cloud synchronization controls
- insider-threat analytics from CERT raw event logs
- ML-driven adaptive access decisions
- policy transparency through reasoned outcomes and audit logs

It is intentionally modular and presentation-friendly for architecture diagrams, workflow explanation, and validation scenarios.
