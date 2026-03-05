import enum
from datetime import date
from typing import Optional
from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class ProyectoEstado(enum.Enum):
    activo = "activo"
    en_pausa = "en_pausa"
    completado = "completado"
    cancelado = "cancelado"


class Proyecto(Base):
    """Modelo SQLAlchemy para la tabla 'proyectos'."""

    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cliente_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    equipo_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    mercado_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    estado: Mapped[ProyectoEstado] = mapped_column(
        Enum(ProyectoEstado),
        default=ProyectoEstado.activo,
        nullable=False,
    )
    fecha_inicio: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    fecha_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    def __repr__(self) -> str:
        return f"<Proyecto(id={self.id}, nombre={self.nombre}, estado={self.estado})>"
