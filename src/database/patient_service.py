"""
Patient database operations.
"""
import pandas as pd
from sqlalchemy import case
from datetime import datetime
from src.database.models import Patient, HospitalVisit, Hospital

from sqlalchemy.orm import Session

from src.database.models import (
    Patient,
    HospitalVisit,
)


def create_or_get_patient(
    db: Session,
    patient_data: dict,
):
    """
    Create patient if not already present.
    Return existing patient otherwise.
    """

    patient_id = patient_data["patient_id"]

    patient = (
        db.query(Patient)
        .filter(Patient.patient_id == patient_id)
        .first()
    )

    if patient is not None:
        patient.name = (
            patient_data.get("name")
            if pd.notna(patient_data.get("name"))
            else patient.name
        )

        patient.age = (
            patient_data.get("age")
            if patient_data.get("age") is not None
            else patient.age
        )

        patient.gender = (
            patient_data.get("gender")
            if pd.notna(patient_data.get("gender"))
            else patient.gender
        )

        patient.disease = (
            patient_data.get("disease")
            if pd.notna(patient_data.get("disease"))
            else patient.disease
        )

        patient.priority = (
            patient_data.get("priority")
            if pd.notna(patient_data.get("priority"))
            else patient.priority
        )

        patient.icu_required = (
            patient_data.get("icu_required")
            if pd.notna(patient_data.get("icu_required"))
            else patient.icu_required
        )

        db.commit()
        db.refresh(patient)

        return patient, False
    else:
        patient = Patient(
            patient_id=patient_id,
            name=patient_data.get("name"),
            age=patient_data.get("age"),
            gender=patient_data.get("gender"),
            disease=patient_data.get("disease"),
            priority=patient_data.get("priority"),
            icu_required=patient_data.get("icu_required"),
        )

        db.add(patient)
        db.commit()
        db.refresh(patient)

        return patient, True


def create_hospital_visit(
    db: Session,
    patient_id: str,
    hospital_id: str,
    admission_type: str = "DIRECT",
    status: str = "NEW",
):
    """
    Create a new hospital visit for a patient.

    Returns None if the patient already has an
    active visit in the same hospital.
    """

    existing_visit = (
        db.query(HospitalVisit)
        .filter(
            HospitalVisit.patient_id == patient_id,
            HospitalVisit.hospital_id == hospital_id,
            HospitalVisit.status.in_(["NEW", "ACTIVE"]),
        )
        .first()
    )

    if existing_visit is not None:
        return None

    visit = HospitalVisit(
        patient_id=patient_id,
        hospital_id=hospital_id,
        admission_type=admission_type,
        status=status,
    )

    db.add(visit)
    db.commit()
    db.refresh(visit)

    return visit

def update_visit_status(
    db: Session,
    visit_id: int,
    status: str,
):
    """
    Update patient treatment status.
    """

    visit = (
        db.query(HospitalVisit)
        .filter(HospitalVisit.id == visit_id)
        .first()
    )

    if visit is None:
        return None

    allowed_transitions = {
        "NEW": ["ACTIVE"],
        "ACTIVE": ["COMPLETED"],
        "COMPLETED": [],
    }

    current_status = visit.status

    if status not in allowed_transitions.get(
        current_status,
        [],
    ):
        raise ValueError(
            f"Invalid status transition: "
            f"{current_status} -> {status}"
        )

    visit.status = status

    if status == "ACTIVE":
        visit.treatment_started_at = datetime.utcnow()

    elif status == "COMPLETED":
        visit.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(visit)

    return visit


def get_hospital_patients(
    db: Session,
    hospital_id: str,
    status: str | None = None,
    priority: str | None = None,
    icu_required: str | None = None,
):
    """
    Return all patients belonging to one hospital.
    """

    query = (
        db.query(HospitalVisit, Patient)
        .join(
            Patient,
            HospitalVisit.patient_id == Patient.patient_id,
        )
        .filter(
            HospitalVisit.hospital_id == hospital_id
        )
    )

    if status is not None:
        query = query.filter(
            HospitalVisit.status == status
        )

    if priority is not None:
        query = query.filter(
            Patient.priority == priority
        )

    if icu_required is not None:
        query = query.filter(
            Patient.icu_required == icu_required
        )

    return query.order_by(
        case(
            (Patient.priority == "Critical", 1),
            (Patient.priority == "Urgent", 2),
            (Patient.priority == "Stable", 3),
            else_=4,
        ),
        HospitalVisit.admitted_at.desc(),
    ).all()


def get_patient_visits(
    db: Session,
    patient_id: str,
):
    """
    Return complete hospital visit history.
    """

    return (
        db.query(HospitalVisit)
        .filter(
            HospitalVisit.patient_id == patient_id
        )
        .order_by(HospitalVisit.admitted_at.asc())
        .all()
    )


def get_patient(
    db: Session,
    patient_id: str,
):
    """
    Return one patient by patient ID.
    """

    return (
        db.query(Patient)
        .filter(Patient.patient_id == patient_id)
        .first()
    )


def get_hospital_patient_summary(
    db: Session,
    hospital_id: str,
):
    """
    Return patient summary for one hospital.
    """

    visits = (
        db.query(HospitalVisit)
        .filter(
            HospitalVisit.hospital_id == hospital_id
        )
        .all()
    )

    total = len(visits)

    new_count = sum(
        1
        for visit in visits
        if visit.status == "NEW"
    )

    active_count = sum(
        1
        for visit in visits
        if visit.status == "ACTIVE"
    )

    completed_count = sum(
        1
        for visit in visits
        if visit.status == "COMPLETED"
    )

    critical_count = sum(
        1
        for visit in visits
        if visit.patient.priority == "Critical"
    )

    icu_required_count = sum(
        1
        for visit in visits
        if visit.patient.icu_required == "Yes"
    )

    return {
        "hospital_id": hospital_id,
        "total_patients": total,
        "new_patients": new_count,
        "active_patients": active_count,
        "completed_patients": completed_count,
        "critical_patients": critical_count,
        "icu_required_patients": icu_required_count,
    }


def update_visit_notes(
    db: Session,
    visit_id: int,
    notes: str,
):
    visit = (
        db.query(HospitalVisit)
        .filter(HospitalVisit.id == visit_id)
        .first()
    )

    if visit is None:
        return None

    visit.notes = notes

    db.commit()
    db.refresh(visit)

    return visit

def get_hospital(
    db: Session,
    hospital_id: str,
):
    """
    Return hospital by hospital ID.
    """

    return (
        db.query(Hospital)
        .filter(Hospital.hospital_id == hospital_id)
        .first()
    )

def get_all_hospitals(
    db: Session,
):
    """
    Return all registered hospitals.
    """

    return (
        db.query(Hospital)
        .order_by(Hospital.hospital_id.asc())
        .all()
    )