# Data Architecture

## Overview
AEROSHIELD's data architecture is built around a spatial-first approach, leveraging PostgreSQL with PostGIS extensions to manage geographical elements natively.

## Key Components

1. **Relational Data & Spatial Data (PostgreSQL + PostGIS)**
   - **Why**: The domain is inherently spatial (zones, tracks, sensors, facilities).
   - **How**: We use `GeoAlchemy2` and SQLAlchemy to map Python domain entities directly to PostGIS geometries.
   - **Primary Use**: Master data, structured domain models, and long-term storage of observations.

2. **In-Memory Store (Redis)**
   - **Why**: High-throughput processing, caching, and pub/sub.
   - **How**: Used as a message broker and state store for real-time sensor streams and ephemeral track states before they are persisted or aggregated into the relational DB.

3. **Data Access Layer**
   - **ORM**: SQLAlchemy 2.0 with a sync core (temporarily rolling back from async due to `psycopg2`/`greenlet` dependencies, aiming for full async once stabilized).
   - **Migrations**: Alembic, explicitly ignoring PostGIS/Tiger system tables to prevent migration conflicts.

## Design Decisions
- `ST_AsEWKB` / `Geometry` columns handle spatial intersections efficiently in database.
- `seed_data.py` populates a known deterministic set of entities for local testing.
- `Alembic` manages schema changes. `include_object` logic prevents it from dropping system extensions.
- Explicit mapping between `API DTOs` (Pydantic) and `Infrastructure Models` (SQLAlchemy).
