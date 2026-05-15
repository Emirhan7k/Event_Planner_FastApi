# Smart Event Planner 🧠

AI-powered event planning platform with content-based recommendation engine.

## Tech Stack
- **Backend**: FastAPI (async) + SQLAlchemy 2.x + SQLite (aiosqlite)
- **AI/ML**: scikit-learn TF-IDF + Cosine Similarity
- **Auth**: JWT (access + refresh tokens, HttpOnly cookies)
- **Frontend**: Jinja2 + Vanilla CSS (responsive, dark mode)
- **Migrations**: Alembic (async)
- **Package Manager**: uv

## Quick Start

```bash
# Install dependencies
uv sync

# Setup database
mkdir data
uv run alembic upgrade head

# Run server
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest tests/ -v
```

## Project Structure

```
app/
├── core/          # Config, JWT security, exceptions
├── db/            # Async engine, session
├── models/        # SQLAlchemy ORM models
├── schemas/       # Pydantic v2 schemas
├── repositories/  # CRUD data access layer
├── services/      # Business logic + AI recommendation
├── api/v1/        # REST API endpoints
├── web/           # Jinja2 page routes
├── middleware/    # Logging middleware
└── templates/     # HTML templates
alembic/           # Database migrations
tests/             # pytest test suite
static/            # CSS, JS, uploads
```

## Features
- 🔐 JWT Authentication (register/login/refresh)
- 📅 Event CRUD with image upload
- 🤖 AI Recommendations (TF-IDF + Cosine Similarity)
- 📊 User dashboard with registered events
- 🎯 Interest-based user profiles
- 🔍 Event search & category filtering
- 📱 Fully responsive UI
