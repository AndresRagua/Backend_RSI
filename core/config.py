import os
from dotenv import load_dotenv
from pathlib import Path

# Especifica la ruta absoluta
env_path = Path('C:/Users/andre/Desktop/RSI_FastAPI_ReactJS/backend/.env.local')

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print("Cargando variables desde .env.local")
else:
    print(".env.local no encontrado. Asumiendo entorno de producción.")

# Ahora determina si estás en desarrollo o producción
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')

if ENVIRONMENT == 'development':
    print("Entorno de desarrollo detectado")
else:
    print("Entorno de producción detectado")

# Clase para la configuración de la base de datos
class Setting:
    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")

    DATABASE_URL: str = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
    print(f"DATABASE_URL: {DATABASE_URL}")  # Depuración

# Instancia de configuración de la base de datos
settings = Setting()

# Clase para la configuración de la URL del frontend
class SettingHost:
    FRONTEND_URL: str = os.getenv("FRONTEND_URL")
    print(f"FRONTEND_URL: {FRONTEND_URL}")  # Depuración

# Instancia de configuración del host
settingsHost = SettingHost()
