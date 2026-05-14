from pydantic import BaseModel

class Produto_Schema(BaseModel):
    nome: str
    descricao: str | None = None    

    class Config:
        from_attributes = True
