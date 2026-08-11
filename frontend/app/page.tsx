"use client";

import { useState } from "react";
import HospitalDashboard from "@/components/HospitalDashboard";

type User = {
  user_id: string;
  username: string;
  name: string;
  role: string;
  hospital_id?: string | null;
  state?: string | null;
  district?: string | null;
};

type Hospital = {
  hospital_id: string;
  hospital_name: string;
  state: string;
  district: string;
  city: string;
  distance_km: number;
  available_beds: number;
  available_icu_beds: number;
  success_probability: number;
  final_score: number;
  recommendation_type: string;
  rank: number;
  specialty_match: number;
  test_match: number;
  bed_match: number;
  icu_match: number;
};

type ApiResponse = {
  success: boolean;
  patient_id: string;
  priority: string;
  total_hospitals: number;
  hospitals: Hospital[];
};

type Referral = {
  referral_id: string;
  patient_id: string;
  from_hospital_id: string;
  to_hospital_id: string;
  reason: string;
  priority: string;
  status: string;
  created_at: string;
  accepted_at?: string | null;
  rejected_at?: string | null;
  in_transit_at?: string | null;
  arrived_at?: string | null;
  treatment_started_at?: string | null;
  completed_at?: string | null;
  transferred_at?: string | null;
  died_at?: string | null;
  closed_at?: string | null;
  reservation_hospital_id?: string;
  bed_type?: string;
  reservation_release_status?: string;
};

type ReferralResponse = {
  success: boolean;
  referral: Referral;
};

type ReferralHistoryResponse = {
  success: boolean;
  patient_id: string;
  total_referrals: number;
  referrals: Referral[];
};

export default function Home() {
  const [user, setUser] = useState<User | null>(null);

  const [loginUsername, setLoginUsername] = useState("gh00046");
  const [loginPassword, setLoginPassword] = useState("hospital123");
  const [loginLoading, setLoginLoading] = useState(false);
  const [loginError, setLoginError] = useState("");

  const login = async () => {
    setLoginLoading(true);
    setLoginError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: loginUsername,
            password: loginPassword,
          }),
        }
      );

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(
          result.detail ||
            result.message ||
            "Login failed."
        );
      }

      setUser(result.user);
    } catch (err) {
      setLoginError(
        err instanceof Error
          ? err.message
          : "Login failed."
      );
    } finally {
      setLoginLoading(false);
    }
  };

  const [patientId, setPatientId] = useState("PAT000002");
  const [data, setData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [reservationLoading, setReservationLoading] = useState(false);
  const [reservationHospitalId, setReservationHospitalId] =
    useState<string | null>(null);
  const [reservation, setReservation] = useState<any>(null);
  const [reservationError, setReservationError] = useState("");

  const [referrals, setReferrals] = useState<Referral[]>([]);
  const [referralLoading, setReferralLoading] = useState(false);
  const [referralError, setReferralError] = useState("");
  const [selectedReferral, setSelectedReferral] =
    useState<Referral | null>(null);

  const findHospitals = async () => {
    setLoading(true);
    setError("");
    setData(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/hospitals?patient_id=${patientId}`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch hospital data");
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(
        "Backend API se connection nahi ho pa raha. Check karo Terminal 1 mein Uvicorn server running hai."
      );
    } finally {
      setLoading(false);
    }
  };

  const reserveHospital = async (hospitalId: string) => {
    setReservationHospitalId(hospitalId);
    setReservationLoading(true);
    setReservationError("");
    setReservation(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/referral", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          patient_id: patientId,
          hospital_id: hospitalId,
        }),
      });

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(result.message || "Hospital reservation failed");
      }

      setReservation(result);
    } catch (err) {
      setReservationError(
        err instanceof Error ? err.message : "Reservation failed"
      );
    } finally {
      setReservationLoading(false);
    }
  };

  const loadReferralHistory = async () => {
    if (!patientId.trim()) return;

    setReferralLoading(true);
    setReferralError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/patients/${patientId}/referrals`
      );

      if (!response.ok) {
        throw new Error("Failed to fetch referral history");
      }

      const result: ReferralHistoryResponse = await response.json();

      if (!result.success) {
        throw new Error("Referral history unavailable");
      }

      setReferrals(result.referrals || []);
    } catch (err) {
      setReferralError(
        err instanceof Error
          ? err.message
          : "Failed to load referral history"
      );
    } finally {
      setReferralLoading(false);
    }
  };

  if (user) {
    if (user.role === "HOSPITAL") {
      return (
        <HospitalDashboard user={user} />
      );
    }

    return (
      <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center">
          <h1 className="text-2xl font-bold">
            Dashboard
          </h1>

          <p className="mt-2 text-slate-400">
            {user.role} dashboard is not configured yet.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      {/* Login */}
      <section className="mx-auto max-w-md px-6 pt-16">

        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">

          <div className="text-center">
            <div className="text-5xl">
              🏥
            </div>

            <h2 className="mt-4 text-2xl font-bold">
              Hospital Referral AI
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Hospital Staff Login
            </p>
          </div>

          <div className="mt-6 space-y-4">

            <div>
              <label className="mb-2 block text-sm text-slate-400">
                Username
              </label>

              <input
                type="text"
                value={loginUsername}
                onChange={(e) =>
                  setLoginUsername(e.target.value)
                }
                className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-blue-500"
                placeholder="Hospital username"
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-400">
                Password
              </label>

              <input
                type="password"
                value={loginPassword}
                onChange={(e) =>
                  setLoginPassword(e.target.value)
                }
                className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 outline-none focus:border-blue-500"
                placeholder="Password"
              />
            </div>

            {loginError && (
              <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-400">
                {loginError}
              </div>
            )}

            <button
              onClick={login}
              disabled={loginLoading}
              className="w-full rounded-xl bg-blue-600 px-5 py-3 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loginLoading
                ? "Signing in..."
                : "Sign In"}
            </button>

          </div>

          <div className="mt-5 rounded-xl bg-slate-950 p-4 text-xs text-slate-500">
            Demo hospital: <span className="text-slate-300">gh00046</span>
          </div>

        </div>

      </section>

      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900 mt-12">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold">🏥 Hospital Referral AI</h1>
            <p className="mt-1 text-sm text-slate-400">
              Intelligent Hospital Recommendation & Bed Reservation System
            </p>
          </div>

          <div className="rounded-full bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400">
            ● API Connected
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-8">
        {/* Patient Search */}
        <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">
          <div className="mb-5">
            <h2 className="text-xl font-semibold">Find Suitable Hospitals</h2>
            <p className="mt-1 text-sm text-slate-400">
              Enter a patient ID to get AI-ranked hospital recommendations.
            </p>
          </div>

          <div className="flex flex-col gap-4 sm:flex-row">
            <input
              type="text"
              value={patientId}
              onChange={(e) => setPatientId(e.target.value)}
              placeholder="Enter Patient ID"
              className="flex-1 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none transition focus:border-blue-500"
            />

            <button
              onClick={findHospitals}
              disabled={loading}
              className="rounded-xl bg-blue-600 px-7 py-3 font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Finding..." : "Find Hospitals"}
            </button>
          </div>

          {error && (
            <div className="mt-4 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
              {error}
            </div>
          )}
        </section>

        {/* Patient Summary */}
        {data && (
          <section className="mt-6 grid gap-4 sm:grid-cols-3">
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <p className="text-sm text-slate-400">Patient ID</p>
              <p className="mt-2 text-xl font-bold">{data.patient_id}</p>
            </div>

            <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-5">
              <p className="text-sm text-slate-400">Priority</p>
              <p className="mt-2 text-xl font-bold text-red-400">
                {data.priority}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">
              <p className="text-sm text-slate-400">Eligible Hospitals</p>
              <p className="mt-2 text-xl font-bold">{data.total_hospitals}</p>
            </div>
          </section>
        )}

        {/* Hospital Results */}
        {data && (
          <section className="mt-8">
            <div className="mb-5">
              <h2 className="text-2xl font-bold">Hospital Recommendations</h2>
              <p className="mt-1 text-sm text-slate-400">
                Hospitals ranked using clinical rules, available resources,
                distance and ML prediction.
              </p>
            </div>

            <div className="space-y-5">
              {data.hospitals.map((hospital) => (
                <div
                  key={hospital.hospital_id}
                  className="rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-lg"
                >
                  {/* Hospital Header */}
                  <div className="flex flex-col justify-between gap-4 md:flex-row">
                    <div>
                      <div className="mb-2 flex items-center gap-3">
                        <span className="rounded-full bg-blue-500/10 px-3 py-1 text-sm font-semibold text-blue-400">
                          Rank #{hospital.rank}
                        </span>

                        {hospital.rank === 1 && (
                          <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-sm font-semibold text-emerald-400">
                            Recommended
                          </span>
                        )}
                      </div>

                      <h3 className="text-xl font-bold">
                        {hospital.hospital_name}
                      </h3>

                      <p className="mt-1 text-sm text-slate-400">
                        {hospital.city}, {hospital.district}, {hospital.state}
                      </p>
                    </div>

                    <div className="text-left md:text-right">
                      <p className="text-sm text-slate-400">Final Score</p>
                      <p className="text-3xl font-bold text-blue-400">
                        {hospital.final_score}
                      </p>
                    </div>
                  </div>

                  {/* Stats */}
                  <div className="mt-6 grid grid-cols-2 gap-3 md:grid-cols-4">
                    <div className="rounded-xl bg-slate-950 p-4">
                      <p className="text-xs text-slate-500">Distance</p>
                      <p className="mt-1 font-semibold">
                        {hospital.distance_km} km
                      </p>
                    </div>

                    <div className="rounded-xl bg-slate-950 p-4">
                      <p className="text-xs text-slate-500">Available Beds</p>
                      <p className="mt-1 font-semibold">
                        {hospital.available_beds}
                      </p>
                    </div>

                    <div className="rounded-xl bg-slate-950 p-4">
                      <p className="text-xs text-slate-500">Available ICU</p>
                      <p className="mt-1 font-semibold text-emerald-400">
                        {hospital.available_icu_beds}
                      </p>
                    </div>

                    <div className="rounded-xl bg-slate-950 p-4">
                      <p className="text-xs text-slate-500">ML Probability</p>
                      <p className="mt-1 font-semibold">
                        {(hospital.success_probability * 100).toFixed(2)}%
                      </p>
                    </div>
                  </div>

                  {/* Matching */}
                  <div className="mt-5">
                    <p className="mb-3 text-sm font-semibold text-slate-300">
                      Capability Match
                    </p>

                    <div className="flex flex-wrap gap-2">
                      <MatchBadge
                        label="Specialty"
                        value={hospital.specialty_match}
                      />
                      <MatchBadge label="Tests" value={hospital.test_match} />
                      <MatchBadge label="Beds" value={hospital.bed_match} />
                      <MatchBadge label="ICU" value={hospital.icu_match} />
                    </div>
                  </div>

                  <div className="mt-5 border-t border-slate-800 pt-4">
                    <span className="text-sm text-slate-400">
                      Recommendation Type:{" "}
                    </span>

                    <span className="text-sm font-semibold text-blue-400">
                      {hospital.recommendation_type}
                    </span>
                  </div>

                  <div className="mt-5 flex justify-end">
                    <button
                      onClick={() => reserveHospital(hospital.hospital_id)}
                      disabled={
                        (reservationLoading &&
                          reservationHospitalId === hospital.hospital_id) ||
                        hospital.available_icu_beds <= 0
                      }
                      className="rounded-xl bg-emerald-600 px-6 py-3 font-semibold transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      {reservationLoading &&
                      reservationHospitalId === hospital.hospital_id
                        ? "Reserving..."
                        : hospital.available_icu_beds <= 0
                        ? "ICU Unavailable"
                        : "Reserve ICU Bed"}
                    </button>
                  </div>

                  {/* In-Card Reservation Result */}
                  {reservationHospitalId === hospital.hospital_id && reservation && (
                    <div className="mt-5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
                      <p className="font-semibold text-emerald-400">
                        ✓ ICU Bed Reserved Successfully
                      </p>

                      <div className="mt-3 grid gap-2 text-sm">
                        <p>
                          <span className="text-slate-400">Patient: </span>
                          {reservation.reservation?.patient_id}
                        </p>

                        <p>
                          <span className="text-slate-400">Bed: </span>
                          {reservation.reservation?.bed_type}
                        </p>

                        <p>
                          <span className="text-slate-400">Status: </span>
                          <span className="font-semibold text-emerald-400">
                            {reservation.reservation?.status}
                          </span>
                        </p>
                      </div>
                    </div>
                  )}

                  {/* In-Card Reservation Error */}
                  {reservationHospitalId === hospital.hospital_id && reservationError && (
                    <div className="mt-5 rounded-xl border border-red-500/30 bg-red-500/10 p-4">
                      <p className="font-semibold text-red-400">
                        Reservation Failed
                      </p>
                      <p className="mt-1 text-sm text-red-300">
                        {reservationError}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Referral History */}
        <section className="mt-8">
          <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-2xl font-bold">
                Patient Referral History
              </h2>

              <p className="mt-1 text-sm text-slate-400">
                Track the patient's complete hospital referral journey.
              </p>
            </div>

            <button
              onClick={loadReferralHistory}
              disabled={referralLoading}
              className="rounded-xl border border-slate-700 bg-slate-900 px-5 py-3 text-sm font-semibold transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {referralLoading ? "Loading..." : "Load Referral History"}
            </button>
          </div>

          {referralError && (
            <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
              {referralError}
            </div>
          )}

          {referrals.length > 0 && (
            <div className="space-y-4">
              {referrals.map((referral) => (
                <div
                  key={referral.referral_id}
                  className="rounded-2xl border border-slate-800 bg-slate-900 p-5"
                >
                  <div className="flex flex-col justify-between gap-4 md:flex-row">
                    <div>
                      <p className="text-xs text-slate-500">Referral ID</p>

                      <p className="font-semibold text-blue-400">
                        {referral.referral_id}
                      </p>
                    </div>

                    <span
                      className={`rounded-full px-3 py-1 text-xs font-semibold ${
                        referral.status === "COMPLETED"
                          ? "bg-emerald-500/10 text-emerald-400"
                          : referral.status === "DIED"
                          ? "bg-red-500/10 text-red-400"
                          : "bg-blue-500/10 text-blue-400"
                      }`}
                    >
                      {referral.status}
                    </span>
                  </div>

                  <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                    <div className="rounded-xl bg-slate-950 p-4">
                      <p className="text-xs text-slate-500">From Hospital</p>
                      <p className="mt-1 font-semibold">
                        {referral.from_hospital_id}
                      </p>
                    </div>

                    <div className="rounded-xl bg-slate-950 p-4">
                      <p className="text-xs text-slate-500">To Hospital</p>
                      <p className="mt-1 font-semibold">
                        {referral.to_hospital_id}
                      </p>
                    </div>

                    <div className="rounded-xl bg-slate-950 p-4">
                      <p className="text-xs text-slate-500">Priority</p>
                      <p className="mt-1 font-semibold">
                        {referral.priority}
                      </p>
                    </div>

                    <div className="rounded-xl bg-slate-950 p-4">
                      <p className="text-xs text-slate-500">Bed</p>
                      <p className="mt-1 font-semibold">
                        {referral.bed_type || "N/A"}
                      </p>
                    </div>
                  </div>

                  <div className="mt-4">
                    <p className="text-xs text-slate-500">Reason</p>

                    <p className="mt-1 text-sm text-slate-300">
                      {referral.reason}
                    </p>
                  </div>

                  <div className="mt-5">
                    <button
                      onClick={() =>
                        setSelectedReferral(
                          selectedReferral?.referral_id ===
                            referral.referral_id
                            ? null
                            : referral
                        )
                      }
                      className="rounded-xl border border-slate-700 px-4 py-2 text-sm font-semibold hover:bg-slate-800"
                    >
                      {selectedReferral?.referral_id === referral.referral_id
                        ? "Hide Timeline"
                        : "View Timeline"}
                    </button>
                  </div>

                  {selectedReferral?.referral_id === referral.referral_id && (
                    <ReferralTimeline referral={referral} />
                  )}
                </div>
              ))}
            </div>
          )}

          {!referralLoading &&
            referrals.length === 0 &&
            !referralError && (
              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-slate-400">
                No referral history loaded.
              </div>
            )}
        </section>

        {/* Initial State */}
        {!data && !loading && !error && (
          <div className="mt-12 text-center">
            <div className="text-6xl">🏥</div>

            <h2 className="mt-5 text-2xl font-bold">
              Intelligent Hospital Referral
            </h2>

            <p className="mx-auto mt-2 max-w-xl text-slate-400">
              Enter a patient ID above to find the most suitable hospitals
              based on clinical requirements, ICU availability, distance,
              hospital capabilities and ML prediction.
            </p>
          </div>
        )}
      </div>
    </main>
  );
}

function MatchBadge({ label, value }: { label: string; value: number }) {
  const matched = value === 1;

  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-semibold ${
        matched
          ? "bg-emerald-500/10 text-emerald-400"
          : "bg-red-500/10 text-red-400"
      }`}
    >
      {matched ? "✓" : "✕"} {label}
    </span>
  );
}

function ReferralTimeline({ referral }: { referral: Referral }) {
  const events = [
    {
      label: "Referral Created",
      time: referral.created_at,
    },
    {
      label: "Accepted",
      time: referral.accepted_at,
    },
    {
      label: "In Transit",
      time: referral.in_transit_at,
    },
    {
      label: "Arrived",
      time: referral.arrived_at,
    },
    {
      label: "Treatment Started",
      time: referral.treatment_started_at,
    },
    {
      label: "Completed",
      time: referral.completed_at,
    },
    {
      label: "Transferred",
      time: referral.transferred_at,
    },
    {
      label: "Died",
      time: referral.died_at,
    },
    {
      label: "Closed",
      time: referral.closed_at,
    },
  ];

  const activeEvents = events.filter((event) => event.time);

  return (
    <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-950 p-5">
      <h3 className="text-lg font-bold">Referral Timeline</h3>

      <div className="mt-5 space-y-5">
        {activeEvents.map((event, index) => (
          <div key={`${event.label}-${event.time}`} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div className="h-3 w-3 rounded-full bg-emerald-400" />

              {index !== activeEvents.length - 1 && (
                <div className="mt-1 h-full w-px bg-slate-700" />
              )}
            </div>

            <div className="pb-3">
              <p className="font-semibold">{event.label}</p>

              <p className="mt-1 text-xs text-slate-500">
                {formatDateTime(event.time!)}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function formatDateTime(value: string) {
  return new Date(value).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "medium",
  });
}