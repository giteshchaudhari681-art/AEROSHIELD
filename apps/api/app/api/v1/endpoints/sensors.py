from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.domain import SensorCreate, SensorRead
from app.schemas.extended import PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.sensors_service import sensors_service
from shapely.geometry import shape, mapping
from geoalchemy2.shape import to_shape
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.post("/", response_model=SensorRead, status_code=201)
def create_sensor(site_id: str, sensor: SensorCreate, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("sensor:write"))):
    if sensors_service.get(db, id=sensor.id): raise HTTPException(status_code=409, detail="Sensor already exists")
    
    from app.infrastructure.db.models import Sensor
    location_wkt = shape(sensor.location).wkt if sensor.location else None
    
    obj = Sensor(id=sensor.id, site_id=site_id, name=sensor.name, sensor_type=sensor.sensor_type, 
                 location=location_wkt, status=sensor.status, manufacturer=sensor.manufacturer, 
                 model=sensor.model, configuration=sensor.configuration)
    db_obj = sensors_service.create(db, obj_in=obj)
    
    loc = mapping(to_shape(db_obj.location)) if db_obj.location else sensor.location
    return SensorRead(id=db_obj.id, site_id=db_obj.site_id, name=db_obj.name, sensor_type=db_obj.sensor_type, 
                      location=loc, status=db_obj.status, manufacturer=db_obj.manufacturer, 
                      model=db_obj.model, configuration=db_obj.configuration, last_seen_at=db_obj.last_seen_at,
                      created_at=db_obj.created_at, updated_at=db_obj.updated_at)

@router.get("/", response_model=PaginatedResponse)
def list_sensors(site_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("sensor:read"))):
    items, total = sensors_service.list(db, skip=skip, limit=limit, site_id=site_id)
    out = []
    for item in items:
        loc = mapping(to_shape(item.location)) if item.location else {"type":"Point","coordinates":[0,0]}
        out.append(SensorRead(id=item.id, site_id=item.site_id, name=item.name, sensor_type=item.sensor_type, 
                      location=loc, status=item.status, manufacturer=item.manufacturer, 
                      model=item.model, configuration=item.configuration, last_seen_at=item.last_seen_at,
                      created_at=item.created_at, updated_at=item.updated_at))
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)
