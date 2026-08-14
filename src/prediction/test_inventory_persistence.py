from src.prediction.bed_reservation import (
    initialize_hospital_beds,
    reserve_bed,
    release_bed,
)

from src.prediction.reservation_store import (
    load_bed_inventory,
    save_bed_inventory,
    get_hospital_inventory,
    load_reservations,
    save_reservations,
)


# ============================================================
# TEST DATA
# ============================================================

HOSPITAL_ID = "GH_PERSISTENCE_TEST"
PATIENT_ID = "PAT_PERSISTENCE_TEST"


# ============================================================
# CLEAN TEST STATE
# ============================================================

def clean_test_state():
    """
    Remove old inventory and reservation data
    created by this test.
    """

    # ----------------------------------------
    # Remove old inventory
    # ----------------------------------------

    inventory_map = load_bed_inventory()

    inventory_map.pop(
        HOSPITAL_ID,
        None
    )

    save_bed_inventory(
        inventory_map
    )

    # ----------------------------------------
    # Remove old reservation
    # ----------------------------------------

    reservations = load_reservations()

    reservation_key = (
        HOSPITAL_ID
        + "_"
        + PATIENT_ID
    )

    reservations.pop(
        reservation_key,
        None
    )

    save_reservations(
        reservations
    )


# ============================================================
# INVENTORY PERSISTENCE TEST
# ============================================================

def test_inventory_persistence():
    """
    Test that:

    1. Hospital physical beds are initialized.
    2. ICU bed can be reserved.
    3. Inventory is persisted to disk.
    4. Reserved physical ICU bed is stored correctly.
    5. Bed can be released successfully.
    """

    # ========================================================
    # CLEAN TEST STATE
    # ========================================================

    clean_test_state()

    try:

        # ====================================================
        # INITIALIZE PHYSICAL BEDS
        # ====================================================

        inventory = initialize_hospital_beds(
            hospital_id=HOSPITAL_ID,
            available_beds=10,
            available_icu_beds=1,
        )

        # ----------------------------------------------------
        # Validate physical bed structure
        # ----------------------------------------------------

        assert "beds" in inventory

        # Expected ICU bed must exist
        assert "ICU-001" in inventory["beds"]

        assert (
            inventory["beds"]["ICU-001"]
            == "AVAILABLE"
        )

        # Expected general bed must exist
        assert "GENERAL-001" in inventory["beds"]

        assert (
            inventory["beds"]["GENERAL-001"]
            == "AVAILABLE"
        )

        # Validate initial counters
        assert inventory["available_beds"] == 10

        assert (
            inventory["available_icu_beds"]
            == 1
        )

        assert inventory["reserved_beds"] == 0

        assert (
            inventory["reserved_icu_beds"]
            == 0
        )


        # ====================================================
        # RESERVE ICU BED
        # ====================================================

        result = reserve_bed(
            hospital_id=HOSPITAL_ID,
            patient_id=PATIENT_ID,
            bed_type="ICU",
            inventory=inventory,
        )

        # Reservation must succeed
        assert result["success"] is True

        assert (
            result["status"]
            == "RESERVED"
        )

        reservation = result["reservation"]

        # Validate reservation
        assert (
            reservation["bed_type"]
            == "ICU"
        )

        assert (
            reservation["bed_id"]
            == "ICU-001"
        )

        assert (
            reservation["status"]
            == "RESERVED"
        )


        # ====================================================
        # CHECK MEMORY INVENTORY
        # ====================================================

        # One ICU bed was reserved
        assert (
            inventory["available_icu_beds"]
            == 0
        )

        assert (
            inventory["reserved_icu_beds"]
            == 1
        )

        # Physical bed status must change
        assert (
            inventory["beds"]["ICU-001"]
            == "RESERVED"
        )


        # ====================================================
        # LOAD INVENTORY FROM DISK
        # ====================================================

        persistent_inventory = get_hospital_inventory(
            HOSPITAL_ID
        )

        assert (
            persistent_inventory
            is not None
        )

        # Validate persisted counters
        assert (
            persistent_inventory[
                "available_icu_beds"
            ]
            == 0
        )

        assert (
            persistent_inventory[
                "reserved_icu_beds"
            ]
            == 1
        )

        # Physical beds must also persist
        assert (
            "beds"
            in persistent_inventory
        )

        assert (
            persistent_inventory[
                "beds"
            ]["ICU-001"]
            == "RESERVED"
        )


        # ====================================================
        # RELEASE BED
        # ====================================================

        release_result = release_bed(
            hospital_id=HOSPITAL_ID,
            patient_id=PATIENT_ID,
            inventory=inventory,
        )

        # Release must succeed
        assert (
            release_result["success"]
            is True
        )

        assert (
            release_result["status"]
            == "RELEASED"
        )


        # ====================================================
        # VERIFY RELEASED INVENTORY
        # ====================================================

        released_inventory = get_hospital_inventory(
            HOSPITAL_ID
        )

        assert (
            released_inventory
            is not None
        )

        # ICU capacity must be restored
        assert (
            released_inventory[
                "available_icu_beds"
            ]
            == 1
        )

        assert (
            released_inventory[
                "reserved_icu_beds"
            ]
            == 0
        )

        # Physical ICU bed must become available again
        assert (
            released_inventory[
                "beds"
            ]["ICU-001"]
            == "AVAILABLE"
        )


    finally:

        # ====================================================
        # CLEANUP TEST DATA
        # ====================================================

        clean_test_state()