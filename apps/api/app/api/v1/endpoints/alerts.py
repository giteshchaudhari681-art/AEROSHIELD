from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.extended import AlertRead, PaginatedResponse
from app.infrastructure.db.session import get_db
from app.services.alerts_service import alerts_service
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.get("/", response_model=PaginatedResponse)
def list_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("alert:read"))):
    items, total = alerts_service.list(db, skip=skip, limit=limit)
    out = [AlertRead.model_validate(i) for i in items]
    return PaginatedResponse(page=skip//limit + 1, page_size=limit, total=total, items=out)

@router.get("/{alert_id}", response_model=AlertRead)
def get_alert(alert_id: str, db: Session = Depends(get_db), current_operator: Operator = Depends(RequirePermission("alert:read"))):
    item = alerts_service.get(db, id=alert_id)
    if not item: raise HTTPException(status_code=404, detail="Alert not found")
    return AlertRead.model_validate(item)
