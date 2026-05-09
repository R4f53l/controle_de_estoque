from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import verificar_token
from database import get_db
from models.compra import Compra
from models.compra_produto import CompraProduto
from schema.compra_schema import CompraComItens_Schema, Compra_Schema
router = APIRouter(prefix="/compras", tags=["compras"], dependencies=[Depends(verificar_token)])

@router.post("/adicionar_compra")
def adicionar_compra(compra: Compra_Schema, db: Session = Depends(get_db)):
    nova_compra = Compra(
        datadecompra=compra.datadecompra,
        dataderecebimento=compra.dataderecebimento,
        valor=compra.valor,
        para_estoque=compra.para_estoque,
        valor_imposto = compra.valor_imposto
    )
    db.add(nova_compra)
    db.commit()
    db.refresh(nova_compra)
    return {"message": "Compra adicionada com sucesso", "compra_id": nova_compra.id}




@router.post("/adicionar_compra_com_itens")
def adicionar_compra_com_itens(compra: CompraComItens_Schema, db: Session = Depends(get_db)):
    if not compra.itens:
        raise HTTPException(status_code=400, detail="Adicione pelo menos um item na compra")

    valor_total = sum(
        item.quantidade * (item.valor_unitario or 0)
        for item in compra.itens
    )

    nova_compra = Compra(
        datadecompra=compra.datadecompra,
        dataderecebimento=compra.dataderecebimento,
        valor=valor_total,
        para_estoque=compra.para_estoque,
        valor_imposto = compra.valor_imposto
    )
    db.add(nova_compra)
    db.flush()

    itens = [
        CompraProduto(
            compra_id=nova_compra.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            valor_unitario=item.valor_unitario
        )
        for item in compra.itens
    ]
    db.add_all(itens)
    db.commit()
    db.refresh(nova_compra)

    return {
        "message": "Compra adicionada com sucesso",
        "compra_id": nova_compra.id,
        "valor": nova_compra.valor,
        "itens": itens
    }

@router.get("/listar_compras")
def listar_compras(db: Session = Depends(get_db)):
    compras = db.query(Compra).all()
    return compras

@router.put("/atualizar_compra/{compra_id}")
def atualizar_compra(compra_id: int, compra: Compra_Schema, db: Session = Depends(get_db)):
    compra_existente = db.query(Compra).filter(Compra.id == compra_id).first()
    if not compra_existente:
        raise HTTPException(status_code=404, detail="Compra não encontrada")
    compra_existente.datadecompra = compra.datadecompra
    compra_existente.dataderecebimento = compra.dataderecebimento
    compra_existente.valor = compra.valor
    compra_existente.para_estoque = compra.para_estoque
    compra_existente.valor_imposto = compra.valor_imposto
    db.commit()
    db.refresh(compra_existente)
    return {"message": "Compra atualizada com sucesso", "compra_id": compra_existente.id}

@router.delete("/excluir_compra/{compra_id}")
def excluir_compra(compra_id: int, db: Session = Depends(get_db)):
    compra_existente = db.query(Compra).filter(Compra.id == compra_id).first()
    if not compra_existente:
        raise HTTPException(status_code=404, detail="Compra não encontrada")
    db.delete(compra_existente)
    db.commit()
    return {"message": "Compra excluída com sucesso"}
