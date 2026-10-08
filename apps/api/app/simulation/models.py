from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
import math

class SimulationConfig(BaseModel):
    enabled: bool = False
    scenario: str = "baseline"
    speed: float = 1.0
    tick_interval_ms: int = 1000
    random_seed: int = 42
    
class SimulatedObject(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    latitude: float
    longitude: float
    altitude: float
    speed: float = 0.0 # m/s
    heading: float = 0.0 # degrees
    vertical_speed: float = 0.0 # m/s
    active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def move(self, dt_seconds: float):
        if not self.active:
            return
            
        # Very simple equirectangular projection motion model for small dt
        # 1 degree lat is approx 111,111 meters
        # 1 degree lon is approx 111,111 * cos(lat) meters
        
        distance = self.speed * dt_seconds
        
        # heading: 0 is North, 90 is East
        heading_rad = math.radians(self.heading)
        dx = distance * math.sin(heading_rad)
        dy = distance * math.cos(heading_rad)
        
        lat_change = dy / 111111.0
        lon_change = dx / (111111.0 * math.cos(math.radians(self.latitude)))
        
        self.latitude += lat_change
        self.longitude += lon_change
        self.altitude += self.vertical_speed * dt_seconds

class SimulationStatus(BaseModel):
    running: bool = False
    scenario: str = "none"
    simulation_time: Optional[datetime] = None
    real_time_factor: float = 1.0
    active_objects: int = 0
    active_sensors: int = 0
    observations_generated: int = 0
    observations_rejected: int = 0
    last_tick: Optional[datetime] = None
