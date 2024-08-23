from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Programa as ProgramaModel
from app.schemas import ProgramaCreate, Programa
from typing import List

router = APIRouter(
    prefix="/programa",
    tags=["Programas"]
)

@router.post('/', response_model=Programa)
def crear_programa(programa: ProgramaCreate, db: Session = Depends(get_db)):
    nuevo_programa = ProgramaModel(**programa.dict())
    db.add(nuevo_programa)
    db.commit()
    db.refresh(nuevo_programa)
    return nuevo_programa

@router.get('/', response_model=List[Programa])
def obtener_programas(radio_id: int = Query(None), db: Session = Depends(get_db)):
    if radio_id is not None:
        programas = db.query(ProgramaModel).filter(ProgramaModel.fk_radio == radio_id).all()
    else:
        programas = db.query(ProgramaModel).all()
    return programas

@router.get('/{programa_id}', response_model=Programa)
def obtener_programa_por_id(programa_id: int, db: Session = Depends(get_db)):
    programa = db.query(ProgramaModel).filter(ProgramaModel.id_programa == programa_id).first()
    if programa is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    return programa

@router.put('/{programa_id}', response_model=Programa)
def actualizar_programa(programa_id: int, programa: ProgramaCreate, db: Session = Depends(get_db)):
    programa_db = db.query(ProgramaModel).filter(ProgramaModel.id_programa == programa_id).first()
    if programa_db is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    for key, value in programa.dict().items():
        setattr(programa_db, key, value)
    db.commit()
    db.refresh(programa_db)
    return programa_db

@router.delete('/{programa_id}', response_model=dict)
def eliminar_programa(programa_id: int, db: Session = Depends(get_db)):
    programa_db = db.query(ProgramaModel).filter(ProgramaModel.id_programa == programa_id).first()
    if programa_db is None:
        raise HTTPException(status_code=404, detail="Programa no encontrado")
    db.delete(programa_db)
    db.commit()
    return {"mensaje": "Programa eliminado satisfactoriamente"}
