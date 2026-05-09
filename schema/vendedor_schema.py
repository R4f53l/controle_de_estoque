from pydantic import BaseModel

class Vendedor_Schema(BaseModel):
    nome: str
    email: str
    senha_hash: str
    class Config:
        from_attributes = True