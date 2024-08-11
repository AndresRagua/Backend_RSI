# publicidad.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Publicidad as PublicidadModel
from app.schemas import PublicidadCreate, Publicidad
from typing import List

router = APIRouter(
    prefix="/publicidad",
    tags=["Publicidades"]
)

@router.post('/', response_model=Publicidad)
def crear_publicidad(publicidad: PublicidadCreate, db: Session = Depends(get_db)):
    nueva_publicidad = PublicidadModel(**publicidad.dict())
    db.add(nueva_publicidad)
    db.commit()
    db.refresh(nueva_publicidad)
    return nueva_publicidad

@router.get('/', response_model=List[Publicidad])
def obtener_publicidades(db: Session = Depends(get_db)):
    publicidades = db.query(PublicidadModel).all()
    return publicidades

@router.get('/{publicidad_id}', response_model=Publicidad)
def obtener_publicidad_por_id(publicidad_id: int, db: Session = Depends(get_db)):
    publicidad = db.query(PublicidadModel).filter(PublicidadModel.id_publicidad == publicidad_id).first()
    if publicidad is None:
        raise HTTPException(status_code=404, detail="Publicidad no encontrada")
    return publicidad

@router.put('/{publicidad_id}', response_model=Publicidad)
def actualizar_publicidad(publicidad_id: int, publicidad: PublicidadCreate, db: Session = Depends(get_db)):
    publicidad_db = db.query(PublicidadModel).filter(PublicidadModel.id_publicidad == publicidad_id).first()
    if publicidad_db is None:
        raise HTTPException(status_code=404, detail="Publicidad no encontrada")
    for key, value in publicidad.dict().items():
        setattr(publicidad_db, key, value)
    db.commit()
    db.refresh(publicidad_db)
    return publicidad_db

@router.delete('/{publicidad_id}', response_model=dict)
def eliminar_publicidad(publicidad_id: int, db: Session = Depends(get_db)):
    publicidad_db = db.query(PublicidadModel).filter(PublicidadModel.id_publicidad == publicidad_id).first()
    if publicidad_db is None:
        raise HTTPException(status_code=404, detail="Publicidad no encontrada")
    db.delete(publicidad_db)
    db.commit()
    return {"mensaje": "Publicidad eliminada satisfactoriamente"}
