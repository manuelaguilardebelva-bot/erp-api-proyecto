from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.timesheet import Log
from pydantic import BaseModel


class LogCreate(BaseModel):
    entity: str
    action: str
    message: str


class LogUpdate(BaseModel):
    pass


class LogRepository(BaseRepository[Log, LogCreate, LogUpdate]):
    pass


log_repository = LogRepository(Log)
