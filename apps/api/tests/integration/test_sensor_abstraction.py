import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def setup_users():
    from tests.integration.test_auth import setup_test_users
    setup_test_users()
    
    from seed_sensor_data import seed_sensors
    seed_sensors()

def get_token(email, password="password"):
    setup_users()
    res = client.post("/api/v1/auth/login", json={"username": email, "password": password})
    if res.status_code != 200:
        return None
    return res.json()["access_token"]

def test_ingest_radar_observation():
    token = get_token("testadmin@aeroshield.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "range_m": 1200,
        "azimuth_deg": 90,
        "elevation_deg": 10,
        "radial_velocity_mps": 25.5,
        "confidence": 0.9,
        "lat": 37.776,
        "lon": -122.418,
        "alt": 200
    }
    
    res = client.post("/api/v1/observations/?sensor_id=sensor-radar-001&correlation_id=test_radar_1", json=payload, headers=headers)
    assert res.status_code == 201
    assert res.json()["ingested"] == 1
    
    # Verify idempotency
    res2 = client.post("/api/v1/observations/?sensor_id=sensor-radar-001&correlation_id=test_radar_1", json=payload, headers=headers)
    assert res2.status_code == 201
    assert res2.json()["ingested"] == 1

def test_ingest_rf_observation():
    token = get_token("testadmin@aeroshield.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "frequency_hz": 2400000000,
        "signal_strength_dbm": -45,
        "confidence": 0.7,
        "bearing": 120
    }
    
    res = client.post("/api/v1/observations/?sensor_id=sensor-rf-001", json=payload, headers=headers)
    assert res.status_code == 201
    assert res.json()["ingested"] == 1

def test_ingest_invalid_speed():
    token = get_token("testadmin@aeroshield.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {
        "radial_velocity_mps": -5.0, # Invalid speed
        "lat": 37.776,
        "lon": -122.418
    }
    
    res = client.post("/api/v1/observations/?sensor_id=sensor-radar-001", json=payload, headers=headers)
    assert res.status_code == 400

def test_ingest_unauthorized():
    payload = {"confidence": 0.5}
    res = client.post("/api/v1/observations/?sensor_id=sensor-acoustic-001", json=payload)
    assert res.status_code == 401

def test_list_observations():
    # Admin has observation:read
    token = get_token("testadmin@aeroshield.com")
    headers = {"Authorization": f"Bearer {token}"}
    
    res = client.get("/api/v1/observations/?sensor_id=sensor-radar-001", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert len(data["items"]) >= 1
    
    obs = data["items"][0]
    assert obs["sensor_id"] == "sensor-radar-001"
    assert obs["sensor_type"] == "RADAR"
    assert obs["observation_type"] == "POSITION"
    assert "received_at" in obs
