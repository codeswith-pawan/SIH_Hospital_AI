"""
Production Referral Feature Builder
AI Powered Smart Hospital Referral System
"""

import pandas as pd

from src.utils.helpers import calculate_distance_km

from src.utils.referral_rules import (
    check_test_availability,
    check_specialty_availability,
)


def build_referral_features(patient, hospital):
    """
    Build referral features from a patient-hospital pair.

    This uses the same business logic that was used
    while generating the historical referral dataset.
    """

    # --------------------------------
    # Distance
    # --------------------------------

    distance_km = calculate_distance_km(
        float(patient["latitude"]),
        float(patient["longitude"]),
        float(hospital["latitude"]),
        float(hospital["longitude"]),
    )

    # --------------------------------
    # Test Match
    # --------------------------------

    test_result = check_test_availability(
        patient,
        hospital,
    )

    test_match = (
        1
        if test_result["all_available"]
        else 0
    )

    # --------------------------------
    # Specialty Match
    # --------------------------------

    specialty_result = check_specialty_availability(
        patient,
        hospital,
    )

    specialty_match = (
        1
        if specialty_result["all_available"]
        else 0
    )

    # --------------------------------
    # ICU Match
    # --------------------------------

    if patient["icu_required"] == "Yes":

        icu_match = (
            1
            if hospital["available_icu_beds"] > 0
            else 0
        )

    else:

        icu_match = 1

    # --------------------------------
    # Bed Match
    # --------------------------------

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

    # --------------------------------
    # Occupancy Rate
    # --------------------------------

    total_beds = hospital["total_beds"]
    occupied_beds = hospital["occupied_beds"]

    occupancy_rate = (
        occupied_beds / total_beds
        if total_beds > 0
        else 1.0
    )

    # --------------------------------
    # Hospital Capabilities
    # --------------------------------

    emergency_24x7 = (
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

    # --------------------------------
    # Return
    # --------------------------------

    return {
        "distance_km": distance_km,

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
            emergency_24x7,

        "ambulance":
            ambulance,

        "oxygen_support":
            oxygen_support,

        "ventilator":
            ventilator,

        "blood_bank":
            blood_bank,
    }