from __future__ import annotations

from datetime import datetime
from enum import Enum as PyEnum
from typing import List, TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.equipo import EquipoUsuario


class RolUsuario(str, PyEnum):
    admin = "admin"
    manager = "manager"
    user = "user"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(
        Enum(RolUsuario, name="rol_usuario"),
        nullable=False,
        default=RolUsuario.user,
    )
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    equipos: Mapped[List["EquipoUsuario"]] = relationship(
        "EquipoUsuario",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
