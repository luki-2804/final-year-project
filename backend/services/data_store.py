from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional

from backend.data.seed_data import RESOURCES, ROLE_POLICIES, SYNC_POLICY, USERS
from backend.models.schemas import AccessRequest, PolicyDecision, Resource, User


class DataStore:
    """In-memory data store for demo; replace with DB in production."""

    def __init__(self) -> None:
        self.users: Dict[str, User] = {u["user_id"]: User(**u) for u in USERS}
        self.users_by_username: Dict[str, User] = {u.username: u for u in self.users.values()}
        self.resources: Dict[str, Resource] = {r["resource_id"]: Resource(**r) for r in RESOURCES}
        self.role_policies = ROLE_POLICIES
        self.sync_policy = SYNC_POLICY
        self.sessions: Dict[str, Dict] = {}
        self.audit_log: List[Dict] = []
        self.sync_log: List[Dict] = []

    def create_user(self, payload: Dict) -> User:
        user = User(**payload)
        self.users[user.user_id] = user
        self.users_by_username[user.username] = user
        return user

    def authenticate(self, username: str, password: str) -> Optional[User]:
        user = self.users_by_username.get(username)
        if not user or user.password != password:
            return None
        return user

    def create_session(self, user: User, mfa_verified: bool = False) -> str:
        session_id = f"sess-{len(self.sessions)+1:04d}"
        self.sessions[session_id] = {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
            "mfa_verified": mfa_verified,
            "created_at": datetime.now(tz=timezone.utc).isoformat(),
        }
        return session_id

    def get_user_by_session(self, session_id: str) -> Optional[User]:
        session = self.sessions.get(session_id)
        if not session:
            return None
        return self.users.get(session["user_id"])

    def set_mfa_verified(self, session_id: str) -> None:
        if session_id in self.sessions:
            self.sessions[session_id]["mfa_verified"] = True

    def log_decision(self, request: AccessRequest, decision: PolicyDecision) -> None:
        entry = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "request": asdict(request),
            "decision": asdict(decision),
        }
        self.audit_log.append(entry)

    def log_sync(self, entry: Dict) -> None:
        entry = {**entry, "timestamp": datetime.now(tz=timezone.utc).isoformat()}
        self.sync_log.append(entry)


store = DataStore()
