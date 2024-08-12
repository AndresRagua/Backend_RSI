import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Setting:
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Setting()

class SettingHost:
    FRONTEND_URL: str = os.getenv("FRONTEND_URL")

settingsHost = SettingHost()