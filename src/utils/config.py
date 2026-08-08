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

# ----------------------------------------
# Indian States -> Districts
# ----------------------------------------

DISTRICTS = {

    "Bihar": [
        "Patna",
        "Purnia",
        "Gaya",
        "Muzaffarpur",
        "Bhagalpur",
        "Darbhanga",
        "Munger",
        "Begusarai"
    ],

    "Punjab": [
        "Mohali",
        "Ludhiana",
        "Patiala",
        "Amritsar",
        "Jalandhar",
        "Bathinda",
        "Hoshiarpur"
    ],

    "Delhi": [
        "New Delhi",
        "North Delhi",
        "South Delhi",
        "East Delhi",
        "West Delhi"
    ],

    "Uttar Pradesh": [
        "Lucknow",
        "Kanpur",
        "Varanasi",
        "Agra",
        "Prayagraj",
        "Meerut",
        "Noida",
        "Gorakhpur"
    ],

    "Maharashtra": [
        "Mumbai",
        "Pune",
        "Nagpur",
        "Nashik",
        "Thane",
        "Aurangabad"
    ],

    "West Bengal": [
        "Kolkata",
        "Howrah",
        "Durgapur",
        "Siliguri",
        "Asansol"
    ],

    "Gujarat": [
        "Ahmedabad",
        "Surat",
        "Vadodara",
        "Rajkot",
        "Gandhinagar"
    ],

    "Tamil Nadu": [
        "Chennai",
        "Coimbatore",
        "Madurai",
        "Salem",
        "Tiruchirappalli"
    ],

    "Karnataka": [
        "Bengaluru",
        "Mysuru",
        "Mangaluru",
        "Hubballi",
        "Belagavi"
    ],

    "Rajasthan": [
        "Jaipur",
        "Jodhpur",
        "Udaipur",
        "Kota",
        "Ajmer",
        "Bikaner"
    ]

}

# ----------------------------------------
# Approximate District Coordinates
# ----------------------------------------

DISTRICT_COORDINATES = {

    "Patna": (25.5941, 85.1376),
    "Purnia": (25.7771, 87.4753),
    "Gaya": (24.7914, 85.0002),
    "Muzaffarpur": (26.1197, 85.3910),
    "Bhagalpur": (25.2425, 86.9842),
    "Darbhanga": (26.1542, 85.8918),
    "Munger": (25.3748, 86.4735),
    "Begusarai": (25.4182, 86.1272),

    "Mohali": (30.7046, 76.7179),
    "Ludhiana": (30.9010, 75.8573),
    "Patiala": (30.3398, 76.3869),
    "Amritsar": (31.6340, 74.8723),
    "Jalandhar": (31.3260, 75.5762),
    "Bathinda": (30.2110, 74.9455),
    "Hoshiarpur": (31.5143, 75.9115),

    "New Delhi": (28.6139, 77.2090),
    "North Delhi": (28.7041, 77.1025),
    "South Delhi": (28.5355, 77.3910),
    "East Delhi": (28.6280, 77.2773),
    "West Delhi": (28.6517, 77.1171),

    "Lucknow": (26.8467, 80.9462),
    "Kanpur": (26.4499, 80.3319),
    "Varanasi": (25.3176, 82.9739),
    "Agra": (27.1767, 78.0081),
    "Prayagraj": (25.4358, 81.8463),
    "Meerut": (28.9845, 77.7064),
    "Noida": (28.5355, 77.3910),
    "Gorakhpur": (26.7606, 83.3732),

    "Mumbai": (19.0760, 72.8777),
    "Pune": (18.5204, 73.8567),
    "Nagpur": (21.1458, 79.0882),
    "Nashik": (19.9975, 73.7898),
    "Thane": (19.2183, 72.9781),
    "Aurangabad": (19.8762, 75.3433),

    "Kolkata": (22.5726, 88.3639),
    "Howrah": (22.5958, 88.2636),
    "Durgapur": (23.5204, 87.3119),
    "Siliguri": (26.7271, 88.3953),
    "Asansol": (23.6739, 86.9524),

    "Ahmedabad": (23.0225, 72.5714),
    "Surat": (21.1702, 72.8311),
    "Vadodara": (22.3072, 73.1812),
    "Rajkot": (22.3039, 70.8022),
    "Gandhinagar": (23.2156, 72.6369),

    "Chennai": (13.0827, 80.2707),
    "Coimbatore": (11.0168, 76.9558),
    "Madurai": (9.9252, 78.1198),
    "Salem": (11.6643, 78.1460),
    "Tiruchirappalli": (10.7905, 78.7047),

    "Bengaluru": (12.9716, 77.5946),
    "Mysuru": (12.2958, 76.6394),
    "Mangaluru": (12.9141, 74.8560),
    "Hubballi": (15.3647, 75.1240),
    "Belagavi": (15.8497, 74.4977),

    "Jaipur": (26.9124, 75.7873),
    "Jodhpur": (26.2389, 73.0243),
    "Udaipur": (24.5854, 73.7125),
    "Kota": (25.2138, 75.8648),
    "Ajmer": (26.4499, 74.6399),
    "Bikaner": (28.0229, 73.3119)
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


