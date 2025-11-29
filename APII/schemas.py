from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    username: str
    password: str

class PaqueteOut(BaseModel):
    id: int
    tracking_id: str
    direccion: str
    ciudad: Optional[str]
    cp: Optional[str]
    instruccion: Optional[str]

    model_config = {"from_attributes": True}

class EntregaOut(BaseModel):
    id: int
    paquete: PaqueteOut
    estado: str
    foto_url: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    entregado_en: Optional[datetime]

    model_config = {"from_attributes": True}