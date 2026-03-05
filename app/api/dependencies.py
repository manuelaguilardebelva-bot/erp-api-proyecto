"""
Dependencias compartidas de autenticación y autorización para la API v1.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.usuario import RolUsuario, Usuario
from app.repositories.usuario_repository import usuario_repository

# El tokenUrl apunta al endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Usuario:
    """
    Dependencia: extrae y valida el JWT del header Authorization.
    Retorna el usuario autenticado o lanza 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    usuario = await usuario_repository.get(db, int(user_id))
    if usuario is None or not usuario.activo:
        raise credentials_exception

    return usuario


def require_rol(*roles: RolUsuario):
    """
    Fábrica de dependencias para exigir un rol específico.

    Uso:
        Depends(require_rol(RolUsuario.admin))
        Depends(require_rol(RolUsuario.admin, RolUsuario.manager))
    """
    async def _check(current_user: Usuario = Depends(get_current_user)) -> Usuario:
        if current_user.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes para esta acción.",
            )
        return current_user

    return _check
