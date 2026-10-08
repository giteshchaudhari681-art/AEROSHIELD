import os

def add_fusion_models():
    models_path = "app/infrastructure/db/models.py"
    with open(models_path, "r") as f:
        content = f.read()

    if "FusedContact" not in content:
        fusion_code = """
class FusedContactStatus(str, enum.Enum):
    CANDIDATE = "CANDIDATE"
    CONFIRMED = "CONFIRMED"
    CONFLICTED = "CONFLICTED"

class FusedContact(Base):
    __tablename__ = "fused_contacts"
    
    id = Column(String, primary_key=True, index=True)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    
    reference_time = Column(DateTime(timezone=True), nullable=False, index=True)
    
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    altitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)
    
    position_uncertainty_m = Column(Float, nullable=True)
    
    confidence = Column(Float, nullable=False, default=0.0)
    status = Column(SQLEnum(FusedContactStatus), nullable=False, default=FusedContactStatus.CANDIDATE)
    
    contributing_observation_count = Column(Integer, nullable=False, default=0)
    contributing_sensor_count = Column(Integer, nullable=False, default=0)
    
    fusion_method = Column(String, nullable=False)
    schema_version = Column(Integer, nullable=False, default=1)
    
    conflicts_json = Column(JSON, nullable=True)
    fusion_reasons = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    site = relationship("Site")
    observations = relationship("FusedContactObservation", back_populates="fused_contact")

class FusedContactObservationRole(str, enum.Enum):
    PRIMARY = "PRIMARY"
    SUPPORTING = "SUPPORTING"
    CONFLICTING = "CONFLICTING"

class FusedContactObservation(Base):
    __tablename__ = "fused_contact_observations"
    
    id = Column(String, primary_key=True, index=True)
    fused_contact_id = Column(String, ForeignKey("fused_contacts.id"), nullable=False, index=True)
    observation_id = Column(String, ForeignKey("sensor_observations.id"), nullable=False, index=True)
    
    contribution_score = Column(Float, nullable=True)
    contribution_role = Column(SQLEnum(FusedContactObservationRole), nullable=False, default=FusedContactObservationRole.SUPPORTING)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    fused_contact = relationship("FusedContact", back_populates="observations")
    observation = relationship("SensorObservation")
"""
        with open(models_path, "a") as f:
            f.write(fusion_code)
        print("Fusion models added.")
    else:
        print("Fusion models already exist.")

if __name__ == "__main__":
    add_fusion_models()
