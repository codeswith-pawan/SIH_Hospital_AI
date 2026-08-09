"""
Priority-Aware Hybrid Hospital Ranking Engine
AI Powered Smart Hospital Referral System
"""

import pandas as pd


def get_distance_zone(distance_km):
    """
    Classify hospital by distance.

    LOCAL:
        0 - 50 km

    REGIONAL:
        >50 - 200 km

    EXTENDED:
        >200 km
    """

    if distance_km <= 50:
        return "LOCAL"

    elif distance_km <= 200:
        return "REGIONAL"

    return "EXTENDED"


def calculate_hospital_score(
    hospital,
    priority
):
    """
    Calculate clinical/resource suitability score.

    Maximum score = 100.
    """

    score = 0.0

    # ==================================================
    # CRITICAL
    # ==================================================

    if priority == "Critical":

        # ICU — 30
        icu_beds = hospital["available_icu_beds"]

        if icu_beds >= 30:
            score += 30
        elif icu_beds >= 20:
            score += 27
        elif icu_beds >= 10:
            score += 24
        elif icu_beds > 0:
            score += 18

        # Distance — 25
        distance = hospital["distance_km"]

        if distance <= 5:
            score += 25
        elif distance <= 10:
            score += 23
        elif distance <= 25:
            score += 20
        elif distance <= 50:
            score += 15
        elif distance <= 100:
            score += 8
        elif distance <= 200:
            score += 3

        # Emergency — 15
        if hospital["emergency_24x7"] == "Yes":
            score += 15

        # Ambulance — 10
        if hospital["ambulance"] == "Yes":
            score += 10

        # Oxygen — 5
        if hospital["oxygen_support"] == "Yes":
            score += 5

        # Ventilator — 5
        if hospital["ventilator"] == "Yes":
            score += 5

        # Blood Bank — 5
        if hospital["blood_bank"] == "Yes":
            score += 5

        # Specialty/Test match — 5
        if hospital["specialty_match"] == 1:
            score += 2.5

        if hospital["test_match"] == 1:
            score += 2.5

    # ==================================================
    # URGENT
    # ==================================================

    elif priority == "Urgent":

        # Distance — 30
        distance = hospital["distance_km"]

        if distance <= 5:
            score += 30
        elif distance <= 10:
            score += 28
        elif distance <= 25:
            score += 24
        elif distance <= 50:
            score += 18
        elif distance <= 100:
            score += 10
        elif distance <= 200:
            score += 4

        # Beds — 25
        beds = hospital["available_beds"]

        if beds >= 300:
            score += 25
        elif beds >= 200:
            score += 22
        elif beds >= 100:
            score += 18
        elif beds >= 50:
            score += 12
        elif beds > 0:
            score += 6

        # ICU — 15
        icu_beds = hospital["available_icu_beds"]

        if icu_beds >= 30:
            score += 15
        elif icu_beds >= 20:
            score += 13
        elif icu_beds >= 10:
            score += 11
        elif icu_beds > 0:
            score += 7

        # Emergency — 10
        if hospital["emergency_24x7"] == "Yes":
            score += 10

        # Ambulance — 5
        if hospital["ambulance"] == "Yes":
            score += 5

        # Oxygen — 5
        if hospital["oxygen_support"] == "Yes":
            score += 5

        # Ventilator — 3
        if hospital["ventilator"] == "Yes":
            score += 3

        # Blood bank — 2
        if hospital["blood_bank"] == "Yes":
            score += 2

        # Specialty/Test
        if hospital["specialty_match"] == 1:
            score += 1.5

        if hospital["test_match"] == 1:
            score += 1.5

    # ==================================================
    # STABLE
    # ==================================================

    else:

        # Distance — 35
        distance = hospital["distance_km"]

        if distance <= 5:
            score += 35
        elif distance <= 10:
            score += 33
        elif distance <= 25:
            score += 28
        elif distance <= 50:
            score += 22
        elif distance <= 100:
            score += 14
        elif distance <= 200:
            score += 6

        # Beds — 30
        beds = hospital["available_beds"]

        if beds >= 300:
            score += 30
        elif beds >= 200:
            score += 27
        elif beds >= 100:
            score += 23
        elif beds >= 50:
            score += 16
        elif beds > 0:
            score += 8

        # ICU — 10
        icu_beds = hospital["available_icu_beds"]

        if icu_beds >= 30:
            score += 10
        elif icu_beds >= 20:
            score += 9
        elif icu_beds >= 10:
            score += 7
        elif icu_beds > 0:
            score += 4

        # Emergency — 10
        if hospital["emergency_24x7"] == "Yes":
            score += 10

        # Ambulance — 5
        if hospital["ambulance"] == "Yes":
            score += 5

        # Oxygen — 5
        if hospital["oxygen_support"] == "Yes":
            score += 5

        # Ventilator — 3
        if hospital["ventilator"] == "Yes":
            score += 3

        # Blood bank — 2
        if hospital["blood_bank"] == "Yes":
            score += 2

        # Specialty/Test
        if hospital["specialty_match"] == 1:
            score += 1

        if hospital["test_match"] == 1:
            score += 1

    return round(min(score, 100), 2)


def rank_hospitals(
    hospitals,
    priority
):
    """
    Rank eligible hospitals using:

    1. Distance zone
    2. Clinical/resource score
    3. ML probability

    Extended hospitals are used only as fallback
    when no Local/Regional hospitals exist.
    """

    if hospitals.empty:
        return hospitals

    result = hospitals.copy()

    # ----------------------------------------------
    # Distance Zone
    # ----------------------------------------------

    result["distance_zone"] = result[
        "distance_km"
    ].apply(get_distance_zone)

    # ----------------------------------------------
    # Clinical / Resource Score
    # ----------------------------------------------

    result["hospital_score"] = result.apply(
        lambda row: calculate_hospital_score(
            row,
            priority
        ),
        axis=1
    )

    # ----------------------------------------------
    # Normalize
    # ----------------------------------------------

    result["rule_score_normalized"] = (
        result["hospital_score"] / 100.0
    )

    # ----------------------------------------------
    # ML Score
    # ----------------------------------------------

    result["ml_score"] = (
        result["success_probability"]
        .clip(0, 1)
    )

    # ----------------------------------------------
    # Priority weights
    # ----------------------------------------------

    if priority == "Critical":

        rule_weight = 0.85
        ml_weight = 0.15

    elif priority == "Urgent":

        rule_weight = 0.75
        ml_weight = 0.25

    else:

        rule_weight = 0.65
        ml_weight = 0.35

    # ----------------------------------------------
    # Hybrid score
    # ----------------------------------------------

    result["final_score"] = (
        result["rule_score_normalized"]
        * rule_weight
        +
        result["ml_score"]
        * ml_weight
    )

    result["final_score"] = (
        result["final_score"] * 100
    ).round(2)

    # ----------------------------------------------
    # Determine available zone
    # ----------------------------------------------

    local = result[
        result["distance_zone"] == "LOCAL"
    ]

    regional = result[
        result["distance_zone"] == "REGIONAL"
    ]

    # ----------------------------------------------
    # Recommendation pool
    # ----------------------------------------------

    if not local.empty:

        result = local.copy()

        result["recommendation_type"] = (
            "Primary Recommendation"
        )

    elif not regional.empty:

        result = regional.copy()

        result["recommendation_type"] = (
            "Regional Fallback"
        )

    else:

        result = result[
            result["distance_zone"] == "EXTENDED"
        ].copy()

        result["recommendation_type"] = (
            "Extended Fallback"
        )

    # ----------------------------------------------
    # Sort
    # ----------------------------------------------

    result = result.sort_values(
        by=[
            "final_score",
            "hospital_score",
            "distance_km",
            "available_icu_beds",
            "available_beds"
        ],
        ascending=[
            False,
            False,
            True,
            False,
            False
        ]
    ).reset_index(drop=True)

    # ----------------------------------------------
    # Rank
    # ----------------------------------------------

    result["rank"] = (
        result.index + 1
    )

    return result