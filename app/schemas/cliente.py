from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClienteBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)
    cif: Optional[str] = Field(default=None, max_length=20)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(default=None, max_length=30)
    direccion: Optional[str] = None


class ClienteCreate(ClienteBase):
    activo: bool = True


class ClienteUpdate(ClienteBase):
    activo: bool


class ClienteResponse(ClienteBase):
    id: int
    activo: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
