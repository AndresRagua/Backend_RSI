from typing import List, Optional
from pydantic import BaseModel
from datetime import date

# Schema para la creación de un Administrador
class AdministradorCreate(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str

    class Config:
        from_attributes = True

# Schema para la respuesta de los endpoints que devuelven datos de Administrador
class Administrador(BaseModel):
    id_administrador: int
    nombre: str
    apellido: str
    email: str

    class Config:
        from_attributes = True

class AdministradorLogin(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

# Schema para la creación de una Radio
class RadioCreate(BaseModel):
    nombre: str
    url_logo: str
    url_audio: str
    url_primer_fondo: str
    url_segundo_fondo: str
    url_tercer_fondo: str

    class Config:
        from_attributes = True

# Schema para la respuesta de los endpoints que devuelven datos de Radio
class Radio(BaseModel):
    id: int
    nombre: str
    url_logo: str
    url_audio: str
    url_primer_fondo: str
    url_segundo_fondo: str
    url_tercer_fondo: str

    class Config:
        from_attributes = True

class ProgramacionCreate(BaseModel):
    nombre: str
    url_audio: str
    fecha_transmision: date
    fk_programa: int

    class Config:
        from_attributes = True

class Programacion(BaseModel):
    id_programacion: int
    nombre: str
    url_audio: str
    fecha_transmision: date
    fk_programa: int

    class Config:
        from_attributes = True

class ProgramaCreate(BaseModel):
    nombre: str
    nombre_conductor: str
    certificado_locucion: str
    url_banner: str
    fk_radio: int

    class Config:
        from_attributes = True

class Programa(BaseModel):
    id_programa: int
    nombre: str
    nombre_conductor: str
    certificado_locucion: str
    url_banner: str
    programaciones: List[Programacion] = []  # Se agrega la relación con Programaciones

    class Config:
        from_attributes = True

class ArtistaCreate(BaseModel):
    nombre: str
    informacion: str
    url_image: str
    fk_radio: int

    class Config:
        from_attributes = True

class Artista(BaseModel):
    id_artista: int
    nombre: str
    informacion: str
    url_image: str
    fk_radio: int

    class Config:
        from_attributes = True

class PublicidadCreate(BaseModel):
    nombre: str
    informacion: str
    url_image: str
    url_twitter: str = None
    url_instagram: str = None
    url_facebook: str = None
    fk_radio: int

    class Config:
        from_attributes = True

class Publicidad(BaseModel):
    id_publicidad: int
    nombre: str
    informacion: str
    url_image: str
    url_twitter: str
    url_instagram: str
    url_facebook: str
    fk_radio: int

    class Config:
        from_attributes = True

class UsuarioCreate(BaseModel):
    nombre: str
    correo: str
    telefono: str
    password: str
    fk_radio: int

    class Config:
        from_attributes = True

class Usuario(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    telefono: str
    fk_radio: int

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    correo: str
    password: str

    class Config:
        from_attributes = True

class HiloMusicalCreate(BaseModel):
    nombre: str
    url_musical: str
    url_image: str
    fk_usuario: int

    class Config:
        from_attributes = True

class HiloMusical(BaseModel):
    id_hilo: int
    nombre: str
    url_musical: str
    url_image: str
    fk_usuario: int

    class Config:
        from_attributes = True

# Schema para la creación de un Audio Servicio
class AudioServicioCreate(BaseModel):
    nombre: str
    fecha: date
    url_audio: str
    fk_servicio: int

    class Config:
        from_attributes = True

# Schema para la respuesta de los endpoints que devuelven datos de Audio Servicio
class AudioServicio(BaseModel):
    id_audio: int
    nombre: str
    fecha: date
    url_audio: str
    fk_servicio: int

    class Config:
        from_attributes = True

# Schema para la creación de un Servicio Social
class ServicioSocialCreate(BaseModel):
    nombre: str
    informacion: str
    url_image: str
    url_pagina: str
    tipo: str
    nombre_audios: str
    fk_radio: int

    class Config:
        from_attributes = True

# Schema para la respuesta de los endpoints que devuelven datos de Servicio Social
class ServicioSocial(BaseModel):
    id_servicio: int
    nombre: str
    informacion: str
    url_image: str
    url_pagina: str
    tipo: str
    nombre_audios: str
    fk_radio: int
    audios_servicio: List[AudioServicio] = []

    class Config:
        from_attributes = True

class TelevisionCreate(BaseModel):
    url_stream: str
    segundo_url_stream: Optional[str] = None
    url_image_fondo: str
    segundo_url_image_fondo: Optional[str] = None
    url_twitter: str
    url_instagram: str
    url_facebook: str
    fk_radio: int

class Television(BaseModel):
    id_television: int
    url_stream: str
    segundo_url_stream: Optional[str]
    url_image_fondo: str
    segundo_url_image_fondo: Optional[str]
    url_twitter: str
    url_instagram: str
    url_facebook: str
    fk_radio: int

    class Config:
        from_attributes = True