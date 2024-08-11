# audio_servicio.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import AudioServicio as AudioServicioModel
from app.schemas import AudioServicioCreate, AudioServicio
from typing import List

router = APIRouter(
    prefix="/audio_servicio",
    tags=["Audios de Servicio Social"]
)

@router.post('/', response_model=AudioServicio)
def crear_audio_servicio(audio: AudioServicioCreate, db: Session = Depends(get_db)):
    nuevo_audio = AudioServicioModel(**audio.dict())
    db.add(nuevo_audio)
    db.commit()
    db.refresh(nuevo_audio)
    return nuevo_audio

@router.get('/', response_model=List[AudioServicio])
def obtener_audios_servicio(db: Session = Depends(get_db)):
    audios = db.query(AudioServicioModel).all()
    return audios

@router.get('/{audio_id}', response_model=AudioServicio)
def obtener_audio_servicio_por_id(audio_id: int, db: Session = Depends(get_db)):
    audio = db.query(AudioServicioModel).filter(AudioServicioModel.id_audio == audio_id).first()
    if audio is None:
        raise HTTPException(status_code=404, detail="Audio de servicio social no encontrado")
    return audio

@router.put('/{audio_id}', response_model=AudioServicio)
def actualizar_audio_servicio(audio_id: int, audio: AudioServicioCreate, db: Session = Depends(get_db)):
    audio_db = db.query(AudioServicioModel).filter(AudioServicioModel.id_audio == audio_id).first()
    if audio_db is None:
        raise HTTPException(status_code=404, detail="Audio de servicio social no encontrado")
    for key, value in audio.dict().items():
        setattr(audio_db, key, value)
    db.commit()
    db.refresh(audio_db)
    return audio_db

@router.delete('/{audio_id}', response_model=dict)
def eliminar_audio_servicio(audio_id: int, db: Session = Depends(get_db)):
    audio_db = db.query(AudioServicioModel).filter(AudioServicioModel.id_audio == audio_id).first()
    if audio_db is None:
        raise HTTPException(status_code=404, detail="Audio de servicio social no encontrado")
    db.delete(audio_db)
    db.commit()
    return {"mensaje": "Audio de servicio social eliminado satisfactoriamente"}
