from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class CompraProduto(Base):
    __tablename__ = "compra_produto"
    id = Column(Integer, primary_key=True, index=True)
    compra_id = Column(Integer, ForeignKey("compras.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Float, nullable=True)
    tamanho = Column(String, nullable=True)
    genero = Column(String, nullable=True)

    compra = relationship("Compra", back_populates="produtos")
