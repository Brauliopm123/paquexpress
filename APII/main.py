# main.py → 100% COMPATIBLE CON TU BASE DE DATOS ACTUAL
import os
import shutil
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String, Enum, ForeignKey, DECIMAL, TIMESTAMP, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import List

# ===================== CONFIGURACIÓN =====================
MYSQL_USER = "root"
MYSQL_PASSWORD = "braulio"
MYSQL_HOST = "127.0.0.1"
MYSQL_DB = "paquexpress"
JWT_SECRET = "supersecreto123cambiaesto"
JWT_ALGORITHM = "HS256"
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===================== BASE DE DATOS =====================
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ===================== MODELOS (EXACTO A TU BD) =====================
class Agente(Base):
    __tablename__ = "agentes"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

class Paquete(Base):
    __tablename__ = "paquetes"
    id = Column(Integer, primary_key=True)
    paquete_id = Column(String(100), unique=True, nullable=False)
    direccion = Column(String(255), nullable=False)
    destinatario = Column(String(150))
    estado = Column(Enum('pendiente','en_ruta','entregado','fallido'), default='pendiente')
    asignado_a = Column(Integer, ForeignKey("agentes.id"))

class Entrega(Base):
    __tablename__ = "entregas"
    id = Column(Integer, primary_key=True)
    paquete_id = Column(Integer, ForeignKey("paquetes.id"), nullable=False)
    agente_id = Column(Integer, ForeignKey("agentes.id"), nullable=False)
    url_foto_evidencia = Column(String(500))
    latitud = Column(DECIMAL(10,7))
    longitud = Column(DECIMAL(10,7))
    fecha_entrega = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

# ===================== SEGURIDAD =====================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        return None

# ===================== SCHEMAS =====================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    email: str        # ← Usamos email porque tu tabla tiene email
    password: str

class PaqueteOut(BaseModel):
    id: int
    paquete_id: str
    direccion: str
    destinatario: Optional[str] = None

    model_config = {"from_attributes": True}

class EntregaOut(BaseModel):
    id: int
    paquete: PaqueteOut
    url_foto_evidencia: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    fecha_entrega: Optional[datetime] = None

    model_config = {"from_attributes": True}

# ===================== APP =====================
app = FastAPI(title="Paquexpress - Funciona con tu BD")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_agente(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    email = payload.get("sub")
    agente = db.query(Agente).filter(Agente.email == email).first()
    if not agente:
        raise HTTPException(status_code=401, detail="Agente no encontrado")
    return agente

# ===================== RUTAS =====================
@app.post("/auth/login", response_model=Token)
def login(data: LoginIn, db: Session = Depends(get_db)):
    agente = db.query(Agente).filter(Agente.email == data.email).first()
    if not agente or not verify_password(data.password, agente.password_hash):
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    token = create_access_token({"sub": agente.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/deliveries/assigned", response_model=List[EntregaOut])
def get_assigned(db: Session = Depends(get_db), agente=Depends(get_current_agente)):
    entregas = db.query(Entrega).filter(Entrega.agente_id == agente.id).all()
    result = []
    for e in entregas:
        paquete = db.query(Paquete).filter(Paquete.id == e.paquete_id).first()
        result.append({
            "id": e.id,
            "paquete": paquete,
            "url_foto_evidencia": e.url_foto_evidencia,
            "latitud": float(e.latitud) if e.latitud else None,
            "longitud": float(e.longitud) if e.longitud else None,
            "fecha_entrega": e.fecha_entrega
        })
    return result

@app.post("/deliveries/{entrega_id}/deliver")
async def deliver(
    entrega_id: int,
    lat: float = Form(...),
    lon: float = Form(...),
    file: UploadFile = File(...),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    agente = get_current_agente(token, db)
    entrega = db.query(Entrega).filter(Entrega.id == entrega_id, Entrega.agente_id == agente.id).first()
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")

    filename = f"entrega_{entrega_id}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    entrega.url_foto_evidencia = f"/uploads/{filename}"
    entrega.latitud = lat
    entrega.longitud = lon
    entrega.fecha_entrega = datetime.utcnow()
    db.commit()

    paquete = db.query(Paquete).filter(Paquete.id == entrega.paquete_id).first()
    return {
        "id": entrega.id,
        "paquete": paquete,
        "url_foto_evidencia": entrega.url_foto_evidencia,
        "latitud": float(lat),
        "longitud": float(lon),
        "fecha_entrega": entrega.fecha_entrega
    }

print("API lista → http://127.0.0.1:8000/docs")