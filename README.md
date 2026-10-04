# Explore – Travel Booking Website
Stack: HTML/CSS/JS frontend, Flask REST API, PostgreSQL, JWT auth.
Flow: Signup -> Login -> Home -> Country page -> Book -> My Bookings (edit / cancel).

## Setup
1. Create the DB:  `createdb travel_db`   (or in psql: `CREATE DATABASE travel_db;`)
2. `python -m venv venv && source venv/bin/activate`  (Windows: `venv\Scripts\activate`)
3. `pip install -r requirements.txt`
4. `cp .env.example .env` and edit DATABASE_URL (user/password) + JWT_SECRET_KEY
5. `python app.py`  -> tables are created and 8 countries are seeded automatically
6. Open http://localhost:5000

## API
POST /api/signup, POST /api/login, GET /api/me
GET /api/countries, GET /api/countries/<slug>
POST /api/bookings, GET /api/bookings, PUT /api/bookings/<id>, DELETE /api/bookings/<id> (cancels)
All /api/bookings* and /api/me need header `Authorization: Bearer <token>`.
