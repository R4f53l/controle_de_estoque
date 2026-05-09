from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import verificar_token
from database import get_db
from models.venda import Venda
from models.venda_item import VendaItem
from schema.venda_schema import VendaComItens_Schema, Venda_Schema
router = APIRouter(prefix="/vendas", tags=["vendas"], dependencies=[Depends(verificar_token)])

@router.post("/adicionar_venda")
def adicionar_venda(venda: Venda_Schema, db: Session = Depends(get_db)):
    nova_venda = Venda(
        datadevenda=venda.datadevenda,
        valor=venda.valor,
        venda_direta=venda.venda_direta
    )
    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)
    return {"message": "Venda adicionada com sucesso", "venda_id": nova_venda.id}

@router.post("/adicionar_venda_com_itens")
def adicionar_venda_com_itens(venda: VendaComItens_Schema, db: Session = Depends(get_db)):
    if not venda.itens:
        raise HTTPException(status_code=400, detail="Adicione pelo menos um item na venda")

    valor_total = sum(
        item.quantidade * (item.valor_unitario or 0)
        for item in venda.itens
    )

    nova_venda = Venda(
        datadevenda=venda.datadevenda,
        valor=valor_total,
        venda_direta=venda.venda_direta
    )
    db.add(nova_venda)
    db.flush()

    itens = [
        VendaItem(
            venda_id=nova_venda.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            valor_unitario=item.valor_unitario
        )
        for item in venda.itens
    ]
    db.add_all(itens)
    db.commit()
    db.refresh(nova_venda)

    return {
        "message": "Venda adicionada com sucesso",
        "venda_id": nova_venda.id,
        "valor": nova_venda.valor,
        "itens": itens
    }

@router.get("/listar_vendas")
def listar_vendas(db: Session = Depends(get_db)):
    vendas = db.query(Venda).all()
    return vendas

@router.put("/atualizar_venda/{venda_id}")
def atualizar_venda(venda_id: int, venda: Venda_Schema, db: Session = Depends(get_db)):
    venda_existente = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda_existente:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    venda_existente.datadevenda = venda.datadevenda
    venda_existente.valor = venda.valor
    venda_existente.venda_direta = venda.venda_direta
    db.commit()
    db.refresh(venda_existente)
    return {"message": "Venda atualizada com sucesso", "venda_id": venda_existente.id}

@router.delete("/excluir_venda/{venda_id}")
def excluir_venda(venda_id: int, db: Session = Depends(get_db)):
    venda_existente = db.query(Venda).filter(Venda.id == venda_id).first()
    if not venda_existente:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    db.delete(venda_existente)
    db.commit()
    return {"message": "Venda excluída com sucesso"}
