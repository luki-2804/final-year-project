from __future__ import annotations

from typing import Dict

from backend.models.schemas import AccessRequest
from backend.services.data_store import store
from backend.services.policy_engine import policy_engine


class SyncService:
    def request_sync(self, request: AccessRequest, behavior_features: Dict[str, float], session_mfa_verified: bool) -> Dict:
        user = store.users.get(request.user_id)
        if not user:
            return {"status": "error", "message": "Unknown user"}

        allowed_targets = store.sync_policy.get(request.resource_id, [])
        requested_target = request.context.get("target_resource")
        if requested_target not in allowed_targets:
            return {
                "status": "blocked",
                "decision": "DENY",
                "message": "Requested resource mapping is not allowed for sync.",
            }

        decision = policy_engine.evaluate(user, request, behavior_features)
        store.log_decision(request, decision)

        if decision.decision == "STEP-UP" and not session_mfa_verified:
            return {
                "status": "pending_mfa",
                "decision": decision.decision,
                "risk_score": decision.risk_score,
                "reasons": decision.reasons,
            }

        if decision.decision != "ALLOW":
            store.log_sync(
                {
                    "request_id": request.request_id,
                    "user_id": request.user_id,
                    "source_cloud": request.source_cloud,
                    "target_cloud": request.target_cloud,
                    "resource_id": request.resource_id,
                    "target_resource": requested_target,
                    "status": "denied",
                    "risk_score": decision.risk_score,
                }
            )
            return {
                "status": "denied",
                "decision": decision.decision,
                "risk_score": decision.risk_score,
                "reasons": decision.reasons,
            }

        store.log_sync(
            {
                "request_id": request.request_id,
                "user_id": request.user_id,
                "source_cloud": request.source_cloud,
                "target_cloud": request.target_cloud,
                "resource_id": request.resource_id,
                "target_resource": requested_target,
                "status": "completed",
                "risk_score": decision.risk_score,
            }
        )
        return {
            "status": "completed",
            "decision": decision.decision,
            "risk_score": decision.risk_score,
            "reasons": decision.reasons,
        }


sync_service = SyncService()
