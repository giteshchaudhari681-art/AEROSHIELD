from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List, Tuple
from app.repositories.base import BaseRepository
from app.infrastructure.db.models import SensorObservation

class SensorObservationRepository(BaseRepository[SensorObservation]):
    def __init__(self):
        super().__init__(SensorObservation)

    def get_by_time_range(self, db: Session, start_time: datetime, end_time: datetime, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[SensorObservation], int]:
        query = db.query(self.model).filter(
            and_(
                self.model.observed_at >= start_time,
                self.model.observed_at <= end_time
            )
        )
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
                
        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total
        
    def find_by_correlation_id(self, db: Session, correlation_id: str) -> List[SensorObservation]:
        return db.query(self.model).filter(self.model.correlation_id == correlation_id).all()

observations_repo = SensorObservationRepository()
