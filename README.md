# Securing AI Workloads in Multi-Cloud Environments using Zero Trust Architecture

This repository contains a supervisor-ready academic prototype for a Final Year Project on Zero Trust security for AI workloads across synchronized multi-cloud environments.

## Prototype scope implemented

- Two independent cloud domains (`CloudA`, `CloudB`) with their own users/resources/policies.
- Enterprise fake user directory with RBAC + ABAC attributes.
- Authentication + session handling + MFA step-up.
- Zero Trust policy engine (`ALLOW`, `STEP-UP`, `DENY`) for every request.
- Secure cross-cloud synchronization workflow with policy verification and logging.
- CERT insider-threat raw log ingestion and feature engineering.
- Random Forest insider-threat model with metrics and risk scoring.
- Audit log pipeline for access and sync decisions.
- Professional React console page structure for academic demonstration.

## Repository layout

- `backend/` Flask API and security/ML services
- `frontend/` React interface structure (enterprise console pages)
- `docs/IMPLEMENTATION_PLAN.md` full architecture and implementation narrative

## Quick start

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python backend/app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## CERT dataset placement

Place uploaded CERT CSV log files under:

```text
data/cert/
```

Then trigger training:

```bash
curl -X POST "http://127.0.0.1:5000/api/ml/train?cert_path=data/cert"
```

## Core API endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/mfa`
- `POST /api/access/request`
- `POST /api/sync/request`
- `POST /api/ml/train`
- `GET /api/clouds/overview`
- `GET /api/audit/logs`

## Demo accounts (seed)

Use password `Password@123` for seeded users, e.g. `sec_admin_a`, `cloud_admin_b`, `analyst_a`, `research_user`, `intern_ops`.

## Academic presentation mapping

The implementation supports report and demo discussion on:

- Zero Trust Architecture principles (never trust, always verify)
- multi-cloud workload protection
- cross-cloud synchronization governance
- insider-threat detection using CERT behavior logs
- risk-adaptive authorization decisions
