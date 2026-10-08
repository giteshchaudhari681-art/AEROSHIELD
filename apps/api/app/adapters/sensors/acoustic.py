from typing import Dict, Any, List
from datetime import datetime, timezone
from app.schemas.extended import ObservationBase
from app.infrastructure.db.models import ObservationType
from .base import SensorAdapter

class AcousticAdapter(SensorAdapter):
    @property
    def sensor_type(self) -> str:
        return "ACOUSTIC"
        
    def normalize(self, sensor_id: str, raw_payload: Dict[str, Any]) -> List[ObservationBase]:
        # Synthetic payload example:
        # { "bearing_deg": 45, "frequency_hz": 120, "confidence": 0.5 }
        
        now = datetime.now(timezone.utc)
        
        obs = ObservationBase(
            sensor_id=sensor_id,
            sensor_type=self.sensor_type,
            observation_type=ObservationType.ACOUSTIC,
            observed_at=now,
            received_at=now,
            heading=raw_payload.get("bearing_deg"),
            confidence=max(0.0, min(1.0, float(raw_payload.get("confidence", 0.5))))
        )
        return [obs]
