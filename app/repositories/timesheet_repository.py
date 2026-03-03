import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.repositories.base_repository import BaseRepository
from app.models.timesheet import Timesheet, TimesheetStatus
from app.schemas.timesheet import TimesheetCreate, TimesheetUpdate


class TimesheetRepository(BaseRepository[Timesheet, TimesheetCreate, TimesheetUpdate]):
    async def get_active_timesheet(
        self, db: AsyncSession, usuario_id: uuid.UUID
    ) -> Optional[Timesheet]:
        stmt = (
            select(Timesheet)
            .where(Timesheet.usuario_id == usuario_id)
            .where(Timesheet.status == TimesheetStatus.open)
            .order_by(Timesheet.clock_in.desc())
            .limit(1)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()


timesheet_repository = TimesheetRepository(Timesheet)
