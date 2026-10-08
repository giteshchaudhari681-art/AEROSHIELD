from sqlalchemy.orm import Session
from app.repositories.incidents_repository import incidents_repo
from app.infrastructure.db.models import Incident
from typing import List, Optional, Tuple

class IncidentService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[Incident]:
        return incidents_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[Incident], int]:
        return incidents_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: Incident) -> Incident:
        obj = incidents_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: Incident, obj_in: dict) -> Incident:
        obj = incidents_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[Incident]:
        obj = incidents_repo.delete(db, id=id)
        db.commit()
        return obj

incidents_service = IncidentService()
