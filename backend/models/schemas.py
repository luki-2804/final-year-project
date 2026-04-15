from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class User:
    user_id: str
    full_name: str
    email: str
    username: str
    password: str
    department: str
    role: str
    clearance_level: int
    assigned_clouds: List[str]
    allowed_resources: List[str]
    can_approve_sync: bool = False
    mfa_enabled: bool = True


@dataclass
class Resource:
    resource_id: str
    cloud: str
    name: str
    classification: str
    resource_type: str
    owner_department: str


@dataclass
class AccessRequest:
    request_id: str
    user_id: str
    source_cloud: str
    target_cloud: str
    resource_id: str
    action: str
    context: Dict[str, str] = field(default_factory=dict)


@dataclass
class PolicyDecision:
    decision: str
    risk_score: float
    reasons: List[str]
    mfa_required: bool = False
    obligation: Optional[str] = None
