from src.application.services.pedido_service import PedidoService

from src.infrastructure.repositories.pedido_repository import PedidoRepository
from src.infrastructure.repositories.item_pedido_repository import ItemPedidoRepository
from src.infrastructure.repositories.produto_ingrediente_repository import ProdutoIngredienteRepository
from src.infrastructure.repositories.cardapio_repository import CardapioRepository
from src.infrastructure.repositories.cardapio_produto_repository import CardapioProdutoRepository
from src.infrastructure.repositories.historico_pedido_repository import HistoricoPedidoRepository

from src.application.services.estoque_service import EstoqueService
from src.application.services.fidelidade_service import FidelidadeService


def get_pedido_service():
    return PedidoService(
        PedidoRepository(),
        ItemPedidoRepository(),
        ProdutoIngredienteRepository(),
        EstoqueService(),
        FidelidadeService(),
        CardapioRepository(),
        CardapioProdutoRepository(),
        HistoricoPedidoRepository()  
    )