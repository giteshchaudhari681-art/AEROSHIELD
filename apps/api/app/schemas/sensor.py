from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class SensorType(str, Enum):
    RADAR = "radar"
    RF = "rf"
    EO_IR = "eo_ir"
    ACOUSTIC = "acoustic"

class NormalizedObservation(BaseModel):
    observation_id: str = Field(..., description="Unique identifier for the observation")
    sensor_id: str = Field(..., description="Identifier of the sensor generating the observation")
    sensor_type: SensorType = Field(..., description="Type of the sensor")
    timestamp: datetime = Field(..., description="Time of observation")
    
    # Geographic Data
    latitude: Optional[float] = Field(None, description="Latitude in decimal degrees")
    longitude: Optional[float] = Field(None, description="Longitude in decimal degrees")
    altitude: Optional[float] = Field(None, description="Altitude in meters")
    
    # Kinematics
    velocity_x: Optional[float] = Field(None, description="Velocity X in m/s")
    velocity_y: Optional[float] = Field(None, description="Velocity Y in m/s")
    velocity_z: Optional[float] = Field(None, description="Velocity Z in m/s")
    heading: Optional[float] = Field(None, description="Heading in degrees")
    
    # Intelligence
    classification: Optional[str] = Field(None, description="Classified object type (e.g. quadcopter)")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    
    # Raw Data / Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional sensor-specific metadata")
    correlation_id: Optional[str] = Field(None, description="ID used to correlate this with other observations or tracks")

