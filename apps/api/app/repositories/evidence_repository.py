from app.repositories.base import BaseRepository
from app.infrastructure.db.models import Evidence

class EvidenceRepository(BaseRepository[Evidence]):
    def __init__(self):
        super().__init__(Evidence)

evidence_repo = EvidenceRepository()
