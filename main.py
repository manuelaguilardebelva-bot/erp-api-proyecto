from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from timesheets_router import router as api_router
from database import engine, Base

app = FastAPI(
    title="ERP API Profesional",
    description="Sistema de gestión de tiempos y tareas con auditoría",
    version="1.0.0"
)

# Incluir el router que contiene toda la lógica de negocio
app.include_router(api_router)

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