"""
ML Prediction Layer
AI Powered Smart Hospital Referral System
"""

import os
import joblib
import pandas as pd

from src.prediction.feature_builder import (
    build_referral_features
)


MODEL_PATH = "models/referral_success_model.joblib"


MODEL_FEATURES = [
    "distance_km",
    "available_beds",
    "available_icu_beds",
    "occupancy_rate",
    "specialty_match",
    "test_match",
    "bed_match",
    "icu_match",
    "emergency_24x7",
    "ambulance",
    "oxygen_support",
    "ventilator",
    "blood_bank",
    "disease_Appendicitis",
    "disease_Asthma",
    "disease_Burn Injury",
    "disease_COPD",
    "disease_COVID-like Infection",
    "disease_Dengue",
    "disease_Diabetes",
    "disease_Food Poisoning",
    "disease_Fracture",
    "disease_Heart Attack",
    "disease_Hypertension",
    "disease_Kidney Failure",
    "disease_Malaria",
    "disease_Pneumonia",
    "disease_Sepsis",
    "disease_Stroke",
    "disease_Trauma",
    "disease_Viral Fever",
    "priority_Critical",
    "priority_Stable",
    "priority_Urgent",
]


def load_model():
    """Load trained Random Forest model."""

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def build_prediction_features(patient, hospital):
    """
    Build the exact 34 features required
    by the trained model.
    """

    referral_features = build_referral_features(
        patient,
        hospital
    )

    disease = patient["disease"]
    priority = patient["priority"]

    features = referral_features.copy()

    # --------------------------------
    # Disease one-hot encoding
    # --------------------------------

    for feature in MODEL_FEATURES:

        if feature.startswith("disease_"):

            disease_name = feature.replace(
                "disease_",
                "",
                1
            )

            features[feature] = int(
                disease == disease_name
            )

    # --------------------------------
    # Priority one-hot encoding
    # --------------------------------

    for feature in MODEL_FEATURES:

        if feature.startswith("priority_"):

            priority_name = feature.replace(
                "priority_",
                "",
                1
            )

            features[feature] = int(
                priority == priority_name
            )

    # --------------------------------
    # DataFrame
    # --------------------------------

    X = pd.DataFrame(
        [features],
        columns=MODEL_FEATURES
    )

    return X


def predict_referral_success(
    patient,
    hospital
):
    """
    Predict referral success probability
    for one patient-hospital pair.
    """

    model = load_model()

    X = build_prediction_features(
        patient,
        hospital
    )

    probability = model.predict_proba(
        X
    )[0][1]

    prediction = model.predict(X)[0]

    return {
        "prediction": int(prediction),
        "success_probability": round(
            float(probability),
            4
        )
    }


def validate_model_features():
    """Verify production features match model."""

    model = load_model()

    model_features = list(
        model.feature_names_in_
    )

    if model_features != MODEL_FEATURES:

        raise ValueError(
            "Model feature mismatch!\n"
            f"Expected: {MODEL_FEATURES}\n"
            f"Model: {model_features}"
        )

    return True


if __name__ == "__main__":

    validate_model_features()

    print(
        "Prediction pipeline feature validation: PASSED"
    )

    print(
        f"Feature count: {len(MODEL_FEATURES)}"
    )