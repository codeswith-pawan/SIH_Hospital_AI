import pandas as pd

from src.utils.referral_rules import (
    check_test_availability,
    check_specialty_availability,
    check_hospital_eligibility
)


patients = pd.read_csv(
    "datasets/final/patients.csv"
)

hospitals = pd.read_csv(
    "datasets/final/hospitals.csv"
)


# ----------------------------------------
# Select one patient
# ----------------------------------------

patient = patients.iloc[0]

print("\nPATIENT")
print(patient[
    [
        "patient_id",
        "disease",
        "priority",
        "icu_required",
        "required_test_1",
        "required_test_2",
        "required_test_3",
        "required_test_4"
    ]
])


# ----------------------------------------
# Test first hospital
# ----------------------------------------

hospital = hospitals.iloc[0]

print("\nHOSPITAL")
print(hospital[
    [
        "hospital_id",
        "hospital_name",
        "available_beds",
        "available_icu_beds"
    ]
])


# ----------------------------------------
# Test availability
# ----------------------------------------

test_result = check_test_availability(
    patient,
    hospital
)

print("\nTEST RESULT")
print(test_result)


# ----------------------------------------
# Specialty
# ----------------------------------------

specialty_result = check_specialty_availability(
    patient,
    hospital
)

print("\nSPECIALTY RESULT")
print(specialty_result)


# ----------------------------------------
# Final eligibility
# ----------------------------------------

eligible = check_hospital_eligibility(
    patient,
    hospital
)

print("\nHOSPITAL ELIGIBLE:", eligible)