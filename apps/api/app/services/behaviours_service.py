from sqlalchemy.orm import Session
from app.repositories.behaviours_repository import behaviours_repo
from app.infrastructure.db.models import BehaviourEvent
from typing import List, Optional, Tuple

class BehaviourEventService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[BehaviourEvent]:
        return behaviours_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[BehaviourEvent], int]:
        return behaviours_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: BehaviourEvent) -> BehaviourEvent:
        obj = behaviours_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: BehaviourEvent, obj_in: dict) -> BehaviourEvent:
        obj = behaviours_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[BehaviourEvent]:
        obj = behaviours_repo.delete(db, id=id)
        db.commit()
        return obj

behaviours_service = BehaviourEventService()
