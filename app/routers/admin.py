from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Administrador as AdministradorModel
from app.schemas import AdministradorCreate, Administrador, AdministradorLogin
from passlib.context import CryptContext
from jose import jwt

router = APIRouter(
    prefix="/admin",
    tags=["Administradores"]
)

# Configuración de Passlib para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "123456"  # Cambia esto por una clave secreta segura
ALGORITHM = "HS256"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/login')
def login(administrador: AdministradorLogin, db: Session = Depends(get_db)):
    admin_db = db.query(AdministradorModel).filter(AdministradorModel.email == administrador.email).first()
    if not admin_db or not verify_password(administrador.password, admin_db.password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    access_token = create_access_token(data={"sub": admin_db.email})
    return {"token": access_token}

@router.post('/agregar', response_model=Administrador)
def crear_administrador(administrador: AdministradorCreate, db: Session = Depends(get_db)):
    new_administrador = AdministradorModel(
        nombre=administrador.nombre,
        apellido=administrador.apellido,
        email=administrador.email,
        password=pwd_context.hash(administrador.password)  # Hashear la contraseña antes de almacenarla
    )
    db.add(new_administrador)
    db.commit()
    db.refresh(new_administrador)
    return new_administrador


@router.get('/obtener', response_model=List[Administrador])
def obtener_administradores(db: Session = Depends(get_db)):
    administradores = db.query(AdministradorModel).all()
    return administradores

@router.get('/{administrador_id}', response_model=Administrador)
def obtener_administrador_id(administrador_id: int, db: Session = Depends(get_db)):
    administrador = db.query(AdministradorModel).filter(AdministradorModel.id_administrador == administrador_id).first()
    if administrador is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    return administrador

@router.put('/{administrador_id}', response_model=Administrador)
def actualizar_administrador(administrador_id: int, administrador: AdministradorCreate, db: Session = Depends(get_db)):
    administrador_db = db.query(AdministradorModel).filter(AdministradorModel.id_administrador == administrador_id).first()
    if administrador_db is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    
    administrador_db.nombre = administrador.nombre
    administrador_db.apellido = administrador.apellido
    administrador_db.email = administrador.email
    
    # Verifica si la contraseña ha cambiado antes de hashearla nuevamente
    if administrador.password:
        administrador_db.password = pwd_context.hash(administrador.password)
    
    db.commit()
    db.refresh(administrador_db)
    return administrador_db


@router.delete('/{administrador_id}', response_model=dict)
def eliminar_administrador(administrador_id: int, db: Session = Depends(get_db)):
    administrador_db = db.query(AdministradorModel).filter(AdministradorModel.id_administrador == administrador_id).first()
    if administrador_db is None:
        raise HTTPException(status_code=404, detail="Administrador no encontrado")
    db.delete(administrador_db)
    db.commit()
    return {"mensaje": "Administrador eliminado satisfactoriamente"}
