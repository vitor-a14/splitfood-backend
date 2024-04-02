from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ..settings import settings


Engine = create_engine(settings.db_url, echo=True)

Session = sessionmaker(bind=Engine)

Base = declarative_base()

metadata = Base.metadata


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
