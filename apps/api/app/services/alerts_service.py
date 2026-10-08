from sqlalchemy.orm import Session
from app.repositories.alerts_repository import alerts_repo
from app.infrastructure.db.models import Alert
from typing import List, Optional, Tuple

class AlertService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[Alert]:
        return alerts_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[Alert], int]:
        return alerts_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: Alert) -> Alert:
        obj = alerts_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: Alert, obj_in: dict) -> Alert:
        obj = alerts_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[Alert]:
        obj = alerts_repo.delete(db, id=id)
        db.commit()
        return obj

alerts_service = AlertService()
