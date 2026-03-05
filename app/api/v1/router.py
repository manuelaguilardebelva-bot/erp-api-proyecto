from fastapi import APIRouter
from app.api.v1.endpoints import auth, clientes, equipos, timesheets, usuarios

api_router = APIRouter()

# ── Auth ──────────────────────────────────────────────────────────────────────
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# ── Usuarios ──────────────────────────────────────────────────────────────────
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])

# ── Clientes ─────────────────────────────────────────────────────────────────
api_router.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])

# ── Módulos existentes ────────────────────────────────────────────────────────
api_router.include_router(timesheets.router, prefix="/timesheets", tags=["Timesheets"])
api_router.include_router(equipos.router, prefix="/equipos", tags=["Equipos"])
