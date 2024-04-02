from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.db import Base

class User(Base):
    __tablename__ = 'user'

    cpf = Column(String(length=11), primary_key=True)
    username = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False)
    password = Column(String(length=100), nullable=False)
    role = Column(String(length=100), nullable=False)

