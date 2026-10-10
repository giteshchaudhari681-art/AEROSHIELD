import os

def update_models():
    models_path = "apps/api/app/infrastructure/db/models.py"
    if not os.path.exists(models_path):
        os.makedirs(os.path.dirname(models_path), exist_ok=True)
        with open(models_path, "w") as f:
            f.write("# Stub models.py for AEROSHIELD\n")

    with open(models_path, "r") as f:
        content = f.read()

    if "EvidenceItem" not in content:
        code = """
class EvidenceItem(Base):
    __tablename__ = "evidence_items"
    id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)
    evidence_type = Column(String, nullable=False)
    source_reference = Column(String, nullable=False)
    integrity_digest = Column(String, nullable=True)

class CustodyEvent(Base):
    __tablename__ = "custody_events"
    id = Column(String, primary_key=True, index=True)
    evidence_id = Column(String, ForeignKey("evidence_items.id"), nullable=False)
    action_type = Column(String, nullable=False)
    actor = Column(String, nullable=False)
"""
        content += code

    with open(models_path, "w") as f:
        f.write(content)

def create_services():
    os.makedirs("apps/api/app/services/incident", exist_ok=True)
    
    with open("apps/api/app/services/incident/investigation.py", "w") as f:
        f.write("""
class IncidentInvestigationService:
    def __init__(self, db_session):
        self.db = db_session
        
    def register_evidence(self, incident_id, evidence_data, actor):
        # Register evidence logic
        return {"status": "SUCCESS"}
""")
        
if __name__ == "__main__":
    update_models()
    create_services()
    print("Scaffolded Prompt 13 successfully.")
