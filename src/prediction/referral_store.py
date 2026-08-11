import json
from pathlib import Path
from datetime import datetime

from src.prediction.bed_reservation import (
    release_bed,
)

from src.prediction.reservation_store import (
    get_hospital_inventory,
)


STORE_PATH = Path("data/runtime/referrals.json")


ACTIVE_STATUSES = [
    "PENDING",
    "ACCEPTED",
    "IN_TRANSIT",
    "ARRIVED",
    "TREATMENT_ACTIVE",
]


def _load_referrals():
    if not STORE_PATH.exists():
        return []

    try:
        with open(
            STORE_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):
        return []


def _save_referrals(referrals):
    STORE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        STORE_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            referrals,
            file,
            indent=2,
            ensure_ascii=False
        )


def _generate_referral_id(referrals):
    number = len(referrals) + 1

    return (
        f"REF-{datetime.now().year}-"
        f"{number:06d}"
    )


def create_referral(
    patient_id,
    from_hospital_id,
    to_hospital_id,
    reason,
    priority
):
    referrals = _load_referrals()

    # ----------------------------------------
    # Prevent duplicate active referral
    # ----------------------------------------

    for referral in referrals:

        if (
            referral["patient_id"] == patient_id
            and referral["status"] in ACTIVE_STATUSES
        ):
            return {
                "success": False,
                "status": "ACTIVE_REFERRAL_EXISTS",
                "message": (
                    "Patient already has "
                    "an active referral."
                ),
                "referral": referral,
            }

    now = datetime.now().isoformat()

    referral = {
        "referral_id":
            _generate_referral_id(
                referrals
            ),

        "patient_id":
            patient_id,

        "from_hospital_id":
            from_hospital_id,

        "to_hospital_id":
            to_hospital_id,

        "reason":
            reason,

        "priority":
            priority,

        "status":
            "PENDING",

        "created_at":
            now,

        "accepted_at":
            None,

        "rejected_at":
            None,

        "in_transit_at":
            None,

        "arrived_at":
            None,

        "treatment_started_at":
            None,

        "completed_at":
            None,

        "transferred_at":
            None,

        "died_at":
            None,

        "closed_at":
            None,
    }

    referrals.append(
        referral
    )

    _save_referrals(
        referrals
    )

    return {
        "success": True,
        "status": "PENDING",
        "message":
            "Referral created successfully.",
        "referral":
            referral,
    }


def get_referral(referral_id):

    referrals = _load_referrals()

    for referral in referrals:

        if (
            referral["referral_id"]
            == referral_id
        ):
            return referral

    return None


def get_patient_referrals(
    patient_id
):

    referrals = _load_referrals()

    return [
        referral
        for referral in referrals
        if referral["patient_id"]
        == patient_id
    ]


def update_referral_status(
    referral_id,
    new_status
):
    referrals = _load_referrals()

    referral = None

    for item in referrals:

        if (
            item["referral_id"]
            == referral_id
        ):
            referral = item
            break

    if referral is None:
        return {
            "success": False,
            "status": "NOT_FOUND",
            "message":
                "Referral not found.",
            "referral": None,
        }

    current_status = referral[
        "status"
    ]

    allowed_transitions = {
        "PENDING": [
            "ACCEPTED",
            "REJECTED",
        ],

        "ACCEPTED": [
            "IN_TRANSIT",
        ],

        "IN_TRANSIT": [
            "ARRIVED",
        ],

        "ARRIVED": [
            "TREATMENT_ACTIVE",
        ],

        "TREATMENT_ACTIVE": [
            "COMPLETED",
            "TRANSFERRED",
            "DIED",
        ],
    }

    allowed = allowed_transitions.get(
        current_status,
        []
    )

    if new_status not in allowed:

        return {
            "success": False,
            "status": "INVALID_TRANSITION",
            "message": (
                f"Cannot change referral "
                f"from {current_status} "
                f"to {new_status}."
            ),
            "referral": referral,
        }

    now = datetime.now().isoformat()

    referral["status"] = new_status

    if new_status == "ACCEPTED":
        referral["accepted_at"] = now

    elif new_status == "REJECTED":
        referral["rejected_at"] = now

    elif new_status == "IN_TRANSIT":
        referral["in_transit_at"] = now

    elif new_status == "ARRIVED":
        referral["arrived_at"] = now

    elif new_status == "TREATMENT_ACTIVE":
        referral[
            "treatment_started_at"
        ] = now

    elif new_status == "COMPLETED":
        referral["completed_at"] = now
        referral["closed_at"] = now

    elif new_status == "TRANSFERRED":
        referral["transferred_at"] = now
        referral["closed_at"] = now

    elif new_status == "DIED":
        referral["died_at"] = now
        referral["closed_at"] = now

        # ----------------------------------------
    # Release reserved bed when referral closes
    # ----------------------------------------

    if new_status in [
        "COMPLETED",
        "TRANSFERRED",
        "DIED",
    ]:

        reservation_hospital_id = referral.get(
            "reservation_hospital_id"
        )

        patient_id = referral.get(
            "patient_id"
        )

        if reservation_hospital_id:

            inventory = get_hospital_inventory(
                reservation_hospital_id
            )

            if inventory is not None:

                release_result = release_bed(
                    hospital_id=
                        reservation_hospital_id,

                    patient_id=
                        patient_id,

                    inventory=
                        inventory,
                )

                referral[
                    "reservation_release_status"
                ] = release_result.get(
                    "status"
                )

            else:

                referral[
                    "reservation_release_status"
                ] = "INVENTORY_NOT_FOUND"

        else:

            referral[
                "reservation_release_status"
            ] = "NO_RESERVATION_LINK"

    _save_referrals(
        referrals
    )

    return {
        "success": True,
        "status": new_status,
        "message":
            "Referral status updated.",
        "referral":
            referral,
    }

def attach_reservation(
    referral_id,
    hospital_id,
    bed_type
):
    referrals = _load_referrals()

    for referral in referrals:

        if referral["referral_id"] == referral_id:

            referral["reservation_hospital_id"] = (
                hospital_id
            )

            referral["bed_type"] = (
                bed_type
            )

            _save_referrals(
                referrals
            )

            return {
                "success": True,
                "status": "UPDATED",
                "referral": referral,
            }

    return {
        "success": False,
        "status": "NOT_FOUND",
        "message": "Referral not found.",
        "referral": None,
    }

