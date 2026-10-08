from fastapi import APIRouter, Depends, HTTPException, Query
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
