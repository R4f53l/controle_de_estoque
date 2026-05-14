from sqlalchemy import Column, Integer, String
from database import Base

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)     
    descricao = Column(String, nullable=True)
