import json
from pathlib import Path
from datetime import datetime

STORE_PATH = Path("data/runtime/users.json")


def _load_users():
    if not STORE_PATH.exists():
        return []

    try:
        with open(STORE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def _save_users(users):
    STORE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(STORE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            users,
            file,
            indent=2,
            ensure_ascii=False
        )


def seed_default_users():
    users = _load_users()

    if users:
        return users

    default_users = [
        {
            "user_id": "USR000001",
            "username": "gh00046",
            "password": "hospital123",
            "name": "Regional Amritsar Medical College Hospital",
            "role": "HOSPITAL",
            "hospital_id": "GH00046",
            "state": "Punjab",
            "district": "Amritsar",
            "created_at": datetime.now().isoformat(),
        },
        {
            "user_id": "USR000002",
            "username": "gh00119",
            "password": "hospital123",
            "name": "District Amritsar Medical College Hospital",
            "role": "HOSPITAL",
            "hospital_id": "GH00119",
            "state": "Punjab",
            "district": "Amritsar",
            "created_at": datetime.now().isoformat(),
        },
        {
            "user_id": "USR000003",
            "username": "punjab_admin",
            "password": "admin123",
            "name": "Punjab State Health Administration",
            "role": "STATE_ADMIN",
            "hospital_id": None,
            "state": "Punjab",
            "district": None,
            "created_at": datetime.now().isoformat(),
        },
        {
            "user_id": "USR000004",
            "username": "central_admin",
            "password": "central123",
            "name": "National Hospital Referral Administration",
            "role": "CENTRAL_ADMIN",
            "hospital_id": None,
            "state": None,
            "district": None,
            "created_at": datetime.now().isoformat(),
        },
        {
            "user_id": "USR000005",
            "username": "gh_test_other",
            "password": "hospital123",
            "name": "Test Other Hospital",
            "role": "HOSPITAL",
            "hospital_id": "GH_TEST_OTHER",
            "state": "Punjab",
            "district": "Ludhiana",
            "created_at": datetime.now().isoformat(),
        },
    ]

    _save_users(default_users)

    return default_users


def authenticate_user(username, password):
    users = seed_default_users()

    for user in users:
        if (
            user["username"] == username
            and user["password"] == password
        ):
            return user

    return None


def get_user_by_id(user_id):
    users = seed_default_users()

    for user in users:
        if user["user_id"] == user_id:
            return user

    return None