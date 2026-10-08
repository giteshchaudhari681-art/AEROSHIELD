from sqlalchemy.orm import Session
from app.repositories.sites_repository import sites_repo
from app.infrastructure.db.models import Site
from typing import List, Optional, Tuple

class SiteService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[Site]:
        return sites_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[Site], int]:
        return sites_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: Site) -> Site:
        obj = sites_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: Site, obj_in: dict) -> Site:
        obj = sites_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[Site]:
        obj = sites_repo.delete(db, id=id)
        db.commit()
        return obj

sites_service = SiteService()
