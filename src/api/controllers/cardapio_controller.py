from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.cardapio_repository import CardapioRepository
from src.application.services.cardapio_service import CardapioService
from src.api.schemas.cardapio_schema import CardapioCreate, CardapioResponse
from src.api.dependencies.role_dependency import require_role
from src.domain.entities.usuario import PerfilUsuario

router = APIRouter(prefix="/cardapios", tags=["Cardápios"])


def get_cardapio_service():
    return CardapioService(CardapioRepository())


@router.post("/", response_model=CardapioResponse)
def criar_cardapio(
    cardapio: CardapioCreate,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE)),
    service: CardapioService = Depends(get_cardapio_service)
):
    return service.criar_cardapio(db, cardapio)


@router.get("/", response_model=List[CardapioResponse])
def listar_cardapios(
    db: Session = Depends(get_db),
    service: CardapioService = Depends(get_cardapio_service)
):
    return service.listar_cardapios(db)


@router.get("/ativos", response_model=List[CardapioResponse])
def listar_cardapios_ativos(
    db: Session = Depends(get_db),
    service: CardapioService = Depends(get_cardapio_service)
):
    return service.listar_cardapios_ativos(db)


@router.get("/{cardapio_id}", response_model=CardapioResponse)
def buscar_cardapio(
    cardapio_id: int,
    db: Session = Depends(get_db),
    service: CardapioService = Depends(get_cardapio_service)
):
    return service.buscar_cardapio(db, cardapio_id)