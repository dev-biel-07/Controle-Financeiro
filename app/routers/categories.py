from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas, models
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get(
    "/",
    response_model=List[schemas.CategoryOut],
    summary="Listar categorias",
    description="Retorna todas as categorias criadas pelo usuário autenticado.",
)
def list_categories(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.get_categories(db, owner_id=current_user.id)


@router.post(
    "/",
    response_model=schemas.CategoryOut,
    status_code=201,
    summary="Criar categoria",
    description="Cria uma nova categoria de gastos para o usuário autenticado.",
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_category(db, category, owner_id=current_user.id)
