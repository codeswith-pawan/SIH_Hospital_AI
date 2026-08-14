"""
Import hospitals from CSV into the database.
"""

import pandas as pd

from src.database.database import SessionLocal
from src.database.models import Hospital


HOSPITALS_PATH = "datasets/final/hospitals.csv"


def update_hospital_from_row(
    hospital,
    row,
):
    hospital.name = row["hospital_name"]
    hospital.state = row["state"]
    hospital.district = row["district"]

    hospital.city = row.get("city")

    hospital.latitude = row.get("latitude")
    hospital.longitude = row.get("longitude")

    hospital.total_beds = row.get("total_beds")
    hospital.occupied_beds = row.get("occupied_beds")
    hospital.available_beds = row.get("available_beds")

    hospital.icu_beds = row.get("icu_beds")
    hospital.available_icu_beds = row.get(
        "available_icu_beds"
    )

    hospital.emergency_beds = row.get("emergency_beds")
    hospital.available_emergency_beds = row.get(
        "available_emergency_beds"
    )

    hospital.emergency_24x7 = row.get("emergency_24x7")
    hospital.accepts_referral = row.get("accepts_referral")

    hospital.ambulance = row.get("ambulance")
    hospital.oxygen_support = row.get("oxygen_support")
    hospital.ventilator = row.get("ventilator")
    hospital.blood_bank = row.get("blood_bank")

    hospital.cardiology = row.get("cardiology")
    hospital.neurology = row.get("neurology")
    hospital.nephrology = row.get("nephrology")
    hospital.pulmonology = row.get("pulmonology")
    hospital.orthopedics = row.get("orthopedics")

    hospital.general_medicine = row.get(
        "general_medicine"
    )
    hospital.general_surgery = row.get(
        "general_surgery"
    )

    hospital.trauma_unit = row.get("trauma_unit")
    hospital.burn_unit = row.get("burn_unit")

    hospital.ct_scan = row.get("ct_scan")
    hospital.mri = row.get("mri")
    hospital.xray = row.get("xray")
    hospital.ultrasound = row.get("ultrasound")
    hospital.ecg = row.get("ecg")

    hospital.dialysis = row.get("dialysis")

    hospital.blood_test = row.get("blood_test")
    hospital.cbc = row.get("cbc")
    hospital.troponin_test = row.get("troponin_test")
    hospital.dengue_ns1_test = row.get(
        "dengue_ns1_test"
    )
    hospital.malaria_test = row.get("malaria_test")
    hospital.blood_glucose_test = row.get(
        "blood_glucose_test"
    )
    hospital.hba1c_test = row.get("hba1c_test")
    hospital.kidney_function_test = row.get(
        "kidney_function_test"
    )
    hospital.pulmonary_function_test = row.get(
        "pulmonary_function_test"
    )
    hospital.blood_culture = row.get("blood_culture")
    hospital.lactate_test = row.get("lactate_test")
    hospital.stool_test = row.get("stool_test")


def main():
    df = pd.read_csv(HOSPITALS_PATH)

    db = SessionLocal()

    try:
        created_count = 0
        updated_count = 0

        for _, row in df.iterrows():
            hospital = (
                db.query(Hospital)
                .filter(
                    Hospital.hospital_id == row["hospital_id"]
                )
                .first()
            )

            if hospital is None:
                hospital = Hospital(
                    hospital_id=row["hospital_id"],
                    name=row["hospital_name"],
                )

                db.add(hospital)
                created_count += 1
            else:
                updated_count += 1

            update_hospital_from_row(
                hospital,
                row,
            )

        db.commit()

        print("Hospital import completed.")
        print("Created:", created_count)
        print("Updated:", updated_count)

    finally:
        db.close()


if __name__ == "__main__":
    main()