"""
Funções CRUD: isolam a lógica de acesso ao banco, separada dos endpoints.

Isso facilita testar a lógica de negócio sem precisar subir a API inteira,
e deixa os routers mais limpos e focados em HTTP (status codes, validação).
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import hash_password


# ---------- User ----------
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------- Category ----------
def get_categories(db: Session, owner_id: int) -> List[models.Category]:
    return db.query(models.Category).filter(models.Category.owner_id == owner_id).all()


def create_category(db: Session, category: schemas.CategoryCreate, owner_id: int) -> models.Category:
    db_category = models.Category(name=category.name, owner_id=owner_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# ---------- Expense ----------
def get_expenses(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.Expense]:
    return (
        db.query(models.Expense)
        .filter(models.Expense.owner_id == owner_id)
        .order_by(models.Expense.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_expense(db: Session, expense: schemas.ExpenseCreate, owner_id: int) -> models.Expense:
    db_expense = models.Expense(**expense.model_dump(), owner_id=owner_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def delete_expense(db: Session, expense_id: int, owner_id: int) -> bool:
    expense = (
        db.query(models.Expense)
        .filter(models.Expense.id == expense_id, models.Expense.owner_id == owner_id)
        .first()
    )
    if not expense:
        return False
    db.delete(expense)
    db.commit()
    return True


def get_total_by_category(db: Session, owner_id: int) -> dict:
    """Retorna o total gasto por categoria — útil pra um endpoint de relatório."""
    expenses = get_expenses(db, owner_id, limit=10_000)
    totals: dict = {}
    for e in expenses:
        key = e.category.name if e.category else "Sem categoria"
        totals[key] = totals.get(key, 0) + e.amount
    return totals
