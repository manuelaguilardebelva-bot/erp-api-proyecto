from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services.cliente_service import (
    EntityConflictError,
    EntityNotFoundError,
    cliente_service,
)

router = APIRouter()


@router.get("/", response_model=List[ClienteResponse])
async def get_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    activo: Optional[bool] = Query(None, description="Filtra por estado activo/inactivo"),
    nombre: Optional[str] = Query(None, description="Búsqueda parcial por nombre"),
    db: AsyncSession = Depends(get_db),
):
    """Devuelve la lista de clientes. Soporta filtros por `activo` y búsqueda por `nombre`."""
    return await cliente_service.get_clientes(
        db, skip=skip, limit=limit, activo=activo, nombre=nombre
    )


@router.get("/{id}", response_model=ClienteResponse)
async def get_cliente(id: int, db: AsyncSession = Depends(get_db)):
    """Devuelve un cliente por su ID."""
    try:
        return await cliente_service.get_cliente_by_id(db, id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def create_cliente(payload: ClienteCreate, db: AsyncSession = Depends(get_db)):
    """Crea un nuevo cliente."""
    try:
        return await cliente_service.create_cliente(db, payload)
    except EntityConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}", response_model=ClienteResponse)
async def update_cliente(
    id: int, payload: ClienteUpdate, db: AsyncSession = Depends(get_db)
):
    """Reemplaza todos los campos de un cliente existente."""
    try:
        return await cliente_service.update_cliente(db, id, payload)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cliente(id: int, db: AsyncSession = Depends(get_db)):
    """Elimina permanentemente un cliente."""
    try:
        await cliente_service.delete_cliente(db, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
