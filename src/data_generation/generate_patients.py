"""
Generate Synthetic Patients Dataset
AI Powered Smart Hospital Referral System
"""

import random
import pandas as pd
import numpy as np

from faker import Faker

from src.utils.config import *
from src.utils.helpers import *
from src.utils.medical_rules import *

fake = Faker("en_IN")

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def generate_patient(index):

    patient = {}

    # -------------------------
    # IDs
    # -------------------------

    patient["patient_id"] = generate_patient_id(index)

    patient["abha_id"] = generate_abha_id()

    # -------------------------
    # Gender
    # -------------------------

    gender = np.random.choice(
        list(GENDER_WEIGHTS.keys()),
        p=list(GENDER_WEIGHTS.values())
    )

    patient["gender"] = gender

    # -------------------------
    # Name
    # -------------------------

    if gender == "Male":

        patient["first_name"] = random.choice(FIRST_NAMES_MALE)

    elif gender == "Female":

        patient["first_name"] = random.choice(FIRST_NAMES_FEMALE)

    else:

        patient["first_name"] = "Alex"

    patient["last_name"] = random.choice(LAST_NAMES)

    # -------------------------
    # Age
    # -------------------------

    patient["age"] = generate_age()

    # -------------------------
    # State
    # -------------------------

    state = random.choice(INDIAN_STATES)

    patient["state"] = state

    # -------------------------
    # District
    # -------------------------

    if state in DISTRICTS:

        patient["district"] = random.choice(DISTRICTS[state])

    else:

        patient["district"] = "Unknown"

        # -------------------------
    # Height
    # -------------------------

    patient["height_cm"] = generate_height()

    # -------------------------
    # Weight
    # -------------------------

    patient["weight_kg"] = generate_weight()

    # -------------------------
    # BMI
    # -------------------------

    patient["bmi"] = calculate_bmi(
        patient["height_cm"],
        patient["weight_kg"]
    )

    # -------------------------
    # Blood Group
    # -------------------------

    blood_groups = list(BLOOD_GROUPS.keys())
    blood_probs = np.array(list(BLOOD_GROUPS.values()))
    blood_probs = blood_probs / blood_probs.sum()

    patient["blood_group"] = np.random.choice(
        blood_groups,
        p=blood_probs
)

        # -------------------------
    # Lifestyle
    # -------------------------

    # Smoking probability increases with age
    smoking_prob = 0.05

    if patient["age"] >= 40:
        smoking_prob = 0.15

    if patient["age"] >= 60:
        smoking_prob = 0.25

    patient["smoking"] = np.random.choice(
        ["Yes", "No"],
        p=[smoking_prob, 1 - smoking_prob]
    )

    # Alcohol
    alcohol_prob = 0.08

    if patient["age"] >= 30:
        alcohol_prob = 0.18

    patient["alcohol"] = np.random.choice(
        ["Yes", "No"],
        p=[alcohol_prob, 1 - alcohol_prob]
    )

        # -------------------------
    # Comorbidities
    # -------------------------

    age = patient["age"]

    diabetes_prob = 0.03

    if age >= 40:
        diabetes_prob = 0.12

    if age >= 60:
        diabetes_prob = 0.25

    patient["diabetes"] = np.random.choice(
        ["Yes", "No"],
        p=[diabetes_prob, 1 - diabetes_prob]
    )

    hypertension_prob = 0.04

    if age >= 45:
        hypertension_prob = 0.18

    if age >= 65:
        hypertension_prob = 0.35

    patient["hypertension"] = np.random.choice(
        ["Yes", "No"],
        p=[hypertension_prob, 1 - hypertension_prob]
    )

    heart_prob = 0.01

    if patient["smoking"] == "Yes":
        heart_prob += 0.05

    if patient["diabetes"] == "Yes":
        heart_prob += 0.05

    if age >= 60:
        heart_prob += 0.08

    heart_prob = min(heart_prob, 0.30)

    patient["heart_disease"] = np.random.choice(
        ["Yes", "No"],
        p=[heart_prob, 1 - heart_prob]
    )

    asthma_prob = 0.05

    patient["asthma"] = np.random.choice(
        ["Yes", "No"],
        p=[asthma_prob, 1 - asthma_prob]
    )

 

    return patient


def generate_dataset():

    patients = []

    for i in range(NUM_PATIENTS):

        patients.append(
            generate_patient(i + 1)
        )

    df = pd.DataFrame(patients)

    df.to_csv(
        "datasets/final/patients.csv",
        index=False
    )

    print(f"Generated {len(df)} patients")


if __name__ == "__main__":
    generate_dataset()