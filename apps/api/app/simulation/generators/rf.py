from .base import SensorSimulator
from typing import Dict, Any, Optional
from datetime import datetime
from app.simulation.models import SimulatedObject

class RFSimulator(SensorSimulator):
    def generate_observation(self, obj: SimulatedObject, sim_time: datetime, dist_m: float) -> Optional[Dict[str, Any]]:
        # Only detect objects emitting RF
        if obj.metadata.get("rf_emitter", True) is False:
            return None
            
        bearing = self._bearing_deg(obj)
        bearing_noise = (self.random.random() - 0.5) * 2.0
        
        signal_dbm = -50 - (dist_m / 1000)
        
        return {
            "frequency_hz": 2400000000,
            "signal_strength_dbm": signal_dbm,
            "confidence": 0.7 + (self.random.random() * 0.2 - 0.1),
            "bearing": (bearing + bearing_noise) % 360,
            "lat": self.lat,
            "lon": self.lon
        }
