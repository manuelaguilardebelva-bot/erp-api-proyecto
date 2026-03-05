from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from models.proyecto import ProyectoEstado


# ─── Base ────────────────────────────────────────────────────────────────────

class ProyectoBase(BaseModel):
    """Campos compartidos entre creación y actualización."""

    nombre: str = Field(..., min_length=1, max_length=255, examples=["Plataforma ERP"])
    descripcion: Optional[str] = Field(None, examples=["Sistema de gestión empresarial"])
    cliente_id: Optional[int] = Field(None, examples=[1])
    equipo_id: Optional[int] = Field(None, examples=[2])
    mercado_id: Optional[int] = Field(None, examples=[3])
    estado: ProyectoEstado = Field(ProyectoEstado.activo, examples=["activo"])
    fecha_inicio: Optional[date] = Field(None, examples=["2024-01-15"])
    fecha_fin: Optional[date] = Field(None, examples=["2024-12-31"])


# ─── Create ───────────────────────────────────────────────────────────────────

class ProyectoCreate(ProyectoBase):
    """Payload para crear un proyecto."""
    pass


# ─── Update ───────────────────────────────────────────────────────────────────

class ProyectoUpdate(BaseModel):
    """Payload para actualizar un proyecto (todos los campos son opcionales)."""

    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    descripcion: Optional[str] = None
    cliente_id: Optional[int] = None
    equipo_id: Optional[int] = None
    mercado_id: Optional[int] = None
    estado: Optional[ProyectoEstado] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


# ─── Response ─────────────────────────────────────────────────────────────────

class ProyectoResponse(ProyectoBase):
    """Schema de respuesta — incluye el id generado por la BD."""

    id: int

    model_config = {"from_attributes": True}
