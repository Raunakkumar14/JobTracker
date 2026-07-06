# JobTracker Backend

Backend for JobTracker application built using FastAPI and PostgreSQL.

## Live Links

- API: https://jobtracker-50bn.onrender.com
- Docs: https://jobtracker-50bn.onrender.com/docs

## Tech Stack

- FastAPI
- PostgreSQL (Neon)
- SQLAlchemy
- Alembic
- Uvicorn
- Render

## Features

- User registration and login (JWT)
- Job CRUD operations
- PostgreSQL database integration
- Database migrations using Alembic
- Deployed on Render

## Database

Uses Neon PostgreSQL.

Environment Variable:

- DATABASE_URL

## Run Locally

1. Clone the repository
2. Create virtual environment
3. Install dependencies:
   pip install -r requirements.txt
4. Create `.env` file and add:
   DATABASE_URL
5. Run migrations:
   alembic upgrade head
6. Start server:
   uvicorn app.main:app --reload

## Deployment

- Hosted on Render
- Start command:
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
