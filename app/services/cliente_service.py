from datetime import datetime
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cliente import Cliente
from app.repositories.cliente_repository import cliente_repository
from app.schemas.cliente import ClienteCreate, ClienteUpdate


class EntityNotFoundError(Exception):
    pass


class EntityConflictError(Exception):
    pass


class ClienteService:

    async def get_clientes(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        activo: Optional[bool] = None,
        nombre: Optional[str] = None,
    ) -> List[Cliente]:
        """Retorna la lista de clientes con soporte de filtros opcionales."""
        if nombre:
            return await cliente_repository.get_by_nombre(db, nombre, skip=skip, limit=limit)
        if activo is not None:
            return await cliente_repository.get_by_activo(db, activo, skip=skip, limit=limit)
        return await cliente_repository.get_multi(db, skip=skip, limit=limit)

    async def get_cliente_by_id(self, db: AsyncSession, cliente_id: int) -> Cliente:
        """Obtiene un cliente por su ID o lanza EntityNotFoundError."""
        cliente = await cliente_repository.get(db, cliente_id)
        if not cliente:
            raise EntityNotFoundError("Cliente no encontrado")
        return cliente

    async def create_cliente(self, db: AsyncSession, payload: ClienteCreate) -> Cliente:
        """Crea un nuevo cliente, validando unicidad de CIF si se provee."""
        if payload.cif:
            existing = await cliente_repository.get_by_cif(db, payload.cif)
            if existing:
                raise EntityConflictError(f"Ya existe un cliente con el CIF '{payload.cif}'")
        return await cliente_repository.create(db, payload)

    async def update_cliente(
        self, db: AsyncSession, cliente_id: int, payload: ClienteUpdate
    ) -> Cliente:
        """Actualiza todos los campos de un cliente existente."""
        cliente = await self.get_cliente_by_id(db, cliente_id)

        # Validar unicidad del CIF si cambia
        if payload.cif and payload.cif != cliente.cif:
            existing = await cliente_repository.get_by_cif(db, payload.cif)
            if existing:
                raise EntityConflictError(f"Ya existe un cliente con el CIF '{payload.cif}'")

        for field, value in payload.model_dump().items():
            setattr(cliente, field, value)
        cliente.updated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(cliente)
        return cliente

    async def delete_cliente(self, db: AsyncSession, cliente_id: int) -> None:
        """Elimina permanentemente un cliente."""
        await self.get_cliente_by_id(db, cliente_id)
        deleted = await cliente_repository.delete(db, cliente_id)
        if not deleted:
            raise EntityNotFoundError("Cliente no encontrado")


cliente_service = ClienteService()
