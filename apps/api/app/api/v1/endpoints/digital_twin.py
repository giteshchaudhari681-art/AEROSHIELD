from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_db
from app.api.dependencies.auth import RequirePermission, Operator
from app.schemas.extended import PaginatedResponse
from app.schemas.domain import AssetRead, ZoneRead
from shapely.geometry import mapping
from geoalchemy2.shape import to_shape

router = APIRouter()

@router.get("/assets/_queries/nearby", response_model=PaginatedResponse)
def get_assets_nearby(lat: float, lon: float, radius_m: float = 1000.0, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("asset:read"))):
    from app.services.digital_twin_service import digital_twin_service
    items = digital_twin_service.find_assets_near_point(db, lat, lon, radius_m)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(AssetRead(id=item.id, site_id=item.site_id, name=item.name, asset_code=item.asset_code, asset_type=item.asset_type, 
                     criticality=item.criticality, operational_status=item.operational_status, location=loc, protection_radius=item.protection_radius, 
                     status=item.status, description=item.description, metadata_json=item.metadata_json,
                     created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=1, page_size=len(out), total=len(out), items=out)
    
@router.get("/assets/_queries/inside-zone", response_model=PaginatedResponse)
def get_assets_inside_zone(zone_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("asset:read"))):
    from app.services.digital_twin_service import digital_twin_service
    items = digital_twin_service.find_assets_inside_zone(db, zone_id)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(AssetRead(id=item.id, site_id=item.site_id, name=item.name, asset_code=item.asset_code, asset_type=item.asset_type, 
                     criticality=item.criticality, operational_status=item.operational_status, location=loc, protection_radius=item.protection_radius, 
                     status=item.status, description=item.description, metadata_json=item.metadata_json,
                     created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=1, page_size=len(out), total=len(out), items=out)

@router.get("/zones/_queries/containing", response_model=PaginatedResponse)
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
