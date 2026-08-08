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


# ----------------------------------------
# Select Patient
# ----------------------------------------

patient = patients[
    patients["referral_required"] == "Yes"
].iloc[0]


print("\nPATIENT")
print(
    patient[
        [
            "patient_id",
            "disease",
            "priority",
            "icu_required",
            "referral_required",
            "latitude",
            "longitude"
        ]
    ]
)


# ----------------------------------------
# Find Eligible Hospitals
# ----------------------------------------

eligible = find_eligible_hospitals(
    patient,
    hospitals
)


print("\nELIGIBLE HOSPITALS:")
print(
    len(eligible)
)


# ----------------------------------------
# Display Results
# ----------------------------------------

if not eligible.empty:

    print(
        eligible[
            [
                "rank",
                "hospital_id",
                "hospital_name",
                "state",
                "district",
                "distance_km",
                "available_beds",
                "available_icu_beds",
                "hospital_score"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

else:

    print("No eligible hospital found.")

