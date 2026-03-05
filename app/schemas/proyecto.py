from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProyectoBase(BaseModel):
    nombre: str = Field(..., max_length=120, description="Nombre del proyecto")
    descripcion: str = Field(..., max_length=500, description="Descripción del proyecto")
    cliente_id: int = Field(..., description="ID del cliente asociado")
    equipo_id: Optional[int] = Field(None, description="ID del equipo a cargo")
    mercado_id: Optional[int] = Field(None, description="ID del mercado objetivo")
    activo: Optional[bool] = Field(True, description="Estado del proyecto")


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=120)
    descripcion: Optional[str] = Field(None, max_length=500)
    cliente_id: Optional[int] = None
    equipo_id: Optional[int] = None
    mercado_id: Optional[int] = None
    activo: Optional[bool] = None


class ProyectoResponse(ProyectoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID único del proyecto")
    created_at: datetime
    updated_at: datetime
