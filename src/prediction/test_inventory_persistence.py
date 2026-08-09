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


HOSPITAL_ID = "GH_PERSISTENCE_TEST"
PATIENT_ID = "PAT_PERSISTENCE_TEST"


print("\n==============================")
print("INVENTORY PERSISTENCE TEST")
print("==============================")


# ============================================================
# CLEAN TEST STATE
# ============================================================

# Remove old reservation for this test
reservations = {}

try:
    from src.prediction.reservation_store import load_reservations

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

except Exception:
    pass


# ============================================================
# CLEAN OLD TEST INVENTORY
# ============================================================

inventory_map = load_bed_inventory()

inventory_map.pop(
    HOSPITAL_ID,
    None
)

save_bed_inventory(
    inventory_map
)


# ============================================================
# CLEAN OLD TEST RESERVATION
# ============================================================

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
# INITIALIZE FRESH INVENTORY
# ============================================================

inventory = initialize_hospital_beds(
    hospital_id=HOSPITAL_ID,
    available_beds=10,
    available_icu_beds=1,
)

print("\nInitial Inventory:")
print(inventory)


print("\nInitial Inventory:")
print(inventory)


# ============================================================
# RESERVE ICU
# ============================================================

result = reserve_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_ID,
    bed_type="ICU",
    inventory=inventory,
)


print("\nReservation Result:")
print(result)


# ============================================================
# VALIDATE RESERVATION SUCCESS
# ============================================================

if not result["success"]:

    print("\nFAIL — ICU reservation failed.")
    print(
        "Status:",
        result["status"]
    )

    raise SystemExit(1)


print("\nInventory after reservation:")
print(inventory)


# ============================================================
# LOAD INVENTORY FROM DISK
# ============================================================

persistent_inventory = get_hospital_inventory(
    HOSPITAL_ID
)


print("\nInventory loaded from disk:")
print(persistent_inventory)


# ============================================================
# VALIDATION
# ============================================================

print("\n==============================")
print("VALIDATION")
print("==============================")


if (
    persistent_inventory is not None
    and persistent_inventory["available_icu_beds"] == 0
    and persistent_inventory["reserved_icu_beds"] == 1
):

    print(
        "PASS — Bed inventory was persisted correctly."
    )

else:

    print(
        "FAIL — Bed inventory persistence is incorrect."
    )

    raise SystemExit(1)


# ============================================================
# RELEASE
# ============================================================

print("\n==============================")
print("CLEANUP — RELEASE")
print("==============================")


release_result = release_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_ID,
    inventory=inventory,
)


print(release_result)


if release_result["success"]:

    print(
        "PASS — Test reservation released."
    )

else:

    print(
        "WARNING — Test reservation cleanup failed."
    )


# ============================================================
# FINAL INVENTORY
# ============================================================

final_inventory = get_hospital_inventory(
    HOSPITAL_ID
)


print("\nFinal Persistent Inventory:")
print(final_inventory)


print("\n==============================")
print("INVENTORY PERSISTENCE TEST COMPLETED")
print("==============================")