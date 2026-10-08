from typing import Dict, Any, List
from datetime import datetime, timezone
from app.schemas.extended import ObservationBase
from app.infrastructure.db.models import ObservationType
from .base import SensorAdapter

class EOIRAdapter(SensorAdapter):
    @property
    def sensor_type(self) -> str:
        return "EO_IR"
        
    def normalize(self, sensor_id: str, raw_payload: Dict[str, Any]) -> List[ObservationBase]:
        # Synthetic payload example:
        # { "latitude": 37.77, "longitude": -122.41, "confidence": 0.95 }
        
        now = datetime.now(timezone.utc)
        
        obs = ObservationBase(
            sensor_id=sensor_id,
            sensor_type=self.sensor_type,
            observation_type=ObservationType.DETECTION,
            observed_at=now,
            received_at=now,
            location={"type": "Point", "coordinates": [raw_payload.get("longitude", 0.0), raw_payload.get("latitude", 0.0)]} if "longitude" in raw_payload else None,
            confidence=max(0.0, min(1.0, float(raw_payload.get("confidence", 0.7))))
        )
        return [obs]
