from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "braulio"
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "paquexpress"
    JWT_SECRET: str = "CAMBIA_POR_SECRETO_FUERTE"
    JWT_ALGORITHM: str = "HS256"
    UPLOAD_DIR: str = "./uploads"

    model_config = {"env_file": ".env"}

settings = Settings()