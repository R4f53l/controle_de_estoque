# Sasaqueles Bagres - Sistema de Gestão

Este é um sistema de gestão de estoque, compras e vendas desenvolvido com **FastAPI** no backend e uma interface web simples no frontend.

## 🚀 Tecnologias Utilizadas

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Banco de Dados:** [SQLAlchemy](https://www.sqlalchemy.org/) com [Alembic](https://alembic.sqlalchemy.org/) para migrações.
- **Autenticação:** JWT (JSON Web Tokens) com `passlib` e `python-jose`.
- **Frontend:** HTML5, CSS3 e JavaScript (Vanilla).
- **Ambiente:** Python 3.12+

## 🛠️ Estrutura do Projeto

- `/core`: Configurações de segurança e segurança.
- `/models`: Definições das tabelas do banco de dados.
- `/routers`: Rotas da API divididas por contexto (produtos, compras, vendas, auth).
- `/schema`: Modelos Pydantic para validação de dados.
- `/frontend`: Arquivos estáticos da interface web.
- `/alembic`: Scripts de migração do banco de dados.

## 📦 Instalação

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd sasaquelesbagres
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No Linux/macOS:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🗄️ Banco de Dados

Para aplicar as migrações e criar as tabelas no banco de dados, execute:

```bash
alembic upgrade head
```

## 🏃 Executando a Aplicação

Para iniciar o servidor backend:

```bash
uvicorn main:app --reload
```

Acesse a aplicação em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

- **Dashboard:** Página inicial (redireciona se não logado).
- **Login:** [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)
- **Documentação API (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 📄 Licença

Este projeto está sob a licença MIT.
