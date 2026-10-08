from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.api.dependencies import get_db, get_current_user
from app.infrastructure.db.models import User, FusedContact

router = APIRouter()

@router.get("/contacts")
def list_fused_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    site_id: Optional[str] = None,
    limit: int = 100,
    skip: int = 0
):
    # Ensure role is adequate - reuse observation:read or similar for now
    if not current_user.has_permission("observation:read"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    query = db.query(FusedContact)
    if site_id:
        query = query.filter(FusedContact.site_id == site_id)
        
    contacts = query.order_by(FusedContact.reference_time.desc()).offset(skip).limit(limit).all()
    
    result = []
    for c in contacts:
        result.append({
            "fused_contact_id": c.id,
            "site_id": c.site_id,
            "reference_time": c.reference_time.isoformat(),
            "location": c.location, # In real app, parse this
            "altitude_m": c.altitude,
            "speed_mps": c.speed,
            "heading": c.heading,
            "confidence": c.confidence,
            "status": c.status.value,
            "contributing_observations": c.contributing_observation_count,
            "contributing_sensors": c.contributing_sensor_count,
            "conflicts": c.conflicts_json,
            "fusion_reasons": c.fusion_reasons
        })
    return result

@router.get("/contacts/{contact_id}")
def get_fused_contact(
    contact_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.has_permission("observation:read"):
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    c = db.query(FusedContact).filter(FusedContact.id == contact_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Fused contact not found")
        
    return {
        "fused_contact_id": c.id,
        "site_id": c.site_id,
        "reference_time": c.reference_time.isoformat(),
        "location": c.location,
        "altitude_m": c.altitude,
        "speed_mps": c.speed,
        "heading": c.heading,
        "confidence": c.confidence,
        "status": c.status.value,
        "contributing_observations": c.contributing_observation_count,
        "contributing_sensors": c.contributing_sensor_count,
        "conflicts": c.conflicts_json,
        "fusion_reasons": c.fusion_reasons,
        "observations": [
            {
                "observation_id": obs.observation_id,
                "role": obs.contribution_role.value,
                "score": obs.contribution_score
            }
            for obs in c.observations
        ]
    }
