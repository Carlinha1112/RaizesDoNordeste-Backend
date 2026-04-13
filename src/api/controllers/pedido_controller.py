from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.application.services.pedido_service import PedidoService
from src.infrastructure.repositories.pedido_repository import PedidoRepository
from src.infrastructure.repositories.item_pedido_repository import ItemPedidoRepository
from src.infrastructure.repositories.estoque_repository import EstoqueRepository
from src.infrastructure.repositories.produto_ingrediente_repository import ProdutoIngredienteRepository
from src.infrastructure.repositories.cardapio_repository import CardapioRepository
from src.infrastructure.repositories.cardapio_produto_repository import CardapioProdutoRepository
from src.application.services.fidelidade_service import FidelidadeService
from src.infrastructure.repositories.fidelidade_repository import FidelidadeRepository
from src.infrastructure.repositories.historico_fidelidade_repository import HistoricoFidelidadeRepository
from src.api.schemas.pedido_schema import PedidoCreate, PedidoResponse
from src.api.dependencies.auth_dependency import get_current_user
from src.api.dependencies.role_dependency import require_role
from src.domain.entities.usuario import PerfilUsuario

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def get_fidelidade_service():
    return FidelidadeService(
        FidelidadeRepository(),
        HistoricoFidelidadeRepository()
    )


def get_pedido_service():
    return PedidoService(
        PedidoRepository(),
        ItemPedidoRepository(),
        ProdutoIngredienteRepository(),
        EstoqueRepository(),
        get_fidelidade_service(),
        CardapioRepository(),
        CardapioProdutoRepository()
    )


@router.post("/", response_model=PedidoResponse)
def criar_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(
        PerfilUsuario.CLIENTE,
        PerfilUsuario.ATENDENTE
    )),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.criar_pedido(
        db=db,
        pedido_data=pedido,
        itens=pedido.itens,
        pontos_utilizados=pedido.pontos_utilizados,
        usuario=usuario
    )



@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.buscar_pedido(db, pedido_id, usuario)


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.listar_pedidos(db, usuario)


@router.delete("/{pedido_id}")
def cancelar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(
        PerfilUsuario.CLIENTE,
        PerfilUsuario.ATENDENTE,
        PerfilUsuario.GERENTE
    )),
    service: PedidoService = Depends(get_pedido_service)
):
    return service.cancelar_pedido(db, pedido_id, usuario)