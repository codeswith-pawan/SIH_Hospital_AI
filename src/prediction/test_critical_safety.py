import pandas as pd

from src.prediction.referral_engine import (
    find_eligible_hospitals
)

from src.utils.helpers import (
    calculate_distance_km
)


patients = pd.read_csv(
    "datasets/final/patients.csv"
)

hospitals = pd.read_csv(
    "datasets/final/hospitals.csv"
)

# --------------------------------------------------
# Critical Heart Attack patient
# --------------------------------------------------

patient = patients[
    patients["patient_id"] == "PAT000002"
].iloc[0].to_dict()


# --------------------------------------------------
# Find normal eligible hospitals
# --------------------------------------------------

result = find_eligible_hospitals(
    patient,
    hospitals.copy()
)

print("\n" + "=" * 70)
print("CRITICAL SAFETY TEST")
print("=" * 70)

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


# --------------------------------------------------
# Find nearest hospital
# --------------------------------------------------

hospitals_test = hospitals.copy()

hospitals_test["test_distance"] = (
    hospitals_test.apply(
        lambda row: calculate_distance_km(
            patient["latitude"],
            patient["longitude"],
            row["latitude"],
            row["longitude"]
        ),
        axis=1
    )
)

nearest = hospitals_test.sort_values(
    "test_distance"
).iloc[0]


print("\n" + "-" * 70)
print("NEAREST HOSPITAL")
print("-" * 70)

print(
    "Hospital:",
    nearest["hospital_name"]
)

print(
    "Distance:",
    nearest["test_distance"],
    "km"
)

print(
    "ICU:",
    nearest["available_icu_beds"]
)


# --------------------------------------------------
# Find a capable regional hospital
# --------------------------------------------------

regional_capable = None

for _, row in hospitals_test.sort_values(
    "test_distance"
).iterrows():

    if (
        row["test_distance"] > 50
        and
        row["available_icu_beds"] > 0
        and
        row["cardiology"] == "Yes"
        and
        row["emergency_24x7"] == "Yes"
    ):

        regional_capable = row
        break


if regional_capable is None:

    print(
        "\nNo suitable regional hospital found."
    )

else:

    print("\n" + "-" * 70)
    print("REGIONAL CAPABLE HOSPITAL")
    print("-" * 70)

    print(
        "Hospital:",
        regional_capable["hospital_name"]
    )

    print(
        "Distance:",
        regional_capable["test_distance"],
        "km"
    )

    print(
        "ICU:",
        regional_capable["available_icu_beds"]
    )

    print(
        "Cardiology:",
        regional_capable["cardiology"]
    )

    print(
        "Emergency:",
        regional_capable["emergency_24x7"]
    )


# --------------------------------------------------
# Current recommendation
# --------------------------------------------------

print("\n" + "-" * 70)
print("CURRENT RECOMMENDATION")
print("-" * 70)

if result.empty:

    print(
        "NO ELIGIBLE HOSPITAL"
    )

else:

    top = result.iloc[0]

    print(
        "Hospital:",
        top["hospital_name"]
    )

    print(
        "Distance:",
        top["distance_km"],
        "km"
    )

    print(
        "Zone:",
        top["distance_zone"]
    )

    print(
        "Recommendation:",
        top["recommendation_type"]
    )

    print(
        "ICU:",
        top["available_icu_beds"]
    )

    print(
        "Final Score:",
        top["final_score"]
    )


# --------------------------------------------------
# SAFETY ASSERTION
# --------------------------------------------------

print("\n" + "=" * 70)
print("SAFETY VALIDATION")
print("=" * 70)

if result.empty:

    print(
        "FAIL — No hospital available."
    )

else:

    top = result.iloc[0]

    unsafe = (
        patient["priority"] == "Critical"
        and
        patient["icu_required"] == "Yes"
        and
        top["available_icu_beds"] <= 0
    )

    if unsafe:

        print(
            "FAIL — Critical patient received hospital without ICU."
        )

    else:

        print(
            "PASS — Critical recommendation has ICU capability."
        )

# ============================================================
# SIMULATE NEAREST HOSPITAL ICU FAILURE
# ============================================================

print("\n" + "=" * 70)
print("SIMULATING NEAREST HOSPITAL ICU FAILURE")
print("=" * 70)

# Copy hospital dataset so original CSV is NOT modified
failure_test_hospitals = hospitals.copy()

# Find nearest hospital
failure_test_hospitals["test_distance"] = (
    failure_test_hospitals.apply(
        lambda row: calculate_distance_km(
            patient["latitude"],
            patient["longitude"],
            row["latitude"],
            row["longitude"]
        ),
        axis=1
    )
)

nearest_index = (
    failure_test_hospitals["test_distance"]
    .idxmin()
)

nearest_hospital = (
    failure_test_hospitals.loc[
        nearest_index
    ]
)

print(
    "Blocked Hospital:",
    nearest_hospital["hospital_name"]
)

print(
    "Distance:",
    nearest_hospital["test_distance"],
    "km"
)

print(
    "Original ICU:",
    nearest_hospital["available_icu_beds"]
)

# Simulate ICU becoming unavailable
failure_test_hospitals.loc[
    nearest_index,
    "available_icu_beds"
] = 0

print(
    "Simulated ICU:",
    failure_test_hospitals.loc[
        nearest_index,
        "available_icu_beds"
    ]
)

# Remove helper column
failure_test_hospitals = (
    failure_test_hospitals.drop(
        columns=["test_distance"]
    )
)

# ------------------------------------------------------------
# Run referral engine after ICU failure
# ------------------------------------------------------------

failure_result = find_eligible_hospitals(
    patient,
    failure_test_hospitals
)

print("\n" + "-" * 70)
print("RECOMMENDATION AFTER ICU FAILURE")
print("-" * 70)

if failure_result.empty:

    print(
        "NO ELIGIBLE HOSPITAL"
    )

else:

    columns = [
        "rank",
        "hospital_name",
        "distance_km",
        "distance_zone",
        "recommendation_type",
        "available_icu_beds",
        "success_probability",
        "final_score"
    ]

    print(
        failure_result[
            columns
        ].head(5).to_string(
            index=False
        )
    )


# ============================================================
# SAFETY VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("ICU FAILURE SAFETY VALIDATION")
print("=" * 70)

if failure_result.empty:

    print(
        "NO ELIGIBLE HOSPITAL AFTER ICU FAILURE"
    )

else:

    recommended_ids = set(
        failure_result[
            "hospital_id"
        ].tolist()
    )

    blocked_hospital_id = (
        nearest_hospital["hospital_id"]
    )

    if blocked_hospital_id in recommended_ids:

        print(
            "FAIL — Hospital with simulated ICU failure "
            "was still recommended."
        )

    else:

        print(
            "PASS — Hospital with unavailable ICU "
            "was correctly excluded."
        )

    # Check top recommendation
    top = failure_result.iloc[0]

    if top["available_icu_beds"] > 0:

        print(
            "PASS — Top recommendation has ICU capability."
        )

    else:

        print(
            "FAIL — Top recommendation has no ICU."
        )