"""
usuarios.py — Endpoints de gestión de usuarios:
  GET    /usuarios           → lista todos (admin/manager)
  GET    /usuarios/{id}      → detalle (propietario o admin)
  PUT    /usuarios/{id}      → actualizar (propietario o admin)
  DELETE /usuarios/{id}      → eliminar permanentemente (solo admin)
  PATCH  /usuarios/{id}/activar    → reactivar usuario (admin)
  PATCH  /usuarios/{id}/desactivar → desactivar usuario (admin)
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.dependencies import get_current_user, require_rol
from app.core.database import get_db
from app.models.usuario import RolUsuario, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.services.usuario_service import usuario_service

router = APIRouter()


# ── GET /usuarios ──────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=List[UsuarioResponse],
    summary="Listar usuarios",
    description="Devuelve la lista de todos los usuarios. Requiere rol admin o manager.",
)
async def listar_usuarios(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Máximo de registros"),
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_rol(RolUsuario.admin, RolUsuario.manager)),
):
    return await usuario_service.obtener_todos(db, skip=skip, limit=limit)


# ── GET /usuarios/{id} ─────────────────────────────────────────────────────────

@router.get(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Obtener usuario por ID",
)
async def obtener_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # El propio usuario puede ver su perfil; admin/manager puede ver cualquiera
    if current_user.id != usuario_id and current_user.rol not in (
        RolUsuario.admin,
        RolUsuario.manager,
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")

    usuario = await usuario_service.obtener_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    return usuario


# ── PUT /usuarios/{id} ─────────────────────────────────────────────────────────

@router.put(
    "/{usuario_id}",
    response_model=UsuarioResponse,
    summary="Actualizar usuario",
    description=(
        "Actualiza los datos de un usuario. "
        "El propio usuario puede cambiar nombre, email y contraseña. "
        "Solo admin puede cambiar el rol o el estado activo."
    ),
)
async def actualizar_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # Sólo el propio usuario o un admin pueden modificar
    es_admin = current_user.rol == RolUsuario.admin
    es_propietario = current_user.id == usuario_id

    if not es_admin and not es_propietario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado.")

    # Usuarios no-admin no pueden cambiar rol ni estado activo
    if not es_admin:
        if datos.rol is not None or datos.activo is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un administrador puede cambiar el rol o el estado del usuario.",
            )

    usuario = await usuario_service.actualizar(db, usuario_id, datos)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    return usuario


# ── DELETE /usuarios/{id} ──────────────────────────────────────────────────────

@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar usuario",
    description="Elimina permanentemente el usuario. Solo administradores.",
)
async def eliminar_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_rol(RolUsuario.admin)),
):
    eliminado = await usuario_service.eliminar(db, usuario_id)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")


# ── PATCH /usuarios/{id}/activar ───────────────────────────────────────────────

@router.patch(
    "/{usuario_id}/activar",
    response_model=UsuarioResponse,
    summary="Activar usuario",
    description="Reactiva un usuario desactivado. Solo administradores.",
)
async def activar_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_rol(RolUsuario.admin)),
):
    usuario = await usuario_service.activar(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    return usuario


# ── PATCH /usuarios/{id}/desactivar ───────────────────────────────────────────

@router.patch(
    "/{usuario_id}/desactivar",
    response_model=UsuarioResponse,
    summary="Desactivar usuario",
    description="Desactiva un usuario (soft-delete lógico). Solo administradores.",
)
async def desactivar_usuario(
    usuario_id: int,
    db: AsyncSession = Depends(get_db),
    _: Usuario = Depends(require_rol(RolUsuario.admin)),
):
    usuario = await usuario_service.desactivar(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    return usuario
