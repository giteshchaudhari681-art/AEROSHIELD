from sqlalchemy.orm import Session
from app.repositories.tracks_repository import tracks_repo
from app.infrastructure.db.models import AerialTrack
from typing import List, Optional, Tuple

class AerialTrackService:
    @staticmethod
    def get(db: Session, id: str) -> Optional[AerialTrack]:
        return tracks_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[AerialTrack], int]:
        return tracks_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: AerialTrack) -> AerialTrack:
        obj = tracks_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: AerialTrack, obj_in: dict) -> AerialTrack:
        obj = tracks_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[AerialTrack]:
        obj = tracks_repo.delete(db, id=id)
        db.commit()
        return obj

tracks_service = AerialTrackService()
