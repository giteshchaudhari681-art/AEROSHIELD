# ADR-001: AEROSHIELD Initial System Architecture

**Date:** 2026-10-08
**Status:** Accepted

## Context
AEROSHIELD is an infrastructure-aware drone surveillance and threat intelligence platform. The project needs an extensible and robust foundation capable of accommodating complex intelligence pipelines (multi-sensor fusion, intent estimation, threat prediction, and asset-specific risk) while interfacing eventually with physical sensor hardware. The current scope is an intelligence layer prototype driven by simulated sensors.

## Decisions

1. **Modular Architecture & Hardware Abstraction**
   - The intelligence core must not depend on physical hardware directly. We introduce a **Sensor Abstraction Layer** based on the `NormalizedObservation` schema to decouple the AEROSHIELD intelligence pipeline from specific hardware (Radar, RF, EO/IR, Acoustic).
   - This enables simulated data ingestion to be a drop-in replacement for physical adapters during the prototype phase.

2. **Technology Stack Selection**
   - **Backend:** Python + FastAPI. Python is native to AI/ML workflows and provides necessary numerical computing libraries (NumPy, Pandas, scikit-learn). FastAPI ensures high-performance async APIs.
   - **Database:** PostgreSQL with PostGIS. Threat intelligence is highly geospatial (infrastructure digital twins, restricted zones, track trajectories).
   - **Real-Time Data:** Redis & WebSockets. Required for real-time alerting, tracking, and operational dashboard updates.
   - **Frontend:** React, TypeScript, Vite, Tailwind CSS, MapLibre GL. Offers a high-performance web map interface and modular UI components.

3. **Human-in-the-loop (HITL)**
   - The system is explicitly an intelligence platform (DETECT -> ALERT), not an autonomous weapon or physical countermeasure system. Final security decisions remain with the human operator.

## Consequences
- Development is focused on the intelligence pipeline without being blocked by hardware integrations.
- We require Docker to standardize the local development environment containing PostGIS and Redis dependencies.
- A strict boundary between sensor adapter and intelligence ingestion must be maintained.
