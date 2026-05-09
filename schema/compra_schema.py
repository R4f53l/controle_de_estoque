from pydantic import BaseModel 
from datetime import date

class Compra_Schema(BaseModel):
    datadecompra: date
    dataderecebimento: date | None = None
    valor: float | None = None
    para_estoque: bool = True
    valor_imposto: float | None = None
    class Config:
        from_attributes = True


class CompraItemEntrada_Schema(BaseModel):
    produto_id: int
    quantidade: int
    valor_unitario: float | None = None

    class Config:
        from_attributes = True


class CompraComItens_Schema(BaseModel):
    datadecompra: date
    dataderecebimento: date | None = None
    valor_imposto: float | None = None
    para_estoque: bool = True
    itens: list[CompraItemEntrada_Schema]

    class Config:
        from_attributes = True
