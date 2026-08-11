"""
Persistent Hospital Bed Reservation Engine
AI Powered Smart Hospital Referral System
"""
from datetime import datetime, timedelta
from threading import Lock

from src.prediction.reservation_store import (
    load_reservations,
    save_reservation,
    save_hospital_inventory,
    get_hospital_inventory,
)


# ============================================================
# Reservation Status
# ============================================================

AVAILABLE = "AVAILABLE"
RESERVED = "RESERVED"
CONFIRMED = "CONFIRMED"
OCCUPIED = "OCCUPIED"
RELEASED = "RELEASED"
EXPIRED = "EXPIRED"
RESERVATION_TIMEOUT_MINUTES = 15


# ============================================================
# Process Lock
# ============================================================

RESERVATION_LOCK = Lock()


# ============================================================
# Create Bed Inventory
# ============================================================

def initialize_hospital_beds(
    hospital_id,
    available_beds,
    available_icu_beds
):
    """
    Create or load persistent hospital bed inventory.
    """

    # Check existing persistent inventory
    existing = get_hospital_inventory(
        hospital_id
    )

    # If inventory already exists,
    # return the existing live inventory
    if existing is not None:

        return existing

    # Otherwise create new inventory
    inventory = {
        "hospital_id": hospital_id,

        "available_beds": int(
            available_beds
        ),

        "available_icu_beds": int(
            available_icu_beds
        ),

        "reserved_beds": 0,

        "reserved_icu_beds": 0
    }

    # Persist new inventory
    save_hospital_inventory(
        inventory
    )

    return inventory

# ============================================================
# Reserve Bed
# ============================================================

def reserve_bed(
    hospital_id,
    patient_id,
    bed_type,
    inventory
):
    """
    Reserve a GENERAL or ICU bed.

    Assigns a real physical bed number
    such as GENERAL-001 or ICU-004.
    """

    with RESERVATION_LOCK:

        # ----------------------------------------
        # Validate bed type
        # ----------------------------------------

        bed_type = bed_type.upper()

        if bed_type not in [
            "GENERAL",
            "ICU"
        ]:

            return {
                "success": False,
                "status": "INVALID_BED_TYPE",
                "message": (
                    "Invalid bed type."
                )
            }

        # ----------------------------------------
        # Load persistent reservations
        # ----------------------------------------

        reservations = load_reservations()

        reservation_key = (
            hospital_id
            + "_"
            + patient_id
        )

        existing = reservations.get(
            reservation_key
        )

        # ----------------------------------------
        # Prevent duplicate reservation
        # ----------------------------------------

        if existing is not None:

            if existing["status"] in [
                RESERVED,
                CONFIRMED,
                OCCUPIED
            ]:

                return {
                    "success": False,
                    "status": "ALREADY_RESERVED",
                    "message": (
                        "Patient already has "
                        "an active reservation."
                    ),
                    "reservation": existing
                }

        # ----------------------------------------
        # Physical bed registry
        # ----------------------------------------

        beds = inventory.get(
            "beds",
            {}
        )

        prefix = (
            "ICU-"
            if bed_type == "ICU"
            else "GENERAL-"
        )

        # ----------------------------------------
        # Find first available physical bed
        # ----------------------------------------

        assigned_bed_id = None

        for bed_id, bed_status in beds.items():

            if (
                bed_id.startswith(prefix)
                and bed_status == "AVAILABLE"
            ):

                assigned_bed_id = bed_id
                break

        # ----------------------------------------
        # Physical bed unavailable
        # ----------------------------------------

        if assigned_bed_id is None:

            return {
                "success": False,
                "status": (
                    "NO_ICU_AVAILABLE"
                    if bed_type == "ICU"
                    else "NO_BED_AVAILABLE"
                ),
                "message": (
                    "No physical "
                    + bed_type
                    + " bed available."
                )
            }

        # ----------------------------------------
        # Update physical bed
        # ----------------------------------------

        beds[
            assigned_bed_id
        ] = "RESERVED"

        inventory[
            "beds"
        ] = beds

        # ----------------------------------------
        # Update aggregate inventory
        # ----------------------------------------

        if bed_type == "ICU":

            if inventory[
                "available_icu_beds"
            ] <= 0:

                return {
                    "success": False,
                    "status": "NO_ICU_AVAILABLE",
                    "message": (
                        "No ICU bed available."
                    )
                }

            inventory[
                "available_icu_beds"
            ] -= 1

            inventory[
                "reserved_icu_beds"
            ] += 1

        else:

            if inventory[
                "available_beds"
            ] <= 0:

                return {
                    "success": False,
                    "status": "NO_BED_AVAILABLE",
                    "message": (
                        "No general bed available."
                    )
                }

            inventory[
                "available_beds"
            ] -= 1

            inventory[
                "reserved_beds"
            ] += 1

        # ----------------------------------------
        # Persist inventory
        # ----------------------------------------

        save_hospital_inventory(
            inventory
        )

        # ----------------------------------------
        # Create reservation
        # ----------------------------------------

        now = datetime.now().isoformat()

        reservation = {

            "hospital_id":
                hospital_id,

            "patient_id":
                patient_id,

            "bed_type":
                bed_type,

            "bed_id":
                assigned_bed_id,

            "status":
                RESERVED,

            "reserved_at":
                now
        }

        # ----------------------------------------
        # Persist reservation
        # ----------------------------------------

        save_reservation(
            reservation
        )

        return {
            "success": True,
            "status": RESERVED,
            "message": (
                f"{bed_type} bed "
                f"{assigned_bed_id} "
                "successfully reserved."
            ),
            "reservation": reservation
        }


# ============================================================
# Confirm Reservation
# ============================================================

def confirm_reservation(
    hospital_id,
    patient_id,
    inventory
):
    """
    RESERVED -> CONFIRMED
    """

    with RESERVATION_LOCK:

        reservations = load_reservations()

        key = (
            hospital_id
            + "_"
            + patient_id
        )

        reservation = reservations.get(
            key
        )

        if reservation is None:

            return {
                "success": False,
                "status": "NOT_FOUND"
            }

        if reservation["status"] != RESERVED:

            return {
                "success": False,
                "status": "INVALID_STATUS"
            }

        reservation[
            "status"
        ] = CONFIRMED

        reservation[
            "confirmed_at"
        ] = datetime.now().isoformat()

        save_reservation(
            reservation
        )

        return {
            "success": True,
            "status": CONFIRMED,
            "reservation": reservation
        }


# ============================================================
# Mark Occupied
# ============================================================

def mark_bed_occupied(
    hospital_id,
    patient_id
):
    """
    CONFIRMED -> OCCUPIED
    """

    with RESERVATION_LOCK:

        reservations = load_reservations()

        key = (
            hospital_id
            + "_"
            + patient_id
        )

        reservation = reservations.get(
            key
        )

        if reservation is None:

            return {
                "success": False,
                "status": "NOT_FOUND"
            }

        if reservation["status"] != CONFIRMED:

            return {
                "success": False,
                "status": "INVALID_STATUS"
            }

        reservation[
            "status"
        ] = OCCUPIED

        reservation[
            "occupied_at"
        ] = datetime.now().isoformat()

        save_reservation(
            reservation
        )

        return {
            "success": True,
            "status": OCCUPIED,
            "reservation": reservation
        }

def get_next_available_bed(
    inventory,
    bed_type
):
    """
    Return the first available physical bed ID.

    Example:
    ICU-001
    ICU-002
    GENERAL-001
    """

    bed_type = bed_type.upper()

    beds = inventory.get("beds", {})

    prefix = (
        "ICU"
        if bed_type == "ICU"
        else "GENERAL"
    )

    for bed_id, status in beds.items():

        if (
            bed_id.startswith(prefix + "-")
            and status == AVAILABLE
        ):
            return bed_id

    return None
# ============================================================
# Release Bed
# ============================================================

def release_bed(
    hospital_id,
    patient_id,
    inventory
):
    """
    Release an active reservation.
    """

    with RESERVATION_LOCK:

        reservations = load_reservations()

        key = (
            hospital_id
            + "_"
            + patient_id
        )

        reservation = reservations.get(
            key
        )

        if reservation is None:

            return {
                "success": False,
                "status": "NOT_FOUND"
            }

        if reservation["status"] == RELEASED:

            return {
                "success": False,
                "status": "ALREADY_RELEASED"
            }

        bed_type = reservation[
            "bed_type"
        ]

        # ----------------------------------------
        # Restore inventory
        # ----------------------------------------

        if bed_type == "ICU":

            inventory[
                "available_icu_beds"
            ] += 1

            if inventory[
                "reserved_icu_beds"
            ] > 0:

                inventory[
                    "reserved_icu_beds"
                ] -= 1

        else:

            inventory[
                "available_beds"
            ] += 1

            if inventory[
                "reserved_beds"
            ] > 0:

                inventory[
                    "reserved_beds"
                ] -= 1

        # ----------------------------------------
        # Update reservation
        # ----------------------------------------

        reservation[
            "status"
        ] = RELEASED

        reservation[
            "released_at"
        ] = datetime.now().isoformat()

        # ----------------------------------------
        # Persist updated inventory
        # ----------------------------------------

        save_hospital_inventory(
            inventory
        )

        save_reservation(
            reservation
        )

        return {
            "success": True,
            "status": RELEASED,
            "reservation": reservation
        }


# ============================================================
# Get Reservation
# ============================================================

def get_reservation(
    hospital_id,
    patient_id
):
    """
    Get persistent reservation.
    """

    reservations = load_reservations()

    key = (
        hospital_id
        + "_"
        + patient_id
    )

    return reservations.get(
        key
    )

# ============================================================
# Expire Reservation
# ============================================================

def expire_reservation(
    hospital_id,
    patient_id,
    inventory
):
    """
    Expire an unconfirmed reservation
    after the configured timeout.
    """

    with RESERVATION_LOCK:

        reservations = load_reservations()

        key = (
            hospital_id
            + "_"
            + patient_id
        )

        reservation = reservations.get(
            key
        )

        if reservation is None:

            return {
                "success": False,
                "status": "NOT_FOUND"
            }

        # ----------------------------------------
        # Only RESERVED can expire
        # ----------------------------------------

        if reservation["status"] != RESERVED:

            return {
                "success": False,
                "status": "NOT_EXPIRABLE",
                "message": (
                    "Only RESERVED reservations "
                    "can expire."
                )
            }

        # ----------------------------------------
        # Check timeout
        # ----------------------------------------

        reserved_at = datetime.fromisoformat(
            reservation["reserved_at"]
        )

        expiry_time = (
            reserved_at
            + timedelta(
                minutes=RESERVATION_TIMEOUT_MINUTES
            )
        )

        now = datetime.now()

        if now < expiry_time:

            return {
                "success": False,
                "status": "NOT_EXPIRED",
                "message": (
                    "Reservation timeout has "
                    "not been reached yet."
                ),
                "expires_at":
                    expiry_time.isoformat()
            }

        # ----------------------------------------
        # Return bed
        # ----------------------------------------

        bed_type = reservation[
            "bed_type"
        ]

        if bed_type == "ICU":

            inventory[
                "available_icu_beds"
            ] += 1

            if inventory[
                "reserved_icu_beds"
            ] > 0:

                inventory[
                    "reserved_icu_beds"
                ] -= 1

        else:

            inventory[
                "available_beds"
            ] += 1

            if inventory[
                "reserved_beds"
            ] > 0:

                inventory[
                    "reserved_beds"
                ] -= 1

        # ----------------------------------------
        # Update status
        # ----------------------------------------

        reservation[
            "status"
        ] = EXPIRED

        reservation[
            "expired_at"
        ] = datetime.now().isoformat()

        # ----------------------------------------
        # Persist updated inventory
        # ----------------------------------------

        save_hospital_inventory(
            inventory
        )


        save_reservation(
            reservation
        )

        return {
            "success": True,
            "status": EXPIRED,
            "reservation": reservation
        }


# ============================================================
# Automatic Expiry Cleanup
# ============================================================

def cleanup_expired_reservations(
    inventory_map
):
    """
    Automatically expire all RESERVED reservations
    whose timeout has passed.

    inventory_map format:

    {
        "HOSPITAL_ID": inventory_dict
    }
    """

    reservations = load_reservations()

    expired_count = 0
    skipped_count = 0

    # ----------------------------------------
    # Scan all reservations
    # ----------------------------------------

    for key, reservation in list(
        reservations.items()
    ):

        # Only RESERVED reservations
        if reservation["status"] != RESERVED:
            continue

        hospital_id = reservation[
            "hospital_id"
        ]

        patient_id = reservation[
            "patient_id"
        ]

        # ----------------------------------------
        # Hospital inventory required
        # ----------------------------------------

        inventory = inventory_map.get(
            hospital_id
        )

        if inventory is None:

            skipped_count += 1
            continue

        # ----------------------------------------
        # Check timeout
        # ----------------------------------------

        reserved_at = datetime.fromisoformat(
            reservation["reserved_at"]
        )

        expiry_time = (
            reserved_at
            + timedelta(
                minutes=RESERVATION_TIMEOUT_MINUTES
            )
        )

        if datetime.now() < expiry_time:

            continue

        # ----------------------------------------
        # Release bed
        # ----------------------------------------

        bed_type = reservation[
            "bed_type"
        ]

        if bed_type == "ICU":

            inventory[
                "available_icu_beds"
            ] += 1

            if inventory[
                "reserved_icu_beds"
            ] > 0:

                inventory[
                    "reserved_icu_beds"
                ] -= 1

        else:

            inventory[
                "available_beds"
            ] += 1

            if inventory[
                "reserved_beds"
            ] > 0:

                inventory[
                    "reserved_beds"
                ] -= 1

        # ----------------------------------------
        # Mark expired
        # ----------------------------------------

        reservation[
            "status"
        ] = EXPIRED

        reservation[
            "expired_at"
        ] = datetime.now().isoformat()

        # ----------------------------------------
        # Persist updated inventory
        # ----------------------------------------

        save_hospital_inventory(
            inventory
        )

        save_reservation(
            reservation
        )

        expired_count += 1

    return {
        "expired_count":
            expired_count,

        "skipped_count":
            skipped_count
    }