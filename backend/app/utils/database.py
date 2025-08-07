from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Para PostgreSQL (recomendado)
DATABASE_URL = "postgresql://usuario:contraseña@localhost:5432/nexustock"

# Para SQLite (pruebas locales)
# DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
