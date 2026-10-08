from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import datetime
from app.schemas.extended import ObservationRead, PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.observations_service import observations_service
from shapely.geometry import mapping
from geoalchemy2.shape import to_shape
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.post("/", status_code=201)
def ingest_observation(
    sensor_id: str,
    payload: Dict[str, Any],
    correlation_id: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_operator: Operator = Depends(RequirePermission("observation:write"))
):
    try:
        created = observations_service.ingest_raw(db, sensor_id=sensor_id, raw_payload=payload, correlation_id=correlation_id)
        if not created:
            # Idempotency hit or no observations yielded
            return {"status": "ok", "message": "Idempotent or empty"}
            
        return {"status": "ok", "ingested": len(created)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=ObservationRead)
def get_observation(id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("observation:read"))):
    item = observations_service.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Observation not found")
        
    loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
    return ObservationRead(
        id=item.id, sensor_id=item.sensor_id, track_id=item.track_id,
        sensor_type=item.sensor_type, observation_type=item.observation_type,
        observed_at=item.observed_at, received_at=item.received_at,
        location=loc, altitude=item.altitude, speed=item.speed,
        heading=item.heading, confidence=item.confidence, classification=item.classification,
        created_at=item.created_at
    )

@router.get("/", response_model=PaginatedResponse)
def list_observations(
    sensor_id: Optional[str] = None, 
    observation_type: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_operator: Operator = Depends(RequirePermission("observation:read"))
):
    filters = {}
    if sensor_id: filters["sensor_id"] = sensor_id
    if observation_type: filters["observation_type"] = observation_type
    
    if start_time and end_time:
        items, total = observations_service.get_by_time_range(db, start_time, end_time, skip=skip, limit=limit, **filters)
    else:
        items, total = observations_service.list(db, skip=skip, limit=limit, **filters)
        
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(ObservationRead(id=item.id, sensor_id=item.sensor_id, track_id=item.track_id,
                                   sensor_type=item.sensor_type, observation_type=item.observation_type, 
                                   observed_at=item.observed_at, received_at=item.received_at,
                                   location=loc, altitude=item.altitude, speed=item.speed,
                                   heading=item.heading, confidence=item.confidence, classification=item.classification,
                                   created_at=item.created_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)
