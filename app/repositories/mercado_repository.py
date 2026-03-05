from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mercado import Mercado
from app.repositories.base_repository import BaseRepository
from app.schemas.mercado import MercadoCreate, MercadoUpdate


class MercadoRepository(BaseRepository[Mercado, MercadoCreate, MercadoUpdate]):
    async def get_activos(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Mercado]:
        result = await db.execute(
            select(Mercado).where(Mercado.activo == True).offset(skip).limit(limit)
        )
        return result.scalars().all()


mercado_repository = MercadoRepository(Mercado)
