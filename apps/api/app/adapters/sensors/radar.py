from typing import Dict, Any, List
from datetime import datetime, timezone
from app.schemas.extended import ObservationBase
from app.infrastructure.db.models import ObservationType
from .base import SensorAdapter

class RadarAdapter(SensorAdapter):
    @property
    def sensor_type(self) -> str:
        return "RADAR"
        
    def normalize(self, sensor_id: str, raw_payload: Dict[str, Any]) -> List[ObservationBase]:
        # Synthetic generic payload example:
        # { "range_m": 500, "azimuth_deg": 40, "elevation_deg": 12, "radial_velocity_mps": 15, "confidence": 0.9, "lat": 37.77, "lon": -122.41, "alt": 100 }
        
        now = datetime.now(timezone.utc)
        
        obs = ObservationBase(
            sensor_id=sensor_id,
            sensor_type=self.sensor_type,
            observation_type=ObservationType.POSITION,
            observed_at=now,
            received_at=now,
            location={"type": "Point", "coordinates": [raw_payload.get("lon", 0.0), raw_payload.get("lat", 0.0)]} if "lon" in raw_payload else None,
            altitude=raw_payload.get("alt"),
            speed=raw_payload.get("radial_velocity_mps"),
            heading=raw_payload.get("azimuth_deg"),
            confidence=max(0.0, min(1.0, float(raw_payload.get("confidence", 0.8))))
        )
        return [obs]
