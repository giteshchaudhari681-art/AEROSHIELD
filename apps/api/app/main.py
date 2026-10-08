from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.v1.endpoints import health, websockets, sites, assets, zones, sensors, tracks, observations, alerts, incidents, auth, digital_twin

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title="AEROSHIELD API",
    description="Infrastructure-Aware Airspace Security & Threat Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(websockets.router, prefix="/api/v1")
app.include_router(sites.router, prefix="/api/v1/sites", tags=["Sites"])
app.include_router(digital_twin.router, prefix="/api/v1", tags=["Digital Twin"])
app.include_router(assets.router, prefix="/api/v1/sites/{site_id}/assets", tags=["Assets"])
app.include_router(zones.router, prefix="/api/v1/sites/{site_id}/zones", tags=["Zones"])
app.include_router(sensors.router, prefix="/api/v1/sites/{site_id}/sensors", tags=["Sensors"])
app.include_router(tracks.router, prefix="/api/v1/tracks", tags=["Tracks"])
app.include_router(observations.router, prefix="/api/v1/observations", tags=["Observations"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["Incidents"])

