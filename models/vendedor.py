from sqlalchemy import Column, Date, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Vendedor(Base):
    __tablename__ = "vendedores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)     
    email = Column(String, nullable=False, unique=True)
    senha_hash = Column(String, nullable=False)