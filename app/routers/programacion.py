# programacion.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Programacion as ProgramacionModel
from app.schemas import ProgramacionCreate, Programacion
from typing import List

router = APIRouter(
    prefix="/programacion",
    tags=["Programaciones"]
)

@router.post('/', response_model=Programacion)
def crear_programacion(programacion: ProgramacionCreate, db: Session = Depends(get_db)):
    nueva_programacion = ProgramacionModel(**programacion.dict())
    db.add(nueva_programacion)
    db.commit()
    db.refresh(nueva_programacion)
    return nueva_programacion

@router.get('/', response_model=List[Programacion])
def obtener_programaciones(db: Session = Depends(get_db)):
    programaciones = db.query(ProgramacionModel).all()
    return programaciones

@router.get('/{programacion_id}', response_model=Programacion)
def obtener_programacion_por_id(programacion_id: int, db: Session = Depends(get_db)):
    programacion = db.query(ProgramacionModel).filter(ProgramacionModel.id_programacion == programacion_id).first()
    if programacion is None:
        raise HTTPException(status_code=404, detail="Programacion no encontrada")
    return programacion

@router.put('/{programacion_id}', response_model=Programacion)
def actualizar_programacion(programacion_id: int, programacion: ProgramacionCreate, db: Session = Depends(get_db)):
    programacion_db = db.query(ProgramacionModel).filter(ProgramacionModel.id_programacion == programacion_id).first()
    if programacion_db is None:
        raise HTTPException(status_code=404, detail="Programacion no encontrada")
    for key, value in programacion.dict().items():
        setattr(programacion_db, key, value)
    db.commit()
    db.refresh(programacion_db)
    return programacion_db

@router.delete('/{programacion_id}', response_model=dict)
def eliminar_programacion(programacion_id: int, db: Session = Depends(get_db)):
    programacion_db = db.query(ProgramacionModel).filter(ProgramacionModel.id_programacion == programacion_id).first()
    if programacion_db is None:
        raise HTTPException(status_code=404, detail="Programacion no encontrada")
    db.delete(programacion_db)
    db.commit()
    return {"mensaje": "Programacion eliminada satisfactoriamente"}
