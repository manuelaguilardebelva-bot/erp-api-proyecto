from fastapi import APIRouter
from app.api.v1.endpoints import equipos, timesheets

api_router = APIRouter()
api_router.include_router(timesheets.router, prefix="/timesheets", tags=["Timesheets"])
api_router.include_router(equipos.router, prefix="/equipos", tags=["Equipos"])
