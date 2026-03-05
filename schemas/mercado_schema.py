from typing import Optional
from pydantic import BaseModel, Field


# ─── Base ────────────────────────────────────────────────────────────────────

class MercadoBase(BaseModel):
    """Campos compartidos entre creación y respuesta."""

    nombre: str = Field(..., min_length=1, max_length=255, examples=["Tecnología"])
    descripcion: Optional[str] = Field(
        None, examples=["Mercado enfocado en soluciones tecnológicas"]
    )


# ─── Create ───────────────────────────────────────────────────────────────────

class MercadoCreate(MercadoBase):
    """Payload para crear un mercado."""
    pass


# ─── Response ─────────────────────────────────────────────────────────────────

class MercadoResponse(MercadoBase):
    """Schema de respuesta — incluye el id generado por la BD."""

    id: int

    model_config = {"from_attributes": True}
