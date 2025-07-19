from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/appdb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle de base de données SQLAlchemy
class ItemDB(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Créer les tables
Base.metadata.create_all(bind=engine)

# Dependency pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Mon API", description="API Backend pour l'application", version="1.0.0")

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic pour la validation des données
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    created_at: Optional[datetime] = None

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Base de données simulée en mémoire
items_db = [
    {"id": 1, "name": "Produit 1", "description": "Description du produit 1", "price": 10.99, "created_at": datetime.now()},
    {"id": 2, "name": "Produit 2", "description": "Description du produit 2", "price": 25.50, "created_at": datetime.now()},
]

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API Backend!", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/items", response_model=List[Item])
async def get_items(db: Session = Depends(get_db)):
    """Récupérer tous les items"""
    items = db.query(ItemDB).all()
    return items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Récupérer un item par son ID"""
    item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    return item

@app.post("/items", response_model=Item)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Créer un nouvel item"""
    db_item = ItemDB(
        name=item.name,
        description=item.description,
        price=item.price
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemCreate, db: Session = Depends(get_db)):
    """Mettre à jour un item"""
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    
    db_item.name = item_update.name
    db_item.description = item_update.description
    db_item.price = item_update.price
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Supprimer un item"""
    db_item = db.query(ItemDB).filter(ItemDB.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item non trouvé")
    
    deleted_item = {
        "id": db_item.id,
        "name": db_item.name,
        "description": db_item.description,
        "price": db_item.price,
        "created_at": db_item.created_at
    }
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item supprimé avec succès", "item": deleted_item}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)