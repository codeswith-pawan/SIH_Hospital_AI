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