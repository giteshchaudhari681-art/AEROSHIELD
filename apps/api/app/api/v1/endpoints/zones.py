from fastapi import APIRouter, Depends, HTTPException, Query
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

@router.get("/_queries/containing", response_model=PaginatedResponse)
def get_zones_containing(lat: float, lon: float, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("zone:read"))):
    from app.services.digital_twin_service import digital_twin_service
    items = digital_twin_service.find_zones_containing_point(db, lat, lon)
    out = []
    for item in items:
        bound = mapping(to_shape(item.boundary)) if item.boundary else {"type":"Polygon","coordinates":[]}
        out.append(ZoneRead(id=item.id, site_id=item.site_id, name=item.name, zone_code=item.zone_code, description=item.description, zone_type=item.zone_type, 
                    severity=item.severity, boundary=bound, active=item.active, 
                    created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=1, page_size=len(out), total=len(out), items=out)

@router.post("/", response_model=ZoneRead, status_code=201)
def create_zone(site_id: str, zone: ZoneCreate, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("zone:write"))):
    if zones_service.get(db, id=zone.id): raise HTTPException(status_code=409, detail="Zone already exists")
    
    from app.infrastructure.db.models import RestrictedZone
    boundary_wkt = shape(zone.boundary).wkt if zone.boundary else None
    
    obj = RestrictedZone(id=zone.id, site_id=site_id, name=zone.name, zone_code=zone.zone_code, description=zone.description, zone_type=zone.zone_type, 
                         severity=zone.severity, boundary=boundary_wkt, active=zone.active)
    db_obj = zones_service.create(db, obj_in=obj)
    
    bound = mapping(to_shape(db_obj.boundary)) if db_obj.boundary else zone.boundary
    return ZoneRead(id=db_obj.id, site_id=db_obj.site_id, name=db_obj.name, zone_code=db_obj.zone_code, description=db_obj.description, zone_type=db_obj.zone_type, 
                    severity=db_obj.severity, boundary=bound, active=db_obj.active, 
                    created_at=db_obj.created_at, updated_at=db_obj.updated_at)

@router.get("/", response_model=PaginatedResponse)
def list_zones(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("zone:read"))):
    items, total = zones_service.list(db, skip=skip, limit=limit, site_id=site_id)
    out = []
    for item in items:
        bound = mapping(to_shape(item.boundary)) if item.boundary else {"type":"Polygon","coordinates":[]}
        out.append(ZoneRead(id=item.id, site_id=item.site_id, name=item.name, zone_code=item.zone_code, description=item.description, zone_type=item.zone_type, 
                    severity=item.severity, boundary=bound, active=item.active, 
                    created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)

@router.get("/{zone_id}", response_model=ZoneRead)
def get_zone(zone_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("zone:read"))):
    item = zones_service.get(db, id=zone_id)
    if not item: raise HTTPException(status_code=404, detail="Zone not found")
    bound = mapping(to_shape(item.boundary)) if item.boundary else {"type":"Polygon","coordinates":[]}
    return ZoneRead(id=item.id, site_id=item.site_id, name=item.name, zone_code=item.zone_code, description=item.description, zone_type=item.zone_type, 
                    severity=item.severity, boundary=bound, active=item.active, 
                    created_at=item.created_at, updated_at=item.updated_at)
