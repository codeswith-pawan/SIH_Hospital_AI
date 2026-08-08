"""
Referral Rules & Hospital Capability Mapping
AI Powered Smart Hospital Referral System
"""
import pandas as pd
# ----------------------------------------
# Patient Test -> Hospital Column Mapping
# ----------------------------------------

TEST_TO_HOSPITAL_COLUMN = {

    "ECG": "ecg",

    "CT Scan": "ct_scan",

    "MRI": "mri",

    "X-Ray": "xray",

    "Chest X-Ray": "xray",

    "Ultrasound": "ultrasound",

    "Dialysis": "dialysis",

    "Blood Test": "blood_test",

    "CBC": "cbc",

    "Troponin Test": "troponin_test",

    "Dengue NS1 Test": "dengue_ns1_test",

    "Malaria Test": "malaria_test",

    "Blood Glucose Test": "blood_glucose_test",

    "HbA1c Test": "hba1c_test",

    "Kidney Function Test": "kidney_function_test",

    "Pulmonary Function Test": "pulmonary_function_test",

    "Blood Culture": "blood_culture",

    "Lactate Test": "lactate_test",

    "Stool Test": "stool_test",

    "Oxygen Assessment": "oxygen_support",

    "Blood Pressure Test": "general_medicine"
}


# ----------------------------------------
# Disease -> Required Hospital Specialty
# ----------------------------------------

DISEASE_SPECIALTY = {

    "Heart Attack": [
        "cardiology"
    ],

    "Stroke": [
        "neurology"
    ],

    "Kidney Failure": [
        "nephrology"
    ],

    "Pneumonia": [
        "pulmonology"
    ],

    "Asthma": [
        "pulmonology"
    ],

    "COPD": [
        "pulmonology"
    ],

    "Fracture": [
        "orthopedics"
    ],

    "Trauma": [
        "trauma_unit",
        "orthopedics"
    ],

    "Burn Injury": [
        "burn_unit"
    ],

    "Appendicitis": [
        "general_surgery"
    ],

    "Sepsis": [
        "general_medicine"
    ],

    "Dengue": [
        "general_medicine"
    ],

    "Malaria": [
        "general_medicine"
    ],

    "Viral Fever": [
        "general_medicine"
    ],

    "COVID-like Infection": [
        "pulmonology"
    ],

    "Diabetes": [
        "general_medicine"
    ],

    "Hypertension": [
        "general_medicine"
    ],

    "Food Poisoning": [
        "general_medicine"
    ]
}

# ----------------------------------------
# Check Required Tests
# ----------------------------------------

def check_test_availability(patient, hospital):
    """
    Check whether hospital has all tests
    required by the patient.
    """

    required_tests = []

    for i in range(1, 5):

        test = patient.get(
            f"required_test_{i}"
        )

        # Ignore missing / NaN tests
        if pd.isna(test):
            continue

        if test not in required_tests:
            required_tests.append(test)

    unavailable_tests = []

    for test in required_tests:

        hospital_column = TEST_TO_HOSPITAL_COLUMN.get(test)

        if hospital_column is None:
            unavailable_tests.append(test)
            continue

        if hospital.get(hospital_column) != "Yes":
            unavailable_tests.append(test)

    return {
        "all_available": len(unavailable_tests) == 0,
        "unavailable_tests": unavailable_tests
    }



# ----------------------------------------
# Check Specialty
# ----------------------------------------

def check_specialty_availability(patient, hospital):
    """
    Check whether hospital has the required
    medical specialty.
    """

    disease = patient["disease"]

    required_specialties = DISEASE_SPECIALTY.get(
        disease,
        ["general_medicine"]
    )

    unavailable_specialties = []

    for specialty in required_specialties:

        if hospital.get(specialty) != "Yes":
            unavailable_specialties.append(
                specialty
            )

    return {
        "all_available": (
            len(unavailable_specialties) == 0
        ),
        "unavailable_specialties":
            unavailable_specialties
    }


# ----------------------------------------
# Check Bed Availability
# ----------------------------------------

def check_bed_availability(patient, hospital):
    """
    Check whether hospital has an appropriate
    bed for the patient.
    """

    if patient["icu_required"] == "Yes":

        return hospital["available_icu_beds"] > 0

    if patient["priority"] == "Critical":

        return hospital["available_emergency_beds"] > 0

    return hospital["available_beds"] > 0


# ----------------------------------------
# Complete Hospital Eligibility
# ----------------------------------------

def check_hospital_eligibility(patient, hospital):
    """
    Determine whether a hospital is eligible
    for patient referral.
    """

    if hospital["accepts_referral"] != "Yes":
        return False

    test_result = check_test_availability(
        patient,
        hospital
    )

    if not test_result["all_available"]:
        return False

    specialty_result = check_specialty_availability(
        patient,
        hospital
    )

    if not specialty_result["all_available"]:
        return False

    if not check_bed_availability(
        patient,
        hospital
    ):
        return False

    return True

