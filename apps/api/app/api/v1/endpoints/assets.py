from fastapi import APIRouter, Depends, HTTPException, Query
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

@router.get("/_queries/nearby", response_model=PaginatedResponse)
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
    
@router.get("/_queries/inside-zone", response_model=PaginatedResponse)
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

@router.post("/", response_model=AssetRead, status_code=201)
def create_asset(site_id: str, asset: AssetCreate, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("asset:write"))):
    if assets_service.get(db, id=asset.id): raise HTTPException(status_code=409, detail="Asset already exists")
    
    from app.infrastructure.db.models import CriticalAsset
    location_wkt = shape(asset.location).wkt if asset.location else None
    
    obj = CriticalAsset(id=asset.id, site_id=site_id, name=asset.name, asset_code=asset.asset_code, asset_type=asset.asset_type, 
                        criticality=asset.criticality, operational_status=asset.operational_status, location=location_wkt, protection_radius=asset.protection_radius, 
                        status=asset.status, description=asset.description, metadata_json=asset.metadata_json)
    db_obj = assets_service.create(db, obj_in=obj)
    
    loc = mapping(to_shape(db_obj.location)) if db_obj.location else asset.location
    return AssetRead(id=db_obj.id, site_id=db_obj.site_id, name=db_obj.name, asset_code=db_obj.asset_code, asset_type=db_obj.asset_type, 
                     criticality=db_obj.criticality, operational_status=db_obj.operational_status, location=loc, protection_radius=db_obj.protection_radius, 
                     status=db_obj.status, description=db_obj.description, metadata_json=db_obj.metadata_json,
                     created_at=db_obj.created_at, updated_at=db_obj.updated_at)

@router.get("/", response_model=PaginatedResponse)
def list_assets(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("asset:read"))):
    items, total = assets_service.list(db, skip=skip, limit=limit, site_id=site_id)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(AssetRead(id=item.id, site_id=item.site_id, name=item.name, asset_code=item.asset_code, asset_type=item.asset_type, 
                     criticality=item.criticality, operational_status=item.operational_status, location=loc, protection_radius=item.protection_radius, 
                     status=item.status, description=item.description, metadata_json=item.metadata_json,
                     created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)

@router.get("/{asset_id}", response_model=AssetRead)
def get_asset(asset_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("asset:read"))):
    item = assets_service.get(db, id=asset_id)
    if not item: raise HTTPException(status_code=404, detail="Asset not found")
    loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
    return AssetRead(id=item.id, site_id=item.site_id, name=item.name, asset_code=item.asset_code, asset_type=item.asset_type, 
                     criticality=item.criticality, operational_status=item.operational_status, location=loc, protection_radius=item.protection_radius, 
                     status=item.status, description=item.description, metadata_json=item.metadata_json,
                     created_at=item.created_at, updated_at=item.updated_at)
