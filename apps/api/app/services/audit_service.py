from sqlalchemy.orm import Session
from app.infrastructure.db.models import AuditLog
import uuid
from typing import Optional, Dict, Any

class AuditService:
    @staticmethod
    def log(db: Session, actor_id: str, action: str, entity_type: Optional[str] = None, entity_id: Optional[str] = None, metadata_json: Optional[Dict[str, Any]] = None, ip_address: Optional[str] = None):
        entry = AuditLog(
            id=str(uuid.uuid4()),
            actor_id=actor_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            metadata_json=metadata_json,
            ip_address=ip_address
        )
        db.add(entry)
        db.commit()

audit_service = AuditService()
