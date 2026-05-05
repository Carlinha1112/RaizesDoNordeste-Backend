from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from src.infrastructure.database.database import get_db
from src.api.dependencies.auth_dependency import get_current_user

from src.application.services.relatorio_service import RelatorioService


# Repositories
from src.infrastructure.repositories.movimento_repository import MovimentoRepository
from src.infrastructure.repositories.historico_pedido_repository import HistoricoPedidoRepository
from src.infrastructure.repositories.fidelidade_repository import FidelidadeRepository
from src.infrastructure.repositories.historico_fidelidade_repository import HistoricoFidelidadeRepository

router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"]
)



def get_service():
    return RelatorioService(
        movimento_repository=MovimentoRepository(),
        historico_pedido_repository=HistoricoPedidoRepository(),
        fidelidade_repository=FidelidadeRepository(),
        historico_fidelidade_repository=HistoricoFidelidadeRepository()
    )



@router.get("/estoque")
def relatorio_estoque(
    unidade_id: int | None = None,
    data_inicio: datetime | None = None,
    data_fim: datetime | None = None,
    tipo: str | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    service = get_service()

    return service.relatorio_estoque(
        db=db,
        usuario=usuario,
        unidade_id=unidade_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
        tipo=tipo
    )



@router.get("/pedidos")
def relatorio_pedidos(
    pedido_id: int | None = None,
    data_inicio: datetime | None = None,
    data_fim: datetime | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    service = get_service()

    return service.relatorio_pedidos(
        db=db,
        usuario=usuario,
        pedido_id=pedido_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )


@router.get("/fidelidade")
def relatorio_fidelidade(
    usuario_id: int | None = None,
    data_inicio: datetime | None = None,
    data_fim: datetime | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user)
):
    service = get_service()

    return service.relatorio_fidelidade(
        db=db,
        usuario=usuario,
        usuario_id=usuario_id,
        data_inicio=data_inicio,
        data_fim=data_fim
    )

@router.get("/fidelidade/{usuario_id}")
def relatorio_fidelidade_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_logado=Depends(get_current_user)
):
    service = get_service()

    return service.relatorio_fidelidade_usuario(
        db=db,
        usuario_logado=usuario_logado,
        usuario_id=usuario_id
    )

