from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.proyecto_repository import proyecto_repository
from app.schemas.proyecto import ProyectoCreate, ProyectoUpdate
from app.models.proyecto import Proyecto

class ProyectoService:
    def __init__(self):
        self.repository = proyecto_repository

    async def create(self, db: AsyncSession, obj_in: ProyectoCreate) -> Proyecto:
        return await self.repository.create(db, obj_in)

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Proyecto]:
        return await self.repository.get_multi(db, skip=skip, limit=limit)

    async def get(self, db: AsyncSession, obj_id: int) -> Optional[Proyecto]:
        return await self.repository.get(db, obj_id)

    async def update(self, db: AsyncSession, obj_id: int, obj_in: ProyectoUpdate) -> Optional[Proyecto]:
        obj = await self.repository.get(db, obj_id)
        if not obj:
            return None
        return await self.repository.update(db, obj, obj_in)

    async def delete(self, db: AsyncSession, obj_id: int) -> bool:
        return await self.repository.delete(db, obj_id)

proyecto_service = ProyectoService()
