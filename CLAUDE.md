# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal portfolio website built with Python Flask. Bilingual (Spanish/English), includes admin panel and RESTful API for content management.

- **Backend**: Flask 3.0 (Python 3.11+)
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite (file-based, stored in `data/portfolio.db`)
- **Deployment**: Docker-ready

## Common Commands

```bash
# Setup
cp .env.example .env
python generate_password_hash.py  # Generate admin password hash

# Development with Docker (port 5001, live reload)
./scripts/run-local.sh dev

# Production with Docker (port 8080)
./scripts/run-local.sh prod

# Local development without Docker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed_data.py   # Initialize database with sample data
python app.py         # Runs on http://localhost:5001

# Database utilities
python test_database.py       # Verify database integrity
python migrate_db.py          # Add language support columns
python add_image_url.py       # Add image_url column
python update_translations.py # Update translations
```

## Architecture

```
app.py              # Main Flask app: routes, API endpoints, authentication
database.py         # Data layer: CRUD operations for articles and contacts
templates/
  index.html        # Main portfolio page (bilingual)
  admin.html        # Admin panel interface
  login.html        # Login form
scripts/            # Deployment and helper scripts
data/               # SQLite database directory (created at runtime)
```

## API Endpoints

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | `/api/articles` | Public | Get all articles |
| GET | `/api/articles/<id>` | Public | Get single article |
| POST | `/api/articles` | Required | Create article |
| PUT | `/api/articles/<id>` | Required | Update article |
| DELETE | `/api/articles/<id>` | Required | Delete article |
| POST | `/api/contact` | Public | Submit contact form |

## Database Schema

**portfolio_articles**: `id`, `title`, `description`, `title_en`, `description_en`, `image_url`, `image_gradient`, `image_letter`, `tech_stack` (JSON), `created_at`, `updated_at`

**contact_messages**: `id`, `name`, `email`, `message`, `read_status`, `created_at`

## Key Patterns

- Authentication uses `@login_required` decorator on admin endpoints
- Passwords hashed with Werkzeug's PBKDF2 SHA-256
- `tech_stack` stored as JSON string in database
- Environment variables loaded from `.env` with fallback defaults
- Type hints used throughout codebase

## Environment Variables

Required in `.env`:
- `SECRET_KEY` - Flask session encryption
- `ADMIN_USERNAME` - Admin login (default: admin)
- `ADMIN_PASSWORD_HASH` - Bcrypt password hash (generate with `generate_password_hash.py`)
- `MAIL_*` - Email configuration for contact form notifications

## Deployment

```bash
# Google Cloud Run
./scripts/deploy-gcp.sh your-project-id us-central1

# Docker Registry + SSH
./scripts/build-and-push.sh your-registry/portfolio:latest

# Traditional hosting
gunicorn -w 2 -b 0.0.0.0:8080 app:app
```
