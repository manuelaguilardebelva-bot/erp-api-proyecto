import enum
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Enum, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class TimesheetStatus(enum.Enum):
    open = "open"
    closed = "closed"


class Timesheet(Base):
    __tablename__ = "timesheets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )
    clock_in: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    clock_out: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[TimesheetStatus] = mapped_column(
        Enum(TimesheetStatus), default=TimesheetStatus.open, nullable=False
    )
    minutes_worked: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

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
