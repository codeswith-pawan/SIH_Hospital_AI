"""
Patient management API routes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.database import get_db

from src.database.patient_service import (
    get_patient,
    get_hospital,
    get_all_hospitals,
    get_patient_visits,
    get_hospital_patients,
    create_hospital_visit,
    update_visit_status,
    update_visit_notes,
    get_hospital_patient_summary,
)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.get("/hospitals")
def get_hospitals(
    db: Session = Depends(get_db),
):
    hospitals = get_all_hospitals(db=db)

    return {
        "success": True,
        "count": len(hospitals),
        "hospitals": [
            {
                "hospital_id": hospital.hospital_id,
                "name": hospital.name,
                "state": hospital.state,
                "district": hospital.district,
            }
            for hospital in hospitals
        ],
    }


@router.get("/hospitals/{hospital_id}")
def get_hospital_details(
    hospital_id: str,
    db: Session = Depends(get_db),
):
    hospital = get_hospital(
        db=db,
        hospital_id=hospital_id,
    )

    if hospital is None:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found.",
        )

    return {
        "success": True,
        "hospital": {
            "hospital_id": hospital.hospital_id,
            "name": hospital.name,

            "location": {
                "state": hospital.state,
                "district": hospital.district,
                "city": hospital.city,
                "latitude": hospital.latitude,
                "longitude": hospital.longitude,
            },

            "beds": {
                "total_beds": hospital.total_beds,
                "occupied_beds": hospital.occupied_beds,
                "available_beds": hospital.available_beds,
                "icu_beds": hospital.icu_beds,
                "available_icu_beds": hospital.available_icu_beds,
                "emergency_beds": hospital.emergency_beds,
                "available_emergency_beds": (
                    hospital.available_emergency_beds
                ),
            },

            "services": {
                "emergency_24x7": hospital.emergency_24x7,
                "accepts_referral": hospital.accepts_referral,
                "ambulance": hospital.ambulance,
                "oxygen_support": hospital.oxygen_support,
                "ventilator": hospital.ventilator,
                "blood_bank": hospital.blood_bank,
            },

            "departments": {
                "cardiology": hospital.cardiology,
                "neurology": hospital.neurology,
                "nephrology": hospital.nephrology,
                "pulmonology": hospital.pulmonology,
                "orthopedics": hospital.orthopedics,
                "general_medicine": hospital.general_medicine,
                "general_surgery": hospital.general_surgery,
                "trauma_unit": hospital.trauma_unit,
                "burn_unit": hospital.burn_unit,
            },

            "equipment": {
                "ct_scan": hospital.ct_scan,
                "mri": hospital.mri,
                "xray": hospital.xray,
                "ultrasound": hospital.ultrasound,
                "ecg": hospital.ecg,
                "dialysis": hospital.dialysis,
            },

            "tests": {
                "blood_test": hospital.blood_test,
                "cbc": hospital.cbc,
                "troponin_test": hospital.troponin_test,
                "dengue_ns1_test": hospital.dengue_ns1_test,
                "malaria_test": hospital.malaria_test,
                "blood_glucose_test": hospital.blood_glucose_test,
                "hba1c_test": hospital.hba1c_test,
                "kidney_function_test": (
                    hospital.kidney_function_test
                ),
                "pulmonary_function_test": (
                    hospital.pulmonary_function_test
                ),
                "blood_culture": hospital.blood_culture,
                "lactate_test": hospital.lactate_test,
                "stool_test": hospital.stool_test,
            },

            "created_at": hospital.created_at,
        },
    }

# ============================================================
# HOSPITAL PATIENT LIST
# Must come before /{patient_id}
# ============================================================

@router.get("/hospital/{hospital_id}")
def get_hospital_patient_list(
    hospital_id: str,
    status: str | None = None,
    priority: str | None = None,
    icu_required: str | None = None,
    db: Session = Depends(get_db),
):
    allowed_statuses = [
        "NEW",
        "ACTIVE",
        "COMPLETED",
    ]

    allowed_priorities = [
        "Critical",
        "Urgent",
        "Stable",
    ]

    allowed_icu_values = [
        "Yes",
        "No",
    ]

    if status is not None:
        status = status.upper()

        if status not in allowed_statuses:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid status. Allowed values: "
                    "NEW, ACTIVE, COMPLETED."
                ),
            )

    if priority is not None:
        priority = priority.capitalize()

        if priority not in allowed_priorities:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid priority. Allowed values: "
                    "Critical, Urgent, Stable."
                ),
            )

    if icu_required is not None:
        icu_required = icu_required.capitalize()

        if icu_required not in allowed_icu_values:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid icu_required value. "
                    "Allowed values: Yes, No."
                ),
            )

    patients = get_hospital_patients(
        db=db,
        hospital_id=hospital_id,
        status=status,
        priority=priority,
        icu_required=icu_required,
    )

    return {
        "success": True,
        "hospital_id": hospital_id,
        "count": len(patients),
        "patients": [
            {
                "visit_id": visit.id,
                "patient_id": patient.patient_id,
                "name": patient.name,
                "age": patient.age,
                "gender": patient.gender,
                "disease": patient.disease,
                "priority": patient.priority,
                "icu_required": patient.icu_required,
                "status": visit.status,
                "admission_type": visit.admission_type,
                "admitted_at": visit.admitted_at,
                "treatment_started_at": visit.treatment_started_at,
                "completed_at": visit.completed_at,
            }
            for visit, patient in patients
        ],
    }


# ============================================================
# HOSPITAL DASHBOARD SUMMARY
# Must come before /{patient_id} to avoid path conflict
# ============================================================

@router.get("/hospital/{hospital_id}/summary")
def get_hospital_summary(
    hospital_id: str,
    db: Session = Depends(get_db),
):
    summary = get_hospital_patient_summary(
        db=db,
        hospital_id=hospital_id,
    )

    return {
        "success": True,
        "summary": summary,
    }


# ============================================================
# ADMIT EXISTING PATIENT
# ============================================================

@router.post("/{patient_id}/admit/{hospital_id}")
def admit_patient(
    patient_id: str,
    hospital_id: str,
    db: Session = Depends(get_db),
):
    patient = get_patient(
        db=db,
        patient_id=patient_id,
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found.",
        )
    hospital = get_hospital(
        db=db,
        hospital_id=hospital_id,
    )

    if hospital is None:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found.",
        )

    visit = create_hospital_visit(
        db=db,
        patient_id=patient_id,
        hospital_id=hospital_id,
        admission_type="DIRECT",
        status="NEW",
    )

    if visit is None:
        raise HTTPException(
            status_code=409,
            detail=(
                "Patient already has an active visit "
                "in this hospital."
            ),
        )

    return {
        "success": True,
        "message": "Patient admitted successfully.",
        "visit": {
            "visit_id": visit.id,
            "patient_id": visit.patient_id,
            "hospital_id": visit.hospital_id,
            "status": visit.status,
            "admission_type": visit.admission_type,
            "admitted_at": visit.admitted_at,
        },
    }


# ============================================================
# PATIENT DETAILS + COMPLETE VISIT HISTORY
# ============================================================

@router.get("/{patient_id}")
def get_patient_details(
    patient_id: str,
    db: Session = Depends(get_db),
):
    patient = get_patient(
        db=db,
        patient_id=patient_id,
    )

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found.",
        )

    visits = get_patient_visits(
        db=db,
        patient_id=patient_id,
    )

    return {
        "success": True,
        "patient": {
            "patient_id": patient.patient_id,
            "name": patient.name,
            "age": patient.age,
            "gender": patient.gender,
            "disease": patient.disease,
            "priority": patient.priority,
            "icu_required": patient.icu_required,
            "created_at": patient.created_at,
        },
        "visits": [
            {
                "visit_id": visit.id,
                "hospital_id": visit.hospital_id,
                "status": visit.status,
                "admission_type": visit.admission_type,
                "admitted_at": visit.admitted_at,
                "treatment_started_at": visit.treatment_started_at,
                "completed_at": visit.completed_at,
                "notes": visit.notes,
            }
            for visit in visits
        ],
    }


# ============================================================
# UPDATE PATIENT VISIT STATUS
# ============================================================

@router.patch("/visits/{visit_id}/status/{status}")
def update_patient_visit_status(
    visit_id: int,
    status: str,
    db: Session = Depends(get_db),
):
    allowed_statuses = [
        "NEW",
        "ACTIVE",
        "COMPLETED",
    ]

    status = status.upper()

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid status. Allowed values: "
                "NEW, ACTIVE, COMPLETED."
            ),
        )

    try:
        visit = update_visit_status(
            db=db,
            visit_id=visit_id,
            status=status,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    if visit is None:
        raise HTTPException(
            status_code=404,
            detail="Hospital visit not found.",
        )

    return {
        "success": True,
        "message": "Patient visit status updated successfully.",
        "visit": {
            "visit_id": visit.id,
            "patient_id": visit.patient_id,
            "hospital_id": visit.hospital_id,
            "status": visit.status,
            "admission_type": visit.admission_type,
            "admitted_at": visit.admitted_at,
            "treatment_started_at": visit.treatment_started_at,
            "completed_at": visit.completed_at,
        },
    }


# ============================================================
# UPDATE PATIENT VISIT NOTES
# ============================================================

@router.patch("/visits/{visit_id}/notes")
def update_patient_visit_notes(
    visit_id: int,
    notes: str,
    db: Session = Depends(get_db),
):
    if not notes.strip():
        raise HTTPException(
            status_code=400,
            detail="Notes cannot be empty.",
        )

    visit = update_visit_notes(
        db=db,
        visit_id=visit_id,
        notes=notes.strip(),
    )

    if visit is None:
        raise HTTPException(
            status_code=404,
            detail="Hospital visit not found.",
        )

    return {
        "success": True,
        "message": "Patient visit notes updated successfully.",
        "visit": {
            "visit_id": visit.id,
            "patient_id": visit.patient_id,
            "hospital_id": visit.hospital_id,
            "status": visit.status,
            "notes": visit.notes,
        },
    }