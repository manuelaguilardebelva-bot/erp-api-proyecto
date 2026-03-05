from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usuario import Usuario
from app.repositories.base_repository import BaseRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


class UsuarioRepository(BaseRepository[Usuario, UsuarioCreate, UsuarioUpdate]):
    """Repositorio específico para operaciones con usuarios."""

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[Usuario]:
        """Busca un usuario por su email (único)."""
        result = await db.execute(select(Usuario).where(Usuario.email == email))
        return result.scalars().first()

    async def get_activos(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Usuario]:
        """Retorna únicamente los usuarios activos."""
        result = await db.execute(
            select(Usuario).where(Usuario.activo == True).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def activar(self, db: AsyncSession, usuario_id: int) -> Optional[Usuario]:
        """Activa un usuario desactivado."""
        usuario = await self.get(db, usuario_id)
        if usuario:
            usuario.activo = True
            await db.flush()
            await db.refresh(usuario)
        return usuario

    async def desactivar(self, db: AsyncSession, usuario_id: int) -> Optional[Usuario]:
        """Desactiva (soft-delete lógico) un usuario."""
        usuario = await self.get(db, usuario_id)
        if usuario:
            usuario.activo = False
            await db.flush()
            await db.refresh(usuario)
        return usuario


usuario_repository = UsuarioRepository(Usuario)
