from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.usuario import RolUsuario, Usuario
from app.repositories.usuario_repository import usuario_repository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate


class UsuarioService:
    """Lógica de negocio para la gestión de usuarios."""

    def __init__(self):
        self.repo = usuario_repository

    # ── CRUD ──────────────────────────────────────────────────────────────────

    async def crear_usuario(
        self, db: AsyncSession, data: UsuarioCreate, forzar_rol: Optional[RolUsuario] = None
    ) -> Usuario:
        """
        Crea un nuevo usuario.
        - Verifica que el email no esté en uso.
        - Hashea la contraseña antes de persistir.
        - Si `forzar_rol` se pasa (ej. registro público), sobreescribe el rol indicado.
        """
        existente = await self.repo.get_by_email(db, data.email)
        if existente:
            raise ValueError("El email ya está registrado.")

        hashed = get_password_hash(data.password)
        rol = forzar_rol or data.rol

        usuario = Usuario(
            nombre=data.nombre,
            email=data.email,
            hashed_password=hashed,
            rol=rol,
            activo=True,
        )
        db.add(usuario)
        await db.flush()
        await db.refresh(usuario)
        return usuario

    async def obtener_todos(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Usuario]:
        return await self.repo.get_multi(db, skip=skip, limit=limit)

    async def obtener_por_id(self, db: AsyncSession, usuario_id: int) -> Optional[Usuario]:
        return await self.repo.get(db, usuario_id)

    async def actualizar(
        self, db: AsyncSession, usuario_id: int, data: UsuarioUpdate
    ) -> Optional[Usuario]:
        usuario = await self.repo.get(db, usuario_id)
        if not usuario:
            return None

        update_dict = data.model_dump(exclude_unset=True)

        # Si viene nueva contraseña, hashear antes de guardar
        if "password" in update_dict:
            update_dict["hashed_password"] = get_password_hash(update_dict.pop("password"))

        return await self.repo.update(db, usuario, update_dict)

    async def eliminar(self, db: AsyncSession, usuario_id: int) -> bool:
        return await self.repo.delete(db, usuario_id)

    async def activar(self, db: AsyncSession, usuario_id: int) -> Optional[Usuario]:
        return await self.repo.activar(db, usuario_id)

    async def desactivar(self, db: AsyncSession, usuario_id: int) -> Optional[Usuario]:
        return await self.repo.desactivar(db, usuario_id)

    # ── Auth ───────────────────────────────────────────────────────────────────

    async def autenticar(
        self, db: AsyncSession, email: str, password: str
    ) -> Optional[Usuario]:
        """Autentica por email + contraseña. Devuelve el usuario o None."""
        usuario = await self.repo.get_by_email(db, email)
        if not usuario:
            return None
        if not verify_password(password, usuario.hashed_password):
            return None
        if not usuario.activo:
            return None
        return usuario


usuario_service = UsuarioService()
