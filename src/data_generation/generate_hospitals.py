"""
Generate Synthetic Government Hospital Dataset

AI Powered Smart Hospital Referral System
"""

import random
import pandas as pd
import numpy as np

from src.utils.config import *


# ----------------------------------------
# Random Seed
# ----------------------------------------

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ----------------------------------------
# Hospital Names
# ----------------------------------------

HOSPITAL_PREFIXES = [
    "District",
    "Government",
    "State",
    "Civil",
    "Regional",
    "Integrated"
]

HOSPITAL_TYPES = [
    "Hospital",
    "Medical College Hospital",
    "District Hospital",
    "General Hospital"
]


# ----------------------------------------
# Generate Hospital
# ----------------------------------------

def generate_hospital(index):

    hospital = {}

    # ------------------------------------
    # Identity
    # ------------------------------------

    hospital["hospital_id"] = f"GH{index:05d}"

    state = random.choice(INDIAN_STATES)

    hospital["state"] = state

    if state in DISTRICTS:
        hospital["district"] = random.choice(
            DISTRICTS[state]
        )
    else:
        hospital["district"] = "Unknown"

    hospital["city"] = hospital["district"]

    hospital["hospital_name"] = (
        f"{random.choice(HOSPITAL_PREFIXES)} "
        f"{hospital['district']} "
        f"{random.choice(HOSPITAL_TYPES)}"
    )
    # ------------------------------------
    # Geographic Coordinates
    # ------------------------------------

    base_lat, base_lon = DISTRICT_COORDINATES[
        hospital["district"]
    ]

    # Small variation around district center
    hospital["latitude"] = round(
        base_lat + np.random.uniform(-0.08, 0.08),
        6
    )

    hospital["longitude"] = round(
        base_lon + np.random.uniform(-0.08, 0.08),
        6
    )

    # ------------------------------------
    # Beds
    # ------------------------------------

    total_beds = random.randint(
        100,
        1000
    )

    occupied_beds = random.randint(
    int(total_beds * 0.50),
    total_beds)


    hospital["total_beds"] = total_beds

    hospital["occupied_beds"] = occupied_beds

    hospital["available_beds"] = (
        total_beds - occupied_beds
    )

    # ------------------------------------
    # ICU
    # ------------------------------------

    icu_beds = max(
        5,
        int(total_beds * random.uniform(0.05, 0.15))
    )

    occupied_icu = random.randint(
    int(icu_beds * 0.50),
    icu_beds)

    hospital["icu_beds"] = icu_beds

    hospital["available_icu_beds"] = (
        icu_beds - occupied_icu
    )

    # ------------------------------------
    # Emergency Beds
    # ------------------------------------

    emergency_beds = max(
        10,
        int(total_beds * random.uniform(0.05, 0.12))
    )

    occupied_emergency = random.randint(
    int(emergency_beds * 0.50),
    emergency_beds)
    hospital["emergency_beds"] = emergency_beds

    hospital["available_emergency_beds"] = (
        emergency_beds - occupied_emergency
    )

    # ------------------------------------
    # Basic Services
    # ------------------------------------

    hospital["emergency_24x7"] = "Yes"

    hospital["accepts_referral"] = "Yes"

    hospital["ambulance"] = np.random.choice(
        ["Yes", "No"],
        p=[0.85, 0.15]
    )

    hospital["oxygen_support"] = np.random.choice(
        ["Yes", "No"],
        p=[0.95, 0.05]
    )

    hospital["ventilator"] = np.random.choice(
        ["Yes", "No"],
        p=[0.80, 0.20]
    )

    hospital["blood_bank"] = np.random.choice(
        ["Yes", "No"],
        p=[0.75, 0.25]
    )

        # ------------------------------------
    # Medical Specialties
    # ------------------------------------

    hospital["cardiology"] = np.random.choice(
        ["Yes", "No"],
        p=[0.65, 0.35]
    )

    hospital["neurology"] = np.random.choice(
        ["Yes", "No"],
        p=[0.55, 0.45]
    )

    hospital["nephrology"] = np.random.choice(
        ["Yes", "No"],
        p=[0.50, 0.50]
    )

    hospital["pulmonology"] = np.random.choice(
        ["Yes", "No"],
        p=[0.60, 0.40]
    )

    hospital["orthopedics"] = np.random.choice(
        ["Yes", "No"],
        p=[0.75, 0.25]
    )

    hospital["general_medicine"] = "Yes"

    hospital["general_surgery"] = np.random.choice(
        ["Yes", "No"],
        p=[0.85, 0.15]
    )

    hospital["trauma_unit"] = np.random.choice(
        ["Yes", "No"],
        p=[0.55, 0.45]
    )

    hospital["burn_unit"] = np.random.choice(
        ["Yes", "No"],
        p=[0.35, 0.65]
    )

    # ------------------------------------
    # Diagnostic Tests
    # ------------------------------------

    hospital["ct_scan"] = np.random.choice(
        ["Yes", "No"],
        p=[0.75, 0.25]
    )

    hospital["mri"] = np.random.choice(
        ["Yes", "No"],
        p=[0.55, 0.45]
    )

    hospital["xray"] = "Yes"

    hospital["ultrasound"] = np.random.choice(
        ["Yes", "No"],
        p=[0.90, 0.10]
    )

    hospital["ecg"] = np.random.choice(
        ["Yes", "No"],
        p=[0.90, 0.10]
    )

    hospital["dialysis"] = np.random.choice(
        ["Yes", "No"],
        p=[0.50, 0.50]
    )

        # ------------------------------------
    # Diagnostic Test Availability
    # ------------------------------------

    hospital["blood_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.95, 0.05]
    )

    hospital["cbc"] = np.random.choice(
        ["Yes", "No"],
        p=[0.90, 0.10]
    )

    hospital["troponin_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.70, 0.30]
    )

    hospital["dengue_ns1_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.65, 0.35]
    )

    hospital["malaria_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.70, 0.30]
    )

    hospital["blood_glucose_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.95, 0.05]
    )

    hospital["hba1c_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.80, 0.20]
    )

    hospital["kidney_function_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.80, 0.20]
    )

    hospital["pulmonary_function_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.55, 0.45]
    )

    hospital["blood_culture"] = np.random.choice(
        ["Yes", "No"],
        p=[0.65, 0.35]
    )

    hospital["lactate_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.60, 0.40]
    )

    hospital["stool_test"] = np.random.choice(
        ["Yes", "No"],
        p=[0.65, 0.35]
    )

    return hospital


# ----------------------------------------
# Generate Dataset
# ----------------------------------------

def generate_dataset():

    hospitals = []

    for i in range(NUM_HOSPITALS):

        hospitals.append(
            generate_hospital(i + 1)
        )

    df = pd.DataFrame(hospitals)

    output_path = (
        "datasets/final/hospitals.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Generated {len(df)} hospitals"
    )

    print(
        f"Saved to: {output_path}"
    )


# ----------------------------------------
# Main
# ----------------------------------------

if __name__ == "__main__":

    generate_dataset()