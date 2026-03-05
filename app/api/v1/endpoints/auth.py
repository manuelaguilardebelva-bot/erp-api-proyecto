"""
auth.py — Endpoints de autenticación:
  POST /auth/login     → devuelve JWT
  POST /auth/register  → registro público (rol=user)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token
from app.models.usuario import RolUsuario
from app.schemas.usuario import LoginRequest, RegisterRequest, TokenResponse, UsuarioResponse
from app.services.usuario_service import usuario_service

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Iniciar sesión",
    description="Autentica al usuario con email y contraseña. Retorna un JWT Bearer.",
)
async def login(
    datos: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    usuario = await usuario_service.autenticar(db, datos.email, datos.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos, o usuario inactivo.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(usuario.id)})
    return TokenResponse(
        access_token=access_token,
        usuario=UsuarioResponse.model_validate(usuario),
    )


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registro público",
    description=(
        "Crea una nueva cuenta de usuario con rol 'user'. "
        "Para asignar roles distintos usa el endpoint de administración."
    ),
)
async def register(
    datos: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        usuario = await usuario_service.crear_usuario(
            db, datos, forzar_rol=RolUsuario.user
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    return UsuarioResponse.model_validate(usuario)
