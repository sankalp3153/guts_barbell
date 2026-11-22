# Guts Barbell — Strength, Workout & Nutrition Platform

Full-stack **Django 5.1** fitness platform and JSON backend for structured barbell training programs, TDEE/macro nutrition planning, trainer workflows, and fitness articles.

## Architecture

- **`users/`** — Custom `AbstractUser` model with trainer permission gating (`TrainerRequiredMiddleware`).
- **`workouts/`** — Programs, multi-day training splits, exercise library, and strength analytics (`workouts/analytics.py`: Epley 1RM & weekly muscle-group set volume).
- **`diets/`** — Diet plans, structured meals, recipes, and Mifflin-St Jeor TDEE/macro calculator (`diets/nutrition.py`).
- **`blogs/`** — Training & nutrition articles.
- **`core/`** — Landing pages, JSON REST endpoints (`/api/health/`, `/api/workouts/`, `/api/diets/`, `/api/macros/calculate/`), and demo data seeder (`seed_sample_data`).

## Quick Start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

python3 manage.py migrate
python3 manage.py seed_sample_data
python3 manage.py runserver
```

Or run with PostgreSQL + Gunicorn via Docker Compose:

```bash
docker compose up --build
```

## API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health/` | Service liveness check |
| `GET` | `/api/workouts/?difficulty=intermediate` | Published workout programs |
| `GET` | `/api/diets/?goal=muscle_gain` | Published diet plans with daily macros |
| `POST` | `/api/macros/calculate/` | Computes BMR, TDEE, and daily macro targets |

## Running Tests

```bash
python3 manage.py test -v 2
```
