from datetime import datetime, timedelta

from src.prediction.bed_reservation import (
    initialize_hospital_beds,
    reserve_bed,
    cleanup_expired_reservations,
)

from src.prediction.reservation_store import (
    save_reservation,
    clear_reservations,
)




hospital_id = "GH_AUTO_EXPIRY"
patient_id = "PAT_AUTO_EXPIRY"


# ============================================================
# SETUP
# ============================================================
clear_reservations()
inventory = initialize_hospital_beds(
    hospital_id=hospital_id,
    available_beds=10,
    available_icu_beds=1,
)

inventory_map = {
    hospital_id: inventory
}


print("\n==============================")
print("AUTOMATIC EXPIRY TEST")
print("==============================")


# ============================================================
# RESERVE ICU
# ============================================================

result = reserve_bed(
    hospital_id=hospital_id,
    patient_id=patient_id,
    bed_type="ICU",
    inventory=inventory,
)

print("\nReservation:")
print(result)

print("\nInventory after reservation:")
print(inventory)


# ============================================================
# FORCE OLD RESERVATION
# ============================================================

reservation = result["reservation"]

reservation["reserved_at"] = (
    datetime.now()
    - timedelta(minutes=20)
).isoformat()

save_reservation(reservation)

print(
    "\nReservation artificially aged "
    "by 20 minutes."
)


# ============================================================
# AUTOMATIC CLEANUP
# ============================================================

print("\n==============================")
print("RUNNING CLEANUP")
print("==============================")

cleanup_result = cleanup_expired_reservations(
    inventory_map
)

print(cleanup_result)

print("\nInventory after cleanup:")
print(inventory)


# ============================================================
# VALIDATION
# ============================================================

print("\n==============================")
print("VALIDATION")
print("==============================")

if cleanup_result["expired_count"] == 1:
    print(
        "PASS — Expired reservation "
        "was automatically detected."
    )
else:
    print(
        "FAIL — Expired reservation "
        "was not detected."
    )


if inventory["available_icu_beds"] == 1:
    print(
        "PASS — ICU bed automatically "
        "returned to availability."
    )
else:
    print(
        "FAIL — ICU bed was not restored."
    )


print("\n==============================")
print("AUTOMATIC EXPIRY TEST COMPLETED")
print("==============================")