"""
Medical Rules & Knowledge Base
AI-Powered Smart Hospital Referral System
"""

# -------------------------------
# Symptoms
# -------------------------------

SYMPTOMS = [
    "Chest Pain",
    "Shortness of Breath",
    "High Fever",
    "Low Fever",
    "Headache",
    "Vomiting",
    "Nausea",
    "Cough",
    "Fatigue",
    "Dizziness",
    "Loss of Consciousness",
    "Abdominal Pain",
    "Diarrhea",
    "Back Pain",
    "Joint Pain",
    "Seizure",
    "Weakness",
    "Vision Loss",
    "Speech Difficulty",
    "Bleeding",
    "Burn Injury",
    "Road Accident",
    "Fracture",
    "Skin Rash",
    "Palpitations",
    "Low Oxygen",
    "Body Pain",
    "Chills",
    "Swelling",
    "Neck Pain",
    "Low Blood Pressure",
    "Confusion"
]

# --------------------------------
# Diseases
# --------------------------------

DISEASES = [
    "Viral Fever",
    "Pneumonia",
    "Asthma",
    "COPD",
    "Hypertension",
    "Diabetes",
    "Heart Attack",
    "Stroke",
    "Kidney Failure",
    "Food Poisoning",
    "Dengue",
    "Malaria",
    "COVID-like Infection",
    "Trauma",
    "Burn Injury",
    "Fracture",
    "Appendicitis",
    "Sepsis"
]


# --------------------------------
# Disease -> Common Symptoms
# --------------------------------

DISEASE_SYMPTOMS = {

    "Viral Fever": [
        "High Fever",
        "Body Pain",
        "Fatigue",
        "Chills",
        "Headache"
    ],

    "Pneumonia": [
        "Cough",
        "High Fever",
        "Shortness of Breath",
        "Low Oxygen",
        "Fatigue"
    ],

    "Asthma": [
        "Shortness of Breath",
        "Cough",
        "Chest Pain",
        "Fatigue"
    ],

    "COPD": [
        "Shortness of Breath",
        "Cough",
        "Fatigue",
        "Low Oxygen"
    ],

    "Hypertension": [
        "Headache",
        "Dizziness",
        "Fatigue"
    ],

    "Diabetes": [
        "Fatigue",
        "Weakness",
        "Dizziness",
        "Swelling"
    ],

    "Heart Attack": [
        "Chest Pain",
        "Shortness of Breath",
        "Palpitations",
        "Fatigue",
        "Dizziness"
    ],

    "Stroke": [
        "Speech Difficulty",
        "Weakness",
        "Vision Loss",
        "Dizziness",
        "Loss of Consciousness"
    ],

    "Kidney Failure": [
        "Swelling",
        "Fatigue",
        "Weakness",
        "Nausea",
        "Shortness of Breath"
    ],

    "Food Poisoning": [
        "Vomiting",
        "Diarrhea",
        "Abdominal Pain",
        "Nausea",
        "Weakness"
    ],

    "Dengue": [
        "High Fever",
        "Body Pain",
        "Vomiting",
        "Headache",
        "Fatigue"
    ],

    "Malaria": [
        "High Fever",
        "Chills",
        "Headache",
        "Body Pain",
        "Fatigue"
    ],

    "COVID-like Infection": [
        "Cough",
        "High Fever",
        "Shortness of Breath",
        "Fatigue",
        "Low Oxygen"
    ],

    "Trauma": [
        "Road Accident",
        "Bleeding",
        "Fracture",
        "Loss of Consciousness",
        "Body Pain"
    ],

    "Burn Injury": [
        "Burn Injury",
        "Bleeding",
        "Body Pain"
    ],

    "Fracture": [
        "Fracture",
        "Joint Pain",
        "Swelling",
        "Body Pain"
    ],

    "Appendicitis": [
        "Abdominal Pain",
        "Vomiting",
        "Nausea",
        "High Fever"
    ],

    "Sepsis": [
        "High Fever",
        "Low Blood Pressure",
        "Weakness",
        "Confusion",
        "Shortness of Breath"
    ]
}

# ----------------------------------------
# Disease -> Required Tests
# ----------------------------------------

DISEASE_REQUIRED_TESTS = {

    "Heart Attack": [
        "ECG",
        "Blood Test",
        "Troponin Test"
    ],

    "Stroke": [
        "CT Scan",
        "MRI",
        "Blood Test"
    ],

    "Pneumonia": [
        "Chest X-Ray",
        "Blood Test",
        "Oxygen Assessment"
    ],

    "Asthma": [
        "Chest X-Ray",
        "Oxygen Assessment",
        "Pulmonary Function Test"
    ],

    "COPD": [
        "Chest X-Ray",
        "Oxygen Assessment",
        "Pulmonary Function Test"
    ],

    "Hypertension": [
        "Blood Pressure Test",
        "Blood Test",
        "ECG"
    ],

    "Diabetes": [
        "Blood Glucose Test",
        "HbA1c Test",
        "Kidney Function Test"
    ],

    "Kidney Failure": [
        "Kidney Function Test",
        "Blood Test",
        "Ultrasound",
        "Dialysis"
    ],

    "Food Poisoning": [
        "Blood Test",
        "Stool Test"
    ],

    "Dengue": [
        "CBC",
        "Dengue NS1 Test",
        "Blood Test"
    ],

    "Malaria": [
        "Malaria Test",
        "CBC",
        "Blood Test"
    ],

    "COVID-like Infection": [
        "Chest X-Ray",
        "Oxygen Assessment",
        "Blood Test"
    ],

    "Trauma": [
        "X-Ray",
        "CT Scan",
        "Blood Test"
    ],

    "Burn Injury": [
        "Blood Test",
        "X-Ray"
    ],

    "Fracture": [
        "X-Ray",
        "CT Scan"
    ],

    "Appendicitis": [
        "Ultrasound",
        "Blood Test",
        "CT Scan"
    ],

    "Sepsis": [
        "Blood Test",
        "CBC",
        "Blood Culture",
        "Lactate Test"
    ],

    "Viral Fever": [
        "CBC",
        "Blood Test"
    ]
}


# --------------------------------
# Disease Distribution
# (Approximate prevalence in our synthetic dataset)
# --------------------------------

DISEASE_WEIGHTS = {
    "Viral Fever": 0.18,
    "Hypertension": 0.12,
    "Diabetes": 0.10,
    "Pneumonia": 0.08,
    "Asthma": 0.06,
    "Heart Attack": 0.05,
    "Stroke": 0.04,
    "Trauma": 0.06,
    "Kidney Failure": 0.03,
    "Dengue": 0.04,
    "Malaria": 0.03,
    "COVID-like Infection": 0.03,
    "Food Poisoning": 0.04,
    "Burn Injury": 0.02,
    "Fracture": 0.05,
    "Appendicitis": 0.03,
    "COPD": 0.02,
    "Sepsis": 0.02
}


# --------------------------------
# Disease Severity
# --------------------------------

DISEASE_SEVERITY = {

    "Heart Attack": "Critical",
    "Stroke": "Critical",
    "Sepsis": "Critical",

    "Trauma": "Urgent",
    "Kidney Failure": "Urgent",
    "Pneumonia": "Urgent",
    "Dengue": "Urgent",
    "Appendicitis": "Urgent",
    "Burn Injury": "Urgent",

    "Hypertension": "Stable",
    "Diabetes": "Stable",
    "Asthma": "Stable",
    "COPD": "Stable",
    "Food Poisoning": "Stable",
    "Fracture": "Stable",
    "Malaria": "Stable",
    "COVID-like Infection": "Stable",
    "Viral Fever": "Stable"
}

# --------------------------------
# ICU Requirement
# --------------------------------

ICU_REQUIRED = {

    "Heart Attack": True,
    "Stroke": True,
    "Sepsis": True,

    "Kidney Failure": False,
    "Pneumonia": False,
    "Dengue": False,
    "Trauma": False,

    "Hypertension": False,
    "Diabetes": False,
    "Asthma": False,
    "COPD": False,
    "Food Poisoning": False,
    "Fracture": False,
    "Burn Injury": False,
    "Appendicitis": False,
    "Malaria": False,
    "COVID-like Infection": False,
    "Viral Fever": False
}

# ----------------------------------------
# Disease-wise Vital Ranges
# ----------------------------------------

DISEASE_VITALS = {

    "Viral Fever": {
        "spo2": (95, 100),
        "heart_rate": (80, 120),
        "systolic_bp": (100, 140),
        "diastolic_bp": (65, 90),
        "respiratory_rate": (16, 24),
        "temperature": (99.5, 103.0)
    },

    "Pneumonia": {
        "spo2": (88, 96),
        "heart_rate": (90, 130),
        "systolic_bp": (95, 150),
        "diastolic_bp": (60, 95),
        "respiratory_rate": (20, 32),
        "temperature": (100.0, 104.0)
    },

    "Asthma": {
        "spo2": (88, 96),
        "heart_rate": (85, 125),
        "systolic_bp": (100, 145),
        "diastolic_bp": (65, 90),
        "respiratory_rate": (20, 35),
        "temperature": (97.0, 100.0)
    },

    "COPD": {
        "spo2": (86, 95),
        "heart_rate": (80, 120),
        "systolic_bp": (100, 155),
        "diastolic_bp": (65, 95),
        "respiratory_rate": (20, 32),
        "temperature": (97.0, 100.0)
    },

    "Hypertension": {
        "spo2": (95, 100),
        "heart_rate": (65, 105),
        "systolic_bp": (145, 200),
        "diastolic_bp": (90, 120),
        "respiratory_rate": (14, 22),
        "temperature": (97.0, 99.0)
    },

    "Diabetes": {
        "spo2": (95, 100),
        "heart_rate": (65, 105),
        "systolic_bp": (110, 155),
        "diastolic_bp": (70, 95),
        "respiratory_rate": (14, 24),
        "temperature": (97.0, 99.0)
    },

    "Heart Attack": {
        "spo2": (78, 92),
        "heart_rate": (110, 160),
        "systolic_bp": (80, 180),
        "diastolic_bp": (50, 110),
        "respiratory_rate": (22, 36),
        "temperature": (97.0, 100.0)
    },

    "Stroke": {
        "spo2": (82, 95),
        "heart_rate": (70, 120),
        "systolic_bp": (150, 220),
        "diastolic_bp": (90, 130),
        "respiratory_rate": (16, 30),
        "temperature": (97.0, 100.0)
    },

    "Kidney Failure": {
        "spo2": (90, 98),
        "heart_rate": (75, 115),
        "systolic_bp": (120, 180),
        "diastolic_bp": (75, 110),
        "respiratory_rate": (18, 30),
        "temperature": (97.0, 100.0)
    },

    "Food Poisoning": {
        "spo2": (95, 100),
        "heart_rate": (85, 125),
        "systolic_bp": (90, 135),
        "diastolic_bp": (55, 90),
        "respiratory_rate": (16, 24),
        "temperature": (98.5, 102.5)
    },

    "Dengue": {
        "spo2": (92, 99),
        "heart_rate": (90, 130),
        "systolic_bp": (85, 120),
        "diastolic_bp": (55, 80),
        "respiratory_rate": (16, 26),
        "temperature": (101.0, 105.0)
    },

    "Malaria": {
        "spo2": (93, 99),
        "heart_rate": (85, 130),
        "systolic_bp": (90, 135),
        "diastolic_bp": (55, 90),
        "respiratory_rate": (16, 26),
        "temperature": (100.0, 105.0)
    },

    "COVID-like Infection": {
        "spo2": (88, 97),
        "heart_rate": (85, 130),
        "systolic_bp": (95, 150),
        "diastolic_bp": (60, 95),
        "respiratory_rate": (20, 34),
        "temperature": (99.0, 103.5)
    },

    "Trauma": {
        "spo2": (85, 99),
        "heart_rate": (90, 145),
        "systolic_bp": (80, 150),
        "diastolic_bp": (50, 100),
        "respiratory_rate": (18, 32),
        "temperature": (97.0, 101.0)
    },

    "Burn Injury": {
        "spo2": (88, 99),
        "heart_rate": (90, 145),
        "systolic_bp": (85, 150),
        "diastolic_bp": (55, 100),
        "respiratory_rate": (18, 32),
        "temperature": (97.0, 102.0)
    },

    "Fracture": {
        "spo2": (94, 100),
        "heart_rate": (70, 120),
        "systolic_bp": (100, 150),
        "diastolic_bp": (65, 95),
        "respiratory_rate": (14, 24),
        "temperature": (97.0, 100.0)
    },

    "Appendicitis": {
        "spo2": (95, 100),
        "heart_rate": (85, 125),
        "systolic_bp": (95, 145),
        "diastolic_bp": (60, 95),
        "respiratory_rate": (16, 26),
        "temperature": (99.0, 103.0)
    },

    "Sepsis": {
        "spo2": (82, 96),
        "heart_rate": (100, 160),
        "systolic_bp": (70, 110),
        "diastolic_bp": (40, 75),
        "respiratory_rate": (22, 40),
        "temperature": (96.0, 104.0)
    }
}

# ----------------------------------------
# Ambulance Requirement
# ----------------------------------------

AMBULANCE_REQUIRED = {

    "Heart Attack": True,
    "Stroke": True,
    "Trauma": True,
    "Burn Injury": True,

    "Pneumonia": False,
    "Diabetes": False,
    "Hypertension": False,
    "Asthma": False,
    "Dengue": False,
    "Malaria": False,
    "Food Poisoning": False,
    "Fracture": False,
    "COVID-like Infection": False,
    "Kidney Failure": False,
    "Appendicitis": False,
    "COPD": False,
    "Sepsis": True,
    "Viral Fever": False
}


