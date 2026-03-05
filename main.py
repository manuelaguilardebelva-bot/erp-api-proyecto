from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
#from timesheets_router import router as api_router
from database import engine, Base

# ── Módulo Proyectos & Mercado ─────────────────────────────────────────────────
from routes.proyectos import router as proyectos_router
from routes.mercado import router as mercado_router

app = FastAPI(
    title="ERP API Profesional",
    description="Sistema de gestión de tiempos, tareas, proyectos y mercado",
    version="1.0.0"
)

# Routers existentes
#app.include_router(api_router)

# Routers del módulo Proyectos & Mercado
app.include_router(proyectos_router)
app.include_router(mercado_router)

@app.on_event("startup")
async def startup():
    # Crear tablas automáticamente en Neon al iniciar (Práctico para desarrollo)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {
        "app": "ERP API",
        "status": "online",
        "docs": "/docs"
    }