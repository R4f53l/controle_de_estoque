from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException
from passlib.exc import UnknownHashError
from sqlalchemy.orm import Session
from database import get_db
from models.vendedor import Vendedor
from main import bcrypt_context
from schema.vendedor_schema import Vendedor_Schema
from core.security import verificar_token
from main import SECRET_KEY, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES
router = APIRouter(prefix="/auth", tags=["auth"])

def create_acess_token(id_usuario: int, duracao_token = timedelta(minutes = ACESS_TOKEN_EXPIRE_MINUTES)):    
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    payload = {"sub": str(id_usuario), "iat": datetime.now(timezone.utc), "type": "access", "exp": data_expiracao}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token    

def autenticar_usuario(email: str, senha_hash: str, db: Session):
    vendedor = db.query(Vendedor).filter(Vendedor.email == email).first()
    if not vendedor:
        return None

    if email != vendedor.email or not bcrypt_context.verify(senha_hash, vendedor.senha_hash):
        return None
    
    return vendedor

@router.get("/verificar_token")
def verificar_token(usuario = Depends(verificar_token)):
    return {"message" : "token valido"}

@router.post("/criar_conta")
def criar_conta(vendedor: Vendedor_Schema, db: Session = Depends(get_db)):
    vendedor_existente = db.query(Vendedor).filter(Vendedor.email == vendedor.email).first()
    number_of_vendedores = db.query(Vendedor).count()
    if number_of_vendedores > 5:
        raise HTTPException(status_code=400, detail="Limite de vendedores atingido")
    if vendedor_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")   
    senha_codificada = bcrypt_context.hash(vendedor.senha_hash)
    novo_vendedor = Vendedor(
        nome=vendedor.nome,
        email=vendedor.email,
        senha_hash=senha_codificada
    )
    db.add(novo_vendedor)
    db.commit()
    db.refresh(novo_vendedor)
    return {"message": "Conta criada com sucesso", "vendedor_id": novo_vendedor.id}

@router.post("/login")
def login(dados_forms: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    vendedor = autenticar_usuario(dados_forms.username, dados_forms.password, db)
    if not vendedor:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")    
    token = create_acess_token(vendedor.id)
    return {"access_token": token, "token_type": "bearer"}
