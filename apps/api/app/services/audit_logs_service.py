from sqlalchemy.orm import Session
from app.repositories.audit_logs_repository import audit_logs_repo
from app.infrastructure.db.models import AuditLog
from typing import List, Optional, Tuple

class AuditLogService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[AuditLog]:
        return audit_logs_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[AuditLog], int]:
        return audit_logs_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: AuditLog) -> AuditLog:
        obj = audit_logs_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: AuditLog, obj_in: dict) -> AuditLog:
        obj = audit_logs_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[AuditLog]:
        obj = audit_logs_repo.delete(db, id=id)
        db.commit()
        return obj

audit_logs_service = AuditLogService()
