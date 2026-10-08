from typing import Dict, Any, List
from datetime import datetime, timezone
from app.schemas.extended import ObservationBase
from app.infrastructure.db.models import ObservationType
from .base import SensorAdapter

class RFAdapter(SensorAdapter):
    @property
    def sensor_type(self) -> str:
        return "RF"
        
    def normalize(self, sensor_id: str, raw_payload: Dict[str, Any]) -> List[ObservationBase]:
        # Synthetic payload example:
        # { "frequency_hz": 2400000000, "signal_strength_dbm": -45, "confidence": 0.7, "bearing": 120 }
        
        now = datetime.now(timezone.utc)
        
        obs = ObservationBase(
            sensor_id=sensor_id,
            sensor_type=self.sensor_type,
            observation_type=ObservationType.SIGNAL,
            observed_at=now,
            received_at=now,
            heading=raw_payload.get("bearing"),
            confidence=max(0.0, min(1.0, float(raw_payload.get("confidence", 0.6))))
        )
        return [obs]
