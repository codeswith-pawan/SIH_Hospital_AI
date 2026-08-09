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
# Patient
# --------------------------------

patient = patients[
    patients["patient_id"] == "PAT000002"
].iloc[0].to_dict()


print("\n==============================")
print("PATIENT")
print("==============================")

print("Patient ID:", patient["patient_id"])
print("Disease:", patient["disease"])
print("Priority:", patient["priority"])
print("ICU Required:", patient["icu_required"])


# --------------------------------
# Complete Referral Engine
# --------------------------------

result = find_eligible_hospitals(
    patient,
    hospitals
)


# --------------------------------
# No Hospital
# --------------------------------

if result.empty:

    print("\n==============================")
    print("NO ELIGIBLE HOSPITAL")
    print("==============================")

else:

    print("\n==============================")
    print("FINAL RECOMMENDATIONS")
    print("==============================")

    columns = [
        "rank",
        "hospital_name",
        "distance_km",
        "distance_zone",
        "recommendation_type",
        "available_beds",
        "available_icu_beds",
        "specialty_match",
        "test_match",
        "bed_match",
        "icu_match",
        "success_probability",
        "hospital_score",
        "rule_score_normalized",
        "ml_score",
        "final_score"
        
    ]

    print(
        result[
            columns
        ].head(10).to_string(
            index=False
        )
    )

    print(
        f"\nEligible hospitals: "
        f"{len(result)}"
    )