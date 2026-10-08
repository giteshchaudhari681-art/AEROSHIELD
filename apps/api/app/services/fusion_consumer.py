import json
import logging
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.db.models import SensorObservation
from app.services.fusion.engine import FusionEngine

logger = logging.getLogger(__name__)

class FusionConsumer:
    @staticmethod
    def handle_event(event_data: dict):
        if event_data.get("event_type") != "observation.created":
            return
            
        payload = event_data.get("payload", {})
        observation_id = payload.get("observation_id")
        if not observation_id:
            return
            
        with SessionLocal() as db:
            # Check idempotency/already fused? For prototype, checking if it is already in FusedContactObservation
            from app.infrastructure.db.models import FusedContactObservation
            existing = db.query(FusedContactObservation).filter(FusedContactObservation.observation_id == observation_id).first()
            if existing:
                logger.info(f"Observation {observation_id} already fused, skipping.")
                return
                
            obs = db.query(SensorObservation).filter(SensorObservation.id == observation_id).first()
            if not obs:
                logger.error(f"Observation {observation_id} not found for fusion.")
                return
                
            try:
                fc = FusionEngine.process_observation(db, obs)
                if fc:
                    logger.info(f"Fused contact {fc.id} created from observation {obs.id}")
                    db.commit()
                else:
                    logger.debug(f"No fusion match for observation {obs.id}")
            except Exception as e:
                db.rollback()
                logger.error(f"Error fusing observation {obs.id}: {e}")
