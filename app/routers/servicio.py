from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import ServicioSocial as ServicioSocialModel, AudioServicio as AudioServicioModel
from app.schemas import ServicioSocialCreate, ServicioSocial, AudioServicioCreate, AudioServicio
from typing import List

router = APIRouter(
    prefix="/servicio_social",
    tags=["Servicios Sociales"]
)

@router.post('/', response_model=ServicioSocial)
def crear_servicio_social(servicio: ServicioSocialCreate, db: Session = Depends(get_db)):
    nuevo_servicio = ServicioSocialModel(
        nombre=servicio.nombre,
        informacion=servicio.informacion,
        url_image=servicio.url_image,
        url_pagina=servicio.url_pagina,
        tipo=servicio.tipo,
        nombre_audios=servicio.nombre_audios,
        fk_radio=servicio.fk_radio
    )
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio

@router.get('/', response_model=List[ServicioSocial])
def obtener_servicios_sociales(radio_id: int = Query(None), db: Session = Depends(get_db)):
    if radio_id:
        servicios = db.query(ServicioSocialModel).filter(ServicioSocialModel.fk_radio == radio_id).all()
    else:
        servicios = db.query(ServicioSocialModel).all()
    return servicios

@router.get('/{servicio_id}', response_model=ServicioSocial)
def obtener_servicio_social_por_id(servicio_id: int, db: Session = Depends(get_db)):
    servicio = db.query(ServicioSocialModel).filter(ServicioSocialModel.id_servicio == servicio_id).first()
    if servicio is None:
        raise HTTPException(status_code=404, detail="Servicio social no encontrado")
    return servicio

@router.put('/{servicio_id}', response_model=ServicioSocial)
def actualizar_servicio_social(servicio_id: int, servicio: ServicioSocialCreate, db: Session = Depends(get_db)):
    servicio_db = db.query(ServicioSocialModel).filter(ServicioSocialModel.id_servicio == servicio_id).first()
    if servicio_db is None:
        raise HTTPException(status_code=404, detail="Servicio social no encontrado")
    for key, value in servicio.dict().items():
        setattr(servicio_db, key, value)
    db.commit()
    db.refresh(servicio_db)
    return servicio_db

@router.delete('/{servicio_id}', response_model=dict)
def eliminar_servicio_social(servicio_id: int, db: Session = Depends(get_db)):
    servicio_db = db.query(ServicioSocialModel).filter(ServicioSocialModel.id_servicio == servicio_id).first()
    if servicio_db is None:
        raise HTTPException(status_code=404, detail="Servicio social no encontrado")
    db.delete(servicio_db)
    db.commit()
    return {"mensaje": "Servicio social eliminado satisfactoriamente"}

# Endpoints para los audios de servicios sociales
@router.post('/audio', response_model=AudioServicio)
def crear_audio_servicio(audio: AudioServicioCreate, db: Session = Depends(get_db)):
    nuevo_audio = AudioServicioModel(
        nombre=audio.nombre,
        fecha=audio.fecha,
        url_audio=audio.url_audio,
        fk_servicio=audio.fk_servicio
    )
    db.add(nuevo_audio)
    db.commit()
    db.refresh(nuevo_audio)
    return nuevo_audio

@router.get('/audio/{audio_id}', response_model=AudioServicio)
def obtener_audio_servicio_por_id(audio_id: int, db: Session = Depends(get_db)):
    audio = db.query(AudioServicioModel).filter(AudioServicioModel.id_audio == audio_id).first()
    if audio is None:
        raise HTTPException(status_code=404, detail="Audio del servicio social no encontrado")
    return audio

@router.put('/audio/{audio_id}', response_model=AudioServicio)
def actualizar_audio_servicio(audio_id: int, audio: AudioServicioCreate, db: Session = Depends(get_db)):
    audio_db = db.query(AudioServicioModel).filter(AudioServicioModel.id_audio == audio_id).first()
    if audio_db is None:
        raise HTTPException(status_code=404, detail="Audio del servicio social no encontrado")
    for key, value in audio.dict().items():
        setattr(audio_db, key, value)
    db.commit()
    db.refresh(audio_db)
    return audio_db

@router.delete('/audio/{audio_id}', response_model=dict)
def eliminar_audio_servicio(audio_id: int, db: Session = Depends(get_db)):
    audio_db = db.query(AudioServicioModel).filter(AudioServicioModel.id_audio == audio_id).first()
    if audio_db is None:
        raise HTTPException(status_code=404, detail="Audio del servicio social no encontrado")
    db.delete(audio_db)
    db.commit()
    return {"mensaje": "Audio del servicio social eliminado satisfactoriamente"}
