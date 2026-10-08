from fastapi import APIRouter, Depends, HTTPException
from app.simulation.models import SimulationConfig, SimulationStatus
from app.simulation.runtime import simulation_runtime
from app.api.dependencies.auth import RequirePermission, Operator

router = APIRouter()

@router.get("/status", response_model=SimulationStatus)
def get_status(current_operator: Operator = Depends(RequirePermission("admin:manage"))):
    return simulation_runtime.status

@router.post("/start", response_model=SimulationStatus)
def start_simulation(config: SimulationConfig, current_operator: Operator = Depends(RequirePermission("admin:manage"))):
    if not config.enabled:
        raise HTTPException(status_code=400, detail="Config must have enabled=True to start")
    try:
        simulation_runtime.start(config)
        return simulation_runtime.status
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/stop", response_model=SimulationStatus)
def stop_simulation(current_operator: Operator = Depends(RequirePermission("admin:manage"))):
    simulation_runtime.stop()
    return simulation_runtime.status
