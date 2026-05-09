from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import verificar_token
from database import get_db
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
        valor_unitario=venda_item.valor_unitario
    )
    db.add(nova_venda_item)
    db.commit()
    db.refresh(nova_venda_item)
    return {"message": "Produto adicionado à venda com sucesso", "venda_item": nova_venda_item}

@router.post("/adicionar_com_itens")
def adicionar_venda_com_itens(venda_com_itens: VendaComItem_Schema, db: Session = Depends(get_db)):
    
    if not venda_com_itens.itens:
        raise HTTPException(status_code=400, detail="Adicione pelo menos um item na venda")

    valor_venda = sum(item.quantidade * (item.valor_unitario or 0) for item in venda_com_itens.itens)

    nova_venda = Venda(
        vendaid = venda_com_itens.venda_id,
        datadevenda = venda_com_itens.datadevenda,
        valor = valor_venda
    )

    db.add(nova_venda)
    db.flush()
    itens = [
        VendaItem(
            venda_id=venda_com_itens.venda_id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            valor_unitario=item.valor_unitario
        )
        for item in venda_com_itens.itens
    ]
    db.add_all(itens)
    db.commit()
    return {
        "message": "Itens adicionados à venda com sucesso",
        "venda_id": venda_com_itens.venda_id,
        "itens": itens
    }


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