from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Usuario as UsuarioModel
from app.schemas import UsuarioCreate, Usuario, UsuarioLogin
from passlib.context import CryptContext
from jose import jwt

router = APIRouter(
    prefix="/usuario",
    tags=["Usuarios"]
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
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user_db = db.query(UsuarioModel).filter(UsuarioModel.correo == usuario.correo).first()
    if not user_db or not verify_password(usuario.password, user_db.password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    access_token = create_access_token(data={"sub": user_db.correo})
    return {"token": access_token}

@router.post('/', response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo_usuario = UsuarioModel(
        nombre=usuario.nombre,
        correo=usuario.correo,
        telefono=usuario.telefono,
        password=pwd_context.hash(usuario.password),  # Hashear la contraseña antes de almacenarla
        fk_radio=usuario.fk_radio
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.get('/', response_model=List[Usuario])
def obtener_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioModel).all()
    return usuarios

@router.get('/{usuario_id}', response_model=Usuario)
def obtener_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id_usuario == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put('/{usuario_id}', response_model=Usuario)
def actualizar_usuario(usuario_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_db = db.query(UsuarioModel).filter(UsuarioModel.id_usuario == usuario_id).first()
    if usuario_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario_db.nombre = usuario.nombre
    usuario_db.correo = usuario.correo
    usuario_db.telefono = usuario.telefono
    usuario_db.password = pwd_context.hash(usuario.password)  # Hashear la contraseña antes de almacenarla
    usuario_db.fk_radio = usuario.fk_radio
    
    db.commit()
    db.refresh(usuario_db)
    return usuario_db

@router.delete('/{usuario_id}', response_model=dict)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_db = db.query(UsuarioModel).filter(UsuarioModel.id_usuario == usuario_id).first()
    if usuario_db is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario_db)
    db.commit()
    return {"mensaje": "Usuario eliminado satisfactoriamente"}
