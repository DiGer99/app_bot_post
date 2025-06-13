import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

ADMIN_LOGIN=os.getenv("ADMIN_LOGIN")
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")