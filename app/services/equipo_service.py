from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.equipo import Equipo, EquipoUsuario
from app.schemas.equipo import (
    EquipoCreate,
    EquipoUpdate,
    EquipoUsuarioCreate,
    EquipoUsuarioUpdate,
)


class EntityNotFoundError(Exception):
    pass


class EntityConflictError(Exception):
    pass


class EquipoService:
    async def get_equipos(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Equipo]:
        result = await db.execute(select(Equipo).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_equipo_by_id(self, db: AsyncSession, equipo_id: int) -> Equipo:
        result = await db.execute(select(Equipo).where(Equipo.id == equipo_id))
        equipo = result.scalar_one_or_none()
        if not equipo:
            raise EntityNotFoundError("Equipo no encontrado")
        return equipo

    async def create_equipo(self, db: AsyncSession, payload: EquipoCreate) -> Equipo:
        equipo = Equipo(**payload.model_dump())
        db.add(equipo)
        await db.flush()
        await db.refresh(equipo)
        return equipo

    async def update_equipo(
        self, db: AsyncSession, equipo_id: int, payload: EquipoUpdate
    ) -> Equipo:
        equipo = await self.get_equipo_by_id(db, equipo_id)
        for field, value in payload.model_dump().items():
            setattr(equipo, field, value)
        equipo.updated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(equipo)
        return equipo

    async def set_equipo_activo(
        self, db: AsyncSession, equipo_id: int, activo: bool
    ) -> Equipo:
        equipo = await self.get_equipo_by_id(db, equipo_id)
        equipo.activo = activo
        equipo.updated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(equipo)
        return equipo

    async def delete_equipo(self, db: AsyncSession, equipo_id: int) -> None:
        equipo = await self.get_equipo_by_id(db, equipo_id)
        await db.delete(equipo)
        await db.flush()

    async def get_equipo_usuarios(
        self, db: AsyncSession, equipo_id: int
    ) -> List[EquipoUsuario]:
        await self.get_equipo_by_id(db, equipo_id)
        result = await db.execute(
            select(EquipoUsuario).where(EquipoUsuario.equipo_id == equipo_id)
        )
        return result.scalars().all()

    async def add_usuario_to_equipo(
        self, db: AsyncSession, equipo_id: int, payload: EquipoUsuarioCreate
    ) -> EquipoUsuario:
        await self.get_equipo_by_id(db, equipo_id)
        existing = await self._get_equipo_usuario(db, equipo_id, payload.usuario_id)
        if existing:
            raise EntityConflictError("El usuario ya pertenece al equipo")

        equipo_usuario = EquipoUsuario(equipo_id=equipo_id, **payload.model_dump())
        db.add(equipo_usuario)
        await db.flush()
        await db.refresh(equipo_usuario)
        return equipo_usuario

    async def update_equipo_usuario(
        self,
        db: AsyncSession,
        equipo_id: int,
        usuario_id: int,
        payload: EquipoUsuarioUpdate,
    ) -> EquipoUsuario:
        equipo_usuario = await self._get_equipo_usuario_or_404(db, equipo_id, usuario_id)
        equipo_usuario.rol = payload.rol
        await db.flush()
        await db.refresh(equipo_usuario)
        return equipo_usuario

    async def update_equipo_usuario_rol(
        self, db: AsyncSession, equipo_id: int, usuario_id: int, rol: str
    ) -> EquipoUsuario:
        equipo_usuario = await self._get_equipo_usuario_or_404(db, equipo_id, usuario_id)
        equipo_usuario.rol = rol
        await db.flush()
        await db.refresh(equipo_usuario)
        return equipo_usuario

    async def delete_equipo_usuario(
        self, db: AsyncSession, equipo_id: int, usuario_id: int
    ) -> None:
        equipo_usuario = await self._get_equipo_usuario_or_404(db, equipo_id, usuario_id)
        await db.delete(equipo_usuario)
        await db.flush()

    async def _get_equipo_usuario(
        self, db: AsyncSession, equipo_id: int, usuario_id: int
    ) -> EquipoUsuario | None:
        result = await db.execute(
            select(EquipoUsuario)
            .where(EquipoUsuario.equipo_id == equipo_id)
            .where(EquipoUsuario.usuario_id == usuario_id)
        )
        return result.scalar_one_or_none()

    async def _get_equipo_usuario_or_404(
        self, db: AsyncSession, equipo_id: int, usuario_id: int
    ) -> EquipoUsuario:
        await self.get_equipo_by_id(db, equipo_id)
        equipo_usuario = await self._get_equipo_usuario(db, equipo_id, usuario_id)
        if not equipo_usuario:
            raise EntityNotFoundError("Usuario no pertenece al equipo")
        return equipo_usuario


equipo_service = EquipoService()
