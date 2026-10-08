from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime, timezone
import uuid

from app.repositories.observations_repository import observations_repo
from app.repositories.sensors_repository import sensors_repo
from app.infrastructure.db.models import SensorObservation, SensorStatus
from app.adapters.sensors.base import registry
from app.schemas.extended import ObservationBase
from shapely.geometry import shape

from app.repositories.event_outbox_repository import outbox_repo
from app.domain.events.observations import ObservationCreatedEvent, ObservationCreatedPayload

class SensorObservationService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[SensorObservation]:
        return observations_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[SensorObservation], int]:
        return observations_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def get_by_time_range(db: Session, start_time: datetime, end_time: datetime, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[SensorObservation], int]:
        return observations_repo.get_by_time_range(db, start_time, end_time, skip, limit, **filters)

    @staticmethod
    def ingest_raw(db: Session, sensor_id: str, raw_payload: Dict[str, Any], correlation_id: Optional[str] = None) -> List[SensorObservation]:
        sensor = sensors_repo.get(db, id=sensor_id)
        if not sensor:
            raise ValueError(f"Sensor {sensor_id} not found")
        if not sensor.is_enabled or sensor.operational_status == SensorStatus.INACTIVE:
            raise ValueError(f"Sensor {sensor_id} is not enabled or is inactive")

        try:
            adapter = registry.get(sensor.sensor_type)
        except ValueError as e:
            raise ValueError(str(e))
            
        normalized_obs_list = adapter.normalize(sensor_id, raw_payload)
        
        # Idempotency check via correlation_id if provided (e.g. hash of raw payload)
        if correlation_id:
            existing = observations_repo.find_by_correlation_id(db, correlation_id)
            if existing:
                return existing

        created = []
        for n_obs in normalized_obs_list:
            # Validation
            if n_obs.confidence is not None and (n_obs.confidence < 0.0 or n_obs.confidence > 1.0):
                raise ValueError("Confidence must be between 0 and 1")
            if n_obs.heading is not None and (n_obs.heading < 0.0 or n_obs.heading >= 360.0):
                raise ValueError("Heading must be between 0 and 360")
            if n_obs.speed is not None and n_obs.speed < 0:
                raise ValueError("Speed cannot be negative")

            geom_wkt = None
            if n_obs.location and "coordinates" in n_obs.location:
                lon, lat = n_obs.location["coordinates"]
                if lat < -90 or lat > 90: raise ValueError("Invalid latitude")
                if lon < -180 or lon > 180: raise ValueError("Invalid longitude")
                geom_wkt = shape(n_obs.location).wkt
                
            obs = SensorObservation(
                id=str(uuid.uuid4()),
                sensor_id=sensor_id,
                sensor_type=n_obs.sensor_type,
                observation_type=n_obs.observation_type,
                observed_at=n_obs.observed_at,
                received_at=n_obs.received_at or datetime.now(timezone.utc),
                location=geom_wkt,
                altitude=n_obs.altitude,
                speed=n_obs.speed,
                heading=n_obs.heading,
                confidence=n_obs.confidence,
                classification=n_obs.classification,
                observation_metadata=raw_payload, # Keeping sanitized raw payload for prototype
                correlation_id=correlation_id
            )
            created.append(observations_repo.create(db, obj_in=obs))
            
            # Create outbox event
            payload = ObservationCreatedPayload(
                observation_id=obs.id,
                sensor_id=obs.sensor_id,
                observation_type=obs.observation_type,
                observed_at=obs.observed_at.isoformat(),
                received_at=obs.received_at.isoformat(),
                latitude=lat if geom_wkt else None,
                longitude=lon if geom_wkt else None,
                altitude_m=obs.altitude,
                speed_mps=obs.speed,
                heading_deg=obs.heading,
                confidence=obs.confidence,
                classification=obs.classification
            )
            event = ObservationCreatedEvent(
                correlation_id=correlation_id,
                aggregate_id=obs.id,
                payload=payload.model_dump()
            )
            outbox_repo.create_event(db, event.model_dump())
            
        # Update sensor health
        sensor.last_seen_at = datetime.now(timezone.utc)
        sensor.health_status = adapter.health()
        db.commit()
        
        return created

observations_service = SensorObservationService()
