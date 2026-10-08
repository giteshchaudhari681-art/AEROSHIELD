from sqlalchemy.orm import Session
from app.repositories.sensors_repository import sensors_repo
from app.infrastructure.db.models import Sensor
from typing import List, Optional, Tuple

class SensorService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[Sensor]:
        return sensors_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[Sensor], int]:
        return sensors_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: Sensor) -> Sensor:
        obj = sensors_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: Sensor, obj_in: dict) -> Sensor:
        obj = sensors_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[Sensor]:
        obj = sensors_repo.delete(db, id=id)
        db.commit()
        return obj

sensors_service = SensorService()
