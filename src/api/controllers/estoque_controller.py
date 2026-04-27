from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db

from src.api.dependencies.auth_dependency import (
    get_current_user
)

from src.api.schemas.estoque_schema import (
    EstoqueCreate,
    EstoqueMovimento,
    EstoqueAjuste,
    EstoqueResponse
)

from src.application.services.estoque_service import EstoqueService

router = APIRouter(
    prefix="/estoque",
    tags=["Estoque"]
)

service = EstoqueService()


@router.post("/", response_model=EstoqueResponse)
def criar(
    dados: EstoqueCreate,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return service.criar_ou_repor(
        db,
        dados,
        usuario
    )


@router.get("/", response_model=list[EstoqueResponse])
def listar(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return service.listar(db)


@router.get(
    "/unidade/{unidade_id}",
    response_model=list[EstoqueResponse]
)
def listar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return service.listar_por_unidade(
        db,
        unidade_id
    )


@router.patch("/{id}/entrada", response_model=EstoqueResponse)
def entrada(
    id: int,
    dados: EstoqueMovimento,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return service.entrada(
        db,
        id,
        dados.quantidade,
        usuario
    )


@router.patch("/{id}/saida", response_model=EstoqueResponse)
def saida(
    id: int,
    dados: EstoqueMovimento,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return service.saida(
        db,
        id,
        dados.quantidade,
        usuario
    )


@router.patch("/{id}", response_model=EstoqueResponse)
def ajustar(
    id: int,
    dados: EstoqueAjuste,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    return service.ajustar(
        db,
        id,
        dados.quantidade,
        usuario
    )


@router.delete("/{id}")
def excluir(
    id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    service.excluir(
        db,
        id,
        usuario
    )

    return {"message": "Removido com sucesso"}