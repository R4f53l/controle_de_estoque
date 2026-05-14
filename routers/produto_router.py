from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import verificar_token
from database import get_db
from models.produto import Produto
from schema.produto_schema import Produto_Schema
from models.compra import Compra
from models.compra_produto import CompraProduto
router = APIRouter(prefix="/produtos", tags=["produtos"], dependencies=[Depends(verificar_token)])

@router.post("/adicionar_produto")
def adicionar_produto(produto: Produto_Schema, db: Session = Depends(get_db)):
    produto_existente = db.query(Produto).filter(Produto.nome == produto.nome).first()
    if produto_existente:
        raise HTTPException(status_code=400, detail="Produto já existe")
    novo_produto = Produto(
        nome=produto.nome,
        descricao=produto.descricao
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return {"message": "Produto adicionado com sucesso", "produto_id": novo_produto.id}

@router.get("/listar_produtos")
def listar_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).all()
    return produtos





@router.put("/atualizar_produto/{produto_id}")
def atualizar_produto(produto_id: int, produto: Produto_Schema, db: Session = Depends(get_db)):
    produto_existente = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    produto_existente.nome = produto.nome
    produto_existente.descricao = produto.descricao
    db.commit()
    db.refresh(produto_existente)
    return {"message": "Produto atualizado com sucesso", "produto_id": produto_existente.id}

@router.delete("/excluir_produto/{produto_id}")
def excluir_produto(produto_id: int, db: Session = Depends(get_db)):    
    produto_existente = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto_existente:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto_existente)
    db.commit()
    return {"message": "Produto excluído com sucesso"}
