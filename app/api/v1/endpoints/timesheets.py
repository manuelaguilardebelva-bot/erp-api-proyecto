import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.timesheet_service import timesheet_service
from app.schemas.timesheet import ClockOutResponse

router = APIRouter()


@router.post("/clock-out/{usuario_id}", response_model=ClockOutResponse)
async def clock_out(usuario_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = await timesheet_service.clock_out(db, usuario_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar en la base de datos: {str(e)}",
        )
