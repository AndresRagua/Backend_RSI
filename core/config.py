import os
from dotenv import load_dotenv
from pathlib import Path

# Determina el entorno de ejecución (local o producción)
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

# Cargar el archivo .env adecuado según el entorno
if ENVIRONMENT == 'production':
    load_dotenv(dotenv_path=Path('.') / '.env.production')
else:
    load_dotenv(dotenv_path=Path('.') / '.env.local')

class Setting:
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Setting()

class SettingHost:
    FRONTEND_URL: str = os.getenv("FRONTEND_URL")

settingsHost = SettingHost()
