# Controle Financeiro API

API REST para gerenciar gastos pessoais, com autenticação de usuários, categorias e relatórios — construída com FastAPI e SQLAlchemy.

Projeto pessoal feito para praticar (e mostrar) desenvolvimento backend com Python: modelagem de dados, autenticação JWT, testes automatizados e boas práticas de organização de código.

## Funcionalidades

- Cadastro e login de usuários com senha criptografada (bcrypt)
- Autenticação via **JWT** (JSON Web Token)
- CRUD de categorias de gastos
- CRUD de gastos (criar, listar, deletar)
- Relatório de total gasto por categoria
- Cada usuário só enxerga os próprios dados
- Documentação interativa automática (Swagger UI)
- Testes automatizados cobrindo os principais fluxos

## Stack

- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **SQLite** — banco de dados (fácil trocar por PostgreSQL em produção)
- **python-jose** — geração e validação de tokens JWT
- **passlib (bcrypt)** — hash de senhas
- **pytest** — testes automatizados

## Estrutura do projeto

```
finance-tracker/
├── app/
│   ├── main.py            # ponto de entrada da aplicação
│   ├── database.py        # configuração da conexão com o banco
│   ├── models.py          # modelos SQLAlchemy (tabelas)
│   ├── schemas.py         # schemas Pydantic (validação de entrada/saída)
│   ├── auth.py            # hash de senha e JWT
│   ├── crud.py            # funções de acesso ao banco
│   └── routers/
│       ├── auth.py        # rotas de cadastro/login
│       ├── categories.py  # rotas de categorias
│       └── expenses.py    # rotas de gastos
├── tests/
│   └── test_main.py       # testes automatizados
└── requirements.txt
```

## Como rodar

```bash
# 1. Clone o repositório
git clone <seu-repositorio>
cd finance-tracker

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode a aplicação
uvicorn app.main:app --reload
```

Acesse **http://localhost:8000/docs** para ver a documentação interativa e testar os endpoints direto do navegador.

## Rodando os testes

```bash
pytest -v
```

## Principais endpoints

| Método | Rota                        | Descrição                          | Autenticado |
|--------|-----------------------------|-------------------------------------|:-----------:|
| POST   | `/auth/register`            | Cadastra um novo usuário            | Não |
| POST   | `/auth/login`                | Faz login e retorna o token JWT    | Não |
| GET    | `/categories/`               | Lista categorias do usuário        | Sim |
| POST   | `/categories/`                | Cria uma nova categoria           | Sim |
| GET    | `/expenses/`                  | Lista gastos do usuário           | Sim |
| POST   | `/expenses/`                   | Cria um novo gasto                | Sim |
| DELETE | `/expenses/{id}`               | Remove um gasto                   | Sim |
| GET    | `/expenses/report/by-category` | Total gasto por categoria         | Sim |

