import pytest
from app.infrastructure.db.session import engine
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.infrastructure.db.models import Site, CriticalAsset

def test_db_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1

def test_seeded_data():
    with Session(engine) as session:
        site = session.query(Site).first()
        assert site is not None
        assert site.id == "site-test-01"
        assert site.name == "Delta Power Generation Facility"
        
        assets = session.query(CriticalAsset).filter(CriticalAsset.site_id == site.id).all()
        assert len(assets) == 2
