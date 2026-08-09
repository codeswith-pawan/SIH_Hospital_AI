from datetime import datetime, timedelta

from src.prediction.bed_reservation import (
    initialize_hospital_beds,
    reserve_bed,
    expire_reservation,
    release_bed,
    EXPIRED,
)

from src.prediction.reservation_store import (
    save_reservation,
)


# ============================================================
# TEST IDs
# ============================================================

HOSPITAL_ID = "GH_TEST_EXPIRY"
PATIENT_A = "PAT_TEST_EXPIRY_A"
PATIENT_B = "PAT_TEST_EXPIRY_B"


# ============================================================
# SETUP
# ============================================================

inventory = initialize_hospital_beds(
    hospital_id=HOSPITAL_ID,
    available_beds=10,
    available_icu_beds=1,
)


print("\n==============================")
print("RESERVATION EXPIRY TEST")
print("==============================")


# ============================================================
# PATIENT A RESERVATION
# ============================================================

print("\n==============================")
print("PATIENT A RESERVATION")
print("==============================")

result_a = reserve_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_A,
    bed_type="ICU",
    inventory=inventory,
)

print(result_a)

print("\nInventory:")
print(inventory)


# ============================================================
# FORCE TIMEOUT
# ============================================================

reservation = result_a["reservation"]

reservation["reserved_at"] = (
    datetime.now()
    - timedelta(minutes=20)
).isoformat()

save_reservation(reservation)

print(
    "\nReservation time moved "
    "20 minutes into the past."
)


# ============================================================
# EXPIRE RESERVATION
# ============================================================

print("\n==============================")
print("EXPIRING RESERVATION")
print("==============================")

expiry_result = expire_reservation(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_A,
    inventory=inventory,
)

print(expiry_result)

print("\nInventory after expiry:")
print(inventory)


# ============================================================
# VALIDATION
# ============================================================

print("\n==============================")
print("VALIDATION")
print("==============================")


if (
    expiry_result["success"]
    and expiry_result["status"] == EXPIRED
):

    print(
        "PASS — Reservation expired successfully."
    )

else:

    print(
        "FAIL — Reservation did not expire."
    )


if inventory["available_icu_beds"] == 1:

    print(
        "PASS — ICU bed returned to availability."
    )

else:

    print(
        "FAIL — ICU bed was not released."
    )


# ============================================================
# PATIENT B RETRY
# ============================================================

print("\n==============================")
print("PATIENT B RETRY")
print("==============================")

result_b = reserve_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_B,
    bed_type="ICU",
    inventory=inventory,
)

print(result_b)


if result_b["success"]:

    print(
        "PASS — Patient B successfully "
        "reserved the released ICU bed."
    )

else:

    print(
        "FAIL — Patient B could not reserve "
        "the released ICU bed."
    )


# ============================================================
# TEST CLEANUP
# ============================================================

if result_b["success"]:

    cleanup_result = release_bed(
        hospital_id=HOSPITAL_ID,
        patient_id=PATIENT_B,
        inventory=inventory,
    )

    print("\nTest Cleanup:")
    print(cleanup_result)


# ============================================================
# FINAL
# ============================================================

print("\n==============================")
print("ALL EXPIRY TESTS COMPLETED")
print("==============================")