import os

def create_routers():
    base_dir = "apps/api/app/api/v1/endpoints"
    os.makedirs(base_dir, exist_ok=True)
    
    files = {
        "__init__.py": "",
        "auth.py": """from fastapi import APIRouter
router = APIRouter()
@router.post("/login")
def login(): return {"token": "fake-jwt-token"}
""",
        "sites.py": """from fastapi import APIRouter
router = APIRouter()
@router.get("/")
def get_sites(): return []
@router.post("/")
def create_site(): return {"id": "site-123", "status": "ACTIVE"}
""",
        "sensors.py": """from fastapi import APIRouter
router = APIRouter()
@router.get("/")
def get_sensors(): return []
@router.post("/")
def register_sensor(): return {"id": "sensor-123"}
""",
        "observations.py": """from fastapi import APIRouter
router = APIRouter()
@router.post("/")
def ingest_observation(): return {"status": "accepted"}
""",
        "tracks.py": """from fastapi import APIRouter
router = APIRouter()
@router.get("/")
def get_tracks(): return []
""",
        "incidents.py": """from fastapi import APIRouter
router = APIRouter()
@router.get("/")
def get_incidents(): return []
@router.post("/")
def create_incident(): return {"id": "incident-123"}
"""
    }
    
    for filename, content in files.items():
        with open(os.path.join(base_dir, filename), "w") as f:
            f.write(content)

def create_main():
    main_file = "apps/api/app/main.py"
    os.makedirs(os.path.dirname(main_file), exist_ok=True)
    with open(main_file, "w") as f:
        f.write("""from fastapi import FastAPI
from .api.v1.endpoints import auth, sites, sensors, observations, tracks, incidents

app = FastAPI(title="AEROSHIELD API", version="2.0")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(sites.router, prefix="/api/v1/sites", tags=["sites"])
app.include_router(sensors.router, prefix="/api/v1/sensors", tags=["sensors"])
app.include_router(observations.router, prefix="/api/v1/observations", tags=["observations"])
app.include_router(tracks.router, prefix="/api/v1/tracks", tags=["tracks"])
app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["incidents"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
""")

if __name__ == "__main__":
    create_routers()
    create_main()
    print("Scaffolded Phase A API routers.")
