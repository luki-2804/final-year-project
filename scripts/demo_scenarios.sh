#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://127.0.0.1:5000"

echo "1) Login as research user"
LOGIN=$(curl -s -X POST "$BASE_URL/api/auth/login" -H 'Content-Type: application/json' -d '{"username":"research_user","password":"Password@123"}')
echo "$LOGIN"
SESSION=$(python - <<'PY'
import json,sys
print(json.loads(sys.stdin.read()).get('session_id',''))
PY
<<< "$LOGIN")

echo "2) Access request (cross-cloud AI resource)"
curl -s -X POST "$BASE_URL/api/access/request" \
 -H 'Content-Type: application/json' \
 -d "{\"session_id\":\"$SESSION\",\"source_cloud\":\"CloudA\",\"target_cloud\":\"CloudB\",\"resource_id\":\"cloudb:model-assets\",\"action\":\"view\",\"context\":{\"device_trust\":\"medium\",\"ip_reputation\":\"good\"},\"behavior_features\":{\"event_count\":30,\"odd_hour_activity\":4,\"device_usage\":10,\"suspicious_web_activity\":15,\"login_events\":20,\"cross_cloud_context\":1,\"abnormal_behavior_indicator\":0}}"

echo

echo "3) Sync request"
curl -s -X POST "$BASE_URL/api/sync/request" \
 -H 'Content-Type: application/json' \
 -d "{\"session_id\":\"$SESSION\",\"source_cloud\":\"CloudA\",\"target_cloud\":\"CloudB\",\"resource_id\":\"clouda:ai-training-data\",\"context\":{\"target_resource\":\"cloudb:model-assets\"},\"behavior_features\":{\"event_count\":50,\"odd_hour_activity\":7,\"device_usage\":16,\"suspicious_web_activity\":28,\"login_events\":35,\"cross_cloud_context\":1,\"abnormal_behavior_indicator\":1}}"

