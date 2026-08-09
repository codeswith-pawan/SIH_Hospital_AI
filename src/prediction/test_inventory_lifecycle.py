from datetime import datetime, timedelta

from src.prediction.bed_reservation import (
    initialize_hospital_beds,
    reserve_bed,
    release_bed,
    expire_reservation,
)

from src.prediction.reservation_store import (
    get_hospital_inventory,
    save_reservation,
)


HOSPITAL_ID = "GH_LIFECYCLE_TEST"
PATIENT_A = "PAT_LIFECYCLE_A"
PATIENT_B = "PAT_LIFECYCLE_B"


print("\n==============================")
print("INVENTORY LIFECYCLE TEST")
print("==============================")


# ============================================================
# INITIALIZE
# ============================================================

inventory = initialize_hospital_beds(
    hospital_id=HOSPITAL_ID,
    available_beds=10,
    available_icu_beds=1,
)

print("\nInitial:")
print(inventory)


# ============================================================
# RESERVE
# ============================================================

result_a = reserve_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_A,
    bed_type="ICU",
    inventory=inventory,
)

print("\nAfter Reservation:")
print(inventory)

disk_inventory = get_hospital_inventory(
    HOSPITAL_ID
)

print("\nDisk Inventory:")
print(disk_inventory)


if disk_inventory["available_icu_beds"] == 0:
    print(
        "PASS — Reservation persisted inventory."
    )
else:
    print(
        "FAIL — Reservation did not persist inventory."
    )


# ============================================================
# RELEASE
# ============================================================

release_result = release_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_A,
    inventory=inventory,
)

print("\nAfter Release:")
print(inventory)

disk_inventory = get_hospital_inventory(
    HOSPITAL_ID
)

print("\nDisk Inventory:")
print(disk_inventory)


if disk_inventory["available_icu_beds"] == 1:
    print(
        "PASS — Release persisted inventory."
    )
else:
    print(
        "FAIL — Release did not persist inventory."
    )


# ============================================================
# RESERVE AGAIN
# ============================================================

result_b = reserve_bed(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_B,
    bed_type="ICU",
    inventory=inventory,
)

print("\nPatient B Reservation:")
print(result_b)

print("\nInventory:")
print(inventory)


# ============================================================
# FORCE EXPIRY
# ============================================================

reservation_b = result_b[
    "reservation"
]

reservation_b[
    "reserved_at"
] = (
    datetime.now()
    - timedelta(minutes=20)
).isoformat()

save_reservation(
    reservation_b
)

print(
    "\nPatient B reservation "
    "artificially aged by 20 minutes."
)


# ============================================================
# EXPIRE
# ============================================================

expiry_result = expire_reservation(
    hospital_id=HOSPITAL_ID,
    patient_id=PATIENT_B,
    inventory=inventory,
)

print("\nExpiry Result:")
print(expiry_result)

print("\nAfter Expiry:")
print(inventory)

disk_inventory = get_hospital_inventory(
    HOSPITAL_ID
)

print("\nDisk Inventory:")
print(disk_inventory)


if disk_inventory["available_icu_beds"] == 1:
    print(
        "PASS — Expiry persisted inventory."
    )
else:
    print(
        "FAIL — Expiry did not persist inventory."
    )


print("\n==============================")
print("INVENTORY LIFECYCLE TEST COMPLETED")
print("==============================")