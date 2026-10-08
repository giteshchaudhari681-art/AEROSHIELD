from app.repositories.base import BaseRepository
from app.infrastructure.db.models import CriticalAsset

class CriticalAssetRepository(BaseRepository[CriticalAsset]):
    def __init__(self):
        super().__init__(CriticalAsset)

assets_repo = CriticalAssetRepository()
