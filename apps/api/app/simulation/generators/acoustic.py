from .base import SensorSimulator
from typing import Dict, Any, Optional
from datetime import datetime
from app.simulation.models import SimulatedObject

class AcousticSimulator(SensorSimulator):
    def generate_observation(self, obj: SimulatedObject, sim_time: datetime, dist_m: float) -> Optional[Dict[str, Any]]:
        if dist_m > 3000:
            return None
            
        bearing = self._bearing_deg(obj)
        bearing_noise = (self.random.random() - 0.5) * 5.0
        
        return {
            "bearing_deg": (bearing + bearing_noise) % 360,
            "frequency_hz": 120 + (self.random.random() * 20),
            "confidence": 0.5 + (self.random.random() * 0.3),
            "lat": self.lat,
            "lon": self.lon
        }
