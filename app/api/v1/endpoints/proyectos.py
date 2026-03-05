from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.usuario import Usuario
from app.schemas.proyecto import ProyectoCreate, ProyectoResponse, ProyectoUpdate
from app.services.proyecto_service import proyecto_service

router = APIRouter()


@router.get("/", response_model=List[ProyectoResponse])
async def read_proyectos(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Retrieve projects."""
    return await proyecto_service.get_all(db, skip=skip, limit=limit)


@router.post("/", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
async def create_proyecto(
    proyecto_in: ProyectoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Create new project."""
    return await proyecto_service.create(db, proyecto_in)


@router.get("/{id}", response_model=ProyectoResponse)
async def read_proyecto(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Get project by ID."""
    proyecto = await proyecto_service.get(db, id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return proyecto


@router.put("/{id}", response_model=ProyectoResponse)
async def update_proyecto(
    id: int,
    proyecto_in: ProyectoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Update a project."""
    proyecto = await proyecto_service.update(db, id, proyecto_in)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto not found")
    return proyecto


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proyecto(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Delete a project."""
    deleted = await proyecto_service.delete(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Proyecto not found")
