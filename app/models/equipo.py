from __future__ import annotations

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Equipo(Base):
    __tablename__ = "equipos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    usuarios: Mapped[List["EquipoUsuario"]] = relationship(
        "EquipoUsuario",
        back_populates="equipo",
        cascade="all, delete-orphan",
    )


class EquipoUsuario(Base):
    __tablename__ = "equipo_usuarios"
    __table_args__ = (
        UniqueConstraint("equipo_id", "usuario_id", name="uq_equipo_usuario"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    equipo_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("equipos.id", ondelete="CASCADE"), nullable=False, index=True
    )
    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rol: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )

    equipo: Mapped[Equipo] = relationship("Equipo", back_populates="usuarios")
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="equipos")
