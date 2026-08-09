import pandas as pd

from src.prediction.referral_engine import (
    find_eligible_hospitals
)


PATIENT_ID = "PAT000002"


patients = pd.read_csv(
    "datasets/final/patients.csv"
)

hospitals = pd.read_csv(
    "datasets/final/hospitals.csv"
)


patient = patients[
    patients["patient_id"] == PATIENT_ID
].iloc[0].to_dict()


def print_result(title, result):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    if result.empty:

        print("NO ELIGIBLE HOSPITAL")
        return

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
        result[
            columns
        ].head(5).to_string(
            index=False
        )
    )

    print(
        "\nZones returned:",
        result["distance_zone"].unique().tolist()
    )

    print(
        "Recommendation types:",
        result[
            "recommendation_type"
        ].unique().tolist()
    )


# ============================================================
# CASE 1 — NORMAL
# Local hospitals available
# ============================================================

print("\nPATIENT")
print("=" * 70)

print("Patient ID:", patient["patient_id"])
print("Disease:", patient["disease"])
print("Priority:", patient["priority"])
print("ICU Required:", patient["icu_required"])


result_normal = find_eligible_hospitals(
    patient,
    hospitals.copy()
)

print_result(
    "CASE 1 — LOCAL HOSPITALS AVAILABLE",
    result_normal
)


# ============================================================
# CASE 2 — REMOVE LOCAL HOSPITALS
# Regional fallback should activate
# ============================================================

regional_test_hospitals = hospitals.copy()

# Calculate approximate distance using production engine
from src.utils.helpers import calculate_distance_km


regional_test_hospitals["test_distance_km"] = (
    regional_test_hospitals.apply(
        lambda row: calculate_distance_km(
            patient["latitude"],
            patient["longitude"],
            row["latitude"],
            row["longitude"]
        ),
        axis=1
    )
)

# Remove all hospitals within LOCAL range
regional_test_hospitals = (
    regional_test_hospitals[
        regional_test_hospitals["test_distance_km"] > 50
    ]
    .drop(columns=["test_distance_km"])
    .reset_index(drop=True)
)


result_regional = find_eligible_hospitals(
    patient,
    regional_test_hospitals
)

print_result(
    "CASE 2 — LOCAL REMOVED → REGIONAL FALLBACK",
    result_regional
)


# ============================================================
# CASE 3 — REMOVE LOCAL + REGIONAL
# Extended fallback should activate
# ============================================================

extended_test_hospitals = hospitals.copy()

extended_test_hospitals["test_distance_km"] = (
    extended_test_hospitals.apply(
        lambda row: calculate_distance_km(
            patient["latitude"],
            patient["longitude"],
            row["latitude"],
            row["longitude"]
        ),
        axis=1
    )
)

# Keep only hospitals beyond 200 km
extended_test_hospitals = (
    extended_test_hospitals[
        extended_test_hospitals["test_distance_km"] > 200
    ]
    .drop(columns=["test_distance_km"])
    .reset_index(drop=True)
)


result_extended = find_eligible_hospitals(
    patient,
    extended_test_hospitals
)

print_result(
    "CASE 3 — LOCAL + REGIONAL REMOVED → EXTENDED FALLBACK",
    result_extended
)


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("FALLBACK VALIDATION")
print("=" * 70)


case1_ok = (
    not result_normal.empty
    and
    all(
        result_normal["distance_zone"] == "LOCAL"
    )
)


case2_ok = (
    not result_regional.empty
    and
    all(
        result_regional["distance_zone"] == "REGIONAL"
    )
)


case3_ok = (
    not result_extended.empty
    and
    all(
        result_extended["distance_zone"] == "EXTENDED"
    )
)


print(
    "CASE 1 LOCAL:",
    "PASS" if case1_ok else "FAIL"
)

print(
    "CASE 2 REGIONAL FALLBACK:",
    "PASS" if case2_ok else "FAIL"
)

print(
    "CASE 3 EXTENDED FALLBACK:",
    "PASS" if case3_ok else "FAIL"
)


if case1_ok and case2_ok and case3_ok:

    print(
        "\nALL DISTANCE FALLBACK TESTS PASSED"
    )

else:

    print(
        "\nDISTANCE FALLBACK TEST FAILED"
    )