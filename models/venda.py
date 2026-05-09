from sqlalchemy import Boolean, Column, Date, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Venda(Base):
    __tablename__ = "vendas"
    id = Column(Integer, primary_key=True, index=True)
    datadevenda = Column(Date, nullable=False)
    valor = Column(Float, nullable=True)
    venda_direta = Column(Boolean, default=False)

    itens = relationship("VendaItem", back_populates="venda", cascade="all, delete-orphan")
   