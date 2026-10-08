from typing import Any, Dict, Optional
from datetime import datetime
from pydantic import BaseModel
from .base import DomainEvent

class ObservationCreatedPayload(BaseModel):
    observation_id: str
    sensor_id: str
    observation_type: str
    observed_at: str
    received_at: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude_m: Optional[float] = None
    speed_mps: Optional[float] = None
    heading_deg: Optional[float] = None
    confidence: Optional[float] = None
    classification: Optional[str] = None

class ObservationCreatedEvent(DomainEvent):
    event_type: str = "observation.created"
    aggregate_type: str = "sensor_observation"
