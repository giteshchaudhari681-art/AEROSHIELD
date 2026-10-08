from sqlalchemy.orm import Session
from app.infrastructure.db.models import SensorObservation, FusedContact, FusedContactObservation, FusedContactStatus, FusedContactObservationRole
from app.services.fusion.candidate_generation import CandidateGenerationService
from app.services.fusion.scoring import FusionScoringService
import uuid
import datetime

class FusionEngine:
    @staticmethod
    def process_observation(db: Session, observation: SensorObservation) -> FusedContact | None:
        candidates = CandidateGenerationService.find_candidates(db, observation)
        
        matches = []
        conflicts = []
        fusion_reasons = []
        
        for cand_obs, distance in candidates:
            result = FusionScoringService.score_candidate(observation, cand_obs, distance)
            if result["matched"]:
                matches.append((cand_obs, result))
                if result["conflicts"]:
                    conflicts.extend(result["conflicts"])
                fusion_reasons.extend(result["reasons"])

        if not matches:
            # No fusion
            return None
            
        # We have matches, generate FusedContact
        fused_id = str(uuid.uuid4())
        
        # Calculate weighted averages (simplified for prototype)
        all_obs = [observation] + [m[0] for m in matches]
        
        lats = []
        lons = []
        alts = []
        speeds = []
        headings = []
        
        sensor_ids = set()
        
        for obs in all_obs:
            if obs.location:
                # Naive EWKT parse for prototype: SRID=4326;POINT(lon lat)
                # In real scenario, use PostGIS ST_X/ST_Y via query or Shapely
                pass
            if obs.altitude is not None: alts.append(obs.altitude)
            if obs.speed is not None: speeds.append(obs.speed)
            if obs.heading is not None: headings.append(obs.heading)
            if obs.sensor_id: sensor_ids.add(obs.sensor_id)
            
        # Proper query to get ST_X and ST_Y for all_obs
        obs_ids = [o.id for o in all_obs]
        from sqlalchemy import text
        coords = db.execute(
            text(f"SELECT id, ST_X(location::geometry) as lon, ST_Y(location::geometry) as lat FROM sensor_observations WHERE id IN ({','.join([':id'+str(i) for i in range(len(obs_ids))])})"),
            {f"id{i}": obs_ids[i] for i in range(len(obs_ids))}
        ).fetchall()
        
        for row in coords:
            lons.append(row.lon)
            lats.append(row.lat)
            
        avg_lat = sum(lats)/len(lats) if lats else 0
        avg_lon = sum(lons)/len(lons) if lons else 0
        avg_alt = sum(alts)/len(alts) if alts else None
        avg_speed = sum(speeds)/len(speeds) if speeds else None
        avg_heading = sum(headings)/len(headings) if headings else None
        
        avg_confidence = sum([m[1]["score"] for m in matches]) / len(matches)
        
        fc = FusedContact(
            id=fused_id,
            site_id=observation.sensor.site_id if observation.sensor else "unknown", # Ensure valid site
            reference_time=observation.observed_at,
            location=f"SRID=4326;POINT({avg_lon} {avg_lat})",
            altitude=avg_alt,
            speed=avg_speed,
            heading=avg_heading,
            confidence=round(avg_confidence, 2),
            status=FusedContactStatus.CONFIRMED if not conflicts else FusedContactStatus.CONFLICTED,
            contributing_observation_count=len(all_obs),
            contributing_sensor_count=len(sensor_ids),
            fusion_method="weighted_gated_fusion_v1",
            schema_version=1,
            conflicts_json={"conflicts": list(set(conflicts))} if conflicts else None,
            fusion_reasons=list(set(fusion_reasons))
        )
        
        db.add(fc)
        
        # Add roles
        fco_primary = FusedContactObservation(
            id=str(uuid.uuid4()),
            fused_contact_id=fused_id,
            observation_id=observation.id,
            contribution_score=1.0,
            contribution_role=FusedContactObservationRole.PRIMARY
        )
        db.add(fco_primary)
        
        for m_obs, m_res in matches:
            fco_supp = FusedContactObservation(
                id=str(uuid.uuid4()),
                fused_contact_id=fused_id,
                observation_id=m_obs.id,
                contribution_score=m_res["score"],
                contribution_role=FusedContactObservationRole.SUPPORTING if not m_res["conflicts"] else FusedContactObservationRole.CONFLICTING
            )
            db.add(fco_supp)
            
        db.flush()
        return fc
