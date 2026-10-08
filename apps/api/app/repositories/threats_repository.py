from app.repositories.base import BaseRepository
from app.infrastructure.db.models import ThreatAssessment

class ThreatAssessmentRepository(BaseRepository[ThreatAssessment]):
    def __init__(self):
        super().__init__(ThreatAssessment)

threats_repo = ThreatAssessmentRepository()
