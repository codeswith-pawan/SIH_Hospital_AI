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
print("LIVE INVENTORY FALLBACK TEST")
print("==============================")


print("\nPatient:")
print(
    patient["patient_id"],
    patient["disease"],
    patient["priority"]
)


# ============================================================
# FIND FIRST HOSPITAL
# ============================================================

first_hospital = hospitals.iloc[0]

hospital_id = first_hospital[
    "hospital_id"
]

hospital_name = first_hospital[
    "hospital_name"
]


print("\nTarget Hospital:")
print(hospital_name)
print("Hospital ID:", hospital_id)


# ============================================================
# FORCE ICU UNAVAILABLE
# ============================================================

inventory = (
    get_hospital_inventory(
        hospital_id
    )
)

if inventory is None:

    inventory = (
        initialize_hospital_beds(
            hospital_id=hospital_id,
            available_beds=int(
                first_hospital[
                    "available_beds"
                ]
            ),
            available_icu_beds=int(
                first_hospital[
                    "available_icu_beds"
                ]
            ),
        )
    )

# Save original state
original_inventory = inventory.copy()


print("\nOriginal Live Inventory:")
print(inventory)


# Force ICU unavailable
inventory[
    "available_icu_beds"
] = 0

inventory[
    "reserved_icu_beds"
] = 0

save_hospital_inventory(
    inventory
)


print("\nSimulated ICU Failure:")
print(
    get_hospital_inventory(
        hospital_id
    )
)


# ============================================================
# RUN REFERRAL + RESERVATION
# ============================================================

print("\n==============================")
print("RUNNING REFERRAL ENGINE")
print("==============================")

result = reserve_best_hospital(
    patient,
    hospitals
)


print("\nFinal Result:")
print(result)


# ============================================================
# VALIDATION
# ============================================================

print("\n==============================")
print("VALIDATION")
print("==============================")


if result["success"]:

    selected_id = result[
        "hospital"
    ][
        "hospital_id"
    ]

    if selected_id != hospital_id:

        print(
            "PASS — Hospital with unavailable "
            "ICU was skipped."
        )

    else:

        print(
            "FAIL — Hospital with unavailable "
            "ICU was selected."
        )

else:

    print(
        "FAIL — Referral engine could not "
        "find a fallback hospital."
    )


# ============================================================
# RESTORE ORIGINAL INVENTORY
# ============================================================

save_hospital_inventory(
    original_inventory
)

print("\nOriginal inventory restored.")

print("\n==============================")
print("LIVE INVENTORY FALLBACK TEST COMPLETED")
print("==============================")