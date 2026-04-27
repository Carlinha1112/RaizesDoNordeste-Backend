from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.pedido_repository import PedidoRepository

from src.application.services.cozinha_service import CozinhaService

from src.domain.entities.pedido import StatusPreparo
from src.domain.entities.usuario import PerfilUsuario

from src.api.schemas.pedido_schema import PedidoResponse

from src.api.dependencies.role_dependency import require_role


router = APIRouter(prefix="/cozinha", tags=["Cozinha"])


def get_cozinha_service():
    return CozinhaService(PedidoRepository())


@router.get("/aguardando", response_model=List[PedidoResponse])
def listar_aguardando(
    db: Session = Depends(get_db),
    usuario=Depends(require_role(PerfilUsuario.ATENDENTE, PerfilUsuario.GERENTE)),
    service: CozinhaService = Depends(get_cozinha_service)
):
    return service.listar_por_status_preparo(
        db,
        StatusPreparo.AGUARDANDO_PREPARO,
        usuario
    )


@router.get("/em-preparo", response_model=List[PedidoResponse])
def listar_em_preparo(
    db: Session = Depends(get_db),
    usuario=Depends(require_role(PerfilUsuario.ATENDENTE, PerfilUsuario.GERENTE)),
    service: CozinhaService = Depends(get_cozinha_service)
):
    return service.listar_por_status_preparo(
        db,
        StatusPreparo.EM_PREPARO,
        usuario
    )


@router.get("/prontos", response_model=List[PedidoResponse])
def listar_prontos(
    db: Session = Depends(get_db),
    usuario=Depends(require_role(PerfilUsuario.ATENDENTE, PerfilUsuario.GERENTE)),
    service: CozinhaService = Depends(get_cozinha_service)
):
    return service.listar_por_status_preparo(
        db,
        StatusPreparo.PRONTO,
        usuario
    )


@router.patch("/{pedido_id}/iniciar", response_model=PedidoResponse)
def iniciar_preparo(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_role(PerfilUsuario.ATENDENTE,PerfilUsuario.GERENTE)),
    service: CozinhaService = Depends(get_cozinha_service)
):
    return service.atualizar_status(
        db,
        pedido_id,
        StatusPreparo.EM_PREPARO,
        usuario
    )


@router.patch("/{pedido_id}/pronto", response_model=PedidoResponse)
def marcar_pronto(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_role(PerfilUsuario.ATENDENTE, PerfilUsuario.GERENTE)),    
    service: CozinhaService = Depends(get_cozinha_service)
):
    return service.atualizar_status(
        db,
        pedido_id,
        StatusPreparo.PRONTO,
        usuario
    )


@router.patch("/{pedido_id}/finalizar", response_model=PedidoResponse)
def finalizar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_role(PerfilUsuario.ATENDENTE, PerfilUsuario.GERENTE)),
    service: CozinhaService = Depends(get_cozinha_service)
):
    return service.atualizar_status(
        db,
        pedido_id,
        StatusPreparo.FINALIZADO,
        usuario
    )