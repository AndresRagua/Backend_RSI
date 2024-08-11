from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Radio as RadioModel
from app.schemas import RadioCreate, Radio  # Asumiendo que tienes un esquema para crear radios

router = APIRouter(
    prefix="/radio",
    tags=["Radios"]
)

@router.post('/agregar', response_model=Radio)
def crear_radio(radio: RadioCreate, db: Session = Depends(get_db)):
    try:
        radio_existente = db.query(RadioModel).filter(RadioModel.nombre == radio.nombre).first()
        if radio_existente:
            raise HTTPException(status_code=400, detail="El nombre de la radio ya está registrado")
        new_radio = RadioModel(
            nombre=radio.nombre,
            url_logo=radio.url_logo,
            url_audio=radio.url_audio,
            url_primer_fondo=radio.url_primer_fondo,
            url_segundo_fondo=radio.url_segundo_fondo,
            url_tercer_fondo=radio.url_tercer_fondo
        )
        db.add(new_radio)
        db.commit()
        db.refresh(new_radio)
        return new_radio
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar la radio: {str(e)}")

@router.get('/obtener', response_model=List[Radio])
def obtener_radios(db: Session = Depends(get_db)):
    radios = db.query(RadioModel).all()
    return radios

@router.get('/{radio_id}', response_model=Radio)
def obtener_radio_id(radio_id: int, db: Session = Depends(get_db)):
    radio = db.query(RadioModel).filter(RadioModel.id == radio_id).first()
    if radio is None:
        raise HTTPException(status_code=404, detail="Radio no encontrada")
    return radio

@router.put('/{radio_id}', response_model=Radio)
def actualizar_radio(radio_id: int, radio: RadioCreate, db: Session = Depends(get_db)):
    try:
        radio_db = db.query(RadioModel).filter(RadioModel.id == radio_id).first()
        if radio_db is None:
            raise HTTPException(status_code=404, detail="Radio no encontrada")
        radio_existente = db.query(RadioModel).filter(RadioModel.nombre == radio.nombre, RadioModel.id != radio_id).first()
        if radio_existente:
            raise HTTPException(status_code=400, detail="El nombre de la radio ya está registrado")
        radio_db.nombre = radio.nombre
        radio_db.url_logo = radio.url_logo
        radio_db.url_audio = radio.url_audio
        radio_db.url_primer_fondo = radio.url_primer_fondo
        radio_db.url_segundo_fondo = radio.url_segundo_fondo
        radio_db.url_tercer_fondo = radio.url_tercer_fondo
        db.commit()
        db.refresh(radio_db)
        return radio_db
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la radio: {str(e)}")

@router.delete('/{radio_id}', response_model=dict)
def eliminar_radio(radio_id: int, db: Session = Depends(get_db)):
    radio_db = db.query(RadioModel).filter(RadioModel.id == radio_id).first()
    if radio_db is None:
        raise HTTPException(status_code=404, detail="Radio no encontrada")
    db.delete(radio_db)
    db.commit()
    return {"mensaje": "Radio eliminada satisfactoriamente"}
