from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.cardapio_produto_repository import CardapioProdutoRepository
from src.application.services.cardapio_produto_service import CardapioProdutoService

from src.api.schemas.cardapio_produto_schema import (
    CardapioProdutoCreate,
    CardapioProdutoUpdate,
    CardapioProdutoResponse
)


router = APIRouter(prefix="/cardapios", tags=["Cardápio Produtos"])


def get_service():
    return CardapioProdutoService(CardapioProdutoRepository())


@router.post("/{cardapio_id}/produtos", response_model=CardapioProdutoResponse)
def adicionar_produto(
    cardapio_id: int,
    dados: CardapioProdutoCreate,
    db: Session = Depends(get_db)
):
    service = get_service()
    return service.adicionar_produto(db, cardapio_id, dados)


@router.get("/{cardapio_id}/produtos", response_model=list[CardapioProdutoResponse])
def listar_produtos(
    cardapio_id: int,
    db: Session = Depends(get_db)
):
    service = get_service()
    return service.listar_produtos(db, cardapio_id)


@router.patch("/{cardapio_id}/produtos/{produto_id}", response_model=CardapioProdutoResponse)
def atualizar_produto(
    cardapio_id: int,
    produto_id: int,
    dados: CardapioProdutoUpdate,
    db: Session = Depends(get_db)
):
    service = get_service()
    return service.atualizar_produto(db, cardapio_id, produto_id, dados)