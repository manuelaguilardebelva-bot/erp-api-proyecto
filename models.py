import enum
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class TimesheetStatus(enum.Enum):
    open = "open"
    closed = "closed"

class TareaEstado(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Timesheet(Base):
    __tablename__ = "timesheets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    clock_in: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    clock_out: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    minutes_worked: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[TimesheetStatus] = mapped_column(Enum(TimesheetStatus), default=TimesheetStatus.open, nullable=False)

    def __repr__(self):
        return f"<Timesheet(user={self.usuario_id}, status={self.status})>"

class Tarea(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    estado: Mapped[TareaEstado] = mapped_column(Enum(TareaEstado), default=TareaEstado.pending, nullable=False)
    asignado_a: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)

    def __repr__(self):
        return f"<Tarea(id={self.id}, titulo={self.titulo})>"

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity: Mapped[str] = mapped_column(String(50), nullable=False)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(String(500), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Log(entity={self.entity}, action={self.action})>"
