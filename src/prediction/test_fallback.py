import pandas as pd

from src.prediction.referral_engine import (
    find_eligible_hospitals
)


patients = pd.read_csv(
    "datasets/final/patients.csv"
)

hospitals = pd.read_csv(
    "datasets/final/hospitals.csv"
)


# --------------------------------
# Critical patient
# --------------------------------

patient = patients[
    patients["patient_id"] == "PAT000002"
].iloc[0].to_dict()


print("\n==============================")
print("FALLBACK TEST")
print("==============================")

print(
    "Patient:",
    patient["patient_id"]
)

print(
    "Disease:",
    patient["disease"]
)

print(
    "Priority:",
    patient["priority"]
)


# --------------------------------
# Normal recommendation
# --------------------------------

normal_result = find_eligible_hospitals(
    patient,
    hospitals
)


if normal_result.empty:

    print("\nNo eligible hospital found.")
    raise SystemExit


# --------------------------------
# Original recommendation
# --------------------------------

original = normal_result.iloc[0]

print("\n==============================")
print("ORIGINAL #1")
print("==============================")

print(
    "Hospital:",
    original["hospital_name"]
)

print(
    "Distance:",
    original["distance_km"],
    "km"
)

print(
    "ICU:",
    original["available_icu_beds"]
)


# --------------------------------
# Simulate ICU becoming unavailable
# --------------------------------

blocked_hospital_id = (
    original["hospital_id"]
)

hospitals_simulated = hospitals.copy()

hospitals_simulated.loc[
    hospitals_simulated[
        "hospital_id"
    ] == blocked_hospital_id,
    "available_icu_beds"
] = 0


print("\n==============================")
print("SIMULATING ICU UNAVAILABLE")
print("==============================")

print(
    "Blocked Hospital:",
    original["hospital_name"]
)

print(
    "Hospital ID:",
    blocked_hospital_id
)

print(
    "Available ICU changed to: 0"
)


# --------------------------------
# Run referral again
# --------------------------------

fallback_result = find_eligible_hospitals(
    patient,
    hospitals_simulated
)


if fallback_result.empty:

    print(
        "\nNo fallback hospital found."
    )

else:

    fallback = fallback_result.iloc[0]

    print("\n==============================")
    print("FALLBACK RESULT")
    print("==============================")

    print(
        "Hospital:",
        fallback["hospital_name"]
    )

    print(
        "Distance:",
        fallback["distance_km"],
        "km"
    )

    print(
        "ICU:",
        fallback["available_icu_beds"]
    )

    print(
        "Success Probability:",
        fallback["success_probability"]
    )

    print(
        "Rank:",
        fallback["rank"]
    )

    print(
        "\nFallback successful:",
        fallback["hospital_id"]
        != blocked_hospital_id
    )