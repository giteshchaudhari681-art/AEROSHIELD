import os

base_dir = 'd:/SEVA/apps/api/app/api/v1/endpoints'

# Sites Context
with open(f'{base_dir}/sites.py', 'a') as f:
    f.write('''
@router.get("/{site_id}/context")
def get_site_context(site_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("site:read"))):
    from app.services.digital_twin_service import digital_twin_service
    from geoalchemy2.shape import to_shape
    from shapely.geometry import mapping
    from app.schemas.domain import SiteRead, AssetRead, ZoneRead
    
    ctx = digital_twin_service.get_site_context(db, site_id)
    if not ctx: raise HTTPException(status_code=404, detail="Site not found")
    
    site_item = ctx['site']
    loc = mapping(to_shape(site_item.location)) if site_item.location else {"type":"Point","coordinates":[0,0]}
    bound = mapping(to_shape(site_item.boundary)) if getattr(site_item, 'boundary', None) else None
    
    out_assets = []
    for item in ctx['assets']:
        aloc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out_assets.append(AssetRead(id=item.id, site_id=item.site_id, name=item.name, asset_type=item.asset_type, 
                     criticality=item.criticality, location=aloc, protection_radius=item.protection_radius, 
                     status=item.status, description=item.description, metadata_json=item.metadata_json,
                     created_at=item.created_at, updated_at=item.updated_at))
                     
    out_zones = []
    for item in ctx['restricted_zones']:
        zbound = mapping(to_shape(item.boundary)) if item.boundary else {"type":"Polygon","coordinates":[]}
        out_zones.append(ZoneRead(id=item.id, site_id=item.site_id, name=item.name, zone_type=item.zone_type, 
                    severity=item.severity, boundary=zbound, active=item.active, 
                    created_at=item.created_at, updated_at=item.updated_at))
                    
    return {
        "site": SiteRead(id=site_item.id, name=site_item.name, site_type=site_item.site_type, status=site_item.status,
                    description=site_item.description, location=loc, boundary=bound,
                    created_at=site_item.created_at, updated_at=site_item.updated_at),
        "assets": out_assets,
        "restricted_zones": out_zones
    }
''')

# Assets Nearby
with open(f'{base_dir}/assets.py', 'a') as f:
    f.write('''
@router.get("/_queries/nearby", response_model=PaginatedResponse)
def get_assets_nearby(lat: float, lon: float, radius_m: float = 1000.0, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("asset:read"))):
    from app.services.digital_twin_service import digital_twin_service
    from geoalchemy2.shape import to_shape
    from shapely.geometry import mapping
    
    items = digital_twin_service.find_assets_near_point(db, lat, lon, radius_m)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(AssetRead(id=item.id, site_id=item.site_id, name=item.name, asset_type=item.asset_type, 
                     criticality=item.criticality, location=loc, protection_radius=item.protection_radius, 
                     status=item.status, description=item.description, metadata_json=item.metadata_json,
                     created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=1, page_size=len(out), total=len(out), items=out)
    
@router.get("/_queries/inside-zone", response_model=PaginatedResponse)
def get_assets_inside_zone(zone_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("asset:read"))):
    from app.services.digital_twin_service import digital_twin_service
    from geoalchemy2.shape import to_shape
    from shapely.geometry import mapping
    
    items = digital_twin_service.find_assets_inside_zone(db, zone_id)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(AssetRead(id=item.id, site_id=item.site_id, name=item.name, asset_type=item.asset_type, 
                     criticality=item.criticality, location=loc, protection_radius=item.protection_radius, 
                     status=item.status, description=item.description, metadata_json=item.metadata_json,
                     created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=1, page_size=len(out), total=len(out), items=out)
''')

# Zones Containing
with open(f'{base_dir}/zones.py', 'a') as f:
    f.write('''
@router.get("/_queries/containing", response_model=PaginatedResponse)
def get_zones_containing(lat: float, lon: float, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("zone:read"))):
    from app.services.digital_twin_service import digital_twin_service
    from geoalchemy2.shape import to_shape
    from shapely.geometry import mapping
    
    items = digital_twin_service.find_zones_containing_point(db, lat, lon)
    out = []
    for item in items:
        bound = mapping(to_shape(item.boundary)) if item.boundary else {"type":"Polygon","coordinates":[]}
        out.append(ZoneRead(id=item.id, site_id=item.site_id, name=item.name, zone_type=item.zone_type, 
                    severity=item.severity, boundary=bound, active=item.active, 
                    created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=1, page_size=len(out), total=len(out), items=out)
''')

print('Injected contextual routes')
