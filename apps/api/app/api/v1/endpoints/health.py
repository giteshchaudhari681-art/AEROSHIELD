from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
async def get_health():
    return {"status": "ok", "service": "aeroshield-api"}

@router.get("/ready", tags=["health"])
async def get_ready():
    # TODO: Add database and redis checks here
    return {"status": "ready", "service": "aeroshield-api"}
