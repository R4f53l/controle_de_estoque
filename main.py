import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from passlib.context import CryptContext


load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import auth_router, produto_router, compras_router, compra_produto, venda_item, venda_router
app.include_router(auth_router.router)
app.include_router(produto_router.router)
app.include_router(compras_router.router)
app.include_router(venda_router.router)
app.include_router(compra_produto.router)
app.include_router(venda_item.router)

app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


@app.get("/")
def abrir_dashboard():
    return FileResponse(FRONTEND_DIR / "dashboard.html")


@app.get("/login")
def abrir_login():
    return FileResponse(FRONTEND_DIR / "login.html")
