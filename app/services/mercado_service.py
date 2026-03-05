from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.mercado_repository import mercado_repository
from app.schemas.mercado import MercadoCreate, MercadoUpdate
from app.models.mercado import Mercado

class MercadoService:
    def __init__(self):
        self.repository = mercado_repository

    async def create(self, db: AsyncSession, obj_in: MercadoCreate) -> Mercado:
        return await self.repository.create(db, obj_in)

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Mercado]:
        return await self.repository.get_multi(db, skip=skip, limit=limit)

    async def get(self, db: AsyncSession, obj_id: int) -> Optional[Mercado]:
        return await self.repository.get(db, obj_id)

    async def update(self, db: AsyncSession, obj_id: int, obj_in: MercadoUpdate) -> Optional[Mercado]:
        obj = await self.repository.get(db, obj_id)
        if not obj:
            return None
        return await self.repository.update(db, obj, obj_in)

    async def delete(self, db: AsyncSession, obj_id: int) -> bool:
        return await self.repository.delete(db, obj_id)

mercado_service = MercadoService()
