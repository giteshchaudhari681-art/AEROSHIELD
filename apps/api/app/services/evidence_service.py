from sqlalchemy.orm import Session
from app.repositories.evidence_repository import evidence_repo
from app.infrastructure.db.models import Evidence
from typing import List, Optional, Tuple

class EvidenceService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[Evidence]:
        return evidence_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[Evidence], int]:
        return evidence_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: Evidence) -> Evidence:
        obj = evidence_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: Evidence, obj_in: dict) -> Evidence:
        obj = evidence_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[Evidence]:
        obj = evidence_repo.delete(db, id=id)
        db.commit()
        return obj

evidence_service = EvidenceService()
