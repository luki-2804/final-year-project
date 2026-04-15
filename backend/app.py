from __future__ import annotations

from dataclasses import asdict
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.models.schemas import AccessRequest
from backend.services.auth_service import auth_service
from backend.services.data_store import store
from backend.services.insider_ml_service import ml_service
from backend.services.policy_engine import policy_engine
from backend.services.sync_service import sync_service

app = Flask(__name__)
CORS(app)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "zta-multicloud-prototype"})


@app.post("/api/auth/register")
def register():
    payload = request.get_json(force=True)
    payload["user_id"] = f"u{len(store.users) + 1:03d}"
    user = store.create_user(payload)
    return jsonify({"message": "User created", "user": asdict(user)})


@app.post("/api/auth/login")
def login():
    payload = request.get_json(force=True)
    result = auth_service.login(payload.get("username", ""), payload.get("password", ""))
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify(
        {
            "session_id": result["session_id"],
            "mfa_required": result["mfa_required"],
            "user": asdict(result["user"]),
        }
    )


@app.post("/api/auth/mfa")
def verify_mfa():
    payload = request.get_json(force=True)
    ok = auth_service.verify_mfa(payload.get("session_id", ""), payload.get("code", ""))
    if not ok:
        return jsonify({"verified": False, "message": "Invalid MFA code"}), 400
    return jsonify({"verified": True})


@app.post("/api/ml/train")
def train_ml():
    cert_path = request.args.get("cert_path", "data/cert")
    raw = ml_service.load_cert_logs(cert_root=cert_path)
    engineered = ml_service.engineer_features(raw)
    result = ml_service.train(engineered)
    return jsonify(
        {
            "result": result,
            "raw_events": int(len(raw.index)) if not raw.empty else 0,
            "feature_rows": int(len(engineered.index)) if not engineered.empty else 0,
        }
    )


@app.post("/api/access/request")
def access_request():
    payload = request.get_json(force=True)
    session_id = payload.get("session_id")
    user = store.get_user_by_session(session_id)
    if not user:
        return jsonify({"message": "Invalid session"}), 401

    req = AccessRequest(
        request_id=str(uuid4()),
        user_id=user.user_id,
        source_cloud=payload["source_cloud"],
        target_cloud=payload["target_cloud"],
        resource_id=payload["resource_id"],
        action=payload["action"],
        context=payload.get("context", {}),
    )
    decision = policy_engine.evaluate(user, req, payload.get("behavior_features", {}))
    store.log_decision(req, decision)

    return jsonify({"decision": asdict(decision), "request": asdict(req)})


@app.post("/api/sync/request")
def request_sync():
    payload = request.get_json(force=True)
    session_id = payload.get("session_id")
    user = store.get_user_by_session(session_id)
    if not user:
        return jsonify({"message": "Invalid session"}), 401

    req = AccessRequest(
        request_id=str(uuid4()),
        user_id=user.user_id,
        source_cloud=payload["source_cloud"],
        target_cloud=payload["target_cloud"],
        resource_id=payload["resource_id"],
        action="sync",
        context=payload.get("context", {}),
    )

    session_info = store.sessions.get(session_id, {})
    response = sync_service.request_sync(
        req,
        behavior_features=payload.get("behavior_features", {}),
        session_mfa_verified=bool(session_info.get("mfa_verified", False)),
    )
    return jsonify(response)


@app.get("/api/clouds/overview")
def cloud_overview():
    cloud_a_resources = [asdict(r) for r in store.resources.values() if r.cloud == "CloudA"]
    cloud_b_resources = [asdict(r) for r in store.resources.values() if r.cloud == "CloudB"]
    users = [asdict(u) for u in store.users.values()]
    return jsonify(
        {
            "CloudA": {
                "users": [u for u in users if "CloudA" in u["assigned_clouds"]],
                "resources": cloud_a_resources,
            },
            "CloudB": {
                "users": [u for u in users if "CloudB" in u["assigned_clouds"]],
                "resources": cloud_b_resources,
            },
        }
    )


@app.get("/api/audit/logs")
def audit_logs():
    return jsonify({"audit_log": store.audit_log, "sync_log": store.sync_log})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
