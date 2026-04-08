from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.pedido_repository import PedidoRepository
from src.application.services.cozinha_service import CozinhaService

from src.domain.entities.pedido import StatusPreparo
from src.api.schemas.pedido_schema import PedidoResponse


router = APIRouter(prefix="/cozinha", tags=["Cozinha"])


def get_service():
    return CozinhaService(PedidoRepository())


@router.get("/aguardando", response_model=list[PedidoResponse])
def listar_aguardando(
    db: Session = Depends(get_db),
    service: CozinhaService = Depends(get_service)
):
    return service.listar_por_status_preparo(db, StatusPreparo.AGUARDANDO_PREPARO)


@router.get("/em-preparo", response_model=list[PedidoResponse])
def listar_em_preparo(
    db: Session = Depends(get_db),
    service: CozinhaService = Depends(get_service)
):
    return service.listar_por_status_preparo(db, StatusPreparo.EM_PREPARO)


@router.get("/prontos", response_model=list[PedidoResponse])
def listar_prontos(
    db: Session = Depends(get_db),
    service: CozinhaService = Depends(get_service)
):
    return service.listar_por_status_preparo(db, StatusPreparo.PRONTO)