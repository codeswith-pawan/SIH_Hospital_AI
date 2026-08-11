import os
from datetime import datetime, timedelta, timezone

import jwt


SECRET_KEY = os.getenv(
    "SIH_JWT_SECRET",
    "sih-hospital-ai-demo-secret-change-later"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(user):
    now = datetime.now(timezone.utc)

    payload = {
        "sub": user["user_id"],
        "username": user["username"],
        "role": user["role"],
        "hospital_id": user.get("hospital_id"),
        "state": user.get("state"),
        "district": user.get("district"),
        "iat": now,
        "exp": now + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_access_token(token):
    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None