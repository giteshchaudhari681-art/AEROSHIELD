# AEROSHIELD System Architecture Overview

## Intelligent Pipeline Architecture
The system consists of the following logic layers:

1. **Sensors** (Simulated or Real Hardware via Adapters)
   - Radar
   - RF
   - EO/IR
   - Acoustic
2. **Sensor Abstraction / Ingestion Layer**
   - Normalizes hardware-specific data into the `NormalizedObservation` contract.
3. **Multi-Sensor Fusion**
   - Fuses heterogeneous data to remove duplicates and improve confidence.
4. **Tracking Engine**
   - Assigns tracks to unified multi-sensor observations.
5. **Identity & Classification**
   - AI-based drone type/payload recognition.
6. **Behaviour & Intent Engine**
   - Estimates intention based on movement and targets.
7. **Trajectory Prediction & Infrastructure Digital Twin**
   - Predicts future path against the site's critical assets and zones.
8. **Asset-Specific Risk Engine**
   - Assesses the impact and risk to the specific infrastructure.
9. **Explainability / Evidence Layer**
   - Provides clear justification for alerts (human-readable evidence).
10. **Alert / Incident Engine**
    - Orchestrates alerts for operators based on defined thresholds.
11. **Operator Dashboard**
    - The tactical interface providing real-time situational awareness.

## Current State (Prompt 01)
- The baseline project structure is established.
- API and Web scaffolding is complete.
- WebSocket foundation and Sensor Abstraction schema are prepared.
- PostgreSQL/PostGIS, Redis, and Docker are configured.
- *Note: Complete functional pipeline to be implemented in subsequent iterations.*
