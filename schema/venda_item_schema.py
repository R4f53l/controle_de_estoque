from datetime import date

from pydantic import BaseModel

class VendaItem_Schema(BaseModel):
    venda_id: int
    produto_id: int
    quantidade: int
    valor_unitario: float | None = None
    tamanho: str | None = None
    genero: str | None = None

    class Config:
        from_attributes = True

class VendaItemCreate_Schema(BaseModel):    
    produto_id: int
    quantidade: int
    valor_unitario: float | None = None
    tamanho: str | None = None
    genero: str | None = None

    class Config:
        from_attributes = True

class VendaComItem_Schema(BaseModel):
    datadevenda: date
    venda_id: int
    itens: list[VendaItemCreate_Schema]
    class Config:
        from_attributes = True
