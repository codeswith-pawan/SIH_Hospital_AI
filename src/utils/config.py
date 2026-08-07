"""
Global Configuration for Smart Hospital AI Project
"""

# -----------------------------
# Random Seed
# -----------------------------
RANDOM_SEED = 42

# -----------------------------
# Dataset Size
# -----------------------------
NUM_PATIENTS = 50000
NUM_HOSPITALS = 500
NUM_REFERRALS = 150000
NUM_BED_HISTORY = 250000

# -----------------------------
# Gender Distribution
# -----------------------------
GENDER_WEIGHTS = {
    "Male": 0.51,
    "Female": 0.48,
    "Other": 0.01
}

# -----------------------------
# Blood Groups
# -----------------------------
BLOOD_GROUPS = {
    "O+": 0.37,
    "B+": 0.32,
    "A+": 0.21,
    "AB+": 0.08,
    "O-": 0.01,
    "B-": 0.003,
    "A-": 0.004,
    "AB-": 0.003
}

# -----------------------------
# Priority Classes
# -----------------------------
PRIORITY_CLASSES = [
    "Stable",
    "Urgent",
    "Critical"
]

# -----------------------------
# Outcome Classes
# -----------------------------
OUTCOMES = [
    "Admitted",
    "Transferred",
    "Discharged",
    "Deceased"
]

# -----------------------------
# Lifestyle
# -----------------------------
YES_NO = ["Yes", "No"]


# -----------------------------
# Indian Names
# -----------------------------

FIRST_NAMES_MALE = [
    "Aarav","Vivaan","Aditya","Krishna","Arjun",
    "Rahul","Rohan","Aman","Pawan","Ankit",
    "Sourav","Abhishek","Karan","Shubham","Ritesh",
    "Vikash","Deepak","Nikhil","Ayush","Rohit"
]

FIRST_NAMES_FEMALE = [
    "Priya","Anjali","Neha","Pooja","Sneha",
    "Riya","Kavya","Aditi","Nisha","Sakshi",
    "Simran","Muskan","Komal","Shruti","Khushi",
    "Payal","Divya","Megha","Anu","Preeti"
]

LAST_NAMES = [
    "Sharma","Kumar","Singh","Yadav","Gupta",
    "Patel","Verma","Pandey","Mishra","Das",
    "Roy","Joshi","Thakur","Chauhan","Reddy",
    "Nair","Iyer","Sinha","Jha","Mehta"
]

# -----------------------------
# States
# -----------------------------

INDIAN_STATES = [
    "Bihar",
    "Punjab",
    "Delhi",
    "Maharashtra",
    "Uttar Pradesh",
    "West Bengal",
    "Tamil Nadu",
    "Karnataka",
    "Gujarat",
    "Rajasthan"
]

DISTRICTS = {
    "Bihar": [
        "Patna",
        "Purnia",
        "Bhagalpur",
        "Muzaffarpur",
        "Gaya"
    ],

    "Punjab":[
        "Mohali",
        "Ludhiana",
        "Amritsar",
        "Patiala"
    ],

    "Delhi":[
        "New Delhi",
        "North Delhi",
        "South Delhi"
    ]
}

# ======================================================
# INDIAN NAMES
# ======================================================

FIRST_NAMES_MALE = [
    "Aarav","Vivaan","Aditya","Krishna","Arjun",
    "Rahul","Rohan","Aman","Pawan","Ankit",
    "Abhishek","Karan","Ritesh","Deepak","Rohit",
    "Ayush","Nikhil","Sourav","Vikash","Shubham"
]

FIRST_NAMES_FEMALE = [
    "Priya","Anjali","Neha","Pooja","Sneha",
    "Aditi","Riya","Kavya","Sakshi","Khushi",
    "Muskan","Simran","Komal","Divya","Payal",
    "Shruti","Megha","Nisha","Preeti","Anu"
]

LAST_NAMES = [
    "Sharma","Kumar","Singh","Yadav","Patel",
    "Verma","Gupta","Mishra","Pandey","Das",
    "Roy","Jha","Mehta","Reddy","Nair",
    "Iyer","Thakur","Chauhan","Joshi","Sinha"
]

# ======================================================
# STATES
# ======================================================

INDIAN_STATES = [
    "Bihar",
    "Punjab",
    "Delhi",
    "Uttar Pradesh",
    "Maharashtra",
    "West Bengal",
    "Gujarat",
    "Tamil Nadu",
    "Karnataka",
    "Rajasthan"
]

DISTRICTS = {

    "Bihar":[
        "Patna",
        "Purnia",
        "Gaya",
        "Muzaffarpur",
        "Bhagalpur"
    ],

    "Punjab":[
        "Mohali",
        "Ludhiana",
        "Patiala",
        "Amritsar"
    ],

    "Delhi":[
        "New Delhi",
        "North Delhi",
        "South Delhi"
    ]
}

