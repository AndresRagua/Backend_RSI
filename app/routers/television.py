from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Television as TelevisionModel
from app.schemas import TelevisionCreate, Television
from typing import List

router = APIRouter(
    prefix="/television",
    tags=["Television"]
)

@router.post('/agregar', response_model=Television)
def crear_television(television: TelevisionCreate, db: Session = Depends(get_db)):
    try:
        nueva_television = TelevisionModel(
            url_stream=television.url_stream,
            segundo_url_stream=television.segundo_url_stream,
            url_image_fondo=television.url_image_fondo,
            segundo_url_image_fondo=television.segundo_url_image_fondo,
            url_twitter=television.url_twitter,
            url_instagram=television.url_instagram,
            url_facebook=television.url_facebook,
            fk_radio=television.fk_radio
        )
        db.add(nueva_television)
        db.commit()
        db.refresh(nueva_television)
        return nueva_television
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar la televisión: {str(e)}")

@router.get('/obtener', response_model=List[Television])
def obtener_televisiones(db: Session = Depends(get_db)):
    televisiones = db.query(TelevisionModel).all()
    return televisiones

@router.get('/obtener_por_radio', response_model=List[Television])
def obtener_televisiones_por_radio(radio_id: int, db: Session = Depends(get_db)):
    televisiones = db.query(TelevisionModel).filter(TelevisionModel.fk_radio == radio_id).all()
    return televisiones

@router.get('/{television_id}', response_model=Television)
def obtener_television_id(television_id: int, db: Session = Depends(get_db)):
    television = db.query(TelevisionModel).filter(TelevisionModel.id_television == television_id).first()
    if television is None:
        raise HTTPException(status_code=404, detail="Televisión no encontrada")
    return television

@router.put('/{television_id}', response_model=Television)
def actualizar_television(television_id: int, television: TelevisionCreate, db: Session = Depends(get_db)):
    try:
        television_db = db.query(TelevisionModel).filter(TelevisionModel.id_television == television_id).first()
        if television_db is None:
            raise HTTPException(status_code=404, detail="Televisión no encontrada")
        television_db.url_stream = television.url_stream
        television_db.segundo_url_stream = television.segundo_url_stream
        television_db.url_image_fondo = television.url_image_fondo
        television_db.segundo_url_image_fondo = television.segundo_url_image_fondo
        television_db.url_twitter = television.url_twitter
        television_db.url_instagram = television.url_instagram
        television_db.url_facebook = television.url_facebook
        television_db.fk_radio = television.fk_radio
        db.commit()
        db.refresh(television_db)
        return television_db
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la televisión: {str(e)}")

@router.delete('/{television_id}', response_model=dict)
def eliminar_television(television_id: int, db: Session = Depends(get_db)):
    television_db = db.query(TelevisionModel).filter(TelevisionModel.id_television == television_id).first()
    if television_db is None:
        raise HTTPException(status_code=404, detail="Televisión no encontrada")
    db.delete(television_db)
    db.commit()
    return {"mensaje": "Televisión eliminada satisfactoriamente"}
