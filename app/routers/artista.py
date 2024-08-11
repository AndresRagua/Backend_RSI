# artista.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import ArtistaInvitado as ArtistaModel
from app.schemas import ArtistaCreate, Artista
from typing import List

router = APIRouter(
    prefix="/artista",
    tags=["Artistas"]
)

@router.post('/', response_model=Artista)
def crear_artista(artista: ArtistaCreate, db: Session = Depends(get_db)):
    nuevo_artista = ArtistaModel(**artista.dict())
    db.add(nuevo_artista)
    db.commit()
    db.refresh(nuevo_artista)
    return nuevo_artista

@router.get('/', response_model=List[Artista])
def obtener_artistas(db: Session = Depends(get_db)):
    artistas = db.query(ArtistaModel).all()
    return artistas

@router.get('/{artista_id}', response_model=Artista)
def obtener_artista_por_id(artista_id: int, db: Session = Depends(get_db)):
    artista = db.query(ArtistaModel).filter(ArtistaModel.id_artista == artista_id).first()
    if artista is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista

@router.put('/{artista_id}', response_model=Artista)
def actualizar_artista(artista_id: int, artista: ArtistaCreate, db: Session = Depends(get_db)):
    artista_db = db.query(ArtistaModel).filter(ArtistaModel.id_artista == artista_id).first()
    if artista_db is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    for key, value in artista.dict().items():
        setattr(artista_db, key, value)
    db.commit()
    db.refresh(artista_db)
    return artista_db

@router.delete('/{artista_id}', response_model=dict)
def eliminar_artista(artista_id: int, db: Session = Depends(get_db)):
    artista_db = db.query(ArtistaModel).filter(ArtistaModel.id_artista == artista_id).first()
    if artista_db is None:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    db.delete(artista_db)
    db.commit()
    return {"mensaje": "Artista eliminado satisfactoriamente"}
