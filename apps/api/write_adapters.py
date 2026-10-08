import os

adapters_dir = "d:/SEVA/apps/api/app/adapters/sensors"

adapters = {
    "radar.py": """from typing import Dict, Any, List
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
""",
    "rf.py": """from typing import Dict, Any, List
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
""",
    "eoir.py": """from typing import Dict, Any, List
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
""",
    "acoustic.py": """from typing import Dict, Any, List
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
""",
    "__init__.py": """from .base import registry
from .radar import RadarAdapter
from .rf import RFAdapter
from .eoir import EOIRAdapter
from .acoustic import AcousticAdapter

registry.register(RadarAdapter())
registry.register(RFAdapter())
registry.register(EOIRAdapter())
registry.register(AcousticAdapter())

__all__ = ["registry"]
"""
}

for name, content in adapters.items():
    with open(f"{adapters_dir}/{name}", "w") as f:
        f.write(content)
        
print("Adapters written.")
