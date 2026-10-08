# ADR 002: Persistence and Geospatial Model

## Context
AEROSHIELD is an infrastructure-aware airspace security platform. Tracking airborne entities, establishing no-fly zones, and determining threat trajectories are inherently geospatial operations. We need a robust persistence mechanism capable of managing both standard relational domain models (sites, sensors, audits) and high-performance geospatial operations (intersections, proximities).

## Decision
We will use **PostgreSQL** coupled with the **PostGIS** extension as our primary relational database. 

1. **Database:** PostgreSQL + PostGIS (via the `postgis/postgis:15-3.3` Docker image).
2. **ORM:** SQLAlchemy 2.0.
3. **Geospatial Mapping:** GeoAlchemy2, defining columns using `Geometry(..., srid=4326)`.
4. **Migrations:** Alembic, explicitly configured to ignore the `tiger`, `tiger_data`, and `topology` schemas to prevent autogeneration conflicts.
5. **Real-time State:** Redis for ephemeral state (ongoing tracks) before sinking confirmed events to PostgreSQL.

## Consequences
- **Positive**: PostGIS provides enterprise-grade spatial indexing (GiST) and a comprehensive suite of functions (`ST_Intersects`, `ST_Distance`).
- **Positive**: We consolidate relational and spatial queries in a single mature system.
- **Negative**: PostGIS adds operational overhead. We encountered initial setup issues relating to Alembic attempting to manage PostGIS system tables, which required careful configuration of `include_object` in `env.py`.
- **Negative**: Python `psycopg2` requires native compilation or binary distributions (`psycopg2-binary`), occasionally complicating cross-platform development environments.
