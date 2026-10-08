from .base import SensorSimulator
from typing import Dict, Any, Optional
from datetime import datetime
from app.simulation.models import SimulatedObject

class EOIRSimulator(SensorSimulator):
    def generate_observation(self, obj: SimulatedObject, sim_time: datetime, dist_m: float) -> Optional[Dict[str, Any]]:
        # Lower coverage for optical
        if dist_m > 5000:
            return None
            
        lat_noise = (self.random.random() - 0.5) * 0.00005
        lon_noise = (self.random.random() - 0.5) * 0.00005
        
        return {
            "latitude": obj.latitude + lat_noise,
            "longitude": obj.longitude + lon_noise,
            "altitude": obj.altitude,
            "confidence": 0.85 + (self.random.random() * 0.1)
        }
