from sqlalchemy.orm import Session
from app.repositories.assets_repository import assets_repo
from app.infrastructure.db.models import CriticalAsset
from typing import List, Optional, Tuple

class CriticalAssetService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[CriticalAsset]:
        return assets_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[CriticalAsset], int]:
        return assets_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: CriticalAsset) -> CriticalAsset:
        obj = assets_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: CriticalAsset, obj_in: dict) -> CriticalAsset:
        obj = assets_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[CriticalAsset]:
        obj = assets_repo.delete(db, id=id)
        db.commit()
        return obj

assets_service = CriticalAssetService()
