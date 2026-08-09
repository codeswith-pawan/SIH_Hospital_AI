import pandas as pd

from src.prediction.referral_engine import (
    find_eligible_hospitals,
    reserve_best_hospital,
)

from src.prediction.reservation_store import (
    get_hospital_inventory,
)

from src.prediction.bed_reservation import (
    release_bed,
)


# ============================================================
# LOAD DATA
# ============================================================

patients = pd.read_csv(
    "datasets/final/patients.csv"
)

hospitals = pd.read_csv(
    "datasets/final/hospitals.csv"
)


# ============================================================
# PATIENT
# ============================================================

patient = patients[
    patients["patient_id"] == "PAT000002"
].iloc[0].to_dict()


print("\n==============================")
print("END-TO-END REFERRAL TEST")
print("==============================")


print("\nPatient:")
print(
    patient["patient_id"],
    patient["disease"],
    patient["priority"]
)


# ============================================================
# STEP 1 — FIND ELIGIBLE HOSPITALS
# ============================================================

print("\n==============================")
print("STEP 1 — HOSPITAL RANKING")
print("==============================")


ranked = find_eligible_hospitals(
    patient,
    hospitals
)


if ranked.empty:

    print(
        "FAIL — No eligible hospital found."
    )

    raise SystemExit


print(
    ranked[
        [
            "rank",
            "hospital_id",
            "hospital_name",
            "distance_km",
            "success_probability",
            "final_score",
        ]
    ].head(5).to_string(
        index=False
    )
)


print(
    "\nPASS — Hospital ranking completed."
)


# ============================================================
# STEP 2 — RESERVE BEST AVAILABLE HOSPITAL
# ============================================================

print("\n==============================")
print("STEP 2 — BED RESERVATION")
print("==============================")


result = reserve_best_hospital(
    patient,
    hospitals
)


print("\nReservation Result:")
print(result)


if not result["success"]:

    print(
        "\nFAIL — Could not reserve "
        "a hospital bed."
    )

    raise SystemExit


print(
    "\nPASS — Hospital and bed successfully selected."
)


# ============================================================
# STEP 3 — VERIFY RESERVATION
# ============================================================

print("\n==============================")
print("STEP 3 — RESERVATION VALIDATION")
print("==============================")


reservation = result[
    "reservation"
]

hospital_id = reservation[
    "hospital_id"
]

patient_id = reservation[
    "patient_id"
]


if (
    reservation["status"] == "RESERVED"
    and reservation["bed_type"] == "ICU"
):

    print(
        "PASS — ICU reservation created."
    )

else:

    print(
        "FAIL — Reservation details incorrect."
    )


# ============================================================
# STEP 4 — VERIFY PERSISTENT INVENTORY
# ============================================================

print("\n==============================")
print("STEP 4 — INVENTORY VALIDATION")
print("==============================")


inventory = get_hospital_inventory(
    hospital_id
)


print(
    "\nPersistent Inventory:"
)

print(
    inventory
)


if inventory is None:

    print(
        "FAIL — Inventory not found."
    )

else:

    if (
        inventory["reserved_icu_beds"]
        >= 1
    ):

        print(
            "PASS — ICU reservation "
            "persisted in inventory."
        )

    else:

        print(
            "FAIL — ICU reservation "
            "not persisted."
        )


# ============================================================
# STEP 5 — RELEASE
# ============================================================

print("\n==============================")
print("STEP 5 — RELEASE")
print("==============================")


release_result = release_bed(
    hospital_id=hospital_id,
    patient_id=patient_id,
    inventory=inventory,
)


print(
    release_result
)


if release_result[
    "success"
]:

    print(
        "PASS — Reservation released."
    )

else:

    print(
        "FAIL — Reservation release failed."
    )


# ============================================================
# STEP 6 — VERIFY RESTORED INVENTORY
# ============================================================

print("\n==============================")
print("STEP 6 — FINAL INVENTORY")
print("==============================")


final_inventory = (
    get_hospital_inventory(
        hospital_id
    )
)


print(
    final_inventory
)


if (
    final_inventory[
        "available_icu_beds"
    ]
    >= inventory[
        "available_icu_beds"
    ]
):

    print(
        "PASS — ICU bed returned "
        "to inventory."
    )

else:

    print(
        "FAIL — ICU bed was not restored."
    )


print("\n==============================")
print("END-TO-END REFERRAL TEST COMPLETED")
print("==============================")