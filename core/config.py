import os
from dotenv import load_dotenv
from pathlib import Path

# Determina si estás en desarrollo o producción
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')  # Por defecto es 'production'

if ENVIRONMENT == 'development':
    # Cargar variables de entorno desde el archivo .env.local en desarrollo
    env_path = Path('.env.local')
    load_dotenv(dotenv_path=env_path)
    print("Cargando variables desde .env.local")
else:
    print("Cargando variables desde el entorno de producción")

# Clase para la configuración de la base de datos
class Setting:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
# Instancia de configuración de la base de datos
settings = Setting()

# Clase para la configuración de la URL del frontend
class SettingHost:
    FRONTEND_URL: str = os.getenv("FRONTEND_URL")

# Instancia de configuración del host
settingsHost = SettingHost()

# Accede a las variables de entorno como atributos de tus instancias
print(settings.DATABASE_URL)
print(settingsHost.FRONTEND_URL)
