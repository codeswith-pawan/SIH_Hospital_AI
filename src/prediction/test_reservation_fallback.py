import pandas as pd

from src.prediction.referral_engine import (
    reserve_best_hospital
)

from src.prediction.reservation_store import (
    get_hospital_inventory,
    save_hospital_inventory,
)

from src.prediction.bed_reservation import (
    initialize_hospital_beds,
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


patient = patients[
    patients["patient_id"] == "PAT000002"
].iloc[0].to_dict()


print("\n==============================")
print("RESERVATION FALLBACK TEST")
print("==============================")


# ============================================================
# GET RANKED HOSPITALS
# ============================================================

from src.prediction.referral_engine import (
    find_eligible_hospitals
)

ranked = find_eligible_hospitals(
    patient,
    hospitals
)

print("\nTop Ranked Hospitals:")

print(
    ranked[
        [
            "rank",
            "hospital_id",
            "hospital_name",
            "available_icu_beds",
            "final_score"
        ]
    ].head(5).to_string(
        index=False
    )
)


if len(ranked) < 2:

    print(
        "\nFAIL — Less than 2 eligible hospitals."
    )

    raise SystemExit


# ============================================================
# FIRST HOSPITAL
# ============================================================

first = ranked.iloc[0]

first_id = first[
    "hospital_id"
]

first_name = first[
    "hospital_name"
]


print("\nFirst Ranked Hospital:")
print(first_name)
print(first_id)


# ============================================================
# FORCE FIRST HOSPITAL ICU = 0
# ============================================================

inventory = get_hospital_inventory(
    first_id
)

if inventory is None:

    inventory = initialize_hospital_beds(
        hospital_id=first_id,
        available_beds=int(
            first["available_beds"]
        ),
        available_icu_beds=int(
            first["available_icu_beds"]
        ),
    )


original_inventory = inventory.copy()


inventory[
    "available_icu_beds"
] = 0

inventory[
    "reserved_icu_beds"
] = 0


save_hospital_inventory(
    inventory
)


print("\nForced First Hospital ICU = 0")


# ============================================================
# RUN RESERVATION ENGINE
# ============================================================

print("\n==============================")
print("RUNNING RESERVATION ENGINE")
print("==============================")


result = reserve_best_hospital(
    patient,
    hospitals
)


print("\nResult:")
print(result)


# ============================================================
# VALIDATION
# ============================================================

print("\n==============================")
print("VALIDATION")
print("==============================")


if not result["success"]:

    print(
        "FAIL — Reservation engine "
        "could not find fallback."
    )

else:

    selected_id = result[
        "hospital"
    ][
        "hospital_id"
    ]

    if selected_id != first_id:

        print(
            "PASS — First hospital failed "
            "and fallback hospital was selected."
        )

    else:

        print(
            "FAIL — First unavailable "
            "hospital was selected."
        )


print("\nAttempts:")

for attempt in result[
    "attempts"
]:

    print(
        attempt
    )


# ============================================================
# CLEANUP
# ============================================================

print("\n==============================")
print("TEST CLEANUP")
print("==============================")


# Restore first hospital
save_hospital_inventory(
    original_inventory
)


# Release reservation created by test
if result["success"]:

    selected_hospital_id = result[
        "reservation"
    ][
        "hospital_id"
    ]

    release_inventory = (
        get_hospital_inventory(
            selected_hospital_id
        )
    )

    release_bed(
        hospital_id=selected_hospital_id,
        patient_id=patient["patient_id"],
        inventory=release_inventory,
    )


print(
    "Test cleanup completed."
)


print("\n==============================")
print("RESERVATION FALLBACK TEST COMPLETED")
print("==============================")