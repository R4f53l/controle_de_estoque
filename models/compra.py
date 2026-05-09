from sqlalchemy import Boolean, Column, Date, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Compra(Base):
    __tablename__ = "compras"
    id = Column(Integer, primary_key=True, index=True)
    datadecompra = Column(Date, nullable=False)
    dataderecebimento = Column(Date, nullable=True) 
    valor = Column(Float, nullable=True)
    para_estoque = Column(Boolean, default=True)  
    valor_imposto = Column(Float, nullable=True)

    produtos = relationship("CompraProduto", back_populates="compra", cascade="all, delete-orphan")
    