from __future__ import annotations

from typing import Dict, List

from backend.models.schemas import AccessRequest, PolicyDecision, User
from backend.services.data_store import store
from backend.services.insider_ml_service import ml_service


class ZeroTrustPolicyEngine:
    def evaluate(self, user: User, request: AccessRequest, behavior_features: Dict[str, float]) -> PolicyDecision:
        reasons: List[str] = []
        mfa_required = False

        role_actions = store.role_policies.get(user.role, {}).get("actions", [])
        if request.action not in role_actions:
            reasons.append(f"Role '{user.role}' cannot perform action '{request.action}'.")
            return PolicyDecision(decision="DENY", risk_score=1.0, reasons=reasons)

        if request.target_cloud not in user.assigned_clouds and user.role != "Security Admin":
            reasons.append(f"User not assigned to target cloud {request.target_cloud}.")
            return PolicyDecision(decision="DENY", risk_score=0.95, reasons=reasons)

        if request.resource_id not in user.allowed_resources and "*" not in user.allowed_resources:
            reasons.append("Resource not included in user's allow-list.")
            return PolicyDecision(decision="DENY", risk_score=0.9, reasons=reasons)

        resource = store.resources.get(request.resource_id)
        if resource and resource.classification == "confidential" and user.clearance_level < 3:
            reasons.append("Insufficient clearance for confidential resource.")
            return PolicyDecision(decision="DENY", risk_score=0.92, reasons=reasons)

        ml_risk = ml_service.predict_risk(behavior_features)
        contextual_risk = self._contextual_risk(user, request)
        total_risk = min(1.0, round((0.6 * ml_risk) + (0.4 * contextual_risk), 4))

        if request.action in {"sync", "approve_sync", "modify", "upload"} or resource and resource.classification in {"restricted", "confidential"}:
            mfa_required = True

        if total_risk >= 0.75:
            reasons.append("High combined risk from behavior analytics and context.")
            return PolicyDecision(decision="DENY", risk_score=total_risk, reasons=reasons, mfa_required=mfa_required)
        if total_risk >= 0.45:
            reasons.append("Medium risk requires step-up verification.")
            return PolicyDecision(decision="STEP-UP", risk_score=total_risk, reasons=reasons, mfa_required=True, obligation="Require MFA")

        reasons.append("Risk acceptable under Zero Trust policy.")
        return PolicyDecision(decision="ALLOW", risk_score=total_risk, reasons=reasons, mfa_required=mfa_required)

    @staticmethod
    def _contextual_risk(user: User, request: AccessRequest) -> float:
        risk = 0.15
        if request.source_cloud != request.target_cloud:
            risk += 0.25
        if user.clearance_level <= 2:
            risk += 0.20
        if request.action in {"sync", "approve_sync"} and not user.can_approve_sync:
            risk += 0.30
        if request.context.get("ip_reputation", "unknown") == "bad":
            risk += 0.30
        if request.context.get("device_trust", "low") == "low":
            risk += 0.15
        return min(risk, 1.0)


policy_engine = ZeroTrustPolicyEngine()
