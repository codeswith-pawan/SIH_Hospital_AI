"""
Hospital Recommendation Explanation
AI Powered Smart Hospital Referral System
"""


def generate_recommendation_reason(
    hospital,
    patient
):
    """
    Generate human-readable reasons for
    recommending a hospital.
    """

    reasons = []

    # -------------------------------
    # Distance
    # -------------------------------

    distance = hospital["distance_km"]

    if distance <= 10:
        reasons.append(
            f"Very close to patient ({distance} km)"
        )

    elif distance <= 50:
        reasons.append(
            f"Nearby hospital ({distance} km)"
        )

    else:
        reasons.append(
            f"Distance: {distance} km"
        )

    # -------------------------------
    # Beds
    # -------------------------------

    beds = hospital["available_beds"]

    reasons.append(
        f"{beds} beds available"
    )

    # -------------------------------
    # ICU
    # -------------------------------

    if patient["icu_required"] == "Yes":

        icu = hospital["available_icu_beds"]

        reasons.append(
            f"{icu} ICU beds available"
        )

    # -------------------------------
    # Emergency
    # -------------------------------

    if hospital["emergency_24x7"] == "Yes":
        reasons.append(
            "24x7 emergency service"
        )

    # -------------------------------
    # Ambulance
    # -------------------------------

    if hospital["ambulance"] == "Yes":
        reasons.append(
            "Ambulance available"
        )

    # -------------------------------
    # Oxygen
    # -------------------------------

    if hospital["oxygen_support"] == "Yes":
        reasons.append(
            "Oxygen support available"
        )

    return reasons


def generate_top_recommendations(
    ranked_hospitals,
    patient,
    top_n=5
):
    """
    Return top N hospitals with
    recommendation reasons.
    """

    if ranked_hospitals.empty:
        return []

    recommendations = []

    top_hospitals = ranked_hospitals.head(
        top_n
    )

    for _, hospital in top_hospitals.iterrows():

        reasons = generate_recommendation_reason(
            hospital,
            patient
        )

        recommendations.append({

            "rank": int(
                hospital["rank"]
            ),

            "hospital_id": hospital[
                "hospital_id"
            ],

            "hospital_name": hospital[
                "hospital_name"
            ],

            "distance_km": hospital[
                "distance_km"
            ],

            "hospital_score": hospital[
                "hospital_score"
            ],

            "reasons": reasons
        })

    return recommendations