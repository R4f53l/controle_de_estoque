from pydantic import BaseModel

class CompraProduto_Schema(BaseModel):
    compra_id: int
    produto_id: int
    quantidade: int
    valor_unitario: float | None = None    
    class Config:
        from_attributes = True