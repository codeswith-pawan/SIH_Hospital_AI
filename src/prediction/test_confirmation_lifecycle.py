from src.prediction.bed_reservation import (
    initialize_hospital_beds,
    reserve_bed,
    confirm_reservation,
    release_bed,
)

from src.prediction.reservation_store import (
    get_hospital_inventory,
)


HOSPITAL_ID = "GH_CONFIRM_TEST"

PATIENT_ID = "PAT_CONFIRM_TEST"


print("\n==============================")
print("CONFIRMATION LIFECYCLE TEST")
print("==============================")


# ============================================================
# INITIAL INVENTORY
# ============================================================

inventory = initialize_hospital_beds(
    hospital_id=HOSPITAL_ID,
    available_beds=10,
    available_icu_beds=1,
)


print("\nInitial Inventory:")
print(inventory)


# ============================================================
# STEP 1 — RESERVE
# ============================================================

print("\n==============================")
print("STEP 1 — RESERVE")
print("==============================")


reserve_result = reserve_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_ID,
    bed_type="ICU",
    inventory=inventory,
)


print(reserve_result)

if (
    reserve_result["success"]
    and reserve_result["status"] == "RESERVED"
):

    print(
        "PASS — ICU bed reserved."
    )

else:

    print(
        "FAIL — ICU reservation failed."
    )

print("\nInventory:")
print(inventory)


# ============================================================
# STEP 2 — CONFIRM
# ============================================================

print("\n==============================")
print("STEP 2 — CONFIRM")
print("==============================")


confirm_result = confirm_reservation(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_ID,
    inventory=inventory,
)


print(confirm_result)


if (
    confirm_result["success"]
    and confirm_result["status"] == "CONFIRMED"
):

    print(
        "PASS — Reservation confirmed."
    )

else:

    print(
        "FAIL — Reservation confirmation failed."
    )


print("\nInventory after confirmation:")
print(inventory)


# ============================================================
# STEP 3 — CONFIRM AGAIN
# ============================================================

print("\n==============================")
print("STEP 3 — DUPLICATE CONFIRM")
print("==============================")


second_confirm = confirm_reservation(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_ID,
    inventory=inventory,
)


print(second_confirm)


if not second_confirm["success"]:

    print(
        "PASS — Duplicate confirmation blocked."
    )

else:

    print(
        "FAIL — Duplicate confirmation allowed."
    )


# ============================================================
# STEP 4 — RELEASE
# ============================================================

print("\n==============================")
print("STEP 4 — RELEASE")
print("==============================")


release_result = release_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_ID,
    inventory=inventory,
)


print(release_result)


if (
    release_result["success"]
    and release_result["status"] == "RELEASED"
):

    print(
        "PASS — Confirmed reservation released."
    )

else:

    print(
        "FAIL — Release failed."
    )


print("\nInventory after release:")
print(inventory)


# ============================================================
# STEP 5 — VERIFY INVENTORY
# ============================================================

print("\n==============================")
print("STEP 5 — INVENTORY VALIDATION")
print("==============================")


if (
    inventory["available_icu_beds"] == 1
    and inventory["reserved_icu_beds"] == 0
):

    print(
        "PASS — ICU inventory fully restored."
    )

else:

    print(
        "FAIL — ICU inventory is incorrect."
    )


# ============================================================
# STEP 6 — RELEASE AGAIN
# ============================================================

print("\n==============================")
print("STEP 6 — DUPLICATE RELEASE")
print("==============================")


second_release = release_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_ID,
    inventory=inventory,
)


print(second_release)


if not second_release["success"]:

    print(
        "PASS — Duplicate release blocked."
    )

else:

    print(
        "FAIL — Duplicate release allowed."
    )


# ============================================================
# FINAL
# ============================================================

print("\n==============================")
print("CONFIRMATION LIFECYCLE TEST COMPLETED")
print("==============================")