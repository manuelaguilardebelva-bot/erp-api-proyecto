from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cliente import Cliente
from app.repositories.base_repository import BaseRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class ClienteRepository(BaseRepository[Cliente, ClienteCreate, ClienteUpdate]):
    """Repositorio específico para operaciones con clientes."""

    async def get_by_nombre(
        self, db: AsyncSession, nombre: str, skip: int = 0, limit: int = 100
    ) -> List[Cliente]:
        """Busca clientes cuyo nombre contenga el texto indicado (case-insensitive)."""
        result = await db.execute(
            select(Cliente)
            .where(Cliente.nombre.ilike(f"%{nombre}%"))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_activo(
        self, db: AsyncSession, activo: bool, skip: int = 0, limit: int = 100
    ) -> List[Cliente]:
        """Retorna clientes filtrados por estado activo/inactivo."""
        result = await db.execute(
            select(Cliente)
            .where(Cliente.activo == activo)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_cif(self, db: AsyncSession, cif: str) -> Optional[Cliente]:
        """Busca un cliente por su CIF (único)."""
        result = await db.execute(select(Cliente).where(Cliente.cif == cif))
        return result.scalars().first()


cliente_repository = ClienteRepository(Cliente)
