from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.utils.parameter_provider import ParameterProvider

DATABASE_URL = (
    f"postgresql+psycopg://{ParameterProvider.get_required('db.user')}:"
    f"{ParameterProvider.get_required('db.password')}@"
    f"{ParameterProvider.get_required('db.host')}:"
    f"{ParameterProvider.get_required('db.port')}/"
    f"{ParameterProvider.get_required('db.name')}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()