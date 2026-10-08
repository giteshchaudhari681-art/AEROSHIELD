import os

schema_path = 'd:/SEVA/apps/api/app/schemas/domain.py'
with open(schema_path, 'w') as f:
    f.write('''from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime
from app.infrastructure.db.models import SiteType, AssetCriticality, ZoneSeverity, OperationalStatus

# Base schemas
class SiteBase(BaseModel):
    name: str
    description: Optional[str] = None
    site_code: Optional[str] = None
    site_type: SiteType
    status: str = "ACTIVE"
    location: Optional[dict] = None
    boundary: Optional[dict] = None

class SiteCreate(SiteBase):
    id: str

class SiteRead(SiteBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class AssetBase(BaseModel):
    name: str
    asset_code: Optional[str] = None
    asset_type: str
    description: Optional[str] = None
    criticality: AssetCriticality
    operational_status: OperationalStatus = OperationalStatus.UNKNOWN
    location: Optional[dict] = None
    protection_radius: Optional[float] = None
    status: str = "ACTIVE"
    metadata_json: Optional[dict] = None

class AssetCreate(AssetBase):
    id: str

class AssetRead(AssetBase):
    id: str
    site_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class ZoneBase(BaseModel):
    name: str
    zone_code: Optional[str] = None
    zone_type: str
    description: Optional[str] = None
    severity: ZoneSeverity
    boundary: Optional[dict] = None
    active: bool = True

class ZoneCreate(ZoneBase):
    id: str

class ZoneRead(ZoneBase):
    id: str
    site_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class SensorBase(BaseModel):
    name: str
    sensor_type: str
    status: str = "ACTIVE"
    location: Optional[dict] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    configuration: Optional[dict] = None

class SensorCreate(SensorBase):
    id: str

class SensorRead(SensorBase):
    id: str
    site_id: str
    last_seen_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
''')

print("Updated domain schemas")
