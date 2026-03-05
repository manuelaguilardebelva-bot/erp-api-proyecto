"""
Router para el módulo de Proyectos.

Registro en main.py:
    from routes.proyectos import router as proyectos_router
    app.include_router(proyectos_router)
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.proyecto_schema import ProyectoCreate, ProyectoResponse, ProyectoUpdate
from services import proyecto_service

router = APIRouter(
    prefix="/proyectos",
    tags=["Proyectos"],
)


@router.get(
    "/",
    response_model=List[ProyectoResponse],
    summary="Listar todos los proyectos",
)
async def list_proyectos(db: AsyncSession = Depends(get_db)):
    """Devuelve la lista completa de proyectos registrados."""
    return await proyecto_service.get_all_proyectos(db)


@router.get(
    "/{proyecto_id}",
    response_model=ProyectoResponse,
    summary="Obtener un proyecto por ID",
    responses={404: {"description": "Proyecto no encontrado"}},
)
async def get_proyecto(proyecto_id: int, db: AsyncSession = Depends(get_db)):
    """Devuelve los datos de un proyecto específico. Retorna 404 si no existe."""
    return await proyecto_service.get_proyecto_by_id(db, proyecto_id)


@router.post(
    "/",
    response_model=ProyectoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un proyecto",
)
async def create_proyecto(
    payload: ProyectoCreate, db: AsyncSession = Depends(get_db)
):
    """Crea un nuevo proyecto con los datos proporcionados."""
    return await proyecto_service.create_proyecto(db, payload)


@router.put(
    "/{proyecto_id}",
    response_model=ProyectoResponse,
    summary="Actualizar un proyecto",
    responses={
        400: {"description": "Sin campos para actualizar"},
        404: {"description": "Proyecto no encontrado"},
    },
)
async def update_proyecto(
    proyecto_id: int,
    payload: ProyectoUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza los campos enviados de un proyecto existente.
    Solo se modifican los campos incluidos en el body.
    """
    return await proyecto_service.update_proyecto(db, proyecto_id, payload)


@router.delete(
    "/{proyecto_id}",
    summary="Eliminar un proyecto",
    responses={404: {"description": "Proyecto no encontrado"}},
)
async def delete_proyecto(proyecto_id: int, db: AsyncSession = Depends(get_db)):
    """Elimina definitivamente un proyecto por su ID."""
    return await proyecto_service.delete_proyecto(db, proyecto_id)
