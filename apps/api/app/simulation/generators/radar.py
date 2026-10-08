from .base import SensorSimulator
from typing import Dict, Any, Optional
from datetime import datetime
from app.simulation.models import SimulatedObject

class RadarSimulator(SensorSimulator):
    def generate_observation(self, obj: SimulatedObject, sim_time: datetime, dist_m: float) -> Optional[Dict[str, Any]]:
        # Radar noise
        lat_noise = (self.random.random() - 0.5) * 0.0001
        lon_noise = (self.random.random() - 0.5) * 0.0001
        vel_noise = (self.random.random() - 0.5) * 1.0
        
        bearing = self._bearing_deg(obj)
        
        return {
            "range_m": dist_m,
            "azimuth_deg": bearing,
            "elevation_deg": 10.0,
            "radial_velocity_mps": max(0.0, obj.speed + vel_noise),
            "confidence": 0.9 + (self.random.random() * 0.1 - 0.05),
            "lat": obj.latitude + lat_noise,
            "lon": obj.longitude + lon_noise,
            "alt": obj.altitude
        }
