"""
Helper Functions
AI Powered Smart Hospital Referral System
"""

import random
import uuid
from datetime import datetime, timedelta

import numpy as np


# ----------------------------
# Patient ID
# ----------------------------

def generate_patient_id(index: int) -> str:
    return f"PAT{index:06d}"


# ----------------------------
# ABHA-like ID
# ----------------------------

def generate_abha_id() -> str:
    return "".join(str(random.randint(0, 9)) for _ in range(14))


# ----------------------------
# Age
# ----------------------------

def generate_age():
    return np.random.choice(
        [random.randint(0, 15),
         random.randint(16, 40),
         random.randint(41, 60),
         random.randint(61, 90)],
        p=[0.15, 0.45, 0.25, 0.15]
    )


# ----------------------------
# Height
# ----------------------------

def generate_height():
    return round(random.uniform(145, 190), 1)


# ----------------------------
# Weight
# ----------------------------

def generate_weight():
    return round(random.uniform(40, 110), 1)


# ----------------------------
# BMI
# ----------------------------

def calculate_bmi(height_cm, weight_kg):

    height = height_cm / 100

    return round(weight_kg / (height ** 2), 2)


# ----------------------------
# Random Yes / No
# ----------------------------

def random_yes_no(prob_yes=0.3):

    return np.random.choice(
        ["Yes", "No"],
        p=[prob_yes, 1 - prob_yes]
    )


# ----------------------------
# Timestamp
# ----------------------------

def generate_timestamp():

    start = datetime(2024, 1, 1)

    end = datetime(2025, 12, 31)

    seconds = random.randint(
        0,
        int((end - start).total_seconds())
    )

    return start + timedelta(seconds=seconds)


# ----------------------------
# Generate Symptoms
# ----------------------------

def generate_symptoms(disease, disease_symptoms):
    """
    Generate symptoms based on the patient's disease.
    Returns 2-4 symptoms.
    """

    available_symptoms = disease_symptoms.get(
        disease,
        ["Fatigue"]
    )

    number_of_symptoms = min(
        len(available_symptoms),
        random.randint(2, 4)
    )

    return random.sample(
        available_symptoms,
        number_of_symptoms
    )


# ----------------------------
# Generate Disease-based Vitals
# ----------------------------

def generate_vitals(disease, disease_vitals):
    """
    Generate synthetic vitals based on disease-specific ranges.
    """

    ranges = disease_vitals.get(disease)

    if ranges is None:
        raise ValueError(
            f"No vital ranges configured for disease: {disease}"
        )

    return {
        "spo2": round(
            np.random.uniform(
                ranges["spo2"][0],
                ranges["spo2"][1]
            ),
            1
        ),

        "systolic_bp": int(
            np.random.randint(
                ranges["systolic_bp"][0],
                ranges["systolic_bp"][1] + 1
            )
        ),

        "diastolic_bp": int(
            np.random.randint(
                ranges["diastolic_bp"][0],
                ranges["diastolic_bp"][1] + 1
            )
        ),

        "heart_rate": int(
            np.random.randint(
                ranges["heart_rate"][0],
                ranges["heart_rate"][1] + 1
            )
        ),

        "respiratory_rate": int(
            np.random.randint(
                ranges["respiratory_rate"][0],
                ranges["respiratory_rate"][1] + 1
            )
        ),

        "temperature": round(
            np.random.uniform(
                ranges["temperature"][0],
                ranges["temperature"][1]
            ),
            1
        )
    }

# ----------------------------
# Calculate Severity Score
# ----------------------------

def calculate_severity_score(patient):
    """
    Calculate a synthetic triage severity score from
    patient vitals, age, symptoms and comorbidities.

    Score range: 0-100
    """

    score = 0

    # -------------------------
    # SpO2
    # -------------------------

    spo2 = patient["spo2"]

    if spo2 < 85:
        score += 30
    elif spo2 < 90:
        score += 25
    elif spo2 < 94:
        score += 15
    elif spo2 < 96:
        score += 5

    # -------------------------
    # Systolic BP
    # -------------------------

    systolic_bp = patient["systolic_bp"]

    if systolic_bp < 80:
        score += 25
    elif systolic_bp < 90:
        score += 18
    elif systolic_bp > 180:
        score += 20
    elif systolic_bp > 160:
        score += 12

    # -------------------------
    # Heart Rate
    # -------------------------

    heart_rate = patient["heart_rate"]

    if heart_rate > 140:
        score += 20
    elif heart_rate > 120:
        score += 12
    elif heart_rate < 50:
        score += 15

    # -------------------------
    # Respiratory Rate
    # -------------------------

    respiratory_rate = patient["respiratory_rate"]

    if respiratory_rate > 30:
        score += 20
    elif respiratory_rate > 24:
        score += 10

    # -------------------------
    # Temperature
    # -------------------------

    temperature = patient["temperature"]

    if temperature >= 104:
        score += 15
    elif temperature >= 102:
        score += 8

    # -------------------------
    # Age
    # -------------------------

    age = patient["age"]

    if age >= 75:
        score += 10
    elif age >= 65:
        score += 6

    # -------------------------
    # Comorbidities
    # -------------------------

    if patient["diabetes"] == "Yes":
        score += 3

    if patient["hypertension"] == "Yes":
        score += 3

    if patient["heart_disease"] == "Yes":
        score += 8

    # -------------------------
    # Critical Symptoms
    # -------------------------

    critical_symptoms = {
        "Chest Pain",
        "Shortness of Breath",
        "Loss of Consciousness",
        "Speech Difficulty",
        "Low Oxygen",
        "Bleeding",
        "Seizure",
        "Confusion",
        "Low Blood Pressure"
    }

    patient_symptoms = {
        patient.get("symptom_1"),
        patient.get("symptom_2"),
        patient.get("symptom_3"),
        patient.get("symptom_4")
    }

    critical_symptoms_present = (
        patient_symptoms & critical_symptoms
    )

    score += min(
        len(critical_symptoms_present) * 5,
        15
    )

    return min(score, 100)

# ----------------------------
# Convert Severity Score
# to Priority
# ----------------------------

def severity_to_priority(score):
    """
    Convert severity score into triage priority.
    """

    if score >= 50:
        return "Critical"

    if score >= 25:
        return "Urgent"

    return "Stable"

# ----------------------------
# ICU Requirement
# ----------------------------

def calculate_icu_requirement(patient):
    """
    Determine whether ICU-level care may be required
    based on severity and critical indicators.
    """

    if patient["severity_score"] >= 60:
        return "Yes"

    if patient["spo2"] < 90:
        return "Yes"

    if patient["systolic_bp"] < 90:
        return "Yes"

    if patient["respiratory_rate"] > 30:
        return "Yes"

    if patient["heart_disease"] == "Yes" and patient["severity_score"] >= 40:
        return "Yes"

    return "No"


# ----------------------------
# Ambulance Requirement
# ----------------------------

def calculate_ambulance_requirement(patient):
    """
    Determine whether emergency ambulance transfer
    may be required.
    """

    if patient["priority"] == "Critical":
        return "Yes"

    if patient["spo2"] < 90:
        return "Yes"

    if patient["systolic_bp"] < 90:
        return "Yes"

    if patient["symptom_1"] in [
        "Loss of Consciousness",
        "Seizure",
        "Bleeding"
    ]:
        return "Yes"

    return "No"

# ----------------------------
# Referral Requirement
# ----------------------------

def calculate_referral_requirement(patient):
    """
    Determine whether referral to another hospital
    should be considered.
    """

    if patient["priority"] in ["Critical", "Urgent"]:
        return "Yes"

    if patient["icu_required"] == "Yes":
        return "Yes"

    return "No"

# ----------------------------
# Required Tests
# ----------------------------

def get_required_tests(disease, disease_required_tests):
    """
    Return the main diagnostic tests associated
    with the patient's disease.
    """

    return disease_required_tests.get(
        disease,
        ["Blood Test"]
    )

# ----------------------------
# Calculate Distance
# ----------------------------

def calculate_distance_km(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculate approximate distance between
    patient and hospital using Haversine formula.
    """

    import math

    R = 6371.0

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return round(R * c, 2)