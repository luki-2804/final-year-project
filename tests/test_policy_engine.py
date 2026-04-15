import unittest

from backend.models.schemas import AccessRequest
from backend.services.data_store import store
from backend.services.policy_engine import policy_engine


class PolicyEngineTests(unittest.TestCase):
    def test_intern_denied_confidential_access(self):
        user = store.users_by_username["intern_ops"]
        req = AccessRequest(
            request_id="r1",
            user_id=user.user_id,
            source_cloud="CloudA",
            target_cloud="CloudA",
            resource_id="clouda:ai-training-data",
            action="view",
            context={"device_trust": "low"},
        )
        decision = policy_engine.evaluate(user, req, behavior_features={})
        self.assertEqual(decision.decision, "DENY")


if __name__ == "__main__":
    unittest.main()
