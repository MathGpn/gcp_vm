"""
Configuration avancée de la base de données (optionnel)
Ce fichier peut être utilisé pour une configuration plus complexe
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/appdb")

# Création de l'engine avec des options avancées
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Vérification des connexions
    pool_recycle=3600,   # Recyclage des connexions après 1h
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Metadata pour les migrations futures
metadata = MetaData()

def get_database():
    """Générateur de session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Créer toutes les tables"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Supprimer toutes les tables (utiliser avec précaution!)"""
    Base.metadata.drop_all(bind=engine)