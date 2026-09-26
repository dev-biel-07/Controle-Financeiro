"""
Ponto de entrada da aplicação.

Rode com:
    uvicorn app.main:app --reload

Depois acesse http://localhost:8000/docs para ver a documentação
interativa (Swagger UI) gerada automaticamente pelo FastAPI.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import auth, categories, expenses

# Cria as tabelas no banco caso ainda não existam
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Controle Financeiro API",
    description="API para gerenciar gastos pessoais, categorias e relatórios.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(expenses.router)

# Serve o frontend (HTML/CSS/JS) a partir de /app, na mesma origem da API.
# Isso evita ter que configurar CORS: tudo roda na mesma porta.
app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/")
def root():
    return {"message": "Controle Financeiro API no ar. Acesse /docs para a documentação ou /app para a interface."}
