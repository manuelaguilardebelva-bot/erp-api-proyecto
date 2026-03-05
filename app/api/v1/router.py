from fastapi import APIRouter
from app.api.v1.endpoints import auth, equipos, timesheets, usuarios, mercados, proyectos

api_router = APIRouter()

# ── Auth ──────────────────────────────────────────────────────────────────────
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# ── Usuarios ──────────────────────────────────────────────────────────────────
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])

# ── Proyectos & Mercado ───────────────────────────────────────────────────────
api_router.include_router(mercados.router, prefix="/mercado", tags=["Mercado"])
api_router.include_router(proyectos.router, prefix="/proyectos", tags=["Proyectos"])

# ── Módulos existentes ────────────────────────────────────────────────────────
api_router.include_router(timesheets.router, prefix="/timesheets", tags=["Timesheets"])
api_router.include_router(equipos.router, prefix="/equipos", tags=["Equipos"])
