# Ferrum — Webhook Relay (Phase 2 Complete)

## Overview

Ferrum is a webhook delivery platform built from first principles, evolving from a monolith into a distributed system.

This repository contains the Phase 1 and 2 implementation: a synchronous FastAPI backend with PostgreSQL.

---

## Architecture (Phase 2)
```
Client → FastAPI → Redis (Cache) → PostgreSQL → Response
```
---

## Features Implemented

#### CORE (Phase 1)
* User registration (`/register`)
* Password hashing (bcrypt)
* Duplicate user protection
* Webhook creation & listing
* Event ingestion
* Persistent storage (PostgreSQL)

#### Performance Layer (Phase 2)
* Redis integration for caching
* Cache-aside pattern implementation
* Cache invalidation on write operations
* Request latency tracking (X-Process-Time)

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

### Database Migrations
Alembic integrated:

* Schema version controlled
* `create_all` removed
* Migrations reproducible across environments

### Observability
* Per request latency logging
* X-Process-Time header for benchmarking

### Caching Strategy (Phase 2)
* Caching for only webhook list (read-heavy, low mutation)
#### Pattern Used:
Cache-aside:
1. Check cache
2. If miss → fetch from DB
3. Store in cache with TTL
4. Return response
#### TTL
60 seconds (configurable)

---

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy ORM
* Pydantic
* Passlib (bcrypt)

---

## Observations (Phase 1)
* DB operations are blocking → impacts latency
* Request time dominated by DB commit
* System is CPU-light but I/O-bound

## Observations (Phase 2)
| Scenario | Latency |
| -------- | ------- |
| Cache Miss | ~ 22ms |
| Cache Hit | ~ 1.2ms |

```bash
CACHE MISS
GET /webhooks completed in 0.0220s
INFO:     127.0.0.1:52521 - "GET /webhooks HTTP/1.1" 200 OK
CACHE HIT
GET /webhooks completed in 0.0012s
INFO:     127.0.0.1:52526 - "GET /webhooks HTTP/1.1" 200 OK
```

##### Insight -
* ~18ms improvement on cached reads
* DB latency is dominant on uncached path
* Cache removed DB dependency for repeated reads

---

## Failure Considerations
* Redis down -> fallback to DB
* Stale cache -> migrated via invalidation + TTL
* Cache miss bursts -> potential DB spike

## Deliberate Limitations
* No async DB (potential bottleneck)
* No retry tracking (planned)
* No delivery tracking per attempt

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
```bash
DATABASE_URL = "postgresql://webhook_user:pswd@localhost:5432/webhook_db"
```

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

---

## Key Learnings
* Cache vs DB Tradeoffs
* Cache invalidation complexity
* Latency bottleneck identification
* Read vs. write optimization

## Status

✅ **Phase 1** Complete
✅ **Phase 2** Complete
➡️ Next: **Phase 3** — Async + Messaging 

## Next Phase 
* introduce queue
* add worker service
* implement retries and delivery guarantees
