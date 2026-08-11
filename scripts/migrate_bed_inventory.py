import json

INVENTORY_PATH = "data/bed_inventory.json"


def migrate():

    with open(INVENTORY_PATH, "r") as file:
        inventory_map = json.load(file)

    migrated = 0

    for hospital_id, inventory in inventory_map.items():

        # Already migrated
        if "beds" in inventory:
            continue

        available_beds = int(
            inventory.get("available_beds", 0)
        )

        available_icu_beds = int(
            inventory.get("available_icu_beds", 0)
        )

        reserved_beds = int(
            inventory.get("reserved_beds", 0)
        )

        reserved_icu_beds = int(
            inventory.get("reserved_icu_beds", 0)
        )

        beds = {}

        # GENERAL BEDS
        total_general = (
            available_beds + reserved_beds
        )

        for number in range(
            1,
            total_general + 1
        ):

            bed_id = f"GENERAL-{number:03d}"

            if number <= reserved_beds:
                beds[bed_id] = "RESERVED"
            else:
                beds[bed_id] = "AVAILABLE"

        # ICU BEDS
        total_icu = (
            available_icu_beds + reserved_icu_beds
        )

        for number in range(
            1,
            total_icu + 1
        ):

            bed_id = f"ICU-{number:03d}"

            if number <= reserved_icu_beds:
                beds[bed_id] = "RESERVED"
            else:
                beds[bed_id] = "AVAILABLE"

        inventory["beds"] = beds

        migrated += 1

    # Backup
    backup_path = (
        INVENTORY_PATH + ".backup"
    )

    with open(
        backup_path,
        "w"
    ) as file:

        json.dump(
            inventory_map,
            file,
            indent=4
        )

    # Save migrated data
    with open(
        INVENTORY_PATH,
        "w"
    ) as file:

        json.dump(
            inventory_map,
            file,
            indent=4
        )

    print(
        f"Migration completed: {migrated} hospitals"
    )

    print(
        f"Backup created: {backup_path}"
    )


if __name__ == "__main__":
    migrate()