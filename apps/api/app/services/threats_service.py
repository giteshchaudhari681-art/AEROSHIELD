from sqlalchemy.orm import Session
from app.repositories.threats_repository import threats_repo
from app.infrastructure.db.models import ThreatAssessment
from typing import List, Optional, Tuple

class ThreatAssessmentService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[ThreatAssessment]:
        return threats_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[ThreatAssessment], int]:
        return threats_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: ThreatAssessment) -> ThreatAssessment:
        obj = threats_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: ThreatAssessment, obj_in: dict) -> ThreatAssessment:
        obj = threats_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[ThreatAssessment]:
        obj = threats_repo.delete(db, id=id)
        db.commit()
        return obj

threats_service = ThreatAssessmentService()
