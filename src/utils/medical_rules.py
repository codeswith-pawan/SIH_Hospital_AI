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
    "Neck Pain"
]

# -------------------------------
# Diseases
# -------------------------------

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

DISEASE_SYMPTOMS = {

"Heart Attack":[
    "Chest Pain",
    "Shortness of Breath",
    "Palpitations",
    "Fatigue"
],

"Stroke":[
    "Speech Difficulty",
    "Weakness",
    "Vision Loss"
],

"Pneumonia":[
    "Cough",
    "High Fever",
    "Low Oxygen"
],

"Dengue":[
    "High Fever",
    "Body Pain",
    "Vomiting"
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

    "Heart Attack": {
        "spo2": (78, 92),
        "heart_rate": (110, 160),
        "systolic_bp": (80, 180),
        "diastolic_bp": (50, 110),
        "temperature": (97.0, 100.0)
    },

    "Stroke": {
        "spo2": (82, 95),
        "heart_rate": (70, 120),
        "systolic_bp": (150, 220),
        "diastolic_bp": (90, 130),
        "temperature": (97.0, 100.0)
    },

    "Pneumonia": {
        "spo2": (82, 94),
        "heart_rate": (90, 130),
        "systolic_bp": (95, 150),
        "diastolic_bp": (60, 95),
        "temperature": (100.0, 104.0)
    },

    "Dengue": {
        "spo2": (92, 99),
        "heart_rate": (90, 130),
        "systolic_bp": (85, 120),
        "diastolic_bp": (55, 80),
        "temperature": (101.0, 105.0)
    },

    "Diabetes": {
        "spo2": (95, 100),
        "heart_rate": (65, 100),
        "systolic_bp": (110, 150),
        "diastolic_bp": (70, 95),
        "temperature": (97.0, 99.0)
    },

    "Hypertension": {
        "spo2": (95, 100),
        "heart_rate": (65, 105),
        "systolic_bp": (145, 200),
        "diastolic_bp": (90, 120),
        "temperature": (97.0, 99.0)
    },

    "Asthma": {
        "spo2": (88, 96),
        "heart_rate": (85, 120),
        "systolic_bp": (100, 145),
        "diastolic_bp": (65, 90),
        "temperature": (97.0, 100.0)
    },

    "Viral Fever": {
        "spo2": (95, 100),
        "heart_rate": (80, 120),
        "systolic_bp": (100, 140),
        "diastolic_bp": (65, 90),
        "temperature": (99.5, 103.0)
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


