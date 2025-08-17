# Precision Irrigation System

Monorepo containing Raspberry Pi edge agent, Django REST backend, and React web dashboard for a precision irrigation system.

## Components

| Layer | Folder | Purpose |
|-------|--------|---------|
| Edge / Hardware | `raspberry-pi` | Reads sensors, controls relay/pump, pushes readings to backend, can decide locally when offline. |
| Backend API | `backend` | Django + DRF API storing readings, computing irrigation recommendations, exposing control endpoints. |
| Frontend | `frontend/web-dashboard` | React dashboard for real‑time monitoring & manual control. |
| Integrations | `integrations` | Weather + (optional) cloud sync adapters. |
| Docs | `docs` | Architecture, roadmap, setup guides. |

## Quick Start (Development)

### Backend
```
cd backend
python -m venv .venv
./.venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

### Raspberry Pi (Sim Mode)
```
cd raspberry-pi
python -m venv .venv
./.venv/Scripts/Activate.ps1
pip install -r requirements.txt
python src/main.py --simulate
```

### Frontend
```
cd frontend/web-dashboard
npm install
npm start
```

## Environment Variables (Backend)
Copy `.env.example` to `.env` and adjust.

| Key | Description | Default |
|-----|-------------|---------|
| `SECRET_KEY` | Django secret | dev-temp-key |
| `ALLOWED_HOSTS` | Comma list | * |
| `CORS_ALLOWED_ORIGINS` | Frontend origins | http://localhost:3000 |

## Data Flow (High Level)
1. Edge collects sensor + weather data.
2. Edge posts to `/api/readings/`.
3. Backend persists, runs rule engine / ML placeholder.
4. Decision results returned ("IRRIGATE" or "SKIP").
5. Edge toggles relay if instructed (or local override when offline).
6. Frontend polls/WebSocket for updates.

## Next Steps
See `docs/roadmap.md`.
