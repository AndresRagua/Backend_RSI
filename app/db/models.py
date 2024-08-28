from app.db.database import Base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

class Administrador(Base):
    __tablename__ = 'administrador'
    id_administrador = Column(Integer, primary_key=True)
    nombre = Column(String(250), nullable=False)
    apellido = Column(String(250), nullable=False)
    email = Column(String(500), nullable=False, unique=True)
    password = Column(String(500), nullable=False)

class Radio(Base):
    __tablename__ = 'radio'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    url_audio = Column(String(500), nullable=False)
    url_logo = Column(String(500), nullable=False)
    url_primer_fondo = Column(String(500), nullable=False)
    url_segundo_fondo = Column(String(500), nullable=True)
    url_tercer_fondo = Column(String(500), nullable=True)
    
    programas = relationship('Programa', back_populates='radio')
    artistas = relationship('ArtistaInvitado', back_populates='radio')
    publicidades = relationship('Publicidad', back_populates='radio')
    servicios_sociales = relationship('ServicioSocial', back_populates='radio')
    usuarios = relationship('Usuario', back_populates='radio')
    televisiones = relationship('Television', back_populates='radio')


class Programa(Base):
    __tablename__ = 'programa'
    id_programa = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    nombre_conductor = Column(String(500), nullable=False)
    certificado_locucion = Column(String(500), nullable=False)
    url_banner = Column(String(500), nullable=False)
    fk_radio = Column(Integer, ForeignKey('radio.id'))
    radio = relationship('Radio', back_populates='programas')
    programaciones = relationship('Programacion', back_populates='programa')

class Programacion(Base):
    __tablename__ = 'programacion'
    id_programacion = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    url_audio = Column(String(500), nullable=False)
    fecha_transmision = Column(Date, nullable=False)
    fk_programa = Column(Integer, ForeignKey('programa.id_programa'))
    programa = relationship('Programa', back_populates='programaciones')

class ArtistaInvitado(Base):
    __tablename__ = 'artistas_(invitados)'
    id_artista = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    informacion = Column(String(500), nullable=False)
    url_image = Column(String(500), nullable=False)
    fk_radio = Column(Integer, ForeignKey('radio.id'))
    radio = relationship('Radio', back_populates='artistas')

class Publicidad(Base):
    __tablename__ = 'publicidad'
    id_publicidad = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    informacion = Column(String(500), nullable=False)
    url_image = Column(String(500), nullable=False)
    url_twitter = Column(String(500))
    url_instagram = Column(String(500))
    url_facebook = Column(String(500))
    fk_radio = Column(Integer, ForeignKey('radio.id'))
    radio = relationship('Radio', back_populates='publicidades')

class ServicioSocial(Base):
    __tablename__ = 'servicio_social'
    id_servicio = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    informacion = Column(String(500), nullable=False)
    url_image = Column(String(500), nullable=False)
    url_pagina = Column(String(500), nullable=False)
    tipo = Column(String(500), nullable=False)
    nombre_audios = Column(String(500), nullable=True)
    fk_radio = Column(Integer, ForeignKey('radio.id'))
    radio = relationship('Radio', back_populates='servicios_sociales')
    audios_servicio = relationship('AudioServicio', back_populates='servicio_social')

class AudioServicio(Base):
    __tablename__ = 'audio_servicio'
    id_audio = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    fecha = Column(Date, nullable=False)
    url_audio = Column(String(500), nullable=False)
    fk_servicio = Column(Integer, ForeignKey('servicio_social.id_servicio'))
    servicio_social = relationship('ServicioSocial', back_populates='audios_servicio')

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_usuario = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    correo = Column(String(500), nullable=False)
    telefono = Column(String(500), nullable=False)
    password = Column(String(500), nullable=False)
    fk_radio = Column(Integer, ForeignKey('radio.id'))
    radio = relationship('Radio', back_populates='usuarios')
    hilos_musicales = relationship('HiloMusical', back_populates='usuario')

class HiloMusical(Base):
    __tablename__ = 'hilo_musical'
    id_hilo = Column(Integer, primary_key=True)
    nombre = Column(String(500), nullable=False)
    url_musical = Column(String(500), nullable=False)
    url_image = Column(String(500), nullable=False)
    fk_usuario = Column(Integer, ForeignKey('usuarios.id_usuario'))
    usuario = relationship('Usuario', back_populates='hilos_musicales')

class Television(Base):
    __tablename__ = 'television'
    id_television = Column(Integer, primary_key=True)
    url_stream = Column(String(500), nullable=False)
    segundo_url_stream = Column(String(500), nullable=True)
    url_image_fondo = Column(String(500), nullable=False)
    segundo_url_image_fondo = Column(String(500), nullable=True)
    url_twitter = Column(String(500), nullable=False)
    url_instagram = Column(String(500), nullable=False)
    url_facebook = Column(String(500), nullable=False)
    fk_radio = Column(Integer, ForeignKey('radio.id'), nullable=False)
    
    radio = relationship('Radio', back_populates='televisiones')
