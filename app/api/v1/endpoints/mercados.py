from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.mercado import MercadoCreate, MercadoResponse, MercadoUpdate
from app.services.mercado_service import mercado_service

router = APIRouter()

@router.get("/", response_model=List[MercadoResponse])
async def read_mercados(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Retrieve markets."""
    return await mercado_service.get_all(db, skip=skip, limit=limit)

@router.post("/", response_model=MercadoResponse, status_code=status.HTTP_201_CREATED)
async def create_mercado(
    mercado_in: MercadoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Create new market."""
    return await mercado_service.create(db, mercado_in)

@router.get("/{id}", response_model=MercadoResponse)
async def read_mercado(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Get market by ID."""
    mercado = await mercado_service.get(db, id)
    if not mercado:
        raise HTTPException(status_code=404, detail="Mercado not found")
    return mercado

@router.put("/{id}", response_model=MercadoResponse)
async def update_mercado(
    id: int,
    mercado_in: MercadoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Update a market."""
    mercado = await mercado_service.update(db, id, mercado_in)
    if not mercado:
        raise HTTPException(status_code=404, detail="Mercado not found")
    return mercado

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mercado(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Delete a market."""
    deleted = await mercado_service.delete(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Mercado not found")
