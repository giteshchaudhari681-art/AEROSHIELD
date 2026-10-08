# Data Dictionary

## Core Domain Models

### Site
Represents a geographical location or facility being monitored.
- `id`: UUID (String, Primary Key)
- `name`: String
- `description`: String (Optional)
- `site_type`: String
- `status`: String
- `location`: Geometry(Point, 4326)
- `boundary`: Geometry(Polygon, 4326)
- `created_at`: Datetime
- `updated_at`: Datetime

### CriticalAsset
Represents a specific high-value target or sensitive area within a Site.
- `id`: UUID (String, Primary Key)
- `site_id`: UUID (String, Foreign Key -> Site.id)
- `name`: String
- `asset_type`: String
- `location`: Geometry(Point, 4326)
- `vulnerability_score`: Float
- `created_at`: Datetime

### Zone (RestrictedZone)
Represents airspace restrictions or geofenced areas.
- `id`: UUID (String, Primary Key)
- `site_id`: UUID (String, Foreign Key -> Site.id)
- `name`: String
- `zone_type`: String
- `boundary`: Geometry(Polygon, 4326)
- `min_altitude`: Float
- `max_altitude`: Float
- `is_active`: Boolean
- `created_at`: Datetime

### Sensor
Hardware devices producing observations (e.g., Radar, RF, EO/IR).
- `id`: UUID (String, Primary Key)
- `site_id`: UUID (String, Foreign Key -> Site.id)
- `name`: String
- `sensor_type`: String
- `status`: String
- `location`: Geometry(Point, 4326)
- `coverage_radius`: Float
- `created_at`: Datetime
- `updated_at`: Datetime

### AerialTrack
Represents an object detected in the airspace.
- `id`: UUID (String, Primary Key)
- `site_id`: UUID (String, Foreign Key -> Site.id)
- `track_identifier`: String
- `current_location`: Geometry(Point, 4326)
- `current_altitude`: Float
- `velocity`: Float
- `heading`: Float
- `confidence_score`: Float
- `classification`: String
- `first_detected_at`: Datetime
- `last_updated_at`: Datetime

### ThreatAssessment
Assessed threat level of an AerialTrack against CriticalAssets.
- `id`: UUID (String, Primary Key)
- `track_id`: UUID (String, Foreign Key -> AerialTrack.id)
- `overall_risk_score`: Float
- `threat_level`: String
- `intent_prediction`: String
- `assessed_at`: Datetime
