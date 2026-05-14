from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from core.security import verificar_token
from database import get_db
from models.compra_produto import CompraProduto
from models.venda import Venda
from models.venda_item import VendaItem
from schema.venda_item_schema import VendaComItem_Schema, VendaItem_Schema

router = APIRouter(prefix="/venda_item", tags=["venda_item"], dependencies=[Depends(verificar_token)])

@router.post("/")
def adicionar_venda_item(venda_item: VendaItem_Schema, db: Session = Depends(get_db)):
    nova_venda_item = VendaItem(
        venda_id=venda_item.venda_id,
        produto_id=venda_item.produto_id,
        quantidade=venda_item.quantidade,
        valor_unitario=venda_item.valor_unitario,
        tamanho=venda_item.tamanho,
        genero=venda_item.genero
    )
    db.add(nova_venda_item)
    db.commit()
    db.refresh(nova_venda_item)
    return {"message": "Produto adicionado à venda com sucesso", "venda_item": nova_venda_item}


@router.get("/listar_todos")
def obter_venda_item(db: Session = Depends(get_db)):    
    venda_item = db.query(VendaItem).all()    
    return {"venda_item": venda_item}

@router.put("/atualizar/{venda_item_id}")
def atualizar_venda_item(venda_item_id: int, venda_item: VendaItem_Schema, db: Session = Depends(get_db)):  
    venda_item_db = db.query(VendaItem).filter(VendaItem.id == venda_item_id).first()
    if not venda_item_db:
        raise HTTPException(status_code=404, detail="Produto da venda não encontrado")
    
    venda_item_db.venda_id = venda_item.venda_id
    venda_item_db.produto_id = venda_item.produto_id
    venda_item_db.quantidade = venda_item.quantidade
    venda_item_db.valor_unitario = venda_item.valor_unitario
    venda_item_db.tamanho = venda_item.tamanho
    venda_item_db.genero = venda_item.genero
    
    db.commit()
    db.refresh(venda_item_db)
    return {"message": "Produto da venda atualizado com sucesso", "venda_item": venda_item_db}

def deletar_venda_item(venda_item_id: int, db: Session = Depends(get_db)):  
    venda_item_db = db.query(VendaItem).filter(VendaItem.id == venda_item_id).first()
    if not venda_item_db:
        raise HTTPException(status_code=404, detail="Produto da venda não encontrado")
    
    db.delete(venda_item_db)
    db.commit()
    return {"message": "Produto da venda deletado com sucesso"}
