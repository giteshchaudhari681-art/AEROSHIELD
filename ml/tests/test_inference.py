import pytest
from ml.inference.predictor import MLPredictorService, PredictionRequest

def test_inference_fallback_heuristics():
    # When the model file doesn't exist, it should fallback to heuristics safely.
    predictor = MLPredictorService()
    
    # Heuristic: speed > 15, rcs < 0.05 -> DRONE
    req_drone = PredictionRequest(speed_mps=20.0, altitude_m=100.0, rcs_m2=0.03)
    resp_drone = predictor.predict(req_drone)
    assert resp_drone.classification == "DRONE"
    
    # Heuristic: speed < 15, alt < 100 -> BIRD
    req_bird = PredictionRequest(speed_mps=10.0, altitude_m=50.0, rcs_m2=0.01)
    resp_bird = predictor.predict(req_bird)
    assert resp_bird.classification == "BIRD"
    
def test_inference_invalid_values():
    predictor = MLPredictorService()
    # Unknown fallback
    req_unknown = PredictionRequest(speed_mps=0.0, altitude_m=0.0, rcs_m2=999.0)
    resp_unknown = predictor.predict(req_unknown)
    assert resp_unknown.classification == "UNKNOWN"
