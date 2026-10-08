import os
import shutil

base_dir = "d:/SEVA/apps/api/app"

entities = {
    "site": {"model": "Site", "table": "sites", "has_site_id": False},
    "critical_asset": {"model": "CriticalAsset", "table": "assets", "has_site_id": True},
    "restricted_zone": {"model": "RestrictedZone", "table": "zones", "has_site_id": True},
    "sensor": {"model": "Sensor", "table": "sensors", "has_site_id": True},
    "sensor_observation": {"model": "SensorObservation", "table": "observations", "has_site_id": False},
    "aerial_track": {"model": "AerialTrack", "table": "tracks", "has_site_id": True},
    "behaviour_event": {"model": "BehaviourEvent", "table": "behaviours", "has_site_id": False},
    "threat_assessment": {"model": "ThreatAssessment", "table": "threats", "has_site_id": True},
    "alert": {"model": "Alert", "table": "alerts", "has_site_id": False},
    "incident": {"model": "Incident", "table": "incidents", "has_site_id": True},
    "evidence": {"model": "Evidence", "table": "evidence", "has_site_id": False},
    "audit_log": {"model": "AuditLog", "table": "audit_logs", "has_site_id": False},
}

for e, config in entities.items():
    model = config["model"]
    table = config["table"]
    
    # 1. Repo
    repo_file = f"{base_dir}/repositories/{table}_repository.py"
    repo_content = f"""from app.repositories.base import BaseRepository
from app.infrastructure.db.models import {model}

class {model}Repository(BaseRepository[{model}]):
    def __init__(self):
        super().__init__({model})

{table}_repo = {model}Repository()
"""
    os.makedirs(os.path.dirname(repo_file), exist_ok=True)
    with open(repo_file, "w") as f: f.write(repo_content)

    # 2. Service
    service_file = f"{base_dir}/services/{table}_service.py"
    service_content = f"""from sqlalchemy.orm import Session
from app.repositories.{table}_repository import {table}_repo
from app.infrastructure.db.models import {model}
from typing import List, Optional, Tuple

class {model}Service:
    @staticmethod
    def get(db: Session, id: str) -> Optional[{model}]:
        return {table}_repo.get(db, id=id)

    @staticmethod
    def list(db: Session, skip: int = 0, limit: int = 100, **filters) -> Tuple[List[{model}], int]:
        return {table}_repo.get_multi(db, skip=skip, limit=limit, **filters)

    @staticmethod
    def create(db: Session, obj_in: {model}) -> {model}:
        obj = {table}_repo.create(db, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def update(db: Session, db_obj: {model}, obj_in: dict) -> {model}:
        obj = {table}_repo.update(db, db_obj=db_obj, obj_in=obj_in)
        db.commit()
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> Optional[{model}]:
        obj = {table}_repo.delete(db, id=id)
        db.commit()
        return obj

{table}_service = {model}Service()
"""
    os.makedirs(os.path.dirname(service_file), exist_ok=True)
    with open(service_file, "w") as f: f.write(service_content)

print("Scaffolding complete.")
