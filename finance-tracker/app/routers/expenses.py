from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get(
    "/",
    response_model=List[schemas.ExpenseOut],
    summary="Listar gastos",
    description="Retorna a lista de gastos do usuário autenticado, do mais recente para o mais antigo.",
)
def list_expenses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_expenses(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=schemas.ExpenseOut,
    status_code=201,
    summary="Criar gasto",
    description="Registra um novo gasto para o usuário autenticado.",
)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_expense(db, expense, owner_id=current_user.id)


@router.delete(
    "/{expense_id}",
    status_code=204,
    summary="Remover gasto",
    description="Remove um gasto pelo ID, desde que pertença ao usuário autenticado.",
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    deleted = crud.delete_expense(db, expense_id, owner_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Gasto não encontrado")


@router.get(
    "/report/by-category",
    summary="Relatório por categoria",
    description="Retorna o total gasto, somado por categoria, para o usuário autenticado.",
)
def report_by_category(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_total_by_category(db, owner_id=current_user.id)
