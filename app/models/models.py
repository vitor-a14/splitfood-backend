from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..db.db import Base

association_table = Table(
    'group_users', 
    Base.metadata,   
    Column("user_cpf", ForeignKey("user.cpf")),
    Column("group_id", ForeignKey("group.id")),
)

class User(Base):
    __tablename__ = 'user'

    cpf = Column(String(length=11), primary_key=True)
    username = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=False)
    password = Column(String(length=100), nullable=False)
    role = Column(String(length=100), nullable=False)
    
class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100), nullable=False)
    description = Column(String(length=100), nullable=False)
    status = Column(String(length=100), nullable=False)
    creator_id = Column(String(length=11), ForeignKey("user.cpf"), nullable=False)
    participants = relationship("User", secondary=association_table)
    
class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100), nullable=False)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=False)
    owner_id = Column(String(length=11), ForeignKey("user.cpf"), nullable=False)
    owner = relationship("User")
    group = relationship("Group")
    value = Column(Integer, nullable=False)
