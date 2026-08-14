"use client";

import { useEffect, useState } from "react";

type User = {
  user_id: string;
  username: string;
  name: string;
  role: string;
  hospital_id?: string | null;
  state?: string | null;
  district?: string | null;
};

type Inventory = {
  hospital_id: string;
  available_beds: number;
  available_icu_beds: number;
  reserved_beds: number;
  reserved_icu_beds: number;
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
  hospital_id: string;
  total_referrals: number;
  referrals: Referral[];
};


type PatientResponse = {
  success: boolean;
  hospital_id: string;
  count: number;
  patients: Patient[];
};


type HospitalDashboardProps = {
  user: User;
};

type Patient = {
  visit_id: number;
  patient_id: string;
  name: string;
  age: number;
  gender: string;
  disease: string;
  priority: string;
  icu_required: string;
  status: string;
  admission_type: string;
  admitted_at: string;
  treatment_started_at?: string | null;
  completed_at?: string | null;
};

export default function HospitalDashboard({
  user,
}: HospitalDashboardProps) {
  const [activeTab, setActiveTab] = useState("dashboard");

  const [inventory, setInventory] =
    useState<Inventory | null>(null);
  const [inventoryLoading, setInventoryLoading] = useState(false);
  const [inventoryError, setInventoryError] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [referrals, setReferrals] = useState<Referral[]>([]);
  const [referralLoading, setReferralLoading] = useState(false);
  const [referralError, setReferralError] = useState("");
  const [selectedReferral, setSelectedReferral] =
    useState<Referral | null>(null);
  const [statusLoading, setStatusLoading] = useState(false);

  const [patients, setPatients] = useState<Patient[]>([]);
  const [patientLoading, setPatientLoading] = useState(false);
  const [patientError, setPatientError] = useState("");

  useEffect(() => {
    if (!user.hospital_id) {
      setLoading(false);
      return;
    }

    const loadInitialInventory = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          `http://127.0.0.1:8000/hospitals/${user.hospital_id}/inventory`
        );

        if (!response.ok) {
          throw new Error(
            "Hospital inventory load nahi ho paayi."
          );
        }

        const result = await response.json();

        if (!result.success) {
          throw new Error(
            "Inventory data unavailable."
          );
        }

        setInventory(result.inventory);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load inventory."
        );
      } finally {
        setLoading(false);
      }
    };

    loadInitialInventory();
  }, [user.hospital_id]);

  const loadInventory = async () => {
    if (!user.hospital_id) return;

    setInventoryLoading(true);
    setInventoryError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/hospitals/${user.hospital_id}/inventory`
      );

      if (!response.ok) {
        throw new Error("Failed to load hospital inventory");
      }

      const result = await response.json();

      if (!result.success) {
        throw new Error("Inventory unavailable");
      }

      setInventory(result.inventory);
    } catch (err) {
      setInventoryError(
        err instanceof Error
          ? err.message
          : "Failed to load inventory"
      );
    } finally {
      setInventoryLoading(false);
    }
  };

  const loadReferrals = async () => {
    if (!user.hospital_id) return;

    setReferralLoading(true);
    setReferralError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/hospitals/${user.hospital_id}/referrals`
      );

      if (!response.ok) {
        throw new Error("Failed to load referrals.");
      }

      const result: ReferralResponse =
        await response.json();

      if (!result.success) {
        throw new Error("Referral data unavailable.");
      }

      setReferrals(result.referrals || []);
    } catch (err) {
      setReferralError(
        err instanceof Error
          ? err.message
          : "Failed to load referrals."
      );
    } finally {
      setReferralLoading(false);
    }
  };
  const loadPatients = async () => {
  if (!user.hospital_id) return;

  setPatientLoading(true);
  setPatientError("");

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/patients/hospital/${user.hospital_id}`
    );

    if (!response.ok) {
      throw new Error("Failed to load patients.");
    }

    const result: PatientResponse =
      await response.json();

    if (!result.success) {
      throw new Error("Patient data unavailable.");
    }

    setPatients(result.patients || []);
  } catch (err) {
    setPatientError(
      err instanceof Error
        ? err.message
        : "Failed to load patients."
    );
  } finally {
    setPatientLoading(false);
  }
};

  const updateReferralStatus = async (
    referralId: string,
    newStatus: string
  ) => {
    setStatusLoading(true);
    setReferralError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/referrals/${referralId}/status/${newStatus}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (!response.ok || !result.success) {
        throw new Error(
          result.detail?.message ||
            result.message ||
            "Status update failed."
        );
      }

      await loadReferrals();

      if (selectedReferral?.referral_id === referralId) {
        setSelectedReferral(result.referral);
      }
    } catch (err) {
      setReferralError(
        err instanceof Error
          ? err.message
          : "Status update failed."
      );
    } finally {
      setStatusLoading(false);
    }
  };

  useEffect(() => {

  if (!user.hospital_id) return;

  if (activeTab === "referrals") {
    loadReferrals();
  }

  if (activeTab === "patients") {
    loadPatients();
  }

}, [activeTab, user.hospital_id]);

  return (
    <main className="min-h-screen bg-slate-950 text-white">

      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div>
            <h1 className="text-xl font-bold">
              🏥 Hospital Referral AI
            </h1>

            <p className="mt-1 text-sm text-slate-400">
              {user.name}
            </p>
          </div>

          <div className="text-right">
            <p className="text-sm font-semibold">
              {user.hospital_id || "N/A"}
            </p>

            <p className="text-xs text-emerald-400">
              ● Online
            </p>
          </div>

        </div>
      </header>

      {/* Navigation */}
      <nav className="border-b border-slate-800 bg-slate-900">
        <div className="mx-auto flex max-w-7xl gap-2 px-6 py-3">

          {[
            ["dashboard", "Dashboard"],
            ["referrals", "Referrals"],
            ["inventory", "Bed Inventory"],
            ["patients", "Patients"],
          ].map(([id, label]) => (

            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${
                activeTab === id
                  ? "bg-blue-600 text-white"
                  : "text-slate-400 hover:bg-slate-800 hover:text-white"
              }`}
            >
              {label}
            </button>

          ))}

        </div>
      </nav>

      {/* Content */}
      <div className="mx-auto max-w-7xl px-6 py-8">

        {activeTab === "dashboard" && (
          <>

            <div className="flex flex-col justify-between gap-3 md:flex-row md:items-center">

              <div>
                <h2 className="text-2xl font-bold">
                  Hospital Dashboard
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                  Real-time hospital operations overview.
                </p>
              </div>

              <div className="rounded-lg border border-emerald-500/20 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400">
                ● Live Inventory
              </div>

            </div>

            {/* Error */}
            {error && (
              <div className="mt-6 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
                {error}
              </div>
            )}

            {/* Stats */}
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

              <StatCard
                title="Available Beds"
                value={
                  loading
                    ? "..."
                    : String(
                        inventory?.available_beds ?? 0
                      )
                }
                subtitle="General beds"
              />

              <StatCard
                title="Available ICU"
                value={
                  loading
                    ? "..."
                    : String(
                        inventory?.available_icu_beds ?? 0
                      )
                }
                subtitle="ICU beds"
              />

              <StatCard
                title="Reserved Beds"
                value={
                  loading
                    ? "..."
                    : String(
                        inventory?.reserved_beds ?? 0
                      )
                }
                subtitle="Currently reserved"
              />

              <StatCard
                title="Reserved ICU"
                value={
                  loading
                    ? "..."
                    : String(
                        inventory?.reserved_icu_beds ?? 0
                      )
                }
                subtitle="Currently reserved"
              />

            </div>

            {/* Inventory Overview */}
            <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">

              <h3 className="text-lg font-semibold">
                Bed Inventory Overview
              </h3>

              <div className="mt-5 grid gap-4 md:grid-cols-2">

                <InventoryCard
                  title="General Beds"
                  available={
                    inventory?.available_beds ?? 0
                  }
                  reserved={
                    inventory?.reserved_beds ?? 0
                  }
                />

                <InventoryCard
                  title="ICU Beds"
                  available={
                    inventory?.available_icu_beds ?? 0
                  }
                  reserved={
                    inventory?.reserved_icu_beds ?? 0
                  }
                />

              </div>

            </div>

            {/* Hospital Information */}
            <div className="mt-8 rounded-2xl border border-slate-800 bg-slate-900 p-6">

              <h3 className="text-lg font-semibold">
                Hospital Information
              </h3>

              <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

                <InfoItem
                  label="Hospital ID"
                  value={
                    user.hospital_id || "N/A"
                  }
                />

                <InfoItem
                  label="State"
                  value={
                    user.state || "N/A"
                  }
                />

                <InfoItem
                  label="District"
                  value={
                    user.district || "N/A"
                  }
                />

                <InfoItem
                  label="Role"
                  value={user.role}
                />

              </div>

            </div>

          </>
        )}

        {activeTab === "referrals" && (
          <div>
            <div className="flex flex-col justify-between gap-3 md:flex-row md:items-center">
              <div>
                <h2 className="text-2xl font-bold">
                  Incoming Referrals
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                  Manage patients referred to your hospital.
                </p>
              </div>

              <button
                onClick={loadReferrals}
                disabled={referralLoading}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold hover:bg-blue-500 disabled:opacity-50"
              >
                {referralLoading ? "Refreshing..." : "Refresh Referrals"}
              </button>
            </div>

            {referralError && (
              <div className="mt-5 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
                {referralError}
              </div>
            )}

            {!referralLoading && referrals.length === 0 && (
              <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center">
                <p className="text-slate-400">
                  No incoming referrals found.
                </p>
              </div>
            )}

            <div className="mt-6 space-y-4">
              {referrals.map((referral) => (
                <div
                  key={referral.referral_id}
                  className="rounded-2xl border border-slate-800 bg-slate-900 p-6"
                >
                  <div className="flex flex-col justify-between gap-4 lg:flex-row">
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="rounded-full bg-blue-500/10 px-3 py-1 text-xs font-semibold text-blue-400">
                          {referral.referral_id}
                        </span>

                        <span className="rounded-full bg-red-500/10 px-3 py-1 text-xs font-semibold text-red-400">
                          {referral.priority}
                        </span>

                        <span className="rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-400">
                          {referral.status}
                        </span>
                      </div>

                      <h3 className="mt-3 text-lg font-bold">
                        Patient {referral.patient_id}
                      </h3>

                      <p className="mt-1 text-sm text-slate-400">
                        From Hospital: {referral.from_hospital_id}
                      </p>

                      <p className="mt-1 text-sm text-slate-400">
                        Reason: {referral.reason}
                      </p>
                    </div>

                    <div className="text-left lg:text-right">
                      <p className="text-xs text-slate-500">
                        Bed Required
                      </p>

                      <p className="mt-1 font-semibold">
                        {referral.bed_type || "Not specified"}
                      </p>
                    </div>
                  </div>
                  <div className="mt-5 flex flex-wrap gap-3">

  {referral.status === "PENDING" && (
    <>
      <button
        onClick={() =>
          updateReferralStatus(
            referral.referral_id,
            "ACCEPTED"
          )
        }
        disabled={statusLoading}
        className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold hover:bg-emerald-500 disabled:opacity-50"
      >
        {statusLoading ? "Processing..." : "Accept Referral"}
      </button>

      <button
        onClick={() =>
          updateReferralStatus(
            referral.referral_id,
            "REJECTED"
          )
        }
        disabled={statusLoading}
        className="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold hover:bg-red-500 disabled:opacity-50"
      >
        Reject
      </button>
    </>
  )}

  {referral.status === "ACCEPTED" && (
    <button
      onClick={() =>
        updateReferralStatus(
          referral.referral_id,
          "IN_TRANSIT"
        )
      }
      disabled={statusLoading}
      className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold hover:bg-blue-500 disabled:opacity-50"
    >
      {statusLoading ? "Processing..." : "Mark In Transit"}
    </button>
  )}

  {referral.status === "IN_TRANSIT" && (
    <button
      onClick={() =>
        updateReferralStatus(
          referral.referral_id,
          "ARRIVED"
        )
      }
      disabled={statusLoading}
      className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold hover:bg-indigo-500 disabled:opacity-50"
    >
      {statusLoading ? "Processing..." : "Mark Arrived"}
    </button>
  )}

  {referral.status === "ARRIVED" && (
    <button
      onClick={() =>
        updateReferralStatus(
          referral.referral_id,
          "TREATMENT_ACTIVE"
        )
      }
      disabled={statusLoading}
      className="rounded-lg bg-purple-600 px-4 py-2 text-sm font-semibold hover:bg-purple-500 disabled:opacity-50"
    >
      {statusLoading ? "Processing..." : "Start Treatment"}
    </button>
  )}

  {referral.status === "TREATMENT_ACTIVE" && (
    <button
      onClick={() =>
        updateReferralStatus(
          referral.referral_id,
          "COMPLETED"
        )
      }
      disabled={statusLoading}
      className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold hover:bg-emerald-500 disabled:opacity-50"
    >
      {statusLoading ? "Processing..." : "Complete Treatment"}
    </button>
  )}

  <button
    onClick={() =>
      setSelectedReferral(
        selectedReferral?.referral_id === referral.referral_id
          ? null
          : referral
      )
    }
    className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-300 hover:bg-slate-800"
  >
    {selectedReferral?.referral_id === referral.referral_id
      ? "Hide Timeline"
      : "View Timeline"}
  </button>

</div>

                  {selectedReferral?.referral_id ===
                    referral.referral_id && (
                    <ReferralTimeline referral={referral} />
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === "inventory" && (
          <div>
            <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
              <div>
                <h2 className="text-2xl font-bold">
                  Bed & ICU Inventory
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                  Live hospital bed availability.
                </p>
              </div>

              <button
                onClick={loadInventory}
                disabled={inventoryLoading}
                className="rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-semibold hover:bg-blue-500 disabled:opacity-50"
              >
                {inventoryLoading ? "Refreshing..." : "Refresh Inventory"}
              </button>
            </div>

            {inventoryError && (
              <div className="mt-5 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
                {inventoryError}
              </div>
            )}

            {!inventory && !inventoryLoading && !inventoryError && (
              <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center">
                <p className="text-slate-400">
                  Click &quot;Refresh Inventory&quot; to load live inventory.
                </p>
              </div>
            )}

            {inventory && (
              <>
                <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  <InventoryCard
                    title="Available Beds"
                    available={inventory.available_beds}
                    reserved={inventory.reserved_beds}
                  />

                  <InventoryCard
                    title="Available ICU"
                    available={inventory.available_icu_beds}
                    reserved={inventory.reserved_icu_beds}
                  />

                  <StatCard
                    title="Reserved Beds"
                    value={String(inventory.reserved_beds)}
                    subtitle="Currently reserved"
                  />

                  <StatCard
                    title="Reserved ICU"
                    value={String(inventory.reserved_icu_beds)}
                    subtitle="Currently reserved"
                  />
                </div>

                <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-6">
                  <h3 className="text-lg font-semibold">
                    Inventory Summary
                  </h3>

                  <div className="mt-4 grid gap-4 sm:grid-cols-2">
                    <InfoItem
                      label="Hospital ID"
                      value={inventory.hospital_id}
                    />

                    <InfoItem
                      label="Total Available Capacity"
                      value={String(
                        inventory.available_beds +
                          inventory.available_icu_beds
                      )}
                    />
                  </div>
                </div>
              </>
            )}
          </div>
        )}

                {activeTab === "patients" && (
          <section>

            <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">

              <div>
                <h2 className="text-2xl font-bold">
                  Patient Management
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                  View and manage patients currently associated with this hospital.
                </p>
              </div>

              <button
                onClick={loadPatients}
                disabled={patientLoading}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {patientLoading
                  ? "Loading..."
                  : "Refresh Patients"}
              </button>

            </div>

            {patientError && (
              <div className="mt-6 rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-400">
                {patientError}
              </div>
            )}

            {patientLoading && patients.length === 0 && (
              <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6 text-slate-400">
                Loading patients...
              </div>
            )}

            {!patientLoading &&
              !patientError &&
              patients.length === 0 && (
                <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900 p-6 text-slate-400">
                  No patients found for this hospital.
                </div>
              )}

            {patients.length > 0 && (
              <div className="mt-6 grid gap-4 lg:grid-cols-2">

                {patients.map((patient) => (

                  <div
                    key={patient.visit_id}
                    className="rounded-2xl border border-slate-800 bg-slate-900 p-5"
                  >

                    <div className="flex items-start justify-between gap-4">

                      <div>
                        <p className="text-lg font-bold">
                          {patient.name}
                        </p>

                        <p className="mt-1 text-sm text-slate-400">
                          {patient.patient_id}
                        </p>
                      </div>

                      <span className="rounded-full bg-slate-800 px-3 py-1 text-xs font-semibold text-slate-300">
                        {patient.status}
                      </span>

                    </div>

                    <div className="mt-5 grid grid-cols-2 gap-4 text-sm">

                      <div>
                        <p className="text-slate-500">
                          Age / Gender
                        </p>

                        <p className="mt-1 font-semibold">
                          {patient.age} / {patient.gender}
                        </p>
                      </div>

                      <div>
                        <p className="text-slate-500">
                          Priority
                        </p>

                        <p className="mt-1 font-semibold">
                          {patient.priority}
                        </p>
                      </div>

                      <div>
                        <p className="text-slate-500">
                          Disease
                        </p>

                        <p className="mt-1 font-semibold">
                          {patient.disease}
                        </p>
                      </div>

                      <div>
                        <p className="text-slate-500">
                          ICU Required
                        </p>

                        <p className="mt-1 font-semibold">
                          {patient.icu_required}
                        </p>
                      </div>

                      <div>
                        <p className="text-slate-500">
                          Admission Type
                        </p>

                        <p className="mt-1 font-semibold">
                          {patient.admission_type}
                        </p>
                      </div>

                      <div>
                        <p className="text-slate-500">
                          Admitted
                        </p>

                        <p className="mt-1 font-semibold">
                          {new Date(
                            patient.admitted_at
                          ).toLocaleString()}
                        </p>
                      </div>

                    </div>

                  </div>

                ))}

              </div>
            )}

          </section>
        )}

      </div>

    </main>
  );
}

function StatCard({
  title,
  value,
  subtitle,
}: {
  title: string;
  value: string;
  subtitle: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

      <p className="text-sm text-slate-400">
        {title}
      </p>

      <p className="mt-2 text-3xl font-bold">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-500">
        {subtitle}
      </p>

    </div>
  );
}

function InventoryCard({
  title,
  available,
  reserved,
}: {
  title: string;
  available: number;
  reserved: number;
}) {
  const total = available + reserved;

  const occupancy =
    total > 0
      ? Math.round((reserved / total) * 100)
      : 0;

  return (
    <div className="rounded-xl bg-slate-950 p-5">

      <div className="flex items-center justify-between">

        <p className="font-semibold">
          {title}
        </p>

        <span className="text-sm text-slate-400">
          {occupancy}% reserved
        </span>

      </div>

      <div className="mt-4 h-3 overflow-hidden rounded-full bg-slate-800">

        <div
          className="h-full rounded-full bg-blue-500 transition-all"
          style={{
            width: `${occupancy}%`,
          }}
        />

      </div>

      <div className="mt-4 grid grid-cols-2 gap-3">

        <div>
          <p className="text-xs text-slate-500">
            Available
          </p>

          <p className="mt-1 text-xl font-bold text-emerald-400">
            {available}
          </p>
        </div>

        <div>
          <p className="text-xs text-slate-500">
            Reserved
          </p>

          <p className="mt-1 text-xl font-bold">
            {reserved}
          </p>
        </div>

      </div>

    </div>
  );
}

function ReferralTimeline({
  referral,
}: {
  referral: Referral;
}) {
  const events = [
    ["Referral Created", referral.created_at],
    ["Accepted", referral.accepted_at],
    ["In Transit", referral.in_transit_at],
    ["Arrived", referral.arrived_at],
    ["Treatment Started", referral.treatment_started_at],
    ["Completed", referral.completed_at],
    ["Closed", referral.closed_at],
  ];

  return (
    <div className="mt-6 rounded-xl border border-slate-800 bg-slate-950 p-5">
      <h4 className="text-lg font-semibold">
        Referral Timeline
      </h4>

      <div className="mt-5 space-y-4">
        {events.map(([label, timestamp]) => (
          <div
            key={label}
            className="flex items-start gap-3"
          >
            <div
              className={`mt-1 h-3 w-3 rounded-full ${
                timestamp
                  ? "bg-emerald-400"
                  : "bg-slate-700"
              }`}
            />

            <div>
              <p
                className={`text-sm font-semibold ${
                  timestamp
                    ? "text-white"
                    : "text-slate-600"
                }`}
              >
                {label}
              </p>

              {timestamp && (
                <p className="mt-1 text-xs text-slate-500">
                  {new Date(
                    timestamp
                  ).toLocaleString("en-IN")}
                </p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function InfoItem({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl bg-slate-950 p-4">

      <p className="text-xs text-slate-500">
        {label}
      </p>

      <p className="mt-1 font-semibold">
        {value}
      </p>

    </div>
  );
}

function Placeholder({
  title,
  text,
}: {
  title: string;
  text: string;
}) {
  return (
    <div>

      <h2 className="text-2xl font-bold">
        {title}
      </h2>

      <div className="mt-6 rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center">

        <p className="text-slate-400">
          {text}
        </p>

      </div>

    </div>
  );
}