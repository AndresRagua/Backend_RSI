# hilo_musical.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import HiloMusical as HiloMusicalModel
from app.schemas import HiloMusicalCreate, HiloMusical
from typing import List

router = APIRouter(
    prefix="/hilo_musical",
    tags=["Hilos Musicales"]
)

@router.post('/', response_model=HiloMusical)
def crear_hilo_musical(hilo: HiloMusicalCreate, db: Session = Depends(get_db)):
    nuevo_hilo = HiloMusicalModel(**hilo.dict())
    db.add(nuevo_hilo)
    db.commit()
    db.refresh(nuevo_hilo)
    return nuevo_hilo

@router.get('/', response_model=List[HiloMusical])
def obtener_hilos_musicales(db: Session = Depends(get_db)):
    hilos = db.query(HiloMusicalModel).all()
    return hilos

@router.get('/{hilo_id}', response_model=HiloMusical)
def obtener_hilo_musical_por_id(hilo_id: int, db: Session = Depends(get_db)):
    hilo = db.query(HiloMusicalModel).filter(HiloMusicalModel.id_hilo == hilo_id).first()
    if hilo is None:
        raise HTTPException(status_code=404, detail="Hilo musical no encontrado")
    return hilo

@router.put('/{hilo_id}', response_model=HiloMusical)
def actualizar_hilo_musical(hilo_id: int, hilo: HiloMusicalCreate, db: Session = Depends(get_db)):
    hilo_db = db.query(HiloMusicalModel).filter(HiloMusicalModel.id_hilo == hilo_id).first()
    if hilo_db is None:
        raise HTTPException(status_code=404, detail="Hilo musical no encontrado")
    for key, value in hilo.dict().items():
        setattr(hilo_db, key, value)
    db.commit()
    db.refresh(hilo_db)
    return hilo_db

@router.delete('/{hilo_id}', response_model=dict)
def eliminar_hilo_musical(hilo_id: int, db: Session = Depends(get_db)):
    hilo_db = db.query(HiloMusicalModel).filter(HiloMusicalModel.id_hilo == hilo_id).first()
    if hilo_db is None:
        raise HTTPException(status_code=404, detail="Hilo musical no encontrado")
    db.delete(hilo_db)
    db.commit()
    return {"mensaje": "Hilo musical eliminado satisfactoriamente"}
