from sqlalchemy.orm import Session
from sqlalchemy import func
from app.infrastructure.db.models import SensorObservation
from app.services.fusion.config import FusionConfig
import datetime

class CandidateGenerationService:
    @staticmethod
    def find_candidates(db: Session, incoming_obs: SensorObservation):
        if not incoming_obs.location:
            return []
            
        time_window = datetime.timedelta(milliseconds=FusionConfig.FUSION_TIME_WINDOW_MS)
        time_min = incoming_obs.observed_at - time_window
        time_max = incoming_obs.observed_at + time_window

        # Get candidates within time window and same site, excluding self
        query = db.query(
            SensorObservation, 
            func.ST_DistanceSphere(SensorObservation.location, incoming_obs.location).label("distance")
        ).filter(
            SensorObservation.id != incoming_obs.id,
            SensorObservation.location.isnot(None),
            SensorObservation.observed_at >= time_min,
            SensorObservation.observed_at <= time_max
        )
        
        # Spatial filter
        query = query.filter(
            func.ST_DistanceSphere(SensorObservation.location, incoming_obs.location) <= FusionConfig.FUSION_POSITION_GATE_METERS
        )
        
        # Limit
        query = query.limit(FusionConfig.FUSION_MAX_CANDIDATES)
        
        return query.all()
