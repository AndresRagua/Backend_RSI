import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Setting:
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Setting()

class SettingHost:
    FRONTEND_URL = "http://localhost:3000"

settingsHost = SettingHost()