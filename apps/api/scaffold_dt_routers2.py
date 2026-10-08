import os

base_dir = "d:/SEVA/apps/api/app/api/v1/endpoints"

routers = {
    "sites": """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.domain import SiteCreate, SiteRead, AssetRead, ZoneRead
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
    
    obj = Site(id=site.id, name=site.name, site_code=site.site_code, site_type=site.site_type, status=site.status, 
               description=site.description, location=location_wkt, boundary=boundary_wkt)
    db_obj = sites_service.create(db, obj_in=obj)
    
    loc_geojson = mapping(to_shape(db_obj.location)) if db_obj.location else site.location
    bound_geojson = mapping(to_shape(db_obj.boundary)) if db_obj.boundary else site.boundary
    
    return SiteRead(id=db_obj.id, name=db_obj.name, site_code=db_obj.site_code, site_type=db_obj.site_type, status=db_obj.status, 
                    description=db_obj.description, location=loc_geojson, boundary=bound_geojson, 
                    created_at=db_obj.created_at, updated_at=db_obj.updated_at)

@router.get("/", response_model=PaginatedResponse)
def list_sites(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("site:read"))):
    items, total = sites_service.list(db, skip=skip, limit=limit)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        bound = mapping(to_shape(item.boundary)) if getattr(item, 'boundary', None) else None
        out.append(SiteRead(id=item.id, name=item.name, site_code=item.site_code, site_type=item.site_type, status=item.status,
                            description=item.description, location=loc, boundary=bound,
                            created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)

@router.get("/{site_id}", response_model=SiteRead)
def get_site(site_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("site:read"))):
    item = sites_service.get(db, id=site_id)
    if not item: raise HTTPException(status_code=404, detail="Site not found")
    loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
    bound = mapping(to_shape(item.boundary)) if getattr(item, 'boundary', None) else None
    return SiteRead(id=item.id, name=item.name, site_code=item.site_code, site_type=item.site_type, status=item.status,
                    description=item.description, location=loc, boundary=bound,
                    created_at=item.created_at, updated_at=item.updated_at)

@router.get("/{site_id}/context")
def get_site_context(site_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("site:read"))):
    from app.services.digital_twin_service import digital_twin_service
    ctx = digital_twin_service.get_site_context(db, site_id)
    if not ctx: raise HTTPException(status_code=404, detail="Site not found")
    
    site_item = ctx['site']
    loc = mapping(to_shape(site_item.location)) if site_item.location else {"type":"Point","coordinates":[0,0]}
    bound = mapping(to_shape(site_item.boundary)) if getattr(site_item, 'boundary', None) else None
    
    out_assets = []
    for item in ctx['assets']:
        aloc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out_assets.append(AssetRead(id=item.id, site_id=item.site_id, name=item.name, asset_code=item.asset_code, asset_type=item.asset_type, 
                     criticality=item.criticality, operational_status=item.operational_status, location=aloc, protection_radius=item.protection_radius, 
                     status=item.status, description=item.description, metadata_json=item.metadata_json,
                     created_at=item.created_at, updated_at=item.updated_at))
                     
    out_zones = []
    for item in ctx['restricted_zones']:
        zbound = mapping(to_shape(item.boundary)) if item.boundary else {"type":"Polygon","coordinates":[]}
        out_zones.append(ZoneRead(id=item.id, site_id=item.site_id, name=item.name, zone_code=item.zone_code, zone_type=item.zone_type, 
                    description=item.description, severity=item.severity, boundary=zbound, active=item.active, 
                    created_at=item.created_at, updated_at=item.updated_at))
                    
    return {
        "site": SiteRead(id=site_item.id, name=site_item.name, site_code=site_item.site_code, site_type=site_item.site_type, status=site_item.status,
                    description=site_item.description, location=loc, boundary=bound,
                    created_at=site_item.created_at, updated_at=site_item.updated_at),
        "assets": out_assets,
        "restricted_zones": out_zones
    }
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
"""
}

for name, content in routers.items():
    filepath = f"{base_dir}/{name}.py"
    with open(filepath, "w") as f:
        f.write(content)

print("Scaffolded DT protected routers.")
