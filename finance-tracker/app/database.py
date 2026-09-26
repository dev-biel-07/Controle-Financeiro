"""
Configuração da conexão com o banco de dados usando SQLAlchemy.

Por padrão usa SQLite (arquivo local, zero configuração), mas basta trocar
a variável DATABASE_URL para usar PostgreSQL em produção, por exemplo:
    postgresql://usuario:senha@localhost/finance_db
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./finance.db")

# connect_args só é necessário para SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency do FastAPI: abre uma sessão do banco e garante que ela feche depois."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
