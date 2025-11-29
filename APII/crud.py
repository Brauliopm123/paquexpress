from sqlalchemy.orm import Session
import models
from datetime import datetime

def get_agente_by_username(db: Session, username: str):
    return db.query(models.Agente).filter(models.Agente.username == username).first()

def get_assigned_entregas(db: Session, agente_id: int):
    return db.query(models.Entrega).filter(models.Entrega.agente_id == agente_id).all()

def mark_entrega_delivered(db: Session, entrega_id: int, foto_url: str, lat: float, lon: float):
    entrega = db.query(models.Entrega).filter(models.Entrega.id == entrega_id).first()
    if not entrega:
        return None
    entrega.foto_url = foto_url
    entrega.lat = lat
    entrega.lon = lon
    entrega.estado = models.EstadoEntrega.entregado
    entrega.entregado_en = datetime.utcnow()
    db.commit()
    db.refresh(entrega)
    return entrega