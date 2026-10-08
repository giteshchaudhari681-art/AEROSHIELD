from sqlalchemy.orm import Session
from app.repositories.observations_repository import observations_repo
from app.infrastructure.db.models import SensorObservation
from typing import List, Optional, Tuple

class SensorObservationService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[SensorObservation]:
        return observations_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[SensorObservation], int]:
        return observations_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: SensorObservation) -> SensorObservation:
        obj = observations_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: SensorObservation, obj_in: dict) -> SensorObservation:
        obj = observations_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[SensorObservation]:
        obj = observations_repo.delete(db, id=id)
        db.commit()
        return obj

observations_service = SensorObservationService()
