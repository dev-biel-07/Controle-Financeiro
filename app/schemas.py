"""
Schemas Pydantic: validam os dados que entram e saem da API.

Separar "schema de entrada" (Create) de "schema de saída" é uma boa prática:
nunca devolvemos a senha do usuário, por exemplo.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- User ----------
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    created_at: datetime


# ---------- Auth ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Category ----------
class CategoryCreate(BaseModel):
    name: str


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


# ---------- Expense ----------
class ExpenseCreate(BaseModel):
    description: str
    amount: float
    category_id: Optional[int] = None


class ExpenseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    description: str
    amount: float
    date: datetime
    category_id: Optional[int] = None
