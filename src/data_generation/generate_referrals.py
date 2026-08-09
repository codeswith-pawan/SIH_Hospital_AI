"""
Generate Synthetic Historical Referral Dataset
AI Powered Smart Hospital Referral System
"""

import random
import pandas as pd
import numpy as np

from src.utils.config import RANDOM_SEED
from src.utils.referral_rules import (
    check_test_availability,
    check_specialty_availability
)
from src.utils.helpers import calculate_distance_km


# ----------------------------------------
# Configuration
# ----------------------------------------

NUM_REFERRALS = 150_000

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


# ----------------------------------------
# Load Data
# ----------------------------------------

patients = pd.read_csv(
    "datasets/final/patients.csv"
)

hospitals = pd.read_csv(
    "datasets/final/hospitals.csv"
)


# ----------------------------------------
# Generate Referral
# ----------------------------------------

def generate_referral(
    referral_index,
    patient,
    hospital
):

    # ------------------------------------
    # Distance
    # ------------------------------------

    distance_km = calculate_distance_km(
        patient["latitude"],
        patient["longitude"],
        hospital["latitude"],
        hospital["longitude"]
    )

    # ------------------------------------
    # Test Match
    # ------------------------------------

    test_result = check_test_availability(
        patient,
        hospital
    )

    test_match = (
        1 if test_result["all_available"]
        else 0
    )

    # ------------------------------------
    # Specialty Match
    # ------------------------------------

    specialty_result = (
        check_specialty_availability(
            patient,
            hospital
        )
    )

    specialty_match = (
        1
        if specialty_result["all_available"]
        else 0
    )

    # ------------------------------------
    # ICU Match
    # ------------------------------------

    if patient["icu_required"] == "Yes":

        icu_match = (
            1
            if hospital["available_icu_beds"] > 0
            else 0
        )

    else:

        icu_match = 1

    # ------------------------------------
    # Bed Match
    # ------------------------------------

    if patient["priority"] == "Critical":

        bed_match = (
            1
            if hospital["available_emergency_beds"] > 0
            else 0
        )

    else:

        bed_match = (
            1
            if hospital["available_beds"] > 0
            else 0
        )

    # ------------------------------------
    # Hospital Capability
    # ------------------------------------

    emergency_support = (
        1
        if hospital["emergency_24x7"] == "Yes"
        else 0
    )

    ambulance = (
        1
        if hospital["ambulance"] == "Yes"
        else 0
    )

    oxygen_support = (
        1
        if hospital["oxygen_support"] == "Yes"
        else 0
    )

    ventilator = (
        1
        if hospital["ventilator"] == "Yes"
        else 0
    )

    blood_bank = (
        1
        if hospital["blood_bank"] == "Yes"
        else 0
    )

    # ------------------------------------
    # Hospital Load
    # ------------------------------------

    total_beds = hospital["total_beds"]
    occupied_beds = hospital["occupied_beds"]

    occupancy_rate = (
        occupied_beds / total_beds
        if total_beds > 0
        else 1.0
    )

    # ------------------------------------
    # Referral Acceptance Probability
    # ------------------------------------

    acceptance_probability = 0.50

    # Distance effect
    if distance_km <= 10:
        acceptance_probability += 0.12
    elif distance_km <= 25:
        acceptance_probability += 0.08
    elif distance_km <= 50:
        acceptance_probability += 0.04
    elif distance_km > 200:
        acceptance_probability -= 0.12

    # Tests
    if test_match:
        acceptance_probability += 0.10
    else:
        acceptance_probability -= 0.25

    # Specialty
    if specialty_match:
        acceptance_probability += 0.10
    else:
        acceptance_probability -= 0.25

    # Beds
    if bed_match:
        acceptance_probability += 0.08
    else:
        acceptance_probability -= 0.30

    # ICU
    if icu_match:
        acceptance_probability += 0.10

    else:
        acceptance_probability -= 0.30

    # Emergency
    if emergency_support:
        acceptance_probability += 0.04

    # Ambulance
    if ambulance:
        acceptance_probability += 0.03

    # Oxygen
    if oxygen_support:
        acceptance_probability += 0.03

    # High occupancy reduces acceptance
    if occupancy_rate >= 0.90:
        acceptance_probability -= 0.12

    elif occupancy_rate >= 0.80:
        acceptance_probability -= 0.06

    # Critical patients need stronger capability
    if patient["priority"] == "Critical":

        if hospital["available_icu_beds"] >= 10:
            acceptance_probability += 0.08

        elif hospital["available_icu_beds"] == 0:
            acceptance_probability -= 0.25

    # Keep probability valid
    acceptance_probability = np.clip(
        acceptance_probability,
        0.02,
        0.98
    )

    # ------------------------------------
    # Referral Accepted
    # ------------------------------------

    referral_accepted = np.random.binomial(
        1,
        acceptance_probability
    )

    # ------------------------------------
    # Response Time
    # ------------------------------------

    base_response = 10

    if distance_km > 50:
        base_response += 10

    if occupancy_rate >= 0.80:
        base_response += 10

    if patient["priority"] == "Critical":
        base_response -= 3

    response_time = max(
        2,
        int(
            np.random.normal(
                base_response,
                5
            )
        )
    )

    # ------------------------------------
    # Referral Success
    # ------------------------------------

    success_probability = 0.50

    if referral_accepted:
        success_probability += 0.20
    else:
        success_probability -= 0.35

    if test_match:
        success_probability += 0.10
    else:
        success_probability -= 0.20

    if specialty_match:
        success_probability += 0.10
    else:
        success_probability -= 0.20

    if bed_match:
        success_probability += 0.08
    else:
        success_probability -= 0.20

    if distance_km <= 25:
        success_probability += 0.08

    elif distance_km > 200:
        success_probability -= 0.10

    if occupancy_rate >= 0.90:
        success_probability -= 0.10

    if patient["priority"] == "Critical":

        if hospital["available_icu_beds"] >= 10:
            success_probability += 0.10

        elif hospital["available_icu_beds"] == 0:
            success_probability -= 0.25

    success_probability = np.clip(
        success_probability,
        0.01,
        0.99
    )

    referral_success = np.random.binomial(
        1,
        success_probability
    )

    # ------------------------------------
    # Outcome
    # ------------------------------------

    if referral_success == 1:

        if patient["priority"] == "Critical":
            outcome = "Successfully Treated"

        else:
            outcome = "Successfully Referred"

    elif referral_accepted == 1:

        outcome = "Delayed Treatment"

    else:

        outcome = "Referral Rejected"

    # ------------------------------------
    # Return Record
    # ------------------------------------

    return {

        "referral_id":
            f"REF{referral_index:06d}",

        "patient_id":
            patient["patient_id"],

        "hospital_id":
            hospital["hospital_id"],

        "disease":
            patient["disease"],

        "priority":
            patient["priority"],

        "distance_km":
            distance_km,

        "available_beds":
            hospital["available_beds"],

        "available_icu_beds":
            hospital["available_icu_beds"],

        "occupancy_rate":
            round(occupancy_rate, 3),

        "specialty_match":
            specialty_match,

        "test_match":
            test_match,

        "bed_match":
            bed_match,

        "icu_match":
            icu_match,

        "emergency_24x7":
            emergency_support,

        "ambulance":
            ambulance,

        "oxygen_support":
            oxygen_support,

        "ventilator":
            ventilator,

        "blood_bank":
            blood_bank,

        "referral_accepted":
            referral_accepted,

        "response_time_minutes":
            response_time,

        "referral_success":
            referral_success,

        "outcome":
            outcome
    }


# ----------------------------------------
# Generate Dataset
# ----------------------------------------

def generate_dataset():

    referrals = []

    for i in range(NUM_REFERRALS):

        # Random patient
        patient = patients.iloc[
            np.random.randint(
                0,
                len(patients)
            )
        ]

        # Random hospital
        hospital = hospitals.iloc[
            np.random.randint(
                0,
                len(hospitals)
            )
        ]

        referral = generate_referral(
            i + 1,
            patient,
            hospital
        )

        referrals.append(
            referral
        )

        if (i + 1) % 25_000 == 0:
            print(
                f"Generated {i + 1} referrals"
            )

    df = pd.DataFrame(
        referrals
    )

    df.to_csv(
        "datasets/final/referrals.csv",
        index=False
    )

    print(
        f"Generated {len(df)} referrals"
    )

    print(
        "Saved to: "
        "datasets/final/referrals.csv"
    )


# ----------------------------------------
# Main
# ----------------------------------------

if __name__ == "__main__":
    generate_dataset()