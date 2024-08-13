from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.routers import admin, home, radio, programa, programacion, artista, publicidad, servicio, audio_servicio,usuario, hilo
from app.db.database import Base, engine
from core.config import settingsHost

def create_tables():
    Base.metadata.create_all(bind=engine)
create_tables()

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://134.122.118.217", "*", settingsHost.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(admin.router)
app.include_router(radio.router)
app.include_router(programa.router)
app.include_router(programacion.router)
app.include_router(artista.router)
app.include_router(publicidad.router)
app.include_router(servicio.router)
app.include_router(usuario.router)
app.include_router(hilo.router)
app.include_router(home.router)
app.include_router(audio_servicio.router)



## Ejecutar la aplicacion con "python main.py"
if __name__ == "__main__":
    uvicorn.run("main:app",port=8000,reload=True)