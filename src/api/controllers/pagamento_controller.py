from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.pagamento_repository import PagamentoRepository
from src.infrastructure.repositories.pedido_repository import PedidoRepository
from src.application.services.pagamento_service import PagamentoService
from src.application.services.fidelidade_service import FidelidadeService
from src.infrastructure.repositories.produto_ingrediente_repository import ProdutoIngredienteRepository
from src.infrastructure.repositories.estoque_repository import EstoqueRepository
from src.infrastructure.repositories.fidelidade_repository import FidelidadeRepository
from src.infrastructure.repositories.historico_fidelidade_repository import HistoricoFidelidadeRepository
from src.domain.entities.pagamento import Metodo
from src.api.dependencies.role_dependency import require_role
from src.domain.entities.usuario import PerfilUsuario

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


def get_service():
    return PagamentoService(
        PagamentoRepository(),
        PedidoRepository(),
        ProdutoIngredienteRepository(),
        EstoqueRepository(),
        FidelidadeService(
            FidelidadeRepository(),
            HistoricoFidelidadeRepository()
        )
    )


@router.post("/{pedido_id}")
def pagar_pedido(
    pedido_id: int,
    metodo: Metodo,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.CLIENTE, PerfilUsuario.ATENDENTE)),
    service: PagamentoService = Depends(get_service)
):
    return service.processar_pagamento(db, pedido_id, metodo, usuario)