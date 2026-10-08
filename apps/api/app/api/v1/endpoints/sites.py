from fastapi import APIRouter, Depends, HTTPException, Query
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
