from app.repositories.base import BaseRepository
from app.infrastructure.db.models import Site

class SiteRepository(BaseRepository[Site]):
    def __init__(self):
        super().__init__(Site)

sites_repo = SiteRepository()
