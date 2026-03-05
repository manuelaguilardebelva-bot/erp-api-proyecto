"""
Router para el módulo de Mercado.

Registro en main.py:
    from routes.mercado import router as mercado_router
    app.include_router(mercado_router)
"""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.mercado_schema import MercadoCreate, MercadoResponse
from services import mercado_service

router = APIRouter(
    prefix="/mercado",
    tags=["Mercado"],
)


@router.get(
    "/",
    response_model=List[MercadoResponse],
    summary="Listar todos los mercados",
)
async def list_mercados(db: AsyncSession = Depends(get_db)):
    """Devuelve la lista completa de mercados registrados."""
    return await mercado_service.get_all_mercados(db)


@router.post(
    "/",
    response_model=MercadoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un mercado",
    responses={400: {"description": "Nombre de mercado duplicado"}},
)
async def create_mercado(
    payload: MercadoCreate, db: AsyncSession = Depends(get_db)
):
    """
    Crea un nuevo mercado.
    Valida que no exista otro mercado con el mismo nombre.
    """
    return await mercado_service.create_mercado(db, payload)
