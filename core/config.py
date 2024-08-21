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
    DATABASE_URL: str = os.getenv("DATABASE_URL")
# Instancia de configuración de la base de datos
settings = Setting()

# Clase para la configuración de la URL del frontend
class SettingHost:
    FRONTEND_URL: str = os.getenv("FRONTEND_URL")
    print(f"FRONTEND_URL: {FRONTEND_URL}")  # Depuración

# Instancia de configuración del host
settingsHost = SettingHost()
