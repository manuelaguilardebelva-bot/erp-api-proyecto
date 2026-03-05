from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class MercadoBase(BaseModel):
    nombre: str = Field(..., max_length=120, description="Nombre del mercado")
    descripcion: str = Field(..., max_length=500, description="Descripción del mercado")
    activo: Optional[bool] = Field(True, description="Estado del mercado")


class MercadoCreate(MercadoBase):
    pass


class MercadoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=120)
    descripcion: Optional[str] = Field(None, max_length=500)
    activo: Optional[bool] = None


class MercadoResponse(MercadoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID único del mercado")
    created_at: datetime
    updated_at: datetime
