# programa.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError 
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
    if programa.fk_radio is None:
        raise HTTPException(status_code=400, detail="fk_radio es necesario")
    nueva_programacion = ProgramaModel(**programa.dict())
    db.add(nueva_programacion)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error en la integridad de los datos: " + str(e))
    db.refresh(nueva_programacion)
    return nueva_programacion

@router.get('/', response_model=List[Programa])
def obtener_programas(db: Session = Depends(get_db)):
    programas = db.query(ProgramaModel).options(joinedload(ProgramaModel.programaciones)).all()
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
