from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.equipo import (
    EquipoCreate,
    EquipoResponse,
    EquipoUpdate,
    EquipoUsuarioCreate,
    EquipoUsuarioResponse,
    EquipoUsuarioRolPatch,
    EquipoUsuarioUpdate,
)
from app.services.equipo_service import (
    EntityConflictError,
    EntityNotFoundError,
    equipo_service,
)

router = APIRouter()


@router.get("/", response_model=List[EquipoResponse])
async def get_equipos(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await equipo_service.get_equipos(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=EquipoResponse)
async def get_equipo(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await equipo_service.get_equipo_by_id(db, id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/", response_model=EquipoResponse, status_code=status.HTTP_201_CREATED)
async def create_equipo(payload: EquipoCreate, db: AsyncSession = Depends(get_db)):
    return await equipo_service.create_equipo(db, payload)


@router.put("/{id}", response_model=EquipoResponse)
async def update_equipo(id: int, payload: EquipoUpdate, db: AsyncSession = Depends(get_db)):
    try:
        return await equipo_service.update_equipo(db, id, payload)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{id}/activar", response_model=EquipoResponse)
async def activar_equipo(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await equipo_service.set_equipo_activo(db, id, True)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{id}/desactivar", response_model=EquipoResponse)
async def desactivar_equipo(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await equipo_service.set_equipo_activo(db, id, False)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipo(id: int, db: AsyncSession = Depends(get_db)):
    try:
        await equipo_service.delete_equipo(db, id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{id}/usuarios", response_model=List[EquipoUsuarioResponse])
async def get_equipo_usuarios(id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await equipo_service.get_equipo_usuarios(db, id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post(
    "/{id}/usuarios",
    response_model=EquipoUsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_equipo_usuario(
    id: int, payload: EquipoUsuarioCreate, db: AsyncSession = Depends(get_db)
):
    try:
        return await equipo_service.add_usuario_to_equipo(db, id, payload)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except EntityConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{id}/usuarios/{usuario_id}", response_model=EquipoUsuarioResponse)
async def update_equipo_usuario(
    id: int,
    usuario_id: int,
    payload: EquipoUsuarioUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await equipo_service.update_equipo_usuario(db, id, usuario_id, payload)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{id}/usuarios/{usuario_id}/rol", response_model=EquipoUsuarioResponse)
async def update_equipo_usuario_rol(
    id: int,
    usuario_id: int,
    payload: EquipoUsuarioRolPatch,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await equipo_service.update_equipo_usuario_rol(
            db, id, usuario_id, payload.rol
        )
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_equipo_usuario(
    id: int, usuario_id: int, db: AsyncSession = Depends(get_db)
):
    try:
        await equipo_service.delete_equipo_usuario(db, id, usuario_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
