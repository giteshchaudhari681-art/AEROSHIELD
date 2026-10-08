# ADR-009: Multi-Sensor Fusion Engine

## Status
Accepted

## Context
AEROSHIELD requires a mechanism to fuse multiple overlapping sensor observations into single coherent contacts before forming tracks or evaluating threat levels. We need a deterministic, explainable system to merge data.

## Decision
We implemented a weighted, gated scoring engine for Multi-Sensor Fusion.
1. **Trigger**: Driven by Redis `observation.created` events out-of-band to prevent slowing down ingestion.
2. **Persistence**: `FusedContact` and `FusedContactObservation` tables in PostGIS.
3. **Logic**: Gating on temporal (ms) and spatial (m) windows. Weighted scoring algorithm for time, space, measurements, and sensor reliability.

## Consequences
- **Pros**: Extensible to ML or complex filters later. Deterministic and easy to explain to operators via the `fusion_reasons` and `conflicts_json` fields.
- **Cons**: Naive averaging of position coordinates is used for the prototype; could be improved using proper spatial clustering or Kalman filtering in future iterations.
