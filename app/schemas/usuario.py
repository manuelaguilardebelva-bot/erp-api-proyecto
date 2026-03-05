from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.usuario import RolUsuario


# ── Base ──────────────────────────────────────────────────────────────────────

class UsuarioBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120, examples=["Juan García"])
    email: EmailStr


# ── Crear ─────────────────────────────────────────────────────────────────────

class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8, examples=["S3cret!XY"])
    rol: RolUsuario = RolUsuario.user


# ── Actualizar (PATCH parcial) ─────────────────────────────────────────────────

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=120)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)
    rol: Optional[RolUsuario] = None
    activo: Optional[bool] = None


# ── Respuesta pública (sin password) ──────────────────────────────────────────

class UsuarioResponse(UsuarioBase):
    id: int
    rol: RolUsuario
    activo: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ── Auth schemas ───────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse


class RegisterRequest(UsuarioCreate):
    """Registro público — el rol siempre será 'user' para registros externos."""
    pass
