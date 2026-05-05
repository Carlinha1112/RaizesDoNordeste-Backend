from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db

from src.application.services.pedido_service import PedidoService
from src.application.services.fidelidade_service import FidelidadeService
from src.application.services.estoque_service import EstoqueService
from src.application.services.auditoria_service import AuditoriaService

from src.infrastructure.repositories.pedido_repository import PedidoRepository
from src.infrastructure.repositories.item_pedido_repository import ItemPedidoRepository
from src.infrastructure.repositories.estoque_repository import EstoqueRepository
from src.infrastructure.repositories.produto_ingrediente_repository import ProdutoIngredienteRepository
from src.infrastructure.repositories.cardapio_repository import CardapioRepository
from src.infrastructure.repositories.cardapio_produto_repository import CardapioProdutoRepository
from src.infrastructure.repositories.fidelidade_repository import FidelidadeRepository
from src.infrastructure.repositories.historico_fidelidade_repository import HistoricoFidelidadeRepository
from src.infrastructure.repositories.historico_pedido_repository import HistoricoPedidoRepository
from src.infrastructure.repositories.auditoria_repository import AuditoriaRepository

from src.api.schemas.pedido_schema import PedidoCreate, PedidoResponse, PedidoConfirmacao

from src.api.dependencies.auth_dependency import get_current_user
from src.api.dependencies.role_dependency import require_role
from src.api.dependencies.auditoria_dependency import get_auditoria_service

from src.domain.entities.usuario import PerfilUsuario
from src.domain.entities.pedido import CanalPedido

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


def get_fidelidade_service():
    return FidelidadeService(
        FidelidadeRepository(),
        HistoricoFidelidadeRepository()
    )

def get_pedido_service(
    auditoria_service: AuditoriaService = Depends(get_auditoria_service)
):
    return PedidoService(
        PedidoRepository(),
        ItemPedidoRepository(),
        ProdutoIngredienteRepository(),
        EstoqueService(auditoria_service),
        get_fidelidade_service(),
        CardapioRepository(),
        CardapioProdutoRepository(),
        HistoricoPedidoRepository(),
        auditoria_service
    )


@router.post("/", response_model=PedidoResponse)
def criar_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role(
            PerfilUsuario.CLIENTE,
            PerfilUsuario.ATENDENTE
        )
    ),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.criar_pedido(
        db=db,
        pedido_data=pedido,
        itens=pedido.itens,
        usuario=usuario
    )

@router.get("/{pedido_id}/resumo")
def resumo_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.resumo_pedido_com_fidelidade(
        db,
        pedido_id,
        usuario
    )

@router.post("/{pedido_id}/confirmar", response_model=PedidoResponse)
def confirmar_pedido(
    pedido_id: int,
    dados: PedidoConfirmacao,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role(
            PerfilUsuario.CLIENTE,
            PerfilUsuario.ATENDENTE
        )
    ),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.confirmar_pedido(
        db=db,
        pedido_id=pedido_id,
        usuario=usuario,
        usar_fidelidade=dados.usar_fidelidade,
        pontos=dados.pontos_usados
    )

@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.buscar_pedido(
        db,
        pedido_id,
        usuario
    )


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(
    canal: CanalPedido | None = None,
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.listar_pedidos(
        db,
        usuario,
        canal
    )


@router.delete("/{pedido_id}", response_model=PedidoResponse)
def cancelar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role(
            PerfilUsuario.CLIENTE,
            PerfilUsuario.ATENDENTE,
            PerfilUsuario.GERENTE
        )
    ),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.cancelar_pedido(
        db,
        pedido_id,
        usuario
    )


@router.patch("/{pedido_id}/iniciar-preparo", response_model=PedidoResponse)
def iniciar_preparo(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role(
            PerfilUsuario.ATENDENTE,
            PerfilUsuario.GERENTE
        )
    ),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.iniciar_preparo(
        db,
        pedido_id
    )


@router.patch("/{pedido_id}/pronto", response_model=PedidoResponse)
def marcar_pronto(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role(
            PerfilUsuario.ATENDENTE,
            PerfilUsuario.GERENTE
        )
    ),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.marcar_pronto(
        db,
        pedido_id
    )


@router.patch("/{pedido_id}/finalizar", response_model=PedidoResponse)
def finalizar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(
        require_role(
            PerfilUsuario.ATENDENTE,
            PerfilUsuario.GERENTE
        )
    ),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.finalizar_pedido(
        db,
        pedido_id,
        usuario
    )