from fastapi import APIRouter, Depends, HTTPException, Query
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
