"""
Persistent Reservation Store
AI Powered Smart Hospital Referral System
"""

import json
import os
from threading import Lock


STORE_PATH = "data/reservations.json"

STORE_LOCK = Lock()


def ensure_store():
    """
    Create reservation storage if it does not exist.
    """

    directory = os.path.dirname(STORE_PATH)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    if not os.path.exists(STORE_PATH):

        with open(
            STORE_PATH,
            "w"
        ) as file:

            json.dump(
                {},
                file,
                indent=4
            )


def load_reservations():
    """
    Load all reservations from disk.
    """

    ensure_store()

    with STORE_LOCK:

        with open(
            STORE_PATH,
            "r"
        ) as file:

            return json.load(file)


def save_reservations(
    reservations
):
    """
    Save all reservations to disk.
    """

    ensure_store()

    with STORE_LOCK:

        temp_path = (
            STORE_PATH + ".tmp"
        )

        with open(
            temp_path,
            "w"
        ) as file:

            json.dump(
                reservations,
                file,
                indent=4
            )

        os.replace(
            temp_path,
            STORE_PATH
        )


def save_reservation(
    reservation
):
    """
    Save or update one reservation.
    """

    reservations = load_reservations()

    key = (
        reservation["hospital_id"]
        + "_"
        + reservation["patient_id"]
    )

    reservations[key] = reservation

    save_reservations(
        reservations
    )


def get_reservation(
    hospital_id,
    patient_id
):
    """
    Get one reservation.
    """

    reservations = load_reservations()

    key = (
        hospital_id
        + "_"
        + patient_id
    )

    return reservations.get(
        key
    )


def get_all_reservations():
    """
    Return all stored reservations.
    """

    return load_reservations()

# ============================================================
# Persistent Bed Inventory
# ============================================================

INVENTORY_PATH = "data/bed_inventory.json"


def ensure_inventory_store():
    """
    Create bed inventory storage if it does not exist.
    """

    directory = os.path.dirname(
        INVENTORY_PATH
    )

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    if not os.path.exists(
        INVENTORY_PATH
    ):

        with open(
            INVENTORY_PATH,
            "w"
        ) as file:

            json.dump(
                {},
                file,
                indent=4
            )


def load_bed_inventory():
    """
    Load all hospital bed inventories.
    """

    ensure_inventory_store()

    with STORE_LOCK:

        with open(
            INVENTORY_PATH,
            "r"
        ) as file:

            return json.load(file)


def save_bed_inventory(
    inventory_map
):
    """
    Persist all hospital bed inventories.
    """

    ensure_inventory_store()

    with STORE_LOCK:

        temp_path = (
            INVENTORY_PATH + ".tmp"
        )

        with open(
            temp_path,
            "w"
        ) as file:

            json.dump(
                inventory_map,
                file,
                indent=4
            )

        os.replace(
            temp_path,
            INVENTORY_PATH
        )


def save_hospital_inventory(
    inventory
):
    """
    Save or update one hospital inventory.
    """

    inventory_map = (
        load_bed_inventory()
    )

    hospital_id = inventory[
        "hospital_id"
    ]

    inventory_map[
        hospital_id
    ] = inventory

    save_bed_inventory(
        inventory_map
    )


def get_hospital_inventory(
    hospital_id
):
    """
    Get one hospital's persistent inventory.
    """

    inventory_map = (
        load_bed_inventory()
    )

    return inventory_map.get(
        hospital_id
    )


def clear_reservations():
    """
    Clear all stored reservations.

    Intended mainly for test setup/reset.
    """

    save_reservations({})