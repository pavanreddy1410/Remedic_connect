from itertools import combinations

import pandas as pd
from sklearn.ensemble import IsolationForest

DRUG_RULES = {
    tuple(sorted(["aspirin", "warfarin"])): {
        "interaction_risk": "high",
        "severity": "critical",
        "recommendation": "Avoid combined use unless doctor-supervised due to bleeding risk.",
    },
    tuple(sorted(["ibuprofen", "lisinopril"])): {
        "interaction_risk": "moderate",
        "severity": "medium",
        "recommendation": "Monitor blood pressure and kidney function.",
    },
}


# Lightweight synthetic baseline approximating normal lab ranges.
TRAINING_DATA = pd.DataFrame(
    [
        {"glucose": 90, "cholesterol": 170, "hemoglobin": 14.2},
        {"glucose": 95, "cholesterol": 180, "hemoglobin": 13.8},
        {"glucose": 100, "cholesterol": 190, "hemoglobin": 14.5},
        {"glucose": 110, "cholesterol": 200, "hemoglobin": 13.2},
        {"glucose": 88, "cholesterol": 165, "hemoglobin": 15.1},
        {"glucose": 105, "cholesterol": 210, "hemoglobin": 12.8},
        {"glucose": 115, "cholesterol": 220, "hemoglobin": 13.0},
        {"glucose": 85, "cholesterol": 160, "hemoglobin": 14.8},
    ]
)
MODEL = IsolationForest(contamination=0.15, random_state=42)
MODEL.fit(TRAINING_DATA)


def detect_interactions(medicines: list[str]) -> list[dict]:
    lowered = [m.lower() for m in medicines]
    findings = []
    for a, b in combinations(lowered, 2):
        key = tuple(sorted([a, b]))
        if key in DRUG_RULES:
            findings.append({"pair": [a, b], **DRUG_RULES[key]})
    if not findings:
        findings.append(
            {
                "pair": lowered,
                "interaction_risk": "low",
                "severity": "low",
                "recommendation": "No major known interaction in the starter ruleset.",
            }
        )
    return findings


def analyze_lab_metrics(glucose: float | None, cholesterol: float | None, hemoglobin: float | None) -> dict:
    glucose = glucose if glucose is not None else 100
    cholesterol = cholesterol if cholesterol is not None else 180
    hemoglobin = hemoglobin if hemoglobin is not None else 14

    sample = pd.DataFrame([{"glucose": glucose, "cholesterol": cholesterol, "hemoglobin": hemoglobin}])
    pred = MODEL.predict(sample)[0]  # -1 anomaly, 1 normal
    score = float(MODEL.decision_function(sample)[0])

    suggestions = []
    if glucose > 140:
        suggestions.append("High glucose detected. Recommend diabetes screening.")
    if cholesterol > 240:
        suggestions.append("High cholesterol detected. Recommend lipid management plan.")
    if hemoglobin < 12:
        suggestions.append("Possible anemia indicators found. Recommend CBC follow-up.")

    return {
        "anomaly": pred == -1,
        "anomaly_score": score,
        "suggestions": suggestions or ["No immediate abnormalities detected in provided values."],
    }
