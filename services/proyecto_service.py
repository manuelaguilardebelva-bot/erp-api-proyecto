"""
Servicio para la lógica de negocio del módulo Proyectos.

Separa las operaciones de BD de los routers para mantener el código limpio
y fácilmente testeable.
"""

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.proyecto import Proyecto
from schemas.proyecto_schema import ProyectoCreate, ProyectoUpdate


async def get_all_proyectos(db: AsyncSession) -> List[Proyecto]:
    """Devuelve todos los proyectos registrados."""
    result = await db.execute(select(Proyecto))
    return list(result.scalars().all())


async def get_proyecto_by_id(db: AsyncSession, proyecto_id: int) -> Proyecto:
    """
    Devuelve un proyecto por su ID.
    Lanza HTTP 404 si no existe.
    """
    result = await db.execute(select(Proyecto).where(Proyecto.id == proyecto_id))
    proyecto = result.scalar_one_or_none()
    if proyecto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id={proyecto_id} no encontrado.",
        )
    return proyecto


async def create_proyecto(db: AsyncSession, data: ProyectoCreate) -> Proyecto:
    """Crea y persiste un nuevo proyecto."""
    nuevo = Proyecto(**data.model_dump())
    db.add(nuevo)
    try:
        await db.commit()
        await db.refresh(nuevo)
    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al guardar el proyecto en la base de datos.",
        ) from exc
    return nuevo


async def update_proyecto(
    db: AsyncSession, proyecto_id: int, data: ProyectoUpdate
) -> Proyecto:
    """
    Actualiza los campos enviados de un proyecto existente.
    Solo modifica los campos presentes en el payload (PATCH semántico).
    """
    proyecto = await get_proyecto_by_id(db, proyecto_id)

    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se proporcionaron campos para actualizar.",
        )

    for campo, valor in update_data.items():
        setattr(proyecto, campo, valor)

    try:
        await db.commit()
        await db.refresh(proyecto)
    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar el proyecto.",
        ) from exc
    return proyecto


async def delete_proyecto(db: AsyncSession, proyecto_id: int) -> dict:
    """Elimina un proyecto por su ID. Lanza HTTP 404 si no existe."""
    proyecto = await get_proyecto_by_id(db, proyecto_id)
    try:
        await db.delete(proyecto)
        await db.commit()
    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el proyecto.",
        ) from exc
    return {"message": f"Proyecto con id={proyecto_id} eliminado correctamente."}
