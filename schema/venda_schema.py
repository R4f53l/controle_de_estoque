from pydantic import BaseModel
from datetime import date

class Venda_Schema(BaseModel):
    datadevenda: date
    valor: float | None = None
    venda_direta: bool = False
    class Config:
        from_attributes = True


class VendaItemEntrada_Schema(BaseModel):
    produto_id: int
    quantidade: int
    valor_unitario: float | None = None

    class Config:
        from_attributes = True


class VendaComItens_Schema(BaseModel):
    datadevenda: date
    venda_direta: bool = False
    itens: list[VendaItemEntrada_Schema]

    class Config:
        from_attributes = True
