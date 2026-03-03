from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
import uuid

from database import get_db
from models import Timesheet, TimesheetStatus, Log

router = APIRouter(
    prefix="/timesheets",
    tags=["Timesheets"]
)

@router.post("/clock-out/{usuario_id}")
def clock_out(usuario_id: uuid.UUID, db: Session = Depends(get_db)):
    # 1. Buscar el registro de Timesheet más reciente para ese usuario que todavía tenga el status == 'open'
    stmt = (
        select(Timesheet)
        .where(Timesheet.usuario_id == usuario_id)
        .where(Timesheet.status == TimesheetStatus.open)
        .order_by(Timesheet.clock_in.desc())
        .limit(1)
    )
    
    result = db.execute(stmt)
    timesheet = result.scalar_one_or_none()

    # 2. Si no hay ninguno abierto, devuelve un error 404
    if not timesheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tienes ninguna jornada activa"
        )

    # 3. Lógica de cálculo de tiempo
    current_time = datetime.utcnow()
    
    # Calcular la diferencia entre clock_out y clock_in
    duration = current_time - timesheet.clock_in
    
    # Convertir esa diferencia a minutos totales (entero)
    minutes_worked = int(duration.total_seconds() / 60)

    # 4. Actualizar el modelo
    timesheet.clock_out = current_time
    timesheet.minutes_worked = minutes_worked
    timesheet.status = TimesheetStatus.closed

    # 5. Registro en la tabla logs
    new_log = Log(
        entity="timesheet",
        action="clock-out",
        message=f"El usuario {usuario_id} ha registrado {minutes_worked} minutos"
    )
    db.add(new_log)

    # 6. Seguridad: Commit y refresh
    try:
        db.commit()
        db.refresh(timesheet)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar en la base de datos: {str(e)}"
        )

    # 7. Devolver JSON con los minutos trabajados
    return {
        "message": "Cierre de jornada exitoso",
        "usuario_id": str(usuario_id),
        "minutes_worked": timesheet.minutes_worked,
        "clock_in": timesheet.clock_in,
        "clock_out": timesheet.clock_out
    }
