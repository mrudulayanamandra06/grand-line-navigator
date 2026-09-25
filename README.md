# Grand Line Navigator ☠️

A One Piece command deck and voyage planning application connecting a Streamlit frontend to a modular Flask REST API backend with SQLite persistence.

---

## Architecture

```text
grand-line-navigator/
├── frontend/
│   ├── app.py                     # Streamlit frontend (100% visual parity preserved)
│   └── api_client.py              # Modular API client with session pooling and timeouts
├── backend/
│   ├── __init__.py                # Flask application factory (create_app)
│   ├── app.py                     # Flask executable entrypoint
│   ├── config.py                  # Configurations (Dev, Testing, Prod, SQLite URIs)
│   ├── models.py                  # SQLAlchemy models (UserProfile, FavoriteFruit, etc.)
│   ├── routes/
│   │   ├── __init__.py            # Standard JSON error response helper
│   │   ├── catalog.py             # Public One Piece catalogs & catch-up calculator
│   │   ├── favorites.py           # Devil fruit favorites CRUD
│   │   ├── quiz.py                # Trivia questions (redacted), submissions, leaderboard
│   │   ├── bounty.py              # Bounty calculations, milestone claims & resets
│   │   ├── crew.py                # Crew manifest & training stats persistence
│   │   └── battle.py              # Deterministic faction battle simulation & history
│   └── services/
│       ├── calculations.py        # Authoritative business logic & deterministic formulas
│       └── seed_data.py           # One Piece catalogs (arcs, fruits, bounties, units)
├── tests/
│   ├── conftest.py                # Pytest fixtures with in-memory SQLite database
│   ├── test_health.py             # Health check & catalog verification
│   ├── test_favorites.py          # Favorites persistence & duplicate protection
│   ├── test_quiz.py               # Scoring, question answer redaction, leaderboard
│   ├── test_bounty.py             # Bounty calculations & milestone claims
│   ├── test_crew.py               # Server-side validation rules & crew persistence
│   └── test_battle.py             # Deterministic battle logic & tie-breaking rules
├── instance/
│   └── grand_line.db              # SQLite development database (auto-created)
├── requirements.txt               # Pinned Python package dependencies
├── .env.example                   # Environment variable template
├── .gitignore                     # Git ignore rules for virtualenv, DBs, and cache
└── README.md                      # Documentation and run instructions
```

---

## Installation & Setup

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- Pip

### 2. Environment Setup

#### On Linux / macOS:
```bash
# Clone or navigate to the repository
cd grand-line-navigator

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

#### On Windows (PowerShell):
```powershell
# Navigate to the repository
Set-Location -Path "C:\Users\Mrudula\.gemini\antigravity\scratch\grand-line-navigator"

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment file
Copy-Item .env.example .env
```

---

## Environment Variables

Copy `.env.example` to `.env`. The default settings work out-of-the-box for local development:

```env
FLASK_ENV=development
FLASK_APP=backend.app
BACKEND_URL=http://127.0.0.1:5000
DATABASE_URL=sqlite:///grand_line.db
DEFAULT_USER_ID=local-user
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
```

---

## Running the Application

The application requires two active terminal windows: one for the Flask backend and one for the Streamlit frontend.

### Terminal 1: Start the Flask Backend

#### Linux / macOS:
```bash
source .venv/bin/activate
flask --app backend.app run --port 5000
```

#### Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
python -m backend.app
# OR
flask --app backend.app run --port 5000
```
Backend will be available at: `http://127.0.0.1:5000`

### Terminal 2: Start the Streamlit Frontend

#### Linux / macOS:
```bash
source .venv/bin/activate
streamlit run frontend/app.py --server.port 8501
```

#### Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
streamlit run frontend/app.py --server.port 8501
```
Frontend will be available at: `http://localhost:8501`

---

## REST API Endpoints

All responses and errors adhere to JSON formatting. Errors follow the structure:
```json
{
  "error": {
    "code": "validation_error",
    "message": "Readable explanation"
  }
}
```

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check (`{"status": "ok"}`) |
| `GET` | `/api/arcs` | List of One Piece story arcs and highlights |
| `GET` | `/api/characters` | Wanted characters, bounties, and roles |
| `GET` | `/api/devil-fruits` | Complete Devil Fruit encyclopedia catalog |
| `GET` | `/api/devil-fruit-types` | Fruit classifications, awakenings, and details |
| `GET` | `/api/crew-members` | Canonical crew members and roles |
| `GET` | `/api/factions` | Pirate and Marine faction combat units |
| `POST` | `/api/catch-up/calculate` | Calculates days, completion date, and progress |
| `GET` | `/api/users/<user_id>/favorites` | Retrieves user's saved Devil Fruit favorites |
| `POST` | `/api/users/<user_id>/favorites` | Adds fruit to favorites (duplicate protected) |
| `DELETE` | `/api/users/<user_id>/favorites/<fruit>`| Removes fruit from favorites |
| `GET` | `/api/quiz/questions` | Question bank with correct answers redacted |
| `POST` | `/api/quiz/submit` | Authoritatively scores quiz and saves attempt |
| `GET` | `/api/quiz/leaderboard?limit=10` | Top quiz scores sorted descending |
| `GET` | `/api/bounty/rewards` | Available bounty achievements and rewards |
| `POST` | `/api/bounty/calculate` | Calculates total bounty and threat rank |
| `GET` | `/api/users/<user_id>/rewards` | Retrieves user's claimed achievements |
| `POST` | `/api/users/<user_id>/rewards/claim` | Claims achievement rewards |
| `DELETE` | `/api/users/<user_id>/rewards` | Resets claimed achievements for user |
| `GET` | `/api/users/<user_id>/crew` | Retrieves user's saved crew manifest & stats |
| `PUT` | `/api/users/<user_id>/crew` | Validates and persists crew configuration |
| `DELETE` | `/api/users/<user_id>/crew` | Deletes saved crew configuration |
| `POST` | `/api/battles/simulate` | Executes deterministic simulation & logs battle |
| `GET` | `/api/users/<user_id>/battles` | Retrieves recent battle history for user |

---

## Running the Automated Test Suite

All tests execute against an isolated in-memory SQLite database (`sqlite:///:memory:`) so local development data is never modified.

```bash
# Run all tests with verbose output
python -m pytest -v
```

### Covered Test Areas:
1. Health check and service metadata
2. Devil Fruit favorite addition and removal
3. Duplicate favorite rejection (HTTP 409)
4. Favorites persistence across independent requests
5. Authoritative server-side quiz scoring
6. Redaction of answers from quiz questions endpoint
7. Leaderboard sorting (score descending, newest first)
8. Bounty milestone calculation and rank tiers
9. Milestone claiming and ledger reset
10. Crew member validation (max 9 members, no captain duplicate, stats 0-100)
11. Crew persistence and retrieval
12. Exact deterministic battle scoring formula
13. Tie-break rule verification (Pirates win on tie)
14. Malformed JSON and payload rejection (HTTP 400 & 422)

---

## Database Location

The development SQLite database file is automatically created at:
```text
grand-line-navigator/instance/grand_line.db
```
Tables and initial schemas are auto-migrated on initial launch of the backend application.

---

## Troubleshooting

### 1. Connection Refused
- **Symptom**: Streamlit displays `Could not connect to backend at http://127.0.0.1:5000`.
- **Solution**: Ensure Terminal 1 is running `python -m backend.app` or `flask --app backend.app run --port 5000` before interacting with features that require database persistence.

### 2. CORS Errors
- **Symptom**: Frontend cannot receive responses due to Cross-Origin restrictions.
- **Solution**: Check `CORS_ORIGINS` in `.env`. By default it includes `http://localhost:8501,http://127.0.0.1:8501`. Ensure the Streamlit port matches.

### 3. Port Already Occupied
- **Port 5000 occupied**: Run `flask --app backend.app run --port 5001` and set `BACKEND_URL=http://127.0.0.1:5001` in your `.env`.
- **Port 8501 occupied**: Run `streamlit run frontend/app.py --server.port 8502`.
