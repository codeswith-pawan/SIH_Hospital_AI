"""
Hospital Ranking Engine
AI Powered Smart Hospital Referral System
"""

import pandas as pd


def calculate_hospital_score(
    hospital,
    priority
):
    """
    Calculate hospital suitability score.
    Higher score = better hospital.
    """

    score = 0.0

    # --------------------------------
    # Distance — 30 points
    # --------------------------------

    distance = hospital["distance_km"]

    if distance <= 10:
        score += 30
    elif distance <= 25:
        score += 25
    elif distance <= 50:
        score += 18
    elif distance <= 100:
        score += 10
    elif distance <= 200:
        score += 5
    else:
        score += 0

    # --------------------------------
    # Bed Availability — 25 points
    # --------------------------------

    beds = hospital["available_beds"]

    if beds >= 300:
        score += 25
    elif beds >= 200:
        score += 22
    elif beds >= 100:
        score += 17
    elif beds >= 50:
        score += 10
    elif beds > 0:
        score += 5

    # --------------------------------
    # ICU Availability — 20 points
    # --------------------------------

    if priority == "Critical":

        icu_beds = hospital["available_icu_beds"]

        if icu_beds >= 30:
            score += 20
        elif icu_beds >= 20:
            score += 17
        elif icu_beds >= 10:
            score += 12
        elif icu_beds > 0:
            score += 5

    else:
        score += 10

    # --------------------------------
    # Emergency Support — 10 points
    # --------------------------------

    if hospital["emergency_24x7"] == "Yes":
        score += 10

    # --------------------------------
    # Ambulance — 5 points
    # --------------------------------

    if hospital["ambulance"] == "Yes":
        score += 5

    # --------------------------------
    # Oxygen Support — 5 points
    # --------------------------------

    if hospital["oxygen_support"] == "Yes":
        score += 5

    # --------------------------------
    # Final score
    # --------------------------------

    return round(score, 2)


def rank_hospitals(
    hospitals,
    priority
):
    """
    Rank eligible hospitals from best
    to worst.
    """

    if hospitals.empty:
        return hospitals

    result = hospitals.copy()

    result["hospital_score"] = result.apply(
        lambda row: calculate_hospital_score(
            row,
            priority
        ),
        axis=1
    )

    result = result.sort_values(
        by=[
            "hospital_score",
            "distance_km"
        ],
        ascending=[
            False,
            True
        ]
    ).reset_index(drop=True)

    result["rank"] = (
        result.index + 1
    )

    return result