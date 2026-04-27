# Ferrum — Webhook Relay (Phase 1 Complete)

## Overview

Ferrum is a webhook delivery platform built from first principles, evolving from a monolith into a distributed system.

This repository contains the Phase 1 implementation: a synchronous FastAPI backend with PostgreSQL.

---

## Architecture (Phase 1)

Client → FastAPI → PostgreSQL → Response

---

## Features Implemented

* User registration (`/register`)
* Password hashing (bcrypt)
* Duplicate user protection
* Webhook creation & listing
* Event ingestion
* Persistent storage (PostgreSQL)

---

## Engineering Improvements

### Connection Pooling
Explicit SQLAlchemy pooling configured:

* pool_size=5
* max_overflow=10
* pool_pre_ping=True

Prevents connection exhaustion under load.

### Request Latency Tracking
Middleware added:

* X-Process-Time header on every response
* Logs per-request latency

Baseline established for future performance comparisons.

---

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Pydantic
* Passlib (bcrypt)

---

## Database Migrations
Alembic integrated:

* Schema version controlled
* `create_all` removed
* Migrations reproducible across environments

---

## Observations (Phase 1)
* DB operations are blocking → impacts latency
* Request time dominated by DB commit
* System is CPU-light but I/O-bound

---

## Deliberate Limitations
* No async DB (potential bottleneck)
* No retry tracking (planned)
* No caching (Phase 2)

---

## Run Locally

install postgresql, and python3. Set up a venv, and the do the following

```bash
pip install -r requirements.txt
sudo service postgresql start   # Linux
brew services start postgresql  # Mac
# Open postgress shell:
psql postgres
```

```pysql
CREATE DATABASE webhook_db;

CREATE USER webhook_user WITH PASSWORD 'pswd';

ALTER ROLE webhook_user SET client_encoding TO 'utf8';
ALTER ROLE webhook_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE webhook_user SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE webhook_db TO webhook_user;
\c webhook_db
GRANT ALL ON SCHEMA public TO webhook_user;
\q
```

Create a `.env.db` file with the DATABASE_URL:
```
DATABASE_URL = "postgresql://webhook_user:pswd@localhost:5432/webhook_db"
```

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

---

## Status

✅ Phase 1 Complete
➡️ Next: Phase 2 — Redis + Caching Layer
