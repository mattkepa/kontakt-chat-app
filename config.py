import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """
    Set Flask configuration variables from .env file
    """
    TESTING = os.getenv('TESTING')
    DEBUG = os.getenv('DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SERVER = os.getenv('SERVER')
    SESSION_PERMANENT = False
    SESSION_TYPE = 'filesystem'