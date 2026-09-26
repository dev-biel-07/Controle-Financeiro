"""
Testes de integração dos principais fluxos: cadastro, login, categorias e gastos.

Rode com:
    pytest -v

Usa um banco SQLite separado (test.db) para não misturar com os dados reais.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test.db"):
        os.remove("test.db")


client = TestClient(app)


def get_auth_headers():
    """Cadastra um usuário, faz login e retorna os headers com o token."""
    client.post("/auth/register", json={"email": "teste@example.com", "password": "senha123"})
    response = client.post(
        "/auth/login", data={"username": "teste@example.com", "password": "senha123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_user():
    response = client.post("/auth/register", json={"email": "novo@example.com", "password": "123456"})
    assert response.status_code == 201
    assert response.json()["email"] == "novo@example.com"


def test_register_duplicate_email_fails():
    client.post("/auth/register", json={"email": "dup@example.com", "password": "123456"})
    response = client.post("/auth/register", json={"email": "dup@example.com", "password": "123456"})
    assert response.status_code == 400


def test_login_success():
    client.post("/auth/register", json={"email": "login@example.com", "password": "senha123"})
    response = client.post(
        "/auth/login", data={"username": "login@example.com", "password": "senha123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password_fails():
    client.post("/auth/register", json={"email": "wrong@example.com", "password": "senha123"})
    response = client.post(
        "/auth/login", data={"username": "wrong@example.com", "password": "errada"}
    )
    assert response.status_code == 401


def test_create_expense_requires_auth():
    response = client.post("/expenses/", json={"description": "Mercado", "amount": 150.0})
    assert response.status_code == 401


def test_create_and_list_expense():
    headers = get_auth_headers()
    response = client.post(
        "/expenses/",
        json={"description": "Mercado", "amount": 150.5},
        headers=headers,
    )
    assert response.status_code == 201
    assert response.json()["description"] == "Mercado"

    response = client.get("/expenses/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_create_category_and_link_expense():
    headers = get_auth_headers()
    cat_response = client.post("/categories/", json={"name": "Transporte"}, headers=headers)
    assert cat_response.status_code == 201
    category_id = cat_response.json()["id"]

    exp_response = client.post(
        "/expenses/",
        json={"description": "Uber", "amount": 25.0, "category_id": category_id},
        headers=headers,
    )
    assert exp_response.status_code == 201
    assert exp_response.json()["category_id"] == category_id


def test_delete_expense():
    headers = get_auth_headers()
    create_response = client.post(
        "/expenses/", json={"description": "Cinema", "amount": 40.0}, headers=headers
    )
    expense_id = create_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}", headers=headers)
    assert delete_response.status_code == 204
