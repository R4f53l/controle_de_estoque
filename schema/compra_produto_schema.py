from pydantic import BaseModel

class CompraProduto_Schema(BaseModel):
    compra_id: int
    produto_id: int
    quantidade: int
    valor_unitario: float | None = None    
    tamanho: str | None = None
    genero: str | None = None

    class Config:
        from_attributes = True
