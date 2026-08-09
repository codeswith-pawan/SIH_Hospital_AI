from src.prediction.bed_reservation import (
    initialize_hospital_beds,
    reserve_bed,
    confirm_reservation,
    release_bed,
)

print("\n==============================")
print("BED RESERVATION TEST")
print("==============================")


# ------------------------------------------------------------
# Test IDs
# ------------------------------------------------------------

HOSPITAL_ID = "GH_TEST_BED"
PATIENT_A = "PAT_TEST_A"
PATIENT_B = "PAT_TEST_B"


# ------------------------------------------------------------
# Hospital has only ONE ICU bed
# ------------------------------------------------------------

inventory = initialize_hospital_beds(
    hospital_id=HOSPITAL_ID,
    available_beds=10,
    available_icu_beds=1,
)

print("\nInitial Inventory:")
print(inventory)


# ------------------------------------------------------------
# PATIENT A
# ------------------------------------------------------------

print("\n==============================")
print("PATIENT A")
print("==============================")

result_a = reserve_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_A,
    bed_type="ICU",
    inventory=inventory,
)

print(result_a)

print("\nInventory after Patient A:")
print(inventory)


# ------------------------------------------------------------
# PATIENT B
# ------------------------------------------------------------

print("\n==============================")
print("PATIENT B")
print("==============================")

result_b = reserve_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_B,
    bed_type="ICU",
    inventory=inventory,
)

print(result_b)

print("\nInventory after Patient B:")
print(inventory)


# ------------------------------------------------------------
# DOUBLE BOOKING VALIDATION
# ------------------------------------------------------------

print("\n==============================")
print("DOUBLE BOOKING VALIDATION")
print("==============================")

if result_a["success"]:

    print(
        "PASS — Patient A successfully reserved the ICU bed."
    )

else:

    print(
        "FAIL — Patient A could not reserve the ICU bed."
    )


if (
    not result_b["success"]
    and result_b["status"] == "NO_ICU_AVAILABLE"
):

    print(
        "PASS — Patient B was blocked because "
        "the ICU bed was already reserved."
    )

else:

    print(
        "FAIL — Double booking protection failed."
    )


# ------------------------------------------------------------
# CONFIRM PATIENT A
# ------------------------------------------------------------

print("\n==============================")
print("CONFIRM PATIENT A")
print("==============================")

confirm_result = confirm_reservation(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_A,
    inventory=inventory,
)

print(confirm_result)


# ------------------------------------------------------------
# RELEASE ICU BED
# ------------------------------------------------------------

print("\n==============================")
print("RELEASE ICU BED")
print("==============================")

release_result = release_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_A,
    inventory=inventory,
)

print(release_result)

print("\nFinal Inventory:")
print(inventory)


# ------------------------------------------------------------
# RE-BOOK AFTER RELEASE
# ------------------------------------------------------------

print("\n==============================")
print("PATIENT B RETRY")
print("==============================")

result_b_retry = reserve_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_B,
    bed_type="ICU",
    inventory=inventory,
)

print(result_b_retry)


if result_b_retry["success"]:

    print(
        "PASS — ICU bed became available after release "
        "and Patient B successfully reserved it."
    )

else:

    print(
        "FAIL — Released ICU bed could not be reserved."
    )


# ------------------------------------------------------------
# CLEANUP PATIENT B
# ------------------------------------------------------------

if result_b_retry["success"]:

    cleanup_result = release_bed(
        hospital_id=HOSPITAL_ID,
        patient_id=PATIENT_B,
        inventory=inventory,
    )

    print("\nTest Cleanup:")
    print(cleanup_result)


print("\n==============================")
print("ALL BED RESERVATION TESTS COMPLETED")
print("==============================")