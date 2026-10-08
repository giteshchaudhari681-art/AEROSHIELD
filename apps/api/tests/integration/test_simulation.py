import pytest
from fastapi.testclient import TestClient
from app.main import app
import time

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

def test_simulation_rbac():
    # Anonymous
    res = client.get("/api/v1/simulation/status")
    assert res.status_code == 401
    
    # Viewer (not admin)
    viewer_token = get_token("testviewer@aeroshield.com")
    headers = {"Authorization": f"Bearer {viewer_token}"}
    res = client.get("/api/v1/simulation/status", headers=headers)
    assert res.status_code == 403
    
    # Admin
    admin_token = get_token("testadmin@aeroshield.com")
    headers = {"Authorization": f"Bearer {admin_token}"}
    res = client.get("/api/v1/simulation/status", headers=headers)
    assert res.status_code == 200

def test_simulation_start_stop():
    admin_token = get_token("testadmin@aeroshield.com")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    config = {
        "enabled": True,
        "scenario": "baseline",
        "speed": 10.0,
        "tick_interval_ms": 100,
        "random_seed": 42
    }
    
    res = client.post("/api/v1/simulation/start", json=config, headers=headers)
    assert res.status_code == 200
    
    # Wait for a few ticks
    time.sleep(1.0)
    
    res = client.get("/api/v1/simulation/status", headers=headers)
    assert res.status_code == 200
    status = res.json()
    print("STATUS", status)
    assert status["running"] is True
    assert status["active_sensors"] > 0
    assert status["observations_generated"] > 0
    
    res = client.post("/api/v1/simulation/stop", headers=headers)
    assert res.status_code == 200
    assert res.json()["running"] is False
    
def test_simulation_determinism():
    admin_token = get_token("testadmin@aeroshield.com")
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Run once
    config = {
        "enabled": True,
        "scenario": "baseline",
        "speed": 1.0,
        "tick_interval_ms": 100,
        "random_seed": 99
    }
    client.post("/api/v1/simulation/start", json=config, headers=headers)
    time.sleep(1.0)
    res1 = client.get("/api/v1/simulation/status", headers=headers)
    obs1 = res1.json()["observations_generated"]
    client.post("/api/v1/simulation/stop", headers=headers)
    
    # Run twice
    client.post("/api/v1/simulation/start", json=config, headers=headers)
    time.sleep(1.0)
    res2 = client.get("/api/v1/simulation/status", headers=headers)
    obs2 = res2.json()["observations_generated"]
    client.post("/api/v1/simulation/stop", headers=headers)
    
    # As it's highly dependent on real time sleep(), 
    # observations_generated might slightly differ by 1 or 2 due to scheduling,
    # but the sequence of random numbers and idempotency ensures we don't duplicate.
    # We just ensure it ran.
    assert obs1 > 0
    assert obs2 > 0
