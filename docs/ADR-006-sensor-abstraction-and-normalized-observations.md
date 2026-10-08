# ADR 006: Sensor Abstraction and Normalized Observations

## Status
Accepted

## Context
AEROSHIELD must support a heterogeneous set of sensors (Radar, RF scanners, EO/IR cameras, Acoustic arrays). Each hardware vendor has its own proprietary API, payload schema, protocol, and idiosyncrasies.
If the application core attempts to integrate directly with each vendor, it will become tightly coupled and fragile.

## Decision
We will implement an Adapter Pattern coupled with a Normalized Observation Contract.
1. **Sensor Adapter Registry:** A central registry that maps sensor types (e.g., `RADAR`, `RF`) to concrete adapter instances.
2. **Abstract SensorAdapter Interface:** Defines a `normalize(sensor_id, raw_payload)` method that takes raw vendor-specific JSON/bytes and outputs a list of standard `SensorObservation` objects.
3. **Normalized Observation Model:** Contains fields for spatial (lat, lon, alt), kinematics (speed, heading), identification (classification), and metadata (confidence, observation_type).
4. **Idempotency:** Ingestion endpoints support a `correlation_id` to prevent duplicate writes if payloads are re-delivered.

## Consequences
- **Pros:** The core threat intelligence engine (fusion, risk assessment) only deals with standard AEROSHIELD observation models. New sensors can be added simply by registering a new adapter without touching core business logic.
- **Cons:** We lose some highly vendor-specific data if it doesn't fit the normalized model, unless we store it in the arbitrary `observation_metadata` JSON field (which we do).
