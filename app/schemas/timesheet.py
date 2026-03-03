from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional
from app.models.timesheet import TimesheetStatus


class TimesheetBase(BaseModel):
    usuario_id: UUID4


class TimesheetCreate(TimesheetBase):
    pass


class TimesheetUpdate(TimesheetBase):
    clock_out: Optional[datetime] = None
    minutes_worked: Optional[int] = None
    status: Optional[TimesheetStatus] = None


class TimesheetResponse(TimesheetBase):
    id: UUID4
    clock_in: datetime
    clock_out: Optional[datetime]
    status: TimesheetStatus
    minutes_worked: int

    class Config:
        from_attributes = True


class ClockOutResponse(BaseModel):
    message: str
    usuario_id: str
    minutes_worked: int
    clock_in: datetime
    clock_out: datetime
