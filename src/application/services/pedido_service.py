import logging
from sqlalchemy.orm import Session
from datetime import date
from fastapi import HTTPException

from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.pedido import Pedido
from src.domain.entities.usuario import PerfilUsuario

from src.api.schemas.pedido_schema import CanalPedido
from src.domain.enums.pedido_status import StatusPedido, StatusPreparo

logger = logging.getLogger(__name__)


class PedidoService:

    def __init__(
        self,
        pedido_repository,
        item_pedido_repository,
        produto_ingrediente_repository,
        estoque_repository,
        fidelidade_service,
        cardapio_repository,
        cardapio_produto_repository
    ):
        self.pedido_repository = pedido_repository
        self.item_repository = item_pedido_repository
        self.produto_ingrediente_repository = produto_ingrediente_repository
        self.estoque_repository = estoque_repository
        self.fidelidade_service = fidelidade_service
        self.cardapio_repository = cardapio_repository
        self.cardapio_produto_repository = cardapio_produto_repository

    # =====================================================
    # CRIAR PEDIDO
    # =====================================================
    def criar_pedido(self, db: Session, pedido_data, itens, pontos_utilizados, usuario):

        if not itens:
            raise HTTPException(400, "Pedido não pode ser vazio")

        cardapio = self.cardapio_repository.buscar_cardapio_ativo(
            db,
            pedido_data.id_unidade,
            date.today()
        )

        if not cardapio:
            raise HTTPException(404, "Cardápio não encontrado")

        # ==========================================
        # CALCULA VALOR TOTAL
        # ==========================================
        valor_total = 0

        for item in itens:
            cardapio_produto = self.cardapio_produto_repository.buscar(
                db,
                cardapio.id,
                item.produto_id
            )

            if not cardapio_produto:
                raise HTTPException(404, f"Produto {item.produto_id} não encontrado")

            if not cardapio_produto.ativo_no_cardapio:
                raise HTTPException(400, f"Produto {item.produto_id} indisponível")

            valor_total += float(cardapio_produto.preco_venda) * item.quantidade

        # ==========================================
        # DEFINIÇÃO DO CLIENTE DO PEDIDO
        # ==========================================
        id_cliente = None

        if pedido_data.canal_pedido == CanalPedido.BALCAO:

            # atendente pode informar cliente
            if hasattr(pedido_data, "cliente_id") and pedido_data.cliente_id:
                id_cliente = pedido_data.cliente_id
            else:
                # sem cliente cadastrado → usa atendente como fallback
                id_cliente = usuario.id

        else:
            # outros canais: sempre usuário logado
            id_cliente = usuario.id

        # segurança final
        if id_cliente is None:
            raise HTTPException(
                400,
                "Pedido precisa estar vinculado a um cliente"
            )

        # ==========================================
        # CRIA PEDIDO
        # ==========================================
        pedido = Pedido(
            id_unidade=pedido_data.id_unidade,
            id_usuario=id_cliente,
            canal_pedido=pedido_data.canal_pedido,
            status_pedido=StatusPedido.AGUARDANDO_PAGAMENTO,
            status_preparo=StatusPreparo.AGUARDANDO_PREPARO,
            valor_total=valor_total
        )

        try:
            pedido = self.pedido_repository.criar(db, pedido)

            # itens do pedido
            for item in itens:
                item_pedido = ItemPedido(
                    id_pedido=pedido.id,
                    id_produto=item.produto_id,
                    quantidade=item.quantidade
                )
                self.item_repository.criar(db, item_pedido)

            db.commit()
            db.refresh(pedido)

            return pedido

        except Exception as e:
            db.rollback()
            logger.exception(e)
            raise HTTPException(500, "Erro interno ao criar pedido")

    # =====================================================
    # BUSCAR PEDIDO
    # =====================================================
    def buscar_pedido(self, db: Session, pedido_id: int, usuario):

        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        if usuario.perfil == PerfilUsuario.CLIENTE:
            if pedido.id_usuario != usuario.id:
                raise HTTPException(403, "Acesso negado")

        if usuario.perfil == PerfilUsuario.ATENDENTE:
            if pedido.id_unidade != usuario.id_unidade:
                raise HTTPException(403, "Acesso negado")

        return pedido

    # =====================================================
    # LISTAR PEDIDOS
    # =====================================================
    def listar_pedidos(self, db: Session, usuario, canal: CanalPedido | None = None):

        if usuario.perfil == PerfilUsuario.CLIENTE:
            return self.pedido_repository.listar_por_usuario(db, usuario.id)

        if usuario.perfil == PerfilUsuario.ATENDENTE:
            return self.pedido_repository.listar_por_unidade(db, usuario.id_unidade)

        if usuario.perfil == PerfilUsuario.GERENTE:

            if canal:
                return self.pedido_repository.listar_por_canal(db, canal)

            return self.pedido_repository.listar(db)

        return []

    # =====================================================
    # CANCELAR PEDIDO
    # =====================================================
    def cancelar_pedido(self, db, pedido_id, usuario):

        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        if pedido.status_pedido == StatusPedido.PAGO:
            raise HTTPException(400, "Pedido pago não pode ser cancelado")

        pedido.status_pedido = StatusPedido.CANCELADO

        db.commit()
        db.refresh(pedido)

        return pedido

    # =====================================================
    # PREPARO
    # =====================================================
    def iniciar_preparo(self, db, pedido_id):

        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        pedido.status_preparo = StatusPreparo.EM_PREPARO

        db.commit()
        db.refresh(pedido)

        return pedido

    def marcar_pronto(self, db, pedido_id):

        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        pedido.status_preparo = StatusPreparo.PRONTO

        db.commit()
        db.refresh(pedido)

        return pedido

    def finalizar(self, db, pedido_id):

        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        pedido.status_preparo = StatusPreparo.FINALIZADO

        db.commit()
        db.refresh(pedido)

        return pedido