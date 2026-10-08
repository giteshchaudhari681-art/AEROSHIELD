import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.infrastructure.db.session import SessionLocal
from app.core.config import settings
from app.core.security import get_password_hash
from app.infrastructure.db.models import Operator, Role, Permission
import uuid

client = TestClient(app)

def setup_test_users():
    db = SessionLocal()
    # Ensure test users are there
    admin = db.query(Operator).filter_by(email="testadmin@aeroshield.com").first()
    if not admin:
        admin = Operator(id=str(uuid.uuid4()), name="Test Admin", email="testadmin@aeroshield.com", password_hash=get_password_hash("password"), active=True)
        db.add(admin)
        db.commit()
        # assign ADMIN role if it exists
        r = db.query(Role).filter_by(name="ADMIN").first()
        if r:
            admin.roles.append(r)
            db.commit()
            
    viewer = db.query(Operator).filter_by(email="testviewer@aeroshield.com").first()
    if not viewer:
        viewer = Operator(id=str(uuid.uuid4()), name="Test Viewer", email="testviewer@aeroshield.com", password_hash=get_password_hash("password"), active=True)
        db.add(viewer)
        db.commit()
        r = db.query(Role).filter_by(name="VIEWER").first()
        if r:
            viewer.roles.append(r)
            db.commit()
    db.close()

def test_login_success():
    setup_test_users()
    response = client.post("/api/v1/auth/login", json={"username": "testadmin@aeroshield.com", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_failure():
    response = client.post("/api/v1/auth/login", json={"username": "testadmin@aeroshield.com", "password": "wrongpassword"})
    assert response.status_code == 401

def test_unauthorized_access():
    response = client.get("/api/v1/sites")
    assert response.status_code == 401

def test_viewer_access():
    # Login viewer
    resp = client.post("/api/v1/auth/login", json={"username": "testviewer@aeroshield.com", "password": "password"})
    token = resp.json()["access_token"]
    
    # Can read sites
    read_resp = client.get("/api/v1/sites", headers={"Authorization": f"Bearer {token}"})
    assert read_resp.status_code == 200
    
    # Cannot write sites
    write_resp = client.post("/api/v1/sites", json={"id": "new-site", "name": "New Site", "site_type": "OTHER"}, headers={"Authorization": f"Bearer {token}"})
    assert write_resp.status_code == 403
