# config.py
from pydantic_settings import BaseSettings   # ← NUEVA importación correcta

class Settings(BaseSettings):
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "braulio"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "paquexpress"
    JWT_SECRET: str = "CAMBIA_POR_SECRETO_FUERTE"
    JWT_ALGORITHM: str = "HS256"
    UPLOAD_DIR: str = "./uploads"

    model_config = {"env_file": ".env"}  # ← En v2 se usa model_config en vez de class Config

settings = Settings()