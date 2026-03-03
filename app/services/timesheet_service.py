import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.timesheet_repository import timesheet_repository
from app.repositories.log_repository import log_repository, LogCreate
from app.models.timesheet import TimesheetStatus


class TimesheetService:
    def __init__(self):
        self.repository = timesheet_repository
        self.log_repository = log_repository

    async def clock_out(self, db: AsyncSession, usuario_id: uuid.UUID) -> dict:
        timesheet = await self.repository.get_active_timesheet(db, usuario_id)
        if not timesheet:
            raise ValueError("No tienes ninguna jornada activa")

        current_time = datetime.utcnow()
        duration = current_time - timesheet.clock_in
        minutes_worked = int(duration.total_seconds() / 60)

        # Actualizar timesheet
        await self.repository.update(
            db,
            timesheet,
            {
                "clock_out": current_time,
                "minutes_worked": minutes_worked,
                "status": TimesheetStatus.closed,
            },
        )

        # Insert log
        await self.log_repository.create(
            db,
            LogCreate(
                entity="timesheet",
                action="clock-out",
                message=f"El usuario {usuario_id} ha registrado {minutes_worked} minutos",
            ),
        )

        return {
            "message": "Cierre de jornada exitoso",
            "usuario_id": str(usuario_id),
            "minutes_worked": minutes_worked,
            "clock_in": timesheet.clock_in,
            "clock_out": current_time,
        }


timesheet_service = TimesheetService()
