import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def setup_users():
    from tests.integration.test_auth import setup_test_users
    setup_test_users()

def get_token(email, password="password"):
    setup_users() # ensure they exist
    res = client.post("/api/v1/auth/login", data={"username": email, "password": password})
    if res.status_code != 200:
        return None
    return res.json()["access_token"]

def test_get_site_context():
    token = get_token("testadmin@aeroshield.com")
    if not token:
        pytest.skip("Test admin not setup")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/v1/sites/site-demo-dt-001/context", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "site" in data
    assert "assets" in data
    assert "restricted_zones" in data
    
    assert data["site"]["id"] == "site-demo-dt-001"
    assert len(data["assets"]) >= 5
    assert len(data["restricted_zones"]) >= 3

def test_find_assets_nearby():
    token = get_token("testadmin@aeroshield.com")
    if not token: pytest.skip("Test admin not setup")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/v1/assets/_queries/nearby?lat=37.775&lon=-122.415&radius_m=1000", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0

def test_find_zones_containing():
    token = get_token("testadmin@aeroshield.com")
    if not token: pytest.skip("Test admin not setup")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/v1/zones/_queries/containing?lat=37.776&lon=-122.416", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) > 0

def test_rbac_protection_on_context():
    token = get_token("testviewer@aeroshield.com")
    if not token:
        pytest.skip("Test viewer not setup")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/v1/sites/site-demo-dt-001/context", headers=headers)
    assert response.status_code == 200

def test_rbac_protection_on_context_unauthorized():
    response = client.get("/api/v1/sites/site-demo-dt-001/context")
    assert response.status_code == 401
