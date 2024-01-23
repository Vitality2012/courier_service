from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Environments
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

# URL of our database
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Enigne for SQLAlchemy work
engine = create_engine(DATABASE_URL)

# Session of our database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
	pass
