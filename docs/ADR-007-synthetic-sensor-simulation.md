# ADR 007: Synthetic Sensor Simulation Engine

## Status
Accepted

## Context
AEROSHIELD must be developed, tested, and demonstrated without relying on live hardware deployments (Radar, RF, etc.). 
We need a believable, configurable, deterministic source of sensor telemetry that acts exactly as if it came from physical devices. 
Crucially, it must feed through the *same* ingestion architecture (adapters and observation services) as physical hardware to ensure our integration pathways are fully tested.

## Decision
We implemented a lightweight, multi-threaded `SimulationEngine` that runs concurrently with FastAPI (when enabled).
- **SimulatedObjects**: Synthetic aerial objects move through a simplistic 2D space deterministically using an internal clock.
- **SensorSimulators**: Specific simulators (RadarSimulator, RFSimulator) use the distance/bearing to `SimulatedObjects` to generate realistic synthetic telemetry payloads (incorporating configurable random noise and dropout probabilities).
- **Determinism**: The engine takes a `random_seed`. This ensures scenarios are completely reproducible, making testing idempotent.
- **Integration**: Simulators emit raw dictionary payloads exactly like vendor hardware, submitting them to the `ObservationService` via the `SensorAdapterRegistry`.

## Consequences
- **Pros**: The rest of AEROSHIELD remains ignorant of whether data is real or simulated. We can accelerate time for demonstrations.
- **Cons**: The simplistic motion model and noise properties are not a true physics engine (e.g. no multipath, no occlusion). For software testing purposes, this is acceptable.
