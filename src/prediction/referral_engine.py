"""
Hospital Referral Engine
AI Powered Smart Hospital Referral System
"""

import pandas as pd

from src.prediction.ranking_engine import (
    rank_hospitals
)

from src.utils.referral_rules import (
    check_hospital_eligibility
)

from src.utils.helpers import (
    calculate_distance_km
)


def find_eligible_hospitals(patient, hospitals):
    """
    Find eligible hospitals and calculate
    distance from patient location.
    """

    # --------------------------------
    # Referral Decision
    # --------------------------------

    if patient["referral_required"] != "Yes":
        return pd.DataFrame()

    eligible_hospitals = []

    # --------------------------------
    # Check All Hospitals
    # --------------------------------

    for _, hospital in hospitals.iterrows():

        # --------------------------------
        # Eligibility
        # --------------------------------

        if not check_hospital_eligibility(
            patient,
            hospital
        ):
            continue

        # --------------------------------
        # Distance
        # --------------------------------

        distance = calculate_distance_km(
            patient["latitude"],
            patient["longitude"],
            hospital["latitude"],
            hospital["longitude"]
        )

        hospital_data = hospital.copy()

        hospital_data["distance_km"] = distance

        eligible_hospitals.append(
            hospital_data
        )

    # --------------------------------
    # No Eligible Hospital
    # --------------------------------

    if not eligible_hospitals:
        return pd.DataFrame()

    # --------------------------------
    # Create DataFrame
    # --------------------------------

    result = pd.DataFrame(
        eligible_hospitals
    )

    # --------------------------------
    # Rank Hospitals
    # --------------------------------

    result = rank_hospitals(
        result,
        patient["priority"]
    )

    return result