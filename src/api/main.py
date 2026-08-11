"""
FastAPI Backend
AI Powered Smart Hospital Referral System
"""

import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException

from src.api.schemas import (
    PatientReferralRequest,
    CreateReferralRequest,
)
from src.auth.schemas import (
    LoginRequest,
    LoginResponse,
    UserResponse,
)
from src.auth.jwt_utils import (
    create_access_token,
)

from src.auth.auth_store import (
    authenticate_user,
)
from src.auth.authorization import (
    can_view_referral,
    can_accept_or_reject,
    can_update_referral_status,
)

from src.prediction.referral_engine import (
    reserve_best_hospital
)
from src.prediction.feature_builder import (
    build_referral_features
)

from src.prediction.predict import (
    predict_referral_success
)

from src.prediction.ranking_engine import (
    rank_hospitals
)

from src.utils.referral_rules import (
    evaluate_hospital_capability
)
from src.prediction.bed_reservation import (
    confirm_reservation,
    release_bed,
    get_reservation,
)

from src.prediction.reservation_store import (
    get_hospital_inventory,
)
from src.prediction.referral_store import (
    create_referral as create_stored_referral,
    get_referral,
    get_patient_referrals,
    update_referral_status,
    attach_reservation,
)


app = FastAPI(
    title="AI Powered Smart Hospital Referral System",
    description=(
        "Backend API for AI-based hospital referral, "
        "hospital ranking and bed reservation."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def serialize_hospital(hospital):
    if hospital is None:
        return None

    data = (
        hospital.to_dict()
        if hasattr(hospital, "to_dict")
        else dict(hospital)
    )

    # Convert pandas NaN to None
    for key, value in data.items():
        try:
            if pd.isna(value):
                data[key] = None
        except (TypeError, ValueError):
            pass

    return data


# ============================================================
# DATA
# ============================================================

PATIENTS_PATH = "datasets/final/patients.csv"
HOSPITALS_PATH = "datasets/final/hospitals.csv"


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "success": True,
        "message": (
            "Smart Hospital Referral API is running."
        ),
        "service": "SIH Hospital AI",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health_check():

    return {
        "success": True,
        "status": "healthy",
    }


# ============================================================
# AUTHENTICATION
# ============================================================

@app.post(
    "/login",
    response_model=LoginResponse
)
def login(request: LoginRequest):

    user = authenticate_user(
        request.username,
        request.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    access_token = create_access_token(user)

    return {
        "success": True,
        "message": "Login successful.",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "user_id": user["user_id"],
            "username": user["username"],
            "name": user["name"],
            "role": user["role"],
            "hospital_id": user.get("hospital_id"),
            "state": user.get("state"),
            "district": user.get("district"),
        },
    }
  


# ============================================================
# REFERRAL
# ============================================================

@app.post("/referral")
def create_referral(
    request: PatientReferralRequest
):

    # ----------------------------------------
    # Load datasets
    # ----------------------------------------

    try:

        patients = pd.read_csv(
            PATIENTS_PATH
        )

        hospitals = pd.read_csv(
            HOSPITALS_PATH
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to load referral datasets: "
                f"{str(error)}"
            )
        )

    # ----------------------------------------
    # Find patient
    # ----------------------------------------

    patient_rows = patients[
        patients["patient_id"]
        == request.patient_id
    ]

    if patient_rows.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Patient {request.patient_id} "
                "not found."
            )
        )

    # ----------------------------------------
    # Convert patient to dictionary
    # ----------------------------------------

    patient = (
        patient_rows
        .iloc[0]
        .to_dict()
    )

    # ----------------------------------------
    # Run referral engine
    # ----------------------------------------

    try:

        result = reserve_best_hospital(
            patient,
            hospitals,
            hospital_id=request.hospital_id
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message": (
                    "Referral engine failed."
                ),
                "error": str(error),
            }
        )

    # ----------------------------------------
    # Return result
    # ----------------------------------------

    return {
        "success": result["success"],
        "status": result["status"],
        "message": result.get("message"),
        "hospital": serialize_hospital(
            result.get("hospital")
        ),
        "reservation": result.get(
            "reservation"
        ),
        "attempts": result.get(
            "attempts", []
        ),
    }


# ============================================================
# GET RESERVATION
# ============================================================

@app.get(
    "/reservation/{hospital_id}/{patient_id}"
)
def get_reservation_status(
    hospital_id: str,
    patient_id: str
):

    reservation = get_reservation(
        hospital_id,
        patient_id
    )

    if reservation is None:

        raise HTTPException(
            status_code=404,
            detail="Reservation not found."
        )

    return {
        "success": True,
        "status": reservation["status"],
        "reservation": reservation,
    }


# ============================================================
# CONFIRM RESERVATION
# ============================================================

@app.post(
    "/reservation/{hospital_id}/{patient_id}/confirm"
)
def confirm_reservation_api(
    hospital_id: str,
    patient_id: str
):

    inventory = get_hospital_inventory(
        hospital_id
    )

    if inventory is None:

        raise HTTPException(
            status_code=404,
            detail="Hospital inventory not found."
        )

    result = confirm_reservation(
        hospital_id,
        patient_id,
        inventory
    )

    if not result["success"]:

        raise HTTPException(
            status_code=400,
            detail=result
        )

    return {
        "success": True,
        "status": result["status"],
        "message": "Reservation confirmed successfully.",
        "reservation": result["reservation"],
        "inventory": get_hospital_inventory(
            hospital_id
        ),
    }


# ============================================================
# RELEASE RESERVATION
# ============================================================

@app.post(
    "/reservation/{hospital_id}/{patient_id}/release"
)
def release_reservation_api(
    hospital_id: str,
    patient_id: str
):

    reservation = get_reservation(
        hospital_id,
        patient_id
    )

    if reservation is None:

        raise HTTPException(
            status_code=404,
            detail="Reservation not found."
        )

    inventory = get_hospital_inventory(
        hospital_id
    )

    if inventory is None:

        raise HTTPException(
            status_code=404,
            detail="Hospital inventory not found."
        )

    result = release_bed(
        hospital_id=hospital_id,
        patient_id=patient_id,
        inventory=inventory,
    )

    if not result["success"]:

        raise HTTPException(
            status_code=400,
            detail=result
        )

    return {
        "success": True,
        "status": result["status"],
        "message": "Reservation released successfully.",
        "reservation": result["reservation"],
        "inventory": get_hospital_inventory(
            hospital_id
        ),
    }

# ============================================================
# HOSPITAL DASHBOARD INVENTORY
# ============================================================

@app.get("/hospitals/{hospital_id}/inventory")
def get_hospital_dashboard_inventory(
    hospital_id: str
):
    inventory = get_hospital_inventory(
        hospital_id
    )

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Hospital inventory not found."
        )

    return {
        "success": True,
        "hospital_id": hospital_id,
        "inventory": inventory,
    }


# ============================================================
# RANKED HOSPITALS
# ============================================================

@app.get("/hospitals")
def get_ranked_hospitals(
    patient_id: str
):

    # ----------------------------------------
    # Load datasets
    # ----------------------------------------

    try:

        patients = pd.read_csv(
            PATIENTS_PATH
        )

        hospitals = pd.read_csv(
            HOSPITALS_PATH
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "message":
                    "Failed to load datasets.",
                "error":
                    str(error),
            }
        )

    # ----------------------------------------
    # Find patient
    # ----------------------------------------

    patient_rows = patients[
        patients["patient_id"]
        == patient_id
    ]

    if patient_rows.empty:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Patient {patient_id} "
                "not found."
            )
        )

    patient = (
        patient_rows
        .iloc[0]
        .to_dict()
    )

    # ----------------------------------------
    # Referral required check
    # ----------------------------------------

    if patient["referral_required"] != "Yes":

        return {
            "success": True,
            "patient_id": patient_id,
            "message":
                "Hospital referral is not required.",
            "hospitals": [],
        }

    # ----------------------------------------
    # Build eligible hospitals
    # ----------------------------------------

    eligible_hospitals = []

    for _, hospital_row in hospitals.iterrows():

        hospital = hospital_row.to_dict()

        capability = (
            evaluate_hospital_capability(
                patient,
                hospital
            )
        )

        if not capability["eligible"]:

            continue

        # ------------------------------------
        # Build production features
        # ------------------------------------

        features = (
            build_referral_features(
                patient,
                hospital
            )
        )

        hospital_data = hospital.copy()

        hospital_data.update(
            features
        )

        # ------------------------------------
        # ML prediction
        # ------------------------------------

        prediction = (
            predict_referral_success(
                patient,
                hospital_data
            )
        )

        hospital_data[
            "success_probability"
        ] = prediction[
            "success_probability"
        ]

        hospital_data[
            "ml_prediction"
        ] = prediction[
            "prediction"
        ]

        eligible_hospitals.append(
            hospital_data
        )

    # ----------------------------------------
    # No eligible hospital
    # ----------------------------------------

    if not eligible_hospitals:

        return {
            "success": True,
            "patient_id": patient_id,
            "message":
                "No eligible hospital found.",
            "hospitals": [],
        }

    # ----------------------------------------
    # DataFrame
    # ----------------------------------------

    eligible_df = pd.DataFrame(
        eligible_hospitals
    )

    # ----------------------------------------
    # Rank hospitals
    # ----------------------------------------

    ranked = rank_hospitals(
        eligible_df,
        patient["priority"]
    )

    # ----------------------------------------
    # Top hospitals
    # ----------------------------------------

    ranked = ranked.head(10)

    hospitals_response = []

    for _, hospital in ranked.iterrows():

        hospital_data = (
            hospital.to_dict()
        )

        hospitals_response.append(
            serialize_hospital(
                hospital_data
            )
        )

    return {
        "success": True,
        "patient_id": patient_id,
        "priority":
            patient["priority"],
        "total_hospitals":
            len(hospitals_response),
        "hospitals":
            hospitals_response,
    }


# ============================================================
# LIVE HOSPITAL REFERRAL
# ============================================================

@app.post("/referrals")
def create_live_referral(
    request: CreateReferralRequest
):
    # ----------------------------------------
    # Create referral
    # ----------------------------------------

    result = create_stored_referral(
        patient_id=request.patient_id,
        from_hospital_id=request.from_hospital_id,
        to_hospital_id=request.to_hospital_id,
        reason=request.reason,
        priority=request.priority,
    )

    return result


# ============================================================
# GET REFERRAL
# ============================================================

@app.get("/referrals/{referral_id}")
def get_live_referral(
    referral_id: str
):
    referral = get_referral(
        referral_id
    )

    if referral is None:
        raise HTTPException(
            status_code=404,
            detail="Referral not found."
        )

    return {
        "success": True,
        "referral": referral,
    }


# ============================================================
# PATIENT REFERRAL HISTORY
# ============================================================

@app.get("/patients/{patient_id}/referrals")
def get_patient_referral_history(
    patient_id: str
):
    referrals = get_patient_referrals(
        patient_id
    )

    return {
        "success": True,
        "patient_id": patient_id,
        "total_referrals": len(referrals),
        "referrals": referrals,
    }


# ============================================================
# HOSPITAL REFERRAL INBOX
# ============================================================

@app.get("/hospitals/{hospital_id}/referrals")
def get_hospital_referrals(
    hospital_id: str
):
    from src.prediction.referral_store import _load_referrals

    stored_referrals = _load_referrals()

    hospital_referrals = [
        referral
        for referral in stored_referrals
        if referral.get("to_hospital_id")
        == hospital_id
    ]

    return {
        "success": True,
        "hospital_id": hospital_id,
        "total_referrals": len(
            hospital_referrals
        ),
        "referrals": hospital_referrals,
    }


# ============================================================
# UPDATE REFERRAL STATUS
# ============================================================

@app.post("/referrals/{referral_id}/status/{new_status}")
def update_live_referral_status(
    referral_id: str,
    new_status: str
):
    allowed_statuses = [
        "ACCEPTED",
        "REJECTED",
        "IN_TRANSIT",
        "ARRIVED",
        "TREATMENT_ACTIVE",
        "COMPLETED",
        "TRANSFERRED",
        "DIED",
    ]

    new_status = new_status.upper()

    if new_status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail={
                "message":
                    "Invalid referral status.",
                "allowed_statuses":
                    allowed_statuses,
            }
        )

    result = update_referral_status(
        referral_id,
        new_status
    )

    if not result["success"]:
        status_code = (
            404
            if result["status"] == "NOT_FOUND"
            else 409
        )

        raise HTTPException(
            status_code=status_code,
            detail=result,
        )

    return result


# ============================================================
# ATTACH BED RESERVATION TO REFERRAL
# ============================================================

@app.post("/referrals/{referral_id}/reservation")
def attach_referral_reservation(
    referral_id: str,
    hospital_id: str,
    bed_type: str
):
    bed_type = bed_type.upper()

    if bed_type not in [
        "GENERAL",
        "ICU"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Invalid bed type."
        )

    reservation = get_reservation(
        hospital_id,
        get_referral(
            referral_id
        )["patient_id"]
        if get_referral(referral_id)
        else ""
    )

    if reservation is None:
        raise HTTPException(
            status_code=404,
            detail="Active reservation not found."
        )

    if reservation["bed_type"] != bed_type:
        raise HTTPException(
            status_code=409,
            detail="Bed type does not match reservation."
        )

    result = attach_reservation(
        referral_id=referral_id,
        hospital_id=hospital_id,
        bed_type=bed_type,
    )

    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail=result
        )

    return result