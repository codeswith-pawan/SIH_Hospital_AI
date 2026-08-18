# 🏥 AI-Powered Smart Hospital Referral System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-Frontend-000000?logo=next.js&logoColor=white)](https://nextjs.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

An end-to-end **AI-powered hospital referral and management system** that helps hospitals identify the most suitable destination hospital for patients who need to be transferred — combining machine learning, live bed/ICU availability, a rule-based recommendation engine, full referral lifecycle tracking, and role-based access control behind a modern web dashboard.

Built as a prototype for streamlining hospital-to-hospital referral workflows, reducing manual coordination overhead, and replacing ad-hoc phone/paper processes with a structured, data-driven system.

📌 *Originally developed for Smart India Hackathon (SIH).*

---

## 📖 Table of Contents

- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [How the Recommendation Engine Works](#-how-the-recommendation-engine-works)
- [Machine Learning Component](#-machine-learning-component)
- [Referral Lifecycle](#-referral-lifecycle)
- [Authentication & Authorization](#-authentication--authorization)
- [Bed & ICU Inventory Management](#-bed--icu-inventory-management)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Data](#-data)
- [Documentation](#-documentation)
- [Future Enhancements](#-future-enhancements)
- [Disclaimer](#️-disclaimer)
- [Author](#-author)

---

## 📌 Problem Statement

When a hospital cannot provide the required treatment or infrastructure for a patient, that patient needs to be referred elsewhere. In practice, this process is often slow and error-prone:

- Difficulty identifying the most suitable destination hospital
- Limited visibility into what other hospitals are actually equipped to handle
- Delays caused by manually phoning around to check bed and ICU availability
- No structured way to track a referral's progress
- Poor visibility into which stage a referral is currently at
- Risk of unauthorized access to sensitive referral information
- Difficulty coordinating referral acceptance and treatment updates across hospitals

This project addresses these problems with a centralized platform that pairs an intelligent hospital-recommendation engine with a controlled, auditable referral lifecycle.

---

## 🚀 Key Features

| Category | Highlights |
|---|---|
| **AI Recommendation** | ML-based referral success prediction, hospital ranking & scoring, fallback logic |
| **Live Capacity Tracking** | General bed availability, ICU availability, reservation management |
| **Matching Logic** | Specialty compatibility, required-test compatibility, distance-aware comparison |
| **Referral Management** | Full lifecycle tracking, timestamped timeline, status-based workflows |
| **Security** | JWT authentication, role-based access control, source/destination hospital authorization |
| **Dashboard** | Hospital-facing UI for referrals, inventory, and patient management |
| **Developer Experience** | Swagger/OpenAPI docs, automated test suite for core workflows |

---

## 🤖 How the Recommendation Engine Works

The engine evaluates candidate hospitals against the patient's needs and live infrastructure data before producing a ranked list of recommendations.

```text
Patient Information
        │
        ▼
Patient Requirement Analysis
        │
        ▼
Hospital Capability Filtering
        │
        ▼
Specialty Compatibility Check
        │
        ▼
Required Test Availability Check
        │
        ▼
Live Bed / ICU Capacity Check
        │
        ▼
ML-Based Referral Success Prediction
        │
        ▼
Hospital Scoring & Ranking
        │
        ▼
Recommended Hospitals
```

Each candidate hospital is scored using a weighted combination of factors:

```text
Specialty Match
        +
Test Match
        +
Bed Availability
        +
ICU Availability
        +
Distance Consideration
        +
Predicted Referral Success
        ↓
Final Hospital Score
```

If the top-ranked hospitals don't have sufficient live capacity, the system falls back to the next best matches rather than returning no result.

---

## 🧠 Machine Learning Component

The project includes an ML pipeline for referral outcome prediction and recommendation scoring.

**Pipeline stages:** data preprocessing → feature engineering → model training → referral success prediction → recommendation scoring

**Stack:** Python, Pandas, NumPy, scikit-learn, Joblib

| Item | Location |
|---|---|
| Trained model | `models/referral_success_model.joblib` |
| Training scripts | `src/training/` |
| Preprocessing | `src/preprocessing/` |

---

## 🚑 Referral Lifecycle

```text
PENDING → ACCEPTED → IN_TRANSIT → ARRIVED → TREATMENT_ACTIVE → COMPLETED
```

Additional terminal states: `REJECTED`, `TRANSFERRED`, `DIED`

Every referral stores lifecycle timestamps so the full timeline can be reconstructed:

`created_at` · `accepted_at` · `rejected_at` · `in_transit_at` · `arrived_at` · `treatment_started_at` · `completed_at` · `transferred_at` · `died_at` · `closed_at`

```text
Referral Created → Accepted → In Transit → Arrived → Treatment Started → Completed → Closed
```

---

## 🔐 Authentication & Authorization

Authentication is handled via **JWT tokens**:

```text
User Credentials → Login API → JWT Access Token → Protected API Request → Token Validation → Role & Hospital Authorization
```

### User Roles

| Role | Description |
|---|---|
| `HOSPITAL` | Hospital-level access |
| `STATE_ADMIN` | State-level administration |
| `CENTRAL_ADMIN` | Central-level administration |

### Referral Authorization Rules

Access to a referral is restricted to its authorized participants. Hospital users can only see referrals tied to their own hospital.

| Hospital Role | Can Update Status To |
|---|---|
| **Destination hospital** | `ACCEPTED`, `REJECTED`, `ARRIVED`, `TREATMENT_ACTIVE`, `COMPLETED`, `TRANSFERRED`, `DIED` |
| **Source hospital** | `IN_TRANSIT` |

Unauthorized hospitals attempting to act on a referral receive an access-denied response.

---

## 🛏 Bed & ICU Inventory Management

Tracks live infrastructure availability per hospital:

- Available general beds
- Available ICU beds
- Reserved general beds
- Reserved ICU beds

### Reservation System

Supports `GENERAL` and `ICU` bed reservations, with validation of hospital identity, patient identity, requested bed type, active reservation state, and bed-type consistency.

### Referral ↔ Reservation Integration

When a reservation is attached to a referral, the system validates that:

1. The referral exists
2. The reservation exists
3. The requesting hospital is authorized
4. The requested bed type matches the reservation
5. The reservation belongs to the correct hospital and patient

---

## 💻 Hospital Management Dashboard

Built with **Next.js, React, TypeScript, and Tailwind CSS**. Hospital users get:

- **Dashboard** — hospital info, hospital ID, system status, quick navigation
- **Referrals** — view/refresh referrals, patient & source hospital details, priority, status, reason, timeline, and authorized status actions
- **Bed Inventory** — general and ICU bed availability, reserved capacity
- **Patients** — patient details, admission info, and treatment-related information

---

## 🧩 System Architecture

```text
                    ┌─────────────────────┐
                    │    Next.js Frontend │
                    │  Hospital Dashboard │
                    └──────────┬──────────┘
                               │ REST API
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │  Auth · AuthZ       │
                    │  Referral APIs      │
                    │  Patient APIs       │
                    │  Inventory APIs     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                 ▼
     ┌────────────────┐ ┌──────────────┐ ┌─────────────────┐
     │ Recommendation │ │  Referral    │ │ Bed Reservation │
     │    Engine      │ │   Engine     │ │     Engine      │
     └───────┬────────┘ └──────┬───────┘ └────────┬────────┘
             │                 │                   │
             └─────────────────┼───────────────────┘
                                ▼
                    ┌─────────────────────┐
                    │   Data / ML Layer   │
                    │  SQLite · CSVs      │
                    │  ML Models          │
                    └─────────────────────┘
```

---

## 🛠 Tech Stack

| Layer | Technologies |
|---|---|
| **Backend** | Python, FastAPI, Uvicorn, JWT Auth, SQLite |
| **Machine Learning** | scikit-learn, Pandas, NumPy, Joblib |
| **Frontend** | Next.js, React, TypeScript, Tailwind CSS |
| **Testing** | Pytest, API/referral/recommendation/reservation/inventory test suites |

---

## 📁 Project Structure

```text
SIH_Hospital_AI/
│
├── src/
│   ├── api/                 # FastAPI routes & schemas
│   ├── auth/                 # JWT auth, authorization, dependencies
│   ├── database/              # DB models, services, seed scripts
│   ├── prediction/            # Recommendation, referral & reservation engines
│   ├── preprocessing/          # Feature engineering
│   ├── training/               # Model training scripts
│   ├── data_generation/        # Synthetic data generators
│   └── utils/                  # Rules, helpers, config
│
├── frontend/                  # Next.js dashboard (app, components, public)
├── datasets/final/            # hospitals.csv, patients.csv, referrals.csv
├── models/                    # Trained ML model (.joblib)
├── notebooks/                  # EDA & training notebooks
├── tests/                      # Pytest test suite
├── docs/                       # Data dictionary & medical assumptions
└── requirements.txt
```

---

## ⚙️ Getting Started

### Backend

```bash
# 1. Clone the repository
git clone https://github.com/codeswith-pawan/SIH_Hospital_AI.git
cd SIH_Hospital_AI

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the backend
uvicorn src.api.main:app --reload
```

- Backend: `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- App: `http://localhost:3000`

---

## 📚 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/login` | Authenticate and receive a JWT |
| `GET` | `/hospitals` | List hospitals |
| `POST` | `/referrals` | Create a referral |
| `GET` | `/referrals/{referral_id}` | Get referral details |
| `POST` | `/referrals/{referral_id}/status/{new_status}` | Update referral status |
| `POST` | `/referrals/{referral_id}/reservation` | Attach a bed reservation to a referral |
| `GET` | `/hospitals/{hospital_id}/referrals` | List referrals for a hospital |
| `GET` | `/hospitals/{hospital_id}/inventory` | Get hospital bed/ICU inventory |
| `GET` | `/patients/{patient_id}/referrals` | List referrals for a patient |
| `GET` | `/patients/hospital/{hospital_id}` | List patients for a hospital |

Full interactive documentation is available via Swagger UI at `/docs`.

---

## 🧪 Testing

Covers hospital recommendation, referral engine behavior, status rules, lifecycle transitions, safety checks, fallback logic (hospital/distance/ICU), reservation workflow and expiry, and inventory persistence.

```bash
pytest
```

Module-level tests also live under `src/prediction/`.

---

## 📊 Data

```text
datasets/final/hospitals.csv
datasets/final/patients.csv
datasets/final/referrals.csv
```

Synthetic data-generation modules are included for producing hospital, patient, and referral datasets.

---

## 📖 Documentation

- [`docs/data_dictionary.md`](docs/data_dictionary.md) — dataset field definitions
- [`docs/medical_assumptions.md`](docs/medical_assumptions.md) — project assumptions

---

## 🔮 Future Enhancements

- Real-time WebSocket notifications
- Production-grade user management & password hashing
- PostgreSQL deployment & Redis caching
- Docker containerization & cloud deployment
- SMS/email alerts and ambulance GPS tracking
- Advanced ML models & real-time hospital integration
- Analytics dashboards, admin portal, audit logging, API rate limiting

---

## ⚠️ Disclaimer

This project is an **academic and prototype implementation**. It is **not intended for real-world clinical decision-making** without medical validation, clinical expert review, security hardening, production infrastructure, regulatory compliance, and extensive real-world testing.

---

## 👨‍💻 Author

**Pawan Kumar Sharma**

- GitHub: [@codeswith-pawan](https://github.com/codeswith-pawan)
- Project Repository: [SIH_Hospital_AI](https://github.com/codeswith-pawan/SIH_Hospital_AI)

---

### ⭐ If you find this project useful, consider giving it a star on GitHub!
