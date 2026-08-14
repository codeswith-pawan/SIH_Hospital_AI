"""
Add missing columns to the hospitals table.
"""

from sqlalchemy import inspect, text

from src.database.database import engine


NEW_COLUMNS = {
    "city": "VARCHAR",
    "latitude": "VARCHAR",
    "longitude": "VARCHAR",
    "total_beds": "INTEGER",
    "occupied_beds": "INTEGER",
    "available_beds": "INTEGER",
    "icu_beds": "INTEGER",
    "available_icu_beds": "INTEGER",
    "emergency_beds": "INTEGER",
    "available_emergency_beds": "INTEGER",
    "emergency_24x7": "VARCHAR",
    "accepts_referral": "VARCHAR",
    "ambulance": "VARCHAR",
    "oxygen_support": "VARCHAR",
    "ventilator": "VARCHAR",
    "blood_bank": "VARCHAR",
    "cardiology": "VARCHAR",
    "neurology": "VARCHAR",
    "nephrology": "VARCHAR",
    "pulmonology": "VARCHAR",
    "orthopedics": "VARCHAR",
    "general_medicine": "VARCHAR",
    "general_surgery": "VARCHAR",
    "trauma_unit": "VARCHAR",
    "burn_unit": "VARCHAR",
    "ct_scan": "VARCHAR",
    "mri": "VARCHAR",
    "xray": "VARCHAR",
    "ultrasound": "VARCHAR",
    "ecg": "VARCHAR",
    "dialysis": "VARCHAR",
    "blood_test": "VARCHAR",
    "cbc": "VARCHAR",
    "troponin_test": "VARCHAR",
    "dengue_ns1_test": "VARCHAR",
    "malaria_test": "VARCHAR",
    "blood_glucose_test": "VARCHAR",
    "hba1c_test": "VARCHAR",
    "kidney_function_test": "VARCHAR",
    "pulmonary_function_test": "VARCHAR",
    "blood_culture": "VARCHAR",
    "lactate_test": "VARCHAR",
    "stool_test": "VARCHAR",
}


def main():
    inspector = inspect(engine)

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("hospitals")
    }

    added_count = 0
    skipped_count = 0

    with engine.begin() as connection:

        for column_name, column_type in NEW_COLUMNS.items():

            if column_name in existing_columns:
                print(f"Already exists: {column_name}")
                skipped_count += 1
                continue

            connection.execute(
                text(
                    f"""
                    ALTER TABLE hospitals
                    ADD COLUMN {column_name} {column_type}
                    """
                )
            )

            print(f"Added: {column_name}")
            added_count += 1

    print()
    print("Hospital migration completed.")
    print("Columns added:", added_count)
    print("Already existed:", skipped_count)


if __name__ == "__main__":
    main()