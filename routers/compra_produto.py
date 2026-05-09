from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import verificar_token
from database import get_db
from models.compra_produto import CompraProduto
from routers.auth_router import autenticar_usuario
from schema.compra_produto_schema import CompraProduto_Schema
from models.compra import Compra

router = APIRouter(prefix="/compra_produto", tags=["compra_produto"], dependencies=[Depends(verificar_token)])
@router.post("/")
def adicionar_compra_produto(compra_produto: CompraProduto_Schema, db: Session = Depends(get_db)):
    nova_compra_produto = CompraProduto(
        compra_id=compra_produto.compra_id,
        produto_id=compra_produto.produto_id,
        quantidade=compra_produto.quantidade,
        valor_unitario=compra_produto.valor_unitario
    )
    db.add(nova_compra_produto)
    db.commit()
    db.refresh(nova_compra_produto)
    return {"message": "Produto adicionado à compra com sucesso", "compra_produto": nova_compra_produto}

@router.get("/listar_produtos_em_estoque")
def listar_produtos_em_estoque(db: Session = Depends(get_db)):
    produtos = (
        db.query(CompraProduto)
        .join(Compra, Compra.id == CompraProduto.compra_id)
        .filter(Compra.dataderecebimento.isnot(None))
        .all()
    )
    return {"produtos_em_estoque": produtos}


@router.get("/listar_todos")
def obter_compra_produto(db: Session = Depends(get_db)):
    compra_produto = db.query(CompraProduto).all()    
    return {"compra_produto": compra_produto}

@router.put("/atualizar/{compra_produto_id}")
def atualizar_compra_produto(compra_produto_id: int, compra_produto: CompraProduto_Schema, db: Session = Depends(get_db)):  
    compra_produto_db = db.query(CompraProduto).filter(CompraProduto.id == compra_produto_id).first()
    if not compra_produto_db:
        raise HTTPException(status_code=404, detail="Produto da compra não encontrado")
    
    compra_produto_db.compra_id = compra_produto.compra_id
    compra_produto_db.produto_id = compra_produto.produto_id
    compra_produto_db.quantidade = compra_produto.quantidade
    compra_produto_db.valor_unitario = compra_produto.valor_unitario
    
    db.commit()
    db.refresh(compra_produto_db)
    return {"message": "Produto da compra atualizado com sucesso", "compra_produto": compra_produto_db}