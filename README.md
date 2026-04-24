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

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Pydantic
* Passlib (bcrypt)

---

## Key Learnings

* Request lifecycle with DB interaction
* Blocking I/O and latency sources
* Data validation via Pydantic
* ORM abstraction vs raw SQL
* Persistent state management

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

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

---

## Status

✅ Phase 1 Complete
➡️ Next: Phase 2 — Redis + Caching Layer
