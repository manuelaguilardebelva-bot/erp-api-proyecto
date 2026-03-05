"""
Servicio para la lógica de negocio del módulo Mercado.
"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.mercado import Mercado
from schemas.mercado_schema import MercadoCreate


async def get_all_mercados(db: AsyncSession) -> List[Mercado]:
    """Devuelve todos los mercados registrados."""
    result = await db.execute(select(Mercado))
    return list(result.scalars().all())


async def create_mercado(db: AsyncSession, data: MercadoCreate) -> Mercado:
    """
    Crea y persiste un nuevo mercado.
    Valida que no exista otro mercado con el mismo nombre.
    """
    # Verificar nombre duplicado
    result = await db.execute(select(Mercado).where(Mercado.nombre == data.nombre))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un mercado con el nombre '{data.nombre}'.",
        )

    nuevo = Mercado(**data.model_dump())
    db.add(nuevo)
    try:
        await db.commit()
        await db.refresh(nuevo)
    except Exception as exc:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al guardar el mercado en la base de datos.",
        ) from exc
    return nuevo
