from fastapi import APIRouter
from app.api.v1.endpoints import timesheets

api_router = APIRouter()
api_router.include_router(timesheets.router, prefix="/timesheets", tags=["Timesheets"])
