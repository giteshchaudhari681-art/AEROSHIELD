# Sensor Abstraction

AEROSHIELD interfaces with a variety of hardware sensors (Radar, RF, EO/IR, Acoustic). Rather than building rigid, vendor-specific integrations into the core application, AEROSHIELD uses an **Adapter Architecture**.

## Architecture Overview

### 1. Sensor Models
- `Sensor`: Represents the physical device deployed at a site. Contains metadata like `sensor_code`, `sensor_type`, `is_enabled`, `operational_status`, and `health_status`.
- `SensorObservation`: A normalized data contract representing a single detection, measurement, or status update from a sensor.

### 2. Adapters
Adapters live in `apps/api/app/adapters/sensors/`. Each adapter is responsible for:
- Implementing the `SensorAdapter` abstract base class.
- Declaring its supported `sensor_type` (e.g. `RADAR`).
- Implementing `normalize()`, taking raw vendor payload and yielding normalized `SensorObservation` records.
- Optionally tracking connectivity `health()`.

### 3. Ingestion Pipeline
1. Payload arrives at `POST /api/v1/observations/?sensor_id=...`.
2. The `SensorObservationService` loads the sensor from the database and checks if it is `is_enabled` and active.
3. The service looks up the corresponding adapter in the `AdapterRegistry`.
4. The adapter's `normalize()` method translates the payload.
5. The service persists the normalized observations to PostGIS.

### 4. Idempotency
Ingestion handles duplicate deliveries gracefully via `correlation_id`. If a payload with an existing `correlation_id` is received, the service returns the existing database records without error.

## Adding a New Sensor Type

1. Create `new_sensor.py` in `apps/api/app/adapters/sensors/`.
2. Extend `SensorAdapter` and implement `sensor_type` and `normalize`.
3. Register the adapter in `apps/api/app/adapters/sensors/__init__.py`.
