from app.infrastructure.db.session import engine
from sqlalchemy import text
with engine.begin() as conn:
    conn.execute(text('DROP TABLE IF EXISTS alembic_version CASCADE;'))
    conn.execute(text('DROP INDEX IF EXISTS idx_sites_boundary;'))
    conn.execute(text('DROP INDEX IF EXISTS idx_sites_location;'))
