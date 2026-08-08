"""
Referral Model Preprocessing
AI Powered Smart Hospital Referral System
"""

import pandas as pd


TARGET = "referral_success"


DROP_COLUMNS = [
    "referral_id",
    "patient_id",
    "hospital_id",
    "outcome",
    "referral_accepted",
    "response_time_minutes",
]


def load_referral_data(
    path="datasets/final/referrals.csv"
):
    """
    Load historical referral dataset.
    """

    df = pd.read_csv(path)

    return df


def prepare_referral_data(df):
    """
    Prepare referral dataset for ML.
    """

    df = df.copy()

    # --------------------------------
    # Target
    # --------------------------------

    y = df[TARGET].astype(int)

    # --------------------------------
    # Remove leakage / identifiers
    # --------------------------------

    X = df.drop(
        columns=[
            TARGET,
            *DROP_COLUMNS
        ],
        errors="ignore"
    )

    # --------------------------------
    # Convert categorical columns
    # --------------------------------

    categorical_columns = [
        "disease",
        "priority"
    ]

    X = pd.get_dummies(
        X,
        columns=categorical_columns,
        drop_first=False
    )

    return X, y


def prepare_referral_dataset(
    path="datasets/final/referrals.csv"
):
    """
    Load and prepare referral dataset.
    """

    df = load_referral_data(path)

    X, y = prepare_referral_data(df)

    return X, y