import pandas as pd

from src.prediction.referral_engine import (
    find_eligible_hospitals,
    reserve_best_hospital,
)

from src.prediction.reservation_store import (
    load_bed_inventory,
    save_bed_inventory,
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


patient = patients[
    patients["patient_id"] == "PAT000002"
].iloc[0].to_dict()


print("\n==============================")
print("TRUE ICU CAPACITY FALLBACK TEST")
print("==============================")


# ============================================================
# FIND RANKED HOSPITALS
# ============================================================

ranked = find_eligible_hospitals(
    patient,
    hospitals
)


if len(ranked) < 2:

    print(
        "FAIL — Need at least 2 eligible hospitals."
    )

    raise SystemExit


print("\nRanked Hospitals:")

print(
    ranked[
        [
            "rank",
            "hospital_id",
            "hospital_name",
            "available_icu_beds",
            "final_score",
        ]
    ].head(5).to_string(
        index=False
    )
)


# ============================================================
# SELECT TOP 2
# ============================================================

first = ranked.iloc[0]
second = ranked.iloc[1]

first_id = first["hospital_id"]
second_id = second["hospital_id"]


print("\n==============================")
print("TARGET HOSPITALS")
print("==============================")

print(
    "Rank 1:",
    first["hospital_name"],
    first_id
)

print(
    "Rank 2:",
    second["hospital_name"],
    second_id
)


# ============================================================
# SAVE ORIGINAL INVENTORY
# ============================================================

inventory_map = load_bed_inventory()

original_first = inventory_map.get(
    first_id
)

original_second = inventory_map.get(
    second_id
)


if original_first is None:

    print(
        "FAIL — Rank 1 inventory not found."
    )

    raise SystemExit


if original_second is None:

    print(
        "FAIL — Rank 2 inventory not found."
    )

    raise SystemExit


original_first = original_first.copy()
original_second = original_second.copy()


# ============================================================
# FORCE RANK 1 ICU TO ZERO
# ============================================================

forced_first = original_first.copy()

forced_first[
    "available_icu_beds"
] = 0

forced_first[
    "reserved_icu_beds"
] = 0


inventory_map[
    first_id
] = forced_first


save_bed_inventory(
    inventory_map
)


print("\n==============================")
print("SIMULATED ICU FAILURE")
print("==============================")

print(
    first["hospital_name"]
)

print(
    "Available ICU:",
    0
)


# ============================================================
# RUN REFERRAL + RESERVATION
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
        "FAIL — No hospital could reserve ICU."
    )

else:

    selected_id = result[
        "hospital"
    ][
        "hospital_id"
    ]

    if selected_id == first_id:

        print(
            "FAIL — Rank 1 hospital with "
            "zero ICU was selected."
        )

    elif selected_id == second_id:

        print(
            "PASS — Rank 1 hospital was skipped "
            "because ICU capacity was zero."
        )

        print(
            "PASS — Rank 2 hospital successfully "
            "received the reservation."
        )

    else:

        print(
            "PASS — Fallback hospital selected:",
            selected_id
        )


# ============================================================
# SHOW ATTEMPTS
# ============================================================

print("\n==============================")
print("RESERVATION ATTEMPTS")
print("==============================")


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


# Restore Rank 1 inventory
inventory_map[
    first_id
] = original_first


# Restore Rank 2 inventory
inventory_map[
    second_id
] = original_second


save_bed_inventory(
    inventory_map
)


# Release reservation created by test
if result["success"]:

    selected_id = result[
        "reservation"
    ][
        "hospital_id"
    ]

    selected_inventory = (
        load_bed_inventory()
    ).get(
        selected_id
    )

    if selected_inventory:

        release_bed(
            hospital_id=selected_id,
            patient_id=patient[
                "patient_id"
            ],
            inventory=selected_inventory,
        )


print(
    "Original inventory restored."
)


print("\n==============================")
print("TRUE ICU CAPACITY FALLBACK TEST COMPLETED")
print("==============================")