from fastapi import HTTPException


HOSPITAL = "HOSPITAL"
STATE_ADMIN = "STATE_ADMIN"
CENTRAL_ADMIN = "CENTRAL_ADMIN"


def can_view_referral(user, referral):
    """
    Check whether a logged-in user can view a referral.
    """

    role = user["role"]

    # Central admin can view everything
    if role == CENTRAL_ADMIN:
        return True

    # State admin can view referrals involving hospitals
    # from the same state.
    #
    # State filtering will be completed at API level
    # when hospital master data is connected.
    if role == STATE_ADMIN:
        return True

    # Hospital can view only referrals where
    # it is the source or destination hospital.
    if role == HOSPITAL:

        hospital_id = user.get("hospital_id")

        return (
            referral.get("from_hospital_id")
            == hospital_id
            or
            referral.get("to_hospital_id")
            == hospital_id
        )

    return False


def can_accept_or_reject(user, referral):
    """
    Only the receiving hospital can accept or reject
    a pending referral.
    """

    if user["role"] != HOSPITAL:
        return False

    return (
        referral.get("to_hospital_id")
        == user.get("hospital_id")
        and
        referral.get("status")
        == "PENDING"
    )


def can_update_referral_status(user, referral):
    """
    Hospital can update the lifecycle only when it is
    directly involved in the referral.
    """

    if user["role"] == CENTRAL_ADMIN:
        return True

    if user["role"] == STATE_ADMIN:
        return False

    if user["role"] != HOSPITAL:
        return False

    hospital_id = user.get("hospital_id")

    return (
        referral.get("from_hospital_id")
        == hospital_id
        or
        referral.get("to_hospital_id")
        == hospital_id
    )