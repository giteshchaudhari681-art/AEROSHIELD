from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.extended import IncidentRead, PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.incidents_service import incidents_service
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
def list_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("incident:read"))):
    items, total = incidents_service.list(db, skip=skip, limit=limit)
    out = [IncidentRead.model_validate(i) for i in items]
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)

@router.get("/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("incident:read"))):
    item = incidents_service.get(db, id=incident_id)
    if not item: raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentRead.model_validate(item)
