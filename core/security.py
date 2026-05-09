from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from database import get_db
from main import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

from models.vendedor import Vendedor
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verificar_token(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    print("TOKEN: ", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(payload.get("sub"))
        if id_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(Vendedor).filter(Vendedor.id == id_usuario).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return id_usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")