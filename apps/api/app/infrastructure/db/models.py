from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geometry
from datetime import datetime
import enum

from .base import Base

class SiteType(str, enum.Enum):
    POWER_PLANT = "POWER_PLANT"
    AIRPORT = "AIRPORT"
    PORT = "PORT"
    REFINERY = "REFINERY"
    DEFENCE_INSTALLATION = "DEFENCE_INSTALLATION"
    COMMUNICATION_FACILITY = "COMMUNICATION_FACILITY"
    DATA_CENTER = "DATA_CENTER"
    RAILWAY = "RAILWAY"
    OTHER = "OTHER"

class AssetCriticality(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class OperationalStatus(str, enum.Enum):
    OPERATIONAL = "OPERATIONAL"
    DEGRADED = "DEGRADED"
    MAINTENANCE = "MAINTENANCE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"

class ZoneSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ThreatLevel(str, enum.Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class TrackStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    LOST = "LOST"
    CLOSED = "CLOSED"

class AlertStatus(str, enum.Enum):
    OPEN = "OPEN"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RESOLVED = "RESOLVED"
    DISMISSED = "DISMISSED"

class IncidentStatus(str, enum.Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class SensorStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DEGRADED = "DEGRADED"
    MAINTENANCE = "MAINTENANCE"
    OFFLINE = "OFFLINE"
    UNKNOWN = "UNKNOWN"

class SensorHealthStatus(str, enum.Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"
    
class ObservationType(str, enum.Enum):
    DETECTION = "DETECTION"
    POSITION = "POSITION"
    VELOCITY = "VELOCITY"
    SIGNAL = "SIGNAL"
    THERMAL = "THERMAL"
    ACOUSTIC = "ACOUSTIC"
    IDENTIFICATION = "IDENTIFICATION"
    STATUS = "STATUS"


class Site(Base):
    __tablename__ = "sites"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    site_code = Column(String, nullable=True, unique=True, index=True)
    description = Column(Text, nullable=True)
    site_type = Column(SQLEnum(SiteType), nullable=False)
    status = Column(String, nullable=False, default="ACTIVE")
    
    # Geographic location of the site center (Point)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    # Geographic boundary of the site (Polygon)
    boundary = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    assets = relationship("CriticalAsset", back_populates="site")
    zones = relationship("RestrictedZone", back_populates="site")
    sensors = relationship("Sensor", back_populates="site")
    tracks = relationship("AerialTrack", back_populates="site")
    incidents = relationship("Incident", back_populates="site")

class CriticalAsset(Base):
    __tablename__ = "critical_assets"
    
    id = Column(String, primary_key=True, index=True)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    name = Column(String, nullable=False)
    asset_code = Column(String, nullable=True, index=True)
    asset_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    criticality = Column(SQLEnum(AssetCriticality), nullable=False)
    operational_status = Column(SQLEnum(OperationalStatus), nullable=False, default=OperationalStatus.UNKNOWN)
    
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    protection_radius = Column(Float, nullable=True) # in meters
    
    status = Column(String, nullable=False, default="ACTIVE")
    metadata_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    site = relationship("Site", back_populates="assets")
    threat_assessments = relationship("ThreatAssessment", secondary="asset_threats", back_populates="critical_assets")

class RestrictedZone(Base):
    __tablename__ = "restricted_zones"
    
    id = Column(String, primary_key=True, index=True)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    name = Column(String, nullable=False)
    zone_code = Column(String, nullable=True, index=True)
    zone_type = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    boundary = Column(Geometry(geometry_type='POLYGON', srid=4326), nullable=False)
    severity = Column(SQLEnum(ZoneSeverity), nullable=False)
    active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    site = relationship("Site", back_populates="zones")

class Sensor(Base):
    __tablename__ = "sensors"
    
    id = Column(String, primary_key=True, index=True)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    name = Column(String, nullable=False)
    sensor_code = Column(String, nullable=True, index=True, unique=True)
    sensor_type = Column(String, nullable=False) # e.g. RADAR, RF, EO_IR, ACOUSTIC, SIMULATED
    
    operational_status = Column(SQLEnum(SensorStatus), nullable=False, default=SensorStatus.UNKNOWN)
    health_status = Column(SQLEnum(SensorHealthStatus), nullable=False, default=SensorHealthStatus.UNKNOWN)
    is_enabled = Column(Boolean, nullable=False, default=True)
    status = Column(String, nullable=False, default="ACTIVE")
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    
    manufacturer = Column(String, nullable=True)
    model = Column(String, nullable=True)
    configuration = Column(JSON, nullable=True)
    
    last_seen_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    site = relationship("Site", back_populates="sensors")
    observations = relationship("SensorObservation", back_populates="sensor")

class AerialTrack(Base):
    __tablename__ = "aerial_tracks"
    
    id = Column(String, primary_key=True, index=True)
    track_identifier = Column(String, nullable=False, index=True)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    
    classification = Column(String, nullable=True)
    identification_status = Column(String, nullable=True)
    
    first_seen_at = Column(DateTime(timezone=True), nullable=False)
    last_seen_at = Column(DateTime(timezone=True), nullable=False)
    
    current_location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    current_altitude = Column(Float, nullable=True)
    current_speed = Column(Float, nullable=True)
    current_heading = Column(Float, nullable=True)
    
    confidence = Column(Float, nullable=True)
    status = Column(SQLEnum(TrackStatus), nullable=False, default=TrackStatus.ACTIVE)
    metadata_json = Column(JSON, nullable=True)
    state_version = Column(Integer, nullable=False, default=1)
    update_count = Column(Integer, nullable=False, default=1)
    terminated_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    site = relationship("Site", back_populates="tracks")
    observations = relationship("SensorObservation", back_populates="track")
    behaviour_events = relationship("BehaviourEvent", back_populates="track")
    threat_assessments = relationship("ThreatAssessment", back_populates="track")

class SensorObservation(Base):
    __tablename__ = "sensor_observations"
    
    id = Column(String, primary_key=True, index=True)
    sensor_id = Column(String, ForeignKey("sensors.id"), nullable=False)
    track_id = Column(String, ForeignKey("aerial_tracks.id"), nullable=True) # can be null before fusion
    
    observation_type = Column(SQLEnum(ObservationType), nullable=False, default=ObservationType.DETECTION)
    observed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    received_at = Column(DateTime(timezone=True), nullable=False, index=True)
    sensor_type = Column(String, nullable=False)
    
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True) # Contains lat/lon
    altitude = Column(Float, nullable=True)
    speed = Column(Float, nullable=True)
    heading = Column(Float, nullable=True)
    
    confidence = Column(Float, nullable=True)
    classification = Column(String, nullable=True)
    
    signal_metadata = Column(JSON, nullable=True)
    observation_metadata = Column(JSON, nullable=True)
    correlation_id = Column(String, nullable=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    sensor = relationship("Sensor", back_populates="observations")
    track = relationship("AerialTrack", back_populates="observations")

class BehaviourEvent(Base):
    __tablename__ = "behaviour_events"
    
    id = Column(String, primary_key=True, index=True)
    track_id = Column(String, ForeignKey("aerial_tracks.id"), nullable=False)
    
    event_type = Column(String, nullable=False) # e.g. RESTRICTED_ZONE_ENTRY
    observed_at = Column(DateTime(timezone=True), nullable=False, index=True)
    duration = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    track = relationship("AerialTrack", back_populates="behaviour_events")

class ThreatAssessment(Base):
    __tablename__ = "threat_assessments"
    
    id = Column(String, primary_key=True, index=True)
    track_id = Column(String, ForeignKey("aerial_tracks.id"), nullable=False)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    
    risk_score = Column(Float, nullable=True)
    threat_level = Column(SQLEnum(ThreatLevel), nullable=False)
    confidence = Column(Float, nullable=True)
    
    reasoning = Column(Text, nullable=True)
    model_version = Column(String, nullable=True)
    
    assessed_at = Column(DateTime(timezone=True), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    
    track = relationship("AerialTrack", back_populates="threat_assessments")
    alerts = relationship("Alert", back_populates="threat_assessment")
    critical_assets = relationship("CriticalAsset", secondary="asset_threats", back_populates="threat_assessments")

# Association table for ThreatAssessment <-> CriticalAsset
class AssetThreat(Base):
    __tablename__ = "asset_threats"
    
    threat_assessment_id = Column(String, ForeignKey("threat_assessments.id"), primary_key=True)
    critical_asset_id = Column(String, ForeignKey("critical_assets.id"), primary_key=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, index=True)
    track_id = Column(String, ForeignKey("aerial_tracks.id"), nullable=True)
    threat_assessment_id = Column(String, ForeignKey("threat_assessments.id"), nullable=True)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=True)
    
    alert_type = Column(String, nullable=False)
    severity = Column(SQLEnum(ThreatLevel), nullable=False)
    
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(SQLEnum(AlertStatus), nullable=False, default=AlertStatus.OPEN)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)
    acknowledged_by = Column(String, nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    metadata_json = Column(JSON, nullable=True)
    
    threat_assessment = relationship("ThreatAssessment", back_populates="alerts")
    incident = relationship("Incident", back_populates="alerts")

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(String, primary_key=True, index=True)
    site_id = Column(String, ForeignKey("sites.id"), nullable=False)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(SQLEnum(ThreatLevel), nullable=False)
    status = Column(SQLEnum(IncidentStatus), nullable=False, default=IncidentStatus.OPEN)
    
    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    
    created_by = Column(String, nullable=True)
    resolved_by = Column(String, nullable=True)
    
    metadata_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    site = relationship("Site", back_populates="incidents")
    alerts = relationship("Alert", back_populates="incident")
    evidence = relationship("Evidence", back_populates="incident")

class Evidence(Base):
    __tablename__ = "evidence"
    
    id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey("incidents.id"), nullable=False)
    
    evidence_type = Column(String, nullable=False)
    source = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    confidence = Column(Float, nullable=True)
    
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    incident = relationship("Incident", back_populates="evidence")

class Operator(Base):
    __tablename__ = "operators"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    roles = relationship("Role", secondary="operator_roles", back_populates="operators")
    refresh_tokens = relationship("RefreshToken", back_populates="operator")

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    
    operators = relationship("Operator", secondary="operator_roles", back_populates="roles")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True) # e.g. site:read
    
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")

class OperatorRole(Base):
    __tablename__ = "operator_roles"
    operator_id = Column(String, ForeignKey("operators.id"), primary_key=True)
    role_id = Column(String, ForeignKey("roles.id"), primary_key=True)

class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_id = Column(String, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(String, ForeignKey("permissions.id"), primary_key=True)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(String, primary_key=True, index=True)
    operator_id = Column(String, ForeignKey("operators.id"), nullable=False)
    token_hash = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    operator = relationship("Operator", back_populates="refresh_tokens")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, index=True)
    actor_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    
    entity_type = Column(String, nullable=True)
    entity_id = Column(String, nullable=True)
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    metadata_json = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)

class OutboxStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"

class EventOutbox(Base):
    __tablename__ = "event_outbox"

    id = Column(String, primary_key=True, index=True)
    event_id = Column(String, unique=True, index=True, nullable=False)
    event_type = Column(String, nullable=False)
    schema_version = Column(Integer, nullable=False, default=1)
    aggregate_type = Column(String, nullable=False)
    aggregate_id = Column(String, nullable=False)
    correlation_id = Column(String, nullable=True)
    occurred_at = Column(DateTime(timezone=True), nullable=False)
    
    payload = Column(JSON, nullable=False)
    
    status = Column(SQLEnum(OutboxStatus), nullable=False, default=OutboxStatus.PENDING, index=True)
    attempts = Column(Integer, nullable=False, default=0)
    available_at = Column(DateTime(timezone=True), nullable=False, index=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

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

class TrackObservation(Base):
    __tablename__ = "track_observations"
    
    id = Column(String, primary_key=True, index=True)
    track_id = Column(String, ForeignKey("aerial_tracks.id"), nullable=False, index=True)
    fused_contact_id = Column(String, ForeignKey("fused_contacts.id"), nullable=False, index=True, unique=True)
    
    association_score = Column(Float, nullable=False)
    decision = Column(String, nullable=False)
    evidence = Column(JSON, nullable=True)
    
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    track = relationship("AerialTrack")
    fused_contact = relationship("FusedContact")

class IdentityRecord(Base):
    __tablename__ = "identity_records"
    id = Column(String, primary_key=True, index=True)
    identity_code = Column(String, nullable=False, unique=True)
    display_name = Column(String, nullable=False)
    identity_type = Column(String, nullable=False)
    status = Column(String, nullable=False)

class ClassificationAssessment(Base):
    __tablename__ = "classification_assessments"
    id = Column(String, primary_key=True, index=True)
    track_id = Column(String, ForeignKey("aerial_tracks.id"), nullable=False)
    class_code = Column(String, nullable=False)
    status = Column(String, nullable=False)
    evidence_score = Column(Float, nullable=True)
    
    track = relationship("AerialTrack")

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"
    id = Column(String, primary_key=True, index=True)
    track_id = Column(String, ForeignKey("aerial_tracks.id"), nullable=False)
    assessment_status = Column(String, nullable=False)
    review_priority = Column(String, nullable=False)
    risk_score = Column(Float, nullable=True)
    
    track = relationship("AerialTrack")

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
