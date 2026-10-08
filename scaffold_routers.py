import os

base_dir = "d:/SEVA/apps/api/app/api/v1/endpoints"

routers = {
    "sites": """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.domain import SiteCreate, SiteRead
from app.schemas.extended import PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.sites_service import sites_service
from shapely.geometry import shape, mapping
from geoalchemy2.shape import to_shape
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.post("/", response_model=SiteRead, status_code=201)
def create_site(site: SiteCreate, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("site:write"))):
    if sites_service.get(db, id=site.id):
        raise HTTPException(status_code=409, detail="Site already exists")
    
    from app.infrastructure.db.models import Site
    location_wkt = shape(site.location).wkt if site.location else None
    boundary_wkt = shape(site.boundary).wkt if site.boundary else None
    
    obj = Site(id=site.id, name=site.name, site_type=site.site_type, status=site.status, 
               description=site.description, location=location_wkt, boundary=boundary_wkt)
    db_obj = sites_service.create(db, obj_in=obj)
    
    loc_geojson = mapping(to_shape(db_obj.location)) if db_obj.location else site.location
    bound_geojson = mapping(to_shape(db_obj.boundary)) if db_obj.boundary else site.boundary
    
    return SiteRead(id=db_obj.id, name=db_obj.name, site_type=db_obj.site_type, status=db_obj.status, 
                    description=db_obj.description, location=loc_geojson, boundary=bound_geojson, 
                    created_at=db_obj.created_at, updated_at=db_obj.updated_at)

@router.get("/", response_model=PaginatedResponse)
def list_sites(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("site:read"))):
    items, total = sites_service.list(db, skip=skip, limit=limit)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        bound = mapping(to_shape(item.boundary)) if getattr(item, 'boundary', None) else None
        out.append(SiteRead(id=item.id, name=item.name, site_type=item.site_type, status=item.status,
                            description=item.description, location=loc, boundary=bound,
                            created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)

@router.get("/{site_id}", response_model=SiteRead)
def get_site(site_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("site:read"))):
    item = sites_service.get(db, id=site_id)
    if not item: raise HTTPException(status_code=404, detail="Site not found")
    loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
    bound = mapping(to_shape(item.boundary)) if getattr(item, 'boundary', None) else None
    return SiteRead(id=item.id, name=item.name, site_type=item.site_type, status=item.status,
                    description=item.description, location=loc, boundary=bound,
                    created_at=item.created_at, updated_at=item.updated_at)
""",
    "assets": """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.domain import AssetCreate, AssetRead
from app.schemas.extended import PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.assets_service import assets_service
from shapely.geometry import shape, mapping
from geoalchemy2.shape import to_shape
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.post("/", response_model=AssetRead, status_code=201)
def create_asset(site_id: str, asset: AssetCreate, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("asset:write"))):
    if assets_service.get(db, id=asset.id): raise HTTPException(status_code=409, detail="Asset already exists")
    
    from app.infrastructure.db.models import CriticalAsset
    location_wkt = shape(asset.location).wkt if asset.location else None
    
    obj = CriticalAsset(id=asset.id, site_id=site_id, name=asset.name, asset_type=asset.asset_type, 
                        criticality=asset.criticality, location=location_wkt, protection_radius=asset.protection_radius, 
                        status=asset.status, description=asset.description, metadata_json=asset.metadata_json)
    db_obj = assets_service.create(db, obj_in=obj)
    
    loc = mapping(to_shape(db_obj.location)) if db_obj.location else asset.location
    return AssetRead(id=db_obj.id, site_id=db_obj.site_id, name=db_obj.name, asset_type=db_obj.asset_type, 
                     criticality=db_obj.criticality, location=loc, protection_radius=db_obj.protection_radius, 
                     status=db_obj.status, description=db_obj.description, metadata_json=db_obj.metadata_json,
                     created_at=db_obj.created_at, updated_at=db_obj.updated_at)

@router.get("/", response_model=PaginatedResponse)
def list_assets(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("asset:read"))):
    items, total = assets_service.list(db, skip=skip, limit=limit, site_id=site_id)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(AssetRead(id=item.id, site_id=item.site_id, name=item.name, asset_type=item.asset_type, 
                     criticality=item.criticality, location=loc, protection_radius=item.protection_radius, 
                     status=item.status, description=item.description, metadata_json=item.metadata_json,
                     created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)
""",
    "zones": """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.domain import ZoneCreate, ZoneRead
from app.schemas.extended import PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.zones_service import zones_service
from shapely.geometry import shape, mapping
from geoalchemy2.shape import to_shape
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.post("/", response_model=ZoneRead, status_code=201)
def create_zone(site_id: str, zone: ZoneCreate, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("zone:write"))):
    if zones_service.get(db, id=zone.id): raise HTTPException(status_code=409, detail="Zone already exists")
    
    from app.infrastructure.db.models import RestrictedZone
    boundary_wkt = shape(zone.boundary).wkt if zone.boundary else None
    
    obj = RestrictedZone(id=zone.id, site_id=site_id, name=zone.name, zone_type=zone.zone_type, 
                         severity=zone.severity, boundary=boundary_wkt, active=zone.active)
    db_obj = zones_service.create(db, obj_in=obj)
    
    bound = mapping(to_shape(db_obj.boundary)) if db_obj.boundary else zone.boundary
    return ZoneRead(id=db_obj.id, site_id=db_obj.site_id, name=db_obj.name, zone_type=db_obj.zone_type, 
                    severity=db_obj.severity, boundary=bound, active=db_obj.active, 
                    created_at=db_obj.created_at, updated_at=db_obj.updated_at)

@router.get("/", response_model=PaginatedResponse)
def list_zones(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("zone:read"))):
    items, total = zones_service.list(db, skip=skip, limit=limit, site_id=site_id)
    out = []
    for item in items:
        bound = mapping(to_shape(item.boundary)) if item.boundary else {"type":"Polygon","coordinates":[]}
        out.append(ZoneRead(id=item.id, site_id=item.site_id, name=item.name, zone_type=item.zone_type, 
                    severity=item.severity, boundary=bound, active=item.active, 
                    created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)
""",
    "sensors": """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.domain import SensorCreate, SensorRead
from app.schemas.extended import PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.sensors_service import sensors_service
from shapely.geometry import shape, mapping
from geoalchemy2.shape import to_shape
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.post("/", response_model=SensorRead, status_code=201)
def create_sensor(site_id: str, sensor: SensorCreate, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("sensor:write"))):
    if sensors_service.get(db, id=sensor.id): raise HTTPException(status_code=409, detail="Sensor already exists")
    
    from app.infrastructure.db.models import Sensor
    location_wkt = shape(sensor.location).wkt if sensor.location else None
    
    obj = Sensor(id=sensor.id, site_id=site_id, name=sensor.name, sensor_type=sensor.sensor_type, 
                 location=location_wkt, status=sensor.status, manufacturer=sensor.manufacturer, 
                 model=sensor.model, configuration=sensor.configuration)
    db_obj = sensors_service.create(db, obj_in=obj)
    
    loc = mapping(to_shape(db_obj.location)) if db_obj.location else sensor.location
    return SensorRead(id=db_obj.id, site_id=db_obj.site_id, name=db_obj.name, sensor_type=db_obj.sensor_type, 
                      location=loc, status=db_obj.status, manufacturer=db_obj.manufacturer, 
                      model=db_obj.model, configuration=db_obj.configuration, last_seen_at=db_obj.last_seen_at,
                      created_at=db_obj.created_at, updated_at=db_obj.updated_at)

@router.get("/", response_model=PaginatedResponse)
def list_sensors(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("sensor:read"))):
    items, total = sensors_service.list(db, skip=skip, limit=limit, site_id=site_id)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(SensorRead(id=item.id, site_id=item.site_id, name=item.name, sensor_type=item.sensor_type, 
                      location=loc, status=item.status, manufacturer=item.manufacturer, 
                      model=item.model, configuration=item.configuration, last_seen_at=item.last_seen_at,
                      created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)
""",
    "tracks": """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.extended import TrackRead, PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.tracks_service import tracks_service
from shapely.geometry import mapping
from geoalchemy2.shape import to_shape
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
def list_tracks(site_id: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("track:read"))):
    filters = {}
    if site_id: filters["site_id"] = site_id
    items, total = tracks_service.list(db, skip=skip, limit=limit, **filters)
    out = []
    for item in items:
        loc = mapping(to_shape(item.current_location)) if item.current_location else {"type":"Point","coordinates":[0,0]}
        out.append(TrackRead(id=item.id, site_id=item.site_id, track_identifier=item.track_identifier,
                             classification=item.classification, status=item.status, confidence=item.confidence,
                             current_location=loc, current_altitude=item.current_altitude, current_speed=item.current_speed,
                             current_heading=item.current_heading, first_seen_at=item.first_seen_at, last_seen_at=item.last_seen_at,
                             created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)

@router.get("/{track_id}", response_model=TrackRead)
def get_track(track_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("track:read"))):
    item = tracks_service.get(db, id=track_id)
    if not item: raise HTTPException(status_code=404, detail="Track not found")
    loc = mapping(to_shape(item.current_location)) if item.current_location else {"type":"Point","coordinates":[0,0]}
    return TrackRead(id=item.id, site_id=item.site_id, track_identifier=item.track_identifier,
                     classification=item.classification, status=item.status, confidence=item.confidence,
                     current_location=loc, current_altitude=item.current_altitude, current_speed=item.current_speed,
                     current_heading=item.current_heading, first_seen_at=item.first_seen_at, last_seen_at=item.last_seen_at,
                     created_at=item.created_at, updated_at=item.updated_at)
""",
    "observations": """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.extended import ObservationRead, PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.observations_service import observations_service
from shapely.geometry import mapping
from geoalchemy2.shape import to_shape
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
def list_observations(sensor_id: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("observation:read"))):
    filters = {}
    if sensor_id: filters["sensor_id"] = sensor_id
    items, total = observations_service.list(db, skip=skip, limit=limit, **filters)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(ObservationRead(id=item.id, sensor_id=item.sensor_id, track_id=item.track_id,
                                   sensor_type=item.sensor_type, observed_at=item.observed_at,
                                   location=loc, altitude=item.altitude, speed=item.speed,
                                   heading=item.heading, confidence=item.confidence, classification=item.classification,
                                   created_at=item.created_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)
""",
    "alerts": """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.extended import AlertRead, PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.alerts_service import alerts_service
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
def list_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("alert:read"))):
    items, total = alerts_service.list(db, skip=skip, limit=limit)
    out = [AlertRead.model_validate(i) for i in items]
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)

@router.get("/{alert_id}", response_model=AlertRead)
def get_alert(alert_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("alert:read"))):
    item = alerts_service.get(db, id=alert_id)
    if not item: raise HTTPException(status_code=404, detail="Alert not found")
    return AlertRead.model_validate(item)
""",
    "incidents": """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.extended import IncidentRead, PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.incidents_service import incidents_service
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
def list_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("incident:read"))):
    items, total = incidents_service.list(db, skip=skip, limit=limit)
    out = [IncidentRead.model_validate(i) for i in items]
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)

@router.get("/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("incident:read"))):
    item = incidents_service.get(db, id=incident_id)
    if not item: raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentRead.model_validate(item)
"""
}

for name, content in routers.items():
    filepath = f"{base_dir}/{name}.py"
    with open(filepath, "w") as f:
        f.write(content)

print("Scaffolded protected routers.")
