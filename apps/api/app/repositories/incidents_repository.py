from app.repositories.base import BaseRepository
from app.infrastructure.db.models import Incident

class IncidentRepository(BaseRepository[Incident]):
    def __init__(self):
        super().__init__(Incident)

incidents_repo = IncidentRepository()
