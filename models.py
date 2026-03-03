import enum
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class TimesheetStatus(enum.Enum):
    open = "open"
    closed = "closed"

class Timesheet(Base):
    __tablename__ = "timesheets"

    # ID principal del registro (UUID)
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    
    # ID del usuario al que pertenece el registro
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        nullable=False,
        index=True
    )
    
    # Registro de entrada
    clock_in: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        default=datetime.utcnow
    )
    
    # Registro de salida (opcional)
    clock_out: Mapped[Optional[datetime]] = mapped_column(
        DateTime, 
        nullable=True
    )
    
    # Estado del registro (Enum)
    status: Mapped[TimesheetStatus] = mapped_column(
        Enum(TimesheetStatus), 
        default=TimesheetStatus.open,
        nullable=False
    )
    
    # Minutos totales trabajados
    minutes_worked: Mapped[int] = mapped_column(
        Integer, 
        default=0,
        nullable=False
    )

    def __repr__(self):
        return f"<Timesheet(user={self.usuario_id}, status={self.status})>"

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    entity: Mapped[str] = mapped_column(nullable=False)
    action: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Log(entity={self.entity}, action={self.action})>"
