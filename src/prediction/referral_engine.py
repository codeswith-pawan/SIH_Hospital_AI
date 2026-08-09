"""
Hospital Referral Decision Engine
AI Powered Smart Hospital Referral System
"""

import pandas as pd
from src.prediction.bed_reservation import (
    initialize_hospital_beds,
    reserve_bed,
    cleanup_expired_reservations,
)

from src.prediction.reservation_store import (
    get_hospital_inventory,
)

from src.prediction.feature_builder import (
    build_referral_features
)

from src.prediction.predict import (
    predict_referral_success
)

from src.prediction.ranking_engine import (
    rank_hospitals
)

from src.utils.referral_rules import (
    evaluate_hospital_capability
)


def find_eligible_hospitals(
    patient,
    hospitals
):
    """
    Find eligible hospitals, calculate
    production features, run ML prediction,
    and rank hospitals using hybrid scoring.
    """

    # --------------------------------
    # Referral Decision
    # --------------------------------

    if patient["referral_required"] != "Yes":
        return pd.DataFrame()

    eligible_hospitals = []

    # --------------------------------
    # Evaluate Hospitals
    # --------------------------------

    for _, hospital_row in hospitals.iterrows():

        hospital = hospital_row.to_dict()

        # --------------------------------
        # Rule-based Eligibility
        # --------------------------------

        capability = evaluate_hospital_capability(
        patient,
        hospital)
    

        if not capability["eligible"]:
            continue

        # --------------------------------
        # Production Features
        # --------------------------------

        features = build_referral_features(
            patient,
            hospital
        )

        hospital_data = hospital.copy()

        hospital_data.update(
            features
        )

        # --------------------------------
        # ML Prediction
        # --------------------------------

        prediction = predict_referral_success(
            patient,
            hospital_data
        )

        hospital_data[
            "success_probability"
        ] = prediction[
            "success_probability"
        ]

        hospital_data[
            "ml_prediction"
        ] = prediction[
            "prediction"
        ]

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
    # Hybrid Ranking
    # --------------------------------

    result = rank_hospitals(
        result,
        patient["priority"]
    )

    return result

# ============================================================
# Reserve Best Hospital
# ============================================================

def reserve_best_hospital(
    patient,
    hospitals
):
    """
    Find ranked eligible hospitals and attempt
    bed reservation in ranked order.

    Uses persistent live inventory when available.
    Falls back to CSV inventory for hospitals
    that do not yet have persistent inventory.
    """

    # ----------------------------------------
    # Get ranked hospitals
    # ----------------------------------------

    ranked_hospitals = find_eligible_hospitals(
        patient,
        hospitals
    )

    if ranked_hospitals.empty:

        return {
            "success": False,
            "status": "NO_ELIGIBLE_HOSPITAL",
            "message":
                "No eligible hospital found.",
            "hospital": None,
            "reservation": None,
            "attempts": [],
        }

    # ----------------------------------------
    # Build live inventory map
    # ----------------------------------------

    inventory_map = {}

    for _, hospital in hospitals.iterrows():

        hospital_id = hospital[
            "hospital_id"
        ]

        # ----------------------------------------
        # Load persistent inventory
        # ----------------------------------------

        inventory = get_hospital_inventory(
            hospital_id
        )

        # ----------------------------------------
        # Initialize from CSV if missing
        # ----------------------------------------

        if inventory is None:

            inventory = (
                initialize_hospital_beds(
                    hospital_id=hospital_id,
                    available_beds=int(
                        hospital[
                            "available_beds"
                        ]
                    ),
                    available_icu_beds=int(
                        hospital[
                            "available_icu_beds"
                        ]
                    ),
                )
            )

        inventory_map[
            hospital_id
        ] = inventory

    # ----------------------------------------
    # Automatic expiry cleanup
    # ----------------------------------------

    cleanup_expired_reservations(
        inventory_map
    )

    # ----------------------------------------
    # Determine required bed
    # ----------------------------------------

    if patient["icu_required"] == "Yes":

        bed_type = "ICU"

    else:

        bed_type = "GENERAL"

    # ----------------------------------------
    # Try hospitals in ranking order
    # ----------------------------------------

    attempts = []

    for _, hospital in (
        ranked_hospitals.iterrows()
    ):

        hospital_id = hospital[
            "hospital_id"
        ]

        inventory = inventory_map.get(
            hospital_id
        )

        if inventory is None:

            continue

        # ----------------------------------------
        # Reserve bed
        # ----------------------------------------

        reservation_result = reserve_bed(
            hospital_id=hospital_id,
            patient_id=patient[
                "patient_id"
            ],
            bed_type=bed_type,
            inventory=inventory,
        )

        attempts.append({
            "hospital_id":
                hospital_id,

            "hospital_name":
                hospital[
                    "hospital_name"
                ],

            "status":
                reservation_result[
                    "status"
                ],

            "success":
                reservation_result[
                    "success"
                ],
        })

        # ----------------------------------------
        # Reservation successful
        # ----------------------------------------

        if reservation_result[
            "success"
        ]:

            return {
                "success": True,
                "status": "RESERVED",
                "message":
                    "Hospital selected and "
                    "bed reserved.",
                "hospital":
                    hospital.to_dict(),
                "reservation":
                    reservation_result[
                        "reservation"
                    ],
                "attempts":
                    attempts,
            }

    # ----------------------------------------
    # All hospitals failed
    # ----------------------------------------

    return {
        "success": False,
        "status": "RESERVATION_FAILED",
        "message":
            "No ranked hospital could reserve "
            "the required bed.",
        "hospital": None,
        "reservation": None,
        "attempts": attempts,
    }