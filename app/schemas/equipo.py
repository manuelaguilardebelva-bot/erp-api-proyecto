from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EquipoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    descripcion: str = Field(min_length=1, max_length=500)


class EquipoCreate(EquipoBase):
    activo: bool = True


class EquipoUpdate(EquipoBase):
    activo: bool


class EquipoResponse(EquipoBase):
    id: int
    activo: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EquipoUsuarioBase(BaseModel):
    usuario_id: int
    rol: str = Field(min_length=1, max_length=80)


class EquipoUsuarioCreate(EquipoUsuarioBase):
    pass


class EquipoUsuarioUpdate(BaseModel):
    rol: str = Field(min_length=1, max_length=80)


class EquipoUsuarioRolPatch(BaseModel):
    rol: str = Field(min_length=1, max_length=80)


class EquipoUsuarioResponse(BaseModel):
    id: int
    equipo_id: int
    usuario_id: int
    rol: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
