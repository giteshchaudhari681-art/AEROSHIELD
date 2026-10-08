from sqlalchemy.orm import Session
from app.repositories.zones_repository import zones_repo
from app.infrastructure.db.models import RestrictedZone
from typing import List, Optional, Tuple

class RestrictedZoneService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[RestrictedZone]:
        return zones_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[RestrictedZone], int]:
        return zones_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: RestrictedZone) -> RestrictedZone:
        obj = zones_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: RestrictedZone, obj_in: dict) -> RestrictedZone:
        obj = zones_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[RestrictedZone]:
        obj = zones_repo.delete(db, id=id)
        db.commit()
        return obj

zones_service = RestrictedZoneService()
