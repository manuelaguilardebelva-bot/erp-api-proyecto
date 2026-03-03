from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
import uuid
from typing import List, Optional
from pydantic import BaseModel

from database import get_db
from models import Timesheet, TimesheetStatus, Tarea, TareaEstado, Log

router = APIRouter(tags=["Timesheets & Tareas"])

# --- Schemas ---
class TareaCreate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: TareaEstado = TareaEstado.pending
    asignado_a: Optional[uuid.UUID] = None

class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[TareaEstado] = None
    asignado_a: Optional[uuid.UUID] = None

class ClockInRequest(BaseModel):
    usuario_id: uuid.UUID

# --- Endpoints Timesheets ---

@router.post("/timesheets/clock-in", status_code=status.HTTP_201_CREATED)
async def clock_in(req: ClockInRequest, db: AsyncSession = Depends(get_db)):
    # Verificar si ya tiene una jornada abierta
    stmt = select(Timesheet).where(
        Timesheet.usuario_id == req.usuario_id,
        Timesheet.status == TimesheetStatus.open
    )
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Ya tienes una jornada activa")

    new_ts = Timesheet(usuario_id=req.usuario_id, status=TimesheetStatus.open)
    new_log = Log(
        entity="timesheet",
        action="clock-in",
        message=f"El usuario {req.usuario_id} ha iniciado jornada"
    )
    
    db.add(new_ts)
    db.add(new_log)
    await db.commit()
    return {"message": "Inicio de jornada registrado", "usuario_id": req.usuario_id}

@router.post("/timesheets/clock-out/{usuario_id}")
async def clock_out(usuario_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Timesheet).where(
        Timesheet.usuario_id == usuario_id,
        Timesheet.status == TimesheetStatus.open
    ).order_by(Timesheet.clock_in.desc())
    
    result = await db.execute(stmt)
    timesheet = result.scalar_one_or_none()

    if not timesheet:
        raise HTTPException(status_code=404, detail="No tienes ninguna jornada activa")

    current_time = datetime.utcnow()
    duration = current_time - timesheet.clock_in
    minutes_worked = int(duration.total_seconds() / 60)

    timesheet.clock_out = current_time
    timesheet.minutes_worked = minutes_worked
    timesheet.status = TimesheetStatus.closed

    new_log = Log(
        entity="timesheet",
        action="clock-out",
        message=f"El usuario {usuario_id} ha registrado {minutes_worked} minutos"
    )
    db.add(new_log)
    
    await db.commit()
    await db.refresh(timesheet)
    
    return {
        "message": "Cierre de jornada exitoso",
        "minutes_worked": minutes_worked
    }

@router.get("/timesheets")
async def list_timesheets(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Timesheet))
    return result.scalars().all()

# --- Endpoints Tareas ---

@router.get("/tareas")
async def list_tareas(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tarea))
    return result.scalars().all()

@router.post("/tareas", status_code=status.HTTP_201_CREATED)
async def create_tarea(tarea: TareaCreate, db: AsyncSession = Depends(get_db)):
    new_tarea = Tarea(**tarea.model_dump())
    new_log = Log(
        entity="tarea",
        action="create",
        message=f"Tarea '{tarea.titulo}' creada"
    )
    db.add(new_tarea)
    db.add(new_log)
    await db.commit()
    await db.refresh(new_tarea)
    return new_tarea

@router.put("/tareas/{id}")
async def update_tarea(id: int, tarea_data: TareaUpdate, db: AsyncSession = Depends(get_db)):
    stmt = select(Tarea).where(Tarea.id == id)
    result = await db.execute(stmt)
    tarea = result.scalar_one_or_none()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    update_data = tarea_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(tarea, key, value)
    
    new_log = Log(
        entity="tarea",
        action="update",
        message=f"Tarea ID {id} actualizada"
    )
    db.add(new_log)
    await db.commit()
    await db.refresh(tarea)
    return tarea

@router.delete("/tareas/{id}")
async def delete_tarea(id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Tarea).where(Tarea.id == id)
    result = await db.execute(stmt)
    tarea = result.scalar_one_or_none()
    
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    await db.delete(tarea)
    new_log = Log(
        entity="tarea",
        action="delete",
        message=f"Tarea ID {id} eliminada"
    )
    db.add(new_log)
    await db.commit()
    return {"message": f"Tarea {id} eliminada correctamente"}
