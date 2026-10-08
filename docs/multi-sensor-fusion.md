# Multi-Sensor Fusion Engine

AEROSHIELD's Multi-Sensor Fusion Engine processes normalized sensor observations in real-time to generate fused contacts. It is designed to be deterministic, explainable, and configurable without relying on black-box ML or complex trackers initially.

## Pipeline Flow

1. **Observation Event**: A sensor observation is ingested and persisted. An `observation.created` event is dispatched over Redis.
2. **Consumer**: The `FusionConsumer` picks up this event asynchronously.
3. **Candidate Generation**: The engine queries recent observations within a temporal and spatial gate relative to the incoming observation.
4. **Scoring**: Each candidate is scored on Time Similarity, Spatial Similarity, Measurement Consistency (altitude, speed), and Sensor Reliability.
5. **Fusion**: If the final weighted score exceeds a confidence threshold, the observations are fused into a `FusedContact`.
6. **Persistence**: The `FusedContact` and links back to the observations (`FusedContactObservation`) are stored in PostgreSQL/PostGIS.

## Configuration

Gates and weights are configurable via environment variables or `config.py`:
- `FUSION_TIME_WINDOW_MS`: Maximum time delta for observations (default: 2000)
- `FUSION_POSITION_GATE_METERS`: Maximum spatial distance (default: 50.0)
- `W_TIME`, `W_DISTANCE`, `W_MEASUREMENT`, `W_SENSOR`: Weights for the fusion score equation.
