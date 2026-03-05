from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.proyecto import Proyecto
from app.repositories.base_repository import BaseRepository
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate


class ProyectoRepository(BaseRepository[Proyecto, ProyectoCreate, ProyectoUpdate]):
    async def get_multi_with_relations(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Proyecto]:
        result = await db.execute(
            select(Proyecto)
            .options(
                selectinload(Proyecto.cliente),
                selectinload(Proyecto.equipo),
                selectinload(Proyecto.mercado)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_with_relations(self, db: AsyncSession, id: int) -> Optional[Proyecto]:
        result = await db.execute(
            select(Proyecto)
            .options(
                selectinload(Proyecto.cliente),
                selectinload(Proyecto.equipo),
                selectinload(Proyecto.mercado)
            )
            .where(Proyecto.id == id)
        )
        return result.scalars().first()

    async def get_activos(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Proyecto]:
        result = await db.execute(
            select(Proyecto).where(Proyecto.activo == True).offset(skip).limit(limit)
        )
        return result.scalars().all()


proyecto_repository = ProyectoRepository(Proyecto)
