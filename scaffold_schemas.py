import os

schema_content = """
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Common Pagination
class PaginatedResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[Any]

# Base Error
class ApiErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ApiError(BaseModel):
    error: ApiErrorDetail

# Schemas
class ObservationBase(BaseModel):
    sensor_id: str
    sensor_type: str
    observed_at: datetime
    location: Optional[Dict[str, Any]] = None
    altitude: Optional[float] = None
    speed: Optional[float] = None
    heading: Optional[float] = None
    confidence: Optional[float] = None
    classification: Optional[str] = None

class ObservationRead(ObservationBase):
    id: str
    track_id: Optional[str] = None
    created_at: datetime
    class Config: from_attributes = True

class TrackBase(BaseModel):
    track_identifier: str
    site_id: str
    classification: Optional[str] = None
    status: str
    confidence: Optional[float] = None
    current_location: Dict[str, Any]
    current_altitude: Optional[float] = None
    current_speed: Optional[float] = None
    current_heading: Optional[float] = None

class TrackRead(TrackBase):
    id: str
    first_seen_at: datetime
    last_seen_at: datetime
    created_at: datetime
    updated_at: Optional[datetime]
    class Config: from_attributes = True

class BehaviourEventBase(BaseModel):
    track_id: str
    event_type: str
    observed_at: datetime
    duration: Optional[float] = None
    confidence: Optional[float] = None
    location: Optional[Dict[str, Any]] = None

class BehaviourEventRead(BehaviourEventBase):
    id: str
    created_at: datetime
    class Config: from_attributes = True

class ThreatAssessmentBase(BaseModel):
    track_id: str
    site_id: str
    threat_level: str
    risk_score: Optional[float] = None
    confidence: Optional[float] = None
    reasoning: Optional[str] = None
    model_version: Optional[str] = None
    assessed_at: datetime
    expires_at: Optional[datetime] = None

class ThreatAssessmentRead(ThreatAssessmentBase):
    id: str
    class Config: from_attributes = True

class AlertBase(BaseModel):
    track_id: Optional[str] = None
    threat_assessment_id: Optional[str] = None
    incident_id: Optional[str] = None
    alert_type: str
    severity: str
    title: str
    message: str
    status: str

class AlertRead(AlertBase):
    id: str
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    class Config: from_attributes = True

class IncidentBase(BaseModel):
    site_id: str
    title: str
    description: Optional[str] = None
    severity: str
    status: str
    started_at: datetime
    ended_at: Optional[datetime] = None

class IncidentRead(IncidentBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]
    class Config: from_attributes = True

class EvidenceBase(BaseModel):
    incident_id: str
    evidence_type: str
    source: str
    timestamp: datetime
    confidence: Optional[float] = None
    content: str

class EvidenceRead(EvidenceBase):
    id: str
    created_at: datetime
    class Config: from_attributes = True
"""

with open("d:/SEVA/apps/api/app/schemas/extended.py", "w") as f:
    f.write(schema_content)

print("Schemas scaffolded.")
