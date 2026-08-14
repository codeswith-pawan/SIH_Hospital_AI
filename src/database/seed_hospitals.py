"""
Import hospitals from CSV into the database.
"""

import pandas as pd

from src.database.database import SessionLocal
from src.database.models import Hospital


HOSPITALS_PATH = "datasets/final/hospitals.csv"


def main():
    df = pd.read_csv(HOSPITALS_PATH)

    db = SessionLocal()

    try:
        created_count = 0
        existing_count = 0

        for _, row in df.iterrows():

            hospital_id = row["hospital_id"]

            hospital = (
                db.query(Hospital)
                .filter(
                    Hospital.hospital_id == hospital_id
                )
                .first()
            )

            if hospital is not None:
                existing_count += 1
                continue

            hospital = Hospital(
                hospital_id=hospital_id,
                name=row["hospital_name"],
                state=row.get("state"),
                district=row.get("district"),
            )

            db.add(hospital)
            created_count += 1

        db.commit()

        print("Hospital import completed.")
        print("Created:", created_count)
        print("Already existed:", existing_count)

    finally:
        db.close()


if __name__ == "__main__":
    main()