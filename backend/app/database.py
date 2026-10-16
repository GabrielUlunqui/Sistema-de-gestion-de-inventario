from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DB_PATH = Path(__file__).resolve().parent.parent / "inventario.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_columns():
    """Agrega columnas nuevas a bases ya existentes (migración liviana)."""
    with engine.connect() as conn:
        cols = {row[1] for row in conn.execute(text("PRAGMA table_info(items)"))}
        if "brand" not in cols:
            conn.execute(text("ALTER TABLE items ADD COLUMN brand VARCHAR(80)"))
            conn.commit()


SEED_ITEMS = [
    {"name": "Cámara domo IP 4MP", "sku": "CAM-001", "category": "Cámaras", "brand": "Hikvision", "quantity": 15, "price": 89.99, "min_stock": 5},
    {"name": "Cámara bullet 1080p", "sku": "CAM-002", "category": "Cámaras", "brand": "Hikvision", "quantity": 6, "price": 65.50, "min_stock": 8},
    {"name": "DVR 8 canales", "sku": "DVR-001", "category": "DVR", "brand": "Hikvision", "quantity": 10, "price": 189.99, "min_stock": 3},
    {"name": "DVR 16 canales", "sku": "DVR-002", "category": "DVR", "brand": "Dahua", "quantity": 4, "price": 299.00, "min_stock": 3},
    {"name": "Disco duro 1TB Purple", "sku": "ALM-001", "category": "Almacenamiento", "brand": "Western Digital", "quantity": 12, "price": 59.99, "min_stock": 4},
    {"name": "Disco duro 4TB Purple", "sku": "ALM-002", "category": "Almacenamiento", "brand": "Western Digital", "quantity": 0, "price": 129.99, "min_stock": 2},
    {"name": "Sensor de movimiento PIR", "sku": "SEN-001", "category": "Sensores", "brand": "DSC", "quantity": 25, "price": 24.99, "min_stock": 10},
    {"name": "Sensor magnético de puerta", "sku": "SEN-002", "category": "Sensores", "brand": "Paradox", "quantity": 8, "price": 12.50, "min_stock": 10},
    {"name": "Sensor de humo", "sku": "SEN-003", "category": "Sensores", "brand": "Hikvision", "quantity": 14, "price": 32.00, "min_stock": 5},
    {"name": "Bobina cable UTP Cat6 305m", "sku": "CAB-001", "category": "Cables", "brand": None, "quantity": 9, "price": 95.00, "min_stock": 3},
    {"name": "Cable siamés coaxil (metro)", "sku": "CAB-002", "category": "Cables", "brand": None, "quantity": 500, "price": 0.45, "min_stock": 100},
    {"name": "Fuente 12V 5A", "sku": "FUE-001", "category": "Fuentes", "brand": None, "quantity": 18, "price": 15.99, "min_stock": 6},
    {"name": "Fuente switching 12V 10A", "sku": "FUE-002", "category": "Fuentes", "brand": None, "quantity": 0, "price": 28.00, "min_stock": 4},
    {"name": "Conector BNC macho", "sku": "CON-001", "category": "Conectores", "brand": None, "quantity": 150, "price": 0.80, "min_stock": 50},
    {"name": "Jack DC hembra", "sku": "CON-002", "category": "Conectores", "brand": None, "quantity": 3, "price": 0.50, "min_stock": 20},
]


def seed_if_empty():
    from . import models

    with Session(engine) as session:
        if session.query(models.Item).count() == 0:
            session.add_all([models.Item(**data) for data in SEED_ITEMS])
            session.commit()
