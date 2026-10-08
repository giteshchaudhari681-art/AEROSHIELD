from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .sensor import SensorType

# Base schemas

class SiteBase(BaseModel):
    name: str
    description: Optional[str] = None
    site_type: str
    status: str = "ACTIVE"
    # Keeping location as dict/GeoJSON for simple API interactions
    location: Dict[str, Any] # e.g. {"type": "Point", "coordinates": [lon, lat]}
    boundary: Optional[Dict[str, Any]] = None

class SiteCreate(SiteBase):
    id: str

class SiteRead(SiteBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class AssetBase(BaseModel):
    name: str
    asset_type: str
    description: Optional[str] = None
    criticality: str
    location: Dict[str, Any]
    protection_radius: Optional[float] = None
    status: str = "ACTIVE"
    metadata_json: Optional[Dict[str, Any]] = None

class AssetCreate(AssetBase):
    id: str

class AssetRead(AssetBase):
    id: str
    site_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ZoneBase(BaseModel):
    name: str
    zone_type: str
    boundary: Dict[str, Any]
    severity: str
    active: bool = True

class ZoneCreate(ZoneBase):
    id: str

class ZoneRead(ZoneBase):
    id: str
    site_id: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class SensorBase(BaseModel):
    name: str
    sensor_type: str
    status: str = "ACTIVE"
    location: Dict[str, Any]
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None

class SensorCreate(SensorBase):
    id: str

class SensorRead(SensorBase):
    id: str
    site_id: str
    last_seen_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
