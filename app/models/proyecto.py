from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.equipo import Equipo
    from app.models.mercado import Mercado


class Proyecto(Base):
    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    cliente_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    equipo_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("equipos.id", ondelete="SET NULL"), nullable=True, index=True
    )
    mercado_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("mercados.id", ondelete="SET NULL"), nullable=True, index=True
    )
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    cliente: Mapped["Usuario"] = relationship("Usuario", foreign_keys=[cliente_id])
    equipo: Mapped[Optional["Equipo"]] = relationship("Equipo", foreign_keys=[equipo_id])
    mercado: Mapped[Optional["Mercado"]] = relationship("Mercado", back_populates="proyectos", foreign_keys=[mercado_id])
