import pandas as pd

from src.utils.referral_rules import (
    evaluate_hospital_capability
)


patients = pd.read_csv(
    "datasets/final/patients.csv"
)

hospitals = pd.read_csv(
    "datasets/final/hospitals.csv"
)


# --------------------------------
# Select patient
# --------------------------------

patient = patients.iloc[0].to_dict()


print("\n==============================")
print("PATIENT")
print("==============================")

print("Patient ID:", patient["patient_id"])
print("Disease:", patient["disease"])
print("Priority:", patient["priority"])
print("ICU Required:", patient["icu_required"])


# --------------------------------
# Test first 20 hospitals
# --------------------------------

for _, hospital_row in hospitals.head(20).iterrows():

    hospital = hospital_row.to_dict()

    result = evaluate_hospital_capability(
        patient,
        hospital
    )

    print("\n------------------------------")
    print(
        hospital["hospital_name"]
    )

    print(
        "Eligible:",
        result["eligible"]
    )

    print(
        "Hard Blocks:",
        result["hard_blocks"]
    )

    print(
        "Warnings:",
        result["warnings"]
    )

    print(
        "Unavailable Tests:",
        result["unavailable_tests"]
    )

    print(
        "Unavailable Specialties:",
        result["unavailable_specialties"]
    )