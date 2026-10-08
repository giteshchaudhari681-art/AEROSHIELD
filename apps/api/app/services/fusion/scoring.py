from app.infrastructure.db.models import SensorObservation, OperationalStatus
from app.services.fusion.config import FusionConfig
import datetime

class FusionScoringService:
    @staticmethod
    def calculate_time_similarity(obs1: SensorObservation, obs2: SensorObservation) -> float:
        dt = abs((obs1.observed_at - obs2.observed_at).total_seconds() * 1000.0)
        if dt > FusionConfig.FUSION_TIME_WINDOW_MS:
            return 0.0
        return max(0.0, 1.0 - (dt / FusionConfig.FUSION_TIME_WINDOW_MS))

    @staticmethod
    def calculate_spatial_similarity(distance_m: float) -> float:
        if distance_m > FusionConfig.FUSION_POSITION_GATE_METERS:
            return 0.0
        return max(0.0, 1.0 - (distance_m / FusionConfig.FUSION_POSITION_GATE_METERS))

    @staticmethod
    def calculate_measurement_consistency(obs1: SensorObservation, obs2: SensorObservation) -> tuple[float, list[str]]:
        score = 1.0
        conflicts = []
        
        # Altitude
        if obs1.altitude is not None and obs2.altitude is not None:
            diff = abs(obs1.altitude - obs2.altitude)
            if diff > FusionConfig.FUSION_ALTITUDE_GATE_METERS:
                conflicts.append("altitude")
                score *= 0.5
            else:
                score *= 1.0 # Consistent
                
        # Speed
        if obs1.speed is not None and obs2.speed is not None:
            diff = abs(obs1.speed - obs2.speed)
            if diff > FusionConfig.FUSION_SPEED_GATE_MPS:
                conflicts.append("speed")
                score *= 0.5
            else:
                score *= 1.0
                
        return score, conflicts

    @staticmethod
    def get_sensor_reliability(status: str) -> float:
        if status == OperationalStatus.OPERATIONAL.value:
            return 1.0
        elif status == OperationalStatus.DEGRADED.value:
            return 0.7
        elif status == OperationalStatus.OFFLINE.value:
            return 0.0
        return 0.5 # UNKNOWN

    @classmethod
    def score_candidate(cls, incoming_obs: SensorObservation, candidate_obs: SensorObservation, distance_m: float):
        time_score = cls.calculate_time_similarity(incoming_obs, candidate_obs)
        spatial_score = cls.calculate_spatial_similarity(distance_m)
        meas_score, conflicts = cls.calculate_measurement_consistency(incoming_obs, candidate_obs)
        
        s1_rel = cls.get_sensor_reliability(incoming_obs.sensor.operational_status.value if incoming_obs.sensor else "UNKNOWN")
        s2_rel = cls.get_sensor_reliability(candidate_obs.sensor.operational_status.value if candidate_obs.sensor else "UNKNOWN")
        rel_score = (s1_rel + s2_rel) / 2.0
        
        final_score = (
            FusionConfig.W_TIME * time_score +
            FusionConfig.W_DISTANCE * spatial_score +
            FusionConfig.W_MEASUREMENT * meas_score +
            FusionConfig.W_SENSOR * rel_score
        )
        
        reasons = []
        if time_score > 0: reasons.append("observations_within_time_window")
        if spatial_score > 0: reasons.append("position_distance_acceptable")
        if not conflicts: reasons.append("measurements_consistent")
        if rel_score >= 0.7: reasons.append("sensor_health_acceptable")
        
        return {
            "score": round(final_score, 2),
            "matched": final_score >= FusionConfig.FUSION_MIN_CONFIDENCE and time_score > 0 and spatial_score > 0,
            "reasons": reasons,
            "conflicts": conflicts
        }
