from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class EstadoEntrega(enum.Enum):
    pendiente = "pendiente"
    entregado = "entregado"
    fallido = "fallido"

class Agente(Base):
    __tablename__ = "agentes"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(150))

class Paquete(Base):
    __tablename__ = "paquetes"
    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String(100), unique=True, nullable=False)
    direccion = Column(String(255), nullable=False)
    ciudad = Column(String(100))
    cp = Column(String(20))
    instruccion = Column(String(255))

class Entrega(Base):
    __tablename__ = "entregas"
    id = Column(Integer, primary_key=True, index=True)
    paquete_id = Column(Integer, ForeignKey("paquetes.id"), nullable=False)
    agente_id = Column(Integer, ForeignKey("agentes.id"), nullable=False)
    estado = Column(Enum(EstadoEntrega), default=EstadoEntrega.pendiente)
    foto_url = Column(String(255))
    lat = Column(DECIMAL(10,7))
    lon = Column(DECIMAL(10,7))
    entregado_en = Column(TIMESTAMP, nullable=True)
    asignado_en = Column(TIMESTAMP, server_default=func.now())