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
