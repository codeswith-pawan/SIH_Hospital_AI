"""
Generate Synthetic Patients Dataset
AI Powered Smart Hospital Referral System
"""

import random

import numpy as np
import pandas as pd
from faker import Faker

from src.utils.config import *
from src.utils.helpers import *
from src.utils.medical_rules import *


# ----------------------------------------
# Faker
# ----------------------------------------

fake = Faker("en_IN")

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ----------------------------------------
# Generate One Patient
# ----------------------------------------

def generate_patient(index):

    patient = {}

    # ------------------------------------
    # IDs
    # ------------------------------------

    patient["patient_id"] = generate_patient_id(index)
    patient["abha_id"] = generate_abha_id()

    # ------------------------------------
    # Gender
    # ------------------------------------

    gender = np.random.choice(
        list(GENDER_WEIGHTS.keys()),
        p=list(GENDER_WEIGHTS.values())
    )

    patient["gender"] = gender

    # ------------------------------------
    # Name
    # ------------------------------------

    if gender == "Male":

        patient["first_name"] = random.choice(
            FIRST_NAMES_MALE
        )

    elif gender == "Female":

        patient["first_name"] = random.choice(
            FIRST_NAMES_FEMALE
        )

    else:

        patient["first_name"] = "Alex"

        patient["last_name"] = random.choice(
            LAST_NAMES
    )

    # ------------------------------------
    # Age
    # ------------------------------------

    patient["age"] = generate_age()

    # ------------------------------------
    # State
    # ------------------------------------

    state = random.choice(
        INDIAN_STATES
    )

    patient["state"] = state

    # ------------------------------------
    # District
    # ------------------------------------

    if state in DISTRICTS:

        patient["district"] = random.choice(
            DISTRICTS[state]
        )

    else:

        patient["district"] = "Unknown"

    # ------------------------------------
    # Geographic Coordinates
    # ------------------------------------

    base_lat, base_lon = DISTRICT_COORDINATES[
        patient["district"]
    ]

    # Small random variation around district
    patient["latitude"] = round(
        base_lat + np.random.uniform(-0.08, 0.08),
        6
    )

    patient["longitude"] = round(
        base_lon + np.random.uniform(-0.08, 0.08),
        6
    )

    # ------------------------------------
    # Height
    # ------------------------------------

    patient["height_cm"] = generate_height()

    # ------------------------------------
    # Weight
    # ------------------------------------

    patient["weight_kg"] = generate_weight()

    # ------------------------------------
    # BMI
    # ------------------------------------

    patient["bmi"] = calculate_bmi(
        patient["height_cm"],
        patient["weight_kg"]
    )

    # ------------------------------------
    # Blood Group
    # ------------------------------------

    blood_groups = list(
        BLOOD_GROUPS.keys()
    )

    blood_probs = np.array(
        list(BLOOD_GROUPS.values()),
        dtype=float
    )

    blood_probs = (
        blood_probs /
        blood_probs.sum()
    )

    patient["blood_group"] = np.random.choice(
        blood_groups,
        p=blood_probs
    )

    # ------------------------------------
    # Lifestyle
    # ------------------------------------

    smoking_prob = 0.05

    if patient["age"] >= 40:
        smoking_prob = 0.15

    if patient["age"] >= 60:
        smoking_prob = 0.25

    patient["smoking"] = np.random.choice(
        ["Yes", "No"],
        p=[
            smoking_prob,
            1 - smoking_prob
        ]
    )

    # ------------------------------------
    # Alcohol
    # ------------------------------------

    alcohol_prob = 0.08

    if patient["age"] >= 30:
        alcohol_prob = 0.18

    patient["alcohol"] = np.random.choice(
        ["Yes", "No"],
        p=[
            alcohol_prob,
            1 - alcohol_prob
        ]
    )

    # ------------------------------------
    # Comorbidities
    # ------------------------------------

    age = patient["age"]

    # Diabetes

    diabetes_prob = 0.03

    if age >= 40:
        diabetes_prob = 0.12

    if age >= 60:
        diabetes_prob = 0.25

    patient["diabetes"] = np.random.choice(
        ["Yes", "No"],
        p=[
            diabetes_prob,
            1 - diabetes_prob
        ]
    )

    # Hypertension

    hypertension_prob = 0.04

    if age >= 45:
        hypertension_prob = 0.18

    if age >= 65:
        hypertension_prob = 0.35

    patient["hypertension"] = np.random.choice(
        ["Yes", "No"],
        p=[
            hypertension_prob,
            1 - hypertension_prob
        ]
    )

    # Heart Disease

    heart_prob = 0.01

    if patient["smoking"] == "Yes":
        heart_prob += 0.05

    if patient["diabetes"] == "Yes":
        heart_prob += 0.05

    if age >= 60:
        heart_prob += 0.08

    heart_prob = min(
        heart_prob,
        0.30
    )

    patient["heart_disease"] = np.random.choice(
        ["Yes", "No"],
        p=[
            heart_prob,
            1 - heart_prob
        ]
    )

    # Asthma

    asthma_prob = 0.05

    patient["asthma"] = np.random.choice(
        ["Yes", "No"],
        p=[
            asthma_prob,
            1 - asthma_prob
        ]
    )

    # ------------------------------------
    # Disease
    # ------------------------------------

    disease = select_disease(
        DISEASES,
        DISEASE_WEIGHTS
    )

    patient["disease"] = disease

    # ------------------------------------
    # Required Tests
    # ------------------------------------

    required_tests = get_required_tests(
        disease,
        DISEASE_REQUIRED_TESTS
    )

    patient["required_test_1"] = (
        required_tests[0]
    )

    patient["required_test_2"] = (
        required_tests[1]
        if len(required_tests) > 1
        else None
    )

    patient["required_test_3"] = (
        required_tests[2]
        if len(required_tests) > 2
        else None
    )

    patient["required_test_4"] = (
        required_tests[3]
        if len(required_tests) > 3
        else None
    )


    # ------------------------------------
    # Vitals
    # ------------------------------------

    vitals = generate_vitals(
        disease,
        DISEASE_VITALS
    )

    patient["spo2"] = vitals["spo2"]
    patient["systolic_bp"] = vitals["systolic_bp"]
    patient["diastolic_bp"] = vitals["diastolic_bp"]
    patient["heart_rate"] = vitals["heart_rate"]
    patient["respiratory_rate"] = vitals["respiratory_rate"]
    patient["temperature"] = vitals["temperature"]

    # ------------------------------------
    # Symptoms
    # ------------------------------------

    symptoms = generate_symptoms(
        disease,
        DISEASE_SYMPTOMS
    )

    patient["symptom_1"] = symptoms[0]

    patient["symptom_2"] = symptoms[1]

    patient["symptom_3"] = (
        symptoms[2]
        if len(symptoms) > 2
        else None
    )

    patient["symptom_4"] = (
        symptoms[3]
        if len(symptoms) > 3
        else None
    )

    # ------------------------------------
    # Severity Score
    # ------------------------------------

    patient["severity_score"] = calculate_severity_score(
        patient
    )

    # ------------------------------------
    # Priority
    # ------------------------------------

    patient["priority"] = severity_to_priority(
        patient["severity_score"]
    )

        # ------------------------------------
    # ICU Requirement
    # ------------------------------------

    patient["icu_required"] = calculate_icu_requirement(
        patient
    )

    # ------------------------------------
    # Ambulance Requirement
    # ------------------------------------

    patient["ambulance_required"] = calculate_ambulance_requirement(
        patient
    )

    # ------------------------------------
    # Referral Requirement
    # ------------------------------------

    patient["referral_required"] = calculate_referral_requirement(
        patient
    )

    return patient


# ----------------------------------------
# Generate Complete Dataset
# ----------------------------------------

def generate_dataset():

    patients = []

    for i in range(NUM_PATIENTS):

        patients.append(
            generate_patient(i + 1)
        )

    df = pd.DataFrame(patients)

    output_path = (
        "datasets/final/patients.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Generated {len(df)} patients"
    )

    print(
        f"Saved to: {output_path}"
    )


def generate_symptoms(disease, disease_symptoms):
    """
    Generate 2-4 disease-related symptoms.
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

def select_disease(diseases, weights):
    """
    Select a disease using configured probabilities.
    """

    disease_names = list(diseases)

    probabilities = np.array(
        [weights[disease] for disease in disease_names],
        dtype=float
    )

    probabilities = (
        probabilities /
        probabilities.sum()
    )

    return np.random.choice(
        disease_names,
        p=probabilities
    )


# ----------------------------------------
# Main
# ----------------------------------------

if __name__ == "__main__":

    generate_dataset()