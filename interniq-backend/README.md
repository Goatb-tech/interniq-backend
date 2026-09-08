# InternIQ Backend

AI-powered internship readiness platform backend.

## Tech Stack

- **FastAPI** — Async Python web framework
- **PostgreSQL** — Primary database
- **SQLAlchemy** — Async ORM
- **Alembic** — Database migrations
- **JWT** — Token-based authentication
- **Docker** — Containerization

## Features

1. **User Registration** — Sign up with email and password
2. **User Login** — JWT-based authentication with access + refresh tokens
3. **Resume Upload** — Upload PDF/DOCX files
4. **Resume Storage** — Securely stored per-user
5. **AI Resume Analysis** — Parses skills, experience, education, strengths & gaps
6. **Internship Readiness Score** — 0–100 score calculated from resume data
7. **Dashboard API** — Aggregated stats and score breakdowns

## Project Structure

```
interniq-backend/
├── app/
│   ├── api/v1/          # Route handlers (auth, resume, analysis, dashboard)
│   ├── core/            # Security, storage utilities
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/        # Business logic layer
│   ├── utils/           # Helper functions
│   ├── config.py        # Environment-based settings
│   ├── database.py      # Async DB engine & session
│   ├── dependencies.py  # FastAPI dependency injection
│   └── main.py          # App entry point
├── alembic/             # Database migrations
├── uploads/             # Uploaded resume files
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Docker & Docker Compose (optional)

### Local Development

```bash
# 1. Clone and enter directory
cd interniq-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy env and configure
cp .env.example .env

# 5. Run database migrations
alembic upgrade head

# 6. Start server
uvicorn app.main:app --reload
```

### With Docker

```bash
docker compose up --build
```

Server runs at `http://localhost:8000`.

## API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login, returns JWT tokens |
| GET | `/api/v1/auth/me` | Get current user profile |
| POST | `/api/v1/resumes/upload` | Upload a resume file |
| GET | `/api/v1/resumes/` | List user's resumes |
| GET | `/api/v1/resumes/{id}` | Get resume details |
| POST | `/api/v1/analysis/resumes/{id}` | Run AI analysis on a resume |
| GET | `/api/v1/dashboard/stats` | Get dashboard statistics |
| GET | `/api/v1/dashboard/score/{id}` | Get score breakdown |
| GET | `/health` | Health check |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Async PostgreSQL connection string | `postgresql+asyncpg://postgres:postgres@localhost:5432/interniq` |
| `SECRET_KEY` | JWT signing secret | `change-me-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token TTL | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token TTL | `7` |
| `MAX_UPLOAD_SIZE` | Max resume file size (bytes) | `10485760` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:3000"]` |

## Running Migrations

```bash
# Generate a new migration
alembic revision --autogenerate -m "description"

# Apply pending migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

## License

MIT
