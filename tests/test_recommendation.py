import pandas as pd

from src.prediction.referral_engine import (
    find_eligible_hospitals
)

from src.prediction.recommendation import (
    generate_top_recommendations
)


# ----------------------------------------
# Load datasets
# ----------------------------------------

patients = pd.read_csv(
    "datasets/final/patients.csv"
)

hospitals = pd.read_csv(
    "datasets/final/hospitals.csv"
)


# ----------------------------------------
# Select actual referral patient
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
            "referral_required"
        ]
    ]
)


# ----------------------------------------
# Find eligible hospitals
# ----------------------------------------

eligible = find_eligible_hospitals(
    patient,
    hospitals
)

print(
    "\nELIGIBLE HOSPITALS:",
    len(eligible)
)


# ----------------------------------------
# Generate Top Recommendations
# ----------------------------------------

recommendations = generate_top_recommendations(
    eligible,
    patient,
    top_n=5
)


# ----------------------------------------
# Display Recommendations
# ----------------------------------------

print("\nTOP RECOMMENDED HOSPITALS")


for recommendation in recommendations:

    print("\n--------------------------------")

    print(
        f"Rank: {recommendation['rank']}"
    )

    print(
        f"Hospital: "
        f"{recommendation['hospital_name']}"
    )

    print(
        f"Hospital ID: "
        f"{recommendation['hospital_id']}"
    )

    print(
        f"Distance: "
        f"{recommendation['distance_km']} km"
    )

    print(
        f"Score: "
        f"{recommendation['hospital_score']}"
    )

    print("Reasons:")

    for reason in recommendation["reasons"]:

        print(
            f"  ✓ {reason}"
        )