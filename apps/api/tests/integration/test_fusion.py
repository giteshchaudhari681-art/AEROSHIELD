import pytest
from app.services.fusion.config import FusionConfig
from app.services.fusion.scoring import FusionScoringService
from app.services.fusion.engine import FusionEngine
from app.infrastructure.db.models import SensorObservation
from datetime import datetime, timezone

def test_time_similarity():
    # Helper to test the scoring function directly
    # In a real integration test, we'd persist observations and run engine.
    obs1 = SensorObservation(observed_at=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc))
    obs2 = SensorObservation(observed_at=datetime(2026, 1, 1, 12, 0, 1, tzinfo=timezone.utc)) # 1 sec apart
    
    score = FusionScoringService.calculate_time_similarity(obs1, obs2)
    # 1000ms diff, limit is 2000ms, score is 0.5
    assert 0.49 < score < 0.51

def test_spatial_similarity():
    score = FusionScoringService.calculate_spatial_similarity(25.0)
    # 25m, gate is 50m, score is 0.5
    assert 0.49 < score < 0.51
