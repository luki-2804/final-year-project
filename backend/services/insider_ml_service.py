from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


@dataclass
class ModelArtifacts:
    model: RandomForestClassifier | None = None
    feature_names: List[str] | None = None
    metrics: Dict | None = None


class InsiderThreatMLService:
    def __init__(self) -> None:
        self.artifacts = ModelArtifacts()

    def load_cert_logs(self, cert_root: str = "data/cert") -> pd.DataFrame:
        root = Path(cert_root)
        if not root.exists():
            return pd.DataFrame()

        frames: List[pd.DataFrame] = []
        for csv_file in root.glob("*.csv"):
            try:
                df = pd.read_csv(csv_file)
                df["source_file"] = csv_file.name
                frames.append(df)
            except Exception:
                continue

        if not frames:
            return pd.DataFrame()
        return pd.concat(frames, ignore_index=True)

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame()

        working = df.copy()
        if "date" in working.columns:
            working["date"] = pd.to_datetime(working["date"], errors="coerce")
            working["hour"] = working["date"].dt.hour.fillna(12)
        else:
            working["hour"] = 12

        if "user" not in working.columns:
            working["user"] = "unknown"

        working["odd_hour"] = working["hour"].apply(lambda h: int(h < 6 or h > 20))
        working["is_http"] = working["source_file"].str.contains("http", case=False).astype(int)
        working["is_device"] = working["source_file"].str.contains("device", case=False).astype(int)
        working["is_logon"] = working["source_file"].str.contains("logon", case=False).astype(int)

        grouped = (
            working.groupby("user")
            .agg(
                event_count=("user", "size"),
                odd_hour_activity=("odd_hour", "sum"),
                device_usage=("is_device", "sum"),
                suspicious_web_activity=("is_http", "sum"),
                login_events=("is_logon", "sum"),
            )
            .reset_index()
        )

        grouped["abnormal_behavior_indicator"] = (
            (grouped["odd_hour_activity"] > 5)
            | (grouped["suspicious_web_activity"] > 20)
            | (grouped["event_count"] > grouped["event_count"].quantile(0.90))
        ).astype(int)
        grouped["cross_cloud_context"] = (grouped["event_count"] > grouped["event_count"].median()).astype(int)

        # Proxy label for prototype when dataset lacks explicit labels.
        grouped["label"] = grouped["abnormal_behavior_indicator"]
        return grouped

    def train(self, feature_df: pd.DataFrame) -> Dict:
        if feature_df.empty:
            return {"status": "no_data", "message": "No CERT data found."}

        features = [
            "event_count",
            "odd_hour_activity",
            "device_usage",
            "suspicious_web_activity",
            "login_events",
            "cross_cloud_context",
            "abnormal_behavior_indicator",
        ]
        X = feature_df[features]
        y = feature_df["label"]

        if y.nunique() < 2:
            y = (feature_df["event_count"] > feature_df["event_count"].median()).astype(int)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        metrics = {
            "accuracy": round(float(accuracy_score(y_test, preds)), 4),
            "precision": round(float(precision_score(y_test, preds, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, preds, zero_division=0)), 4),
            "f1": round(float(f1_score(y_test, preds, zero_division=0)), 4),
            "confusion_matrix": confusion_matrix(y_test, preds).tolist(),
            "rows": int(len(feature_df)),
        }

        self.artifacts = ModelArtifacts(model=model, feature_names=features, metrics=metrics)
        return {"status": "trained", "metrics": metrics}

    def predict_risk(self, feature_row: Dict[str, float]) -> float:
        if not self.artifacts.model or not self.artifacts.feature_names:
            return 0.35

        features = [feature_row.get(name, 0.0) for name in self.artifacts.feature_names]
        proba = self.artifacts.model.predict_proba([features])[0][1]
        return float(round(proba, 4))


ml_service = InsiderThreatMLService()
