# ADR-010: Aerial Track Engine

## Status
Accepted

## Context
AEROSHIELD needs to associate fused contacts over time into coherent tracks (Aerial Tracks) to understand object continuity before making threat assessments. 

## Decision
We implemented a deterministic track engine that processes fused contacts asynchronously via the Redis event pipeline (or a durable outbox polling mechanism as an alternative for recovery). 
1. **Trigger**: Driven by fused contacts.
2. **Persistence**: `AerialTrack` and `TrackObservation` tables in PostGIS.
3. **Logic**: Gating on temporal (ms) and spatial (m) windows. Association compares incoming fused contacts against existing active/tentative tracks. 
4. **Lifecycle**: TENTATIVE -> ACTIVE -> STALE -> TERMINATED.

## Consequences
- **Pros**: Extensible to ML or complex filters later. Deterministic and easy to explain.
- **Cons**: No global multi-target assignment is used for the prototype; ambiguous tracks might cause branching or new track creation.
