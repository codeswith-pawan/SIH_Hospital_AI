"""
Database models for the hospital patient management system.
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import relationship

from src.database.database import Base


class Hospital(Base):
    """
    Master hospital record.
    """

    __tablename__ = "hospitals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    hospital_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    name = Column(
        String,
        nullable=False,
    )

    state = Column(
        String,
        nullable=True,
    )

    district = Column(
        String,
        nullable=True,
    )

    city = Column(
        String,
        nullable=True,
    )

    latitude = Column(
        String,
        nullable=True,
    )

    longitude = Column(
        String,
        nullable=True,
    )

    total_beds = Column(
        Integer,
        nullable=True,
    )

    occupied_beds = Column(
        Integer,
        nullable=True,
    )

    available_beds = Column(
        Integer,
        nullable=True,
    )

    icu_beds = Column(
        Integer,
        nullable=True,
    )

    available_icu_beds = Column(
        Integer,
        nullable=True,
    )

    emergency_beds = Column(
        Integer,
        nullable=True,
    )

    available_emergency_beds = Column(
        Integer,
        nullable=True,
    )

    emergency_24x7 = Column(
        String,
        nullable=True,
    )

    accepts_referral = Column(
        String,
        nullable=True,
    )

    ambulance = Column(
        String,
        nullable=True,
    )

    oxygen_support = Column(
        String,
        nullable=True,
    )

    ventilator = Column(
        String,
        nullable=True,
    )

    blood_bank = Column(
        String,
        nullable=True,
    )

    cardiology = Column(
        String,
        nullable=True,
    )

    neurology = Column(
        String,
        nullable=True,
    )

    nephrology = Column(
        String,
        nullable=True,
    )

    pulmonology = Column(
        String,
        nullable=True,
    )

    orthopedics = Column(
        String,
        nullable=True,
    )

    general_medicine = Column(
        String,
        nullable=True,
    )

    general_surgery = Column(
        String,
        nullable=True,
    )

    trauma_unit = Column(
        String,
        nullable=True,
    )

    burn_unit = Column(
        String,
        nullable=True,
    )

    ct_scan = Column(
        String,
        nullable=True,
    )

    mri = Column(
        String,
        nullable=True,
    )

    xray = Column(
        String,
        nullable=True,
    )

    ultrasound = Column(
        String,
        nullable=True,
    )

    ecg = Column(
        String,
        nullable=True,
    )

    dialysis = Column(
        String,
        nullable=True,
    )

    blood_test = Column(
        String,
        nullable=True,
    )

    cbc = Column(
        String,
        nullable=True,
    )

    troponin_test = Column(
        String,
        nullable=True,
    )

    dengue_ns1_test = Column(
        String,
        nullable=True,
    )

    malaria_test = Column(
        String,
        nullable=True,
    )

    blood_glucose_test = Column(
        String,
        nullable=True,
    )

    hba1c_test = Column(
        String,
        nullable=True,
    )

    kidney_function_test = Column(
        String,
        nullable=True,
    )

    pulmonary_function_test = Column(
        String,
        nullable=True,
    )

    blood_culture = Column(
        String,
        nullable=True,
    )

    lactate_test = Column(
        String,
        nullable=True,
    )

    stool_test = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )


class Patient(Base):
    """
    Master patient record.

    One patient can have multiple hospital visits.
    """

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    patient_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)

    disease = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    icu_required = Column(String, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    visits = relationship(
        "HospitalVisit",
        back_populates="patient",
        cascade="all, delete-orphan",
    )


class HospitalVisit(Base):
    """
    Tracks one patient's treatment at one hospital.
    """

    __tablename__ = "hospital_visits"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    patient_id = Column(
        String,
        ForeignKey("patients.patient_id"),
        nullable=False,
        index=True,
    )

    hospital_id = Column(
        String,
        nullable=False,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        default="NEW",
    )

    admission_type = Column(
        String,
        nullable=False,
        default="DIRECT",
    )

    admitted_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    treatment_started_at = Column(
        DateTime,
        nullable=True,
    )

    completed_at = Column(
        DateTime,
        nullable=True,
    )

    notes = Column(
        Text,
        nullable=True,
    )

    patient = relationship(
        "Patient",
        back_populates="visits",
    )


class Referral(Base):
    """
    Tracks referral between hospitals.
    """

    __tablename__ = "referrals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    referral_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    patient_id = Column(
        String,
        ForeignKey("patients.patient_id"),
        nullable=False,
        index=True,
    )

    from_hospital_id = Column(
        String,
        nullable=False,
        index=True,
    )

    to_hospital_id = Column(
        String,
        nullable=False,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        default="PENDING_ARRIVAL",
    )

    reason = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    arrived_at = Column(
        DateTime,
        nullable=True,
    )

    completed_at = Column(
        DateTime,
        nullable=True,
    )