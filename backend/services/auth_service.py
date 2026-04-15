from __future__ import annotations

from typing import Dict, Optional

from backend.services.data_store import store


class AuthService:
    MFA_DEMO_CODE = "123456"

    def login(self, username: str, password: str) -> Optional[Dict]:
        user = store.authenticate(username, password)
        if not user:
            return None
        session_id = store.create_session(user, mfa_verified=False)
        return {
            "session_id": session_id,
            "user": user,
            "mfa_required": user.mfa_enabled,
        }

    def verify_mfa(self, session_id: str, code: str) -> bool:
        if code != self.MFA_DEMO_CODE:
            return False
        store.set_mfa_verified(session_id)
        return True


auth_service = AuthService()
