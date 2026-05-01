import logging
from datetime import date
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.api.schemas.pedido_schema import CanalPedido
from src.domain.entities.item_pedido import ItemPedido
from src.domain.entities.pedido import Pedido
from src.domain.entities.usuario import PerfilUsuario
from src.domain.enums.pedido_status import StatusPedido
from src.domain.entities.historico_status_pedido import HistoricoStatusPedido
from src.infrastructure.repositories.historico_pedido_repository import HistoricoPedidoRepository

logger = logging.getLogger(__name__)


class PedidoService:

    def __init__(
        self,
        pedido_repository,
        item_pedido_repository,
        produto_ingrediente_repository,
        estoque_service,
        fidelidade_service,
        cardapio_repository,
        cardapio_produto_repository,
        historico_pedido_repository
    ):
        self.pedido_repository = pedido_repository
        self.item_repository = item_pedido_repository
        self.produto_ingrediente_repository = produto_ingrediente_repository
        self.estoque_service = estoque_service
        self.fidelidade_service = fidelidade_service
        self.cardapio_repository = cardapio_repository
        self.cardapio_produto_repository = cardapio_produto_repository
        self.historico_repository = historico_pedido_repository

    def criar_pedido(self, db, pedido_data, itens, usuario):

        if not itens:
            raise HTTPException(400, "Pedido não pode ser vazio")

        cardapio = self.cardapio_repository.buscar_cardapio_ativo(
            db,
            pedido_data.id_unidade,
            date.today(),
        )

        if not cardapio:
            raise HTTPException(404, "Cardápio não encontrado")

        valor_total = Decimal("0")
        itens_processados = []

        for item in itens:

            cardapio_produto = self.cardapio_produto_repository.buscar(
                db,
                cardapio.id,
                item.produto_id,
            )

            if not cardapio_produto:
                raise HTTPException(
                    404,
                    f"Produto {item.produto_id} não encontrado no cardápio",
                )

            if not cardapio_produto.ativo_no_cardapio:
                raise HTTPException(
                    400,
                    f"Produto {item.produto_id} indisponível",
                )

            ingredientes = (
                self.produto_ingrediente_repository.listar_por_produto(
                    db,
                    item.produto_id,
                )
            )

            for ingrediente in ingredientes:

                quantidade_necessaria = (
                    float(ingrediente.quantidade) * item.quantidade
                )

                estoque = self.estoque_service.buscar_estoque(
                    db,
                    pedido_data.id_unidade,
                    ingrediente.ingrediente_id,
                )

                if not estoque:
                    raise HTTPException(
                        409,
                        f"Ingrediente {ingrediente.ingrediente_id} sem estoque",
                    )

                if float(estoque.quantidade) < quantidade_necessaria:
                    raise HTTPException(
                        409,
                        f"Estoque insuficiente para produto {item.produto_id}",
                    )

            preco_unitario = Decimal(cardapio_produto.preco_venda)
            subtotal = preco_unitario * item.quantidade
            valor_total += subtotal

            itens_processados.append(
                {
                    "produto_id": item.produto_id,
                    "quantidade": item.quantidade,
                    "preco_unitario": preco_unitario,
                }
            )

        id_cliente = usuario.id

        if usuario.perfil == PerfilUsuario.ATENDENTE:

            if pedido_data.canal_pedido != CanalPedido.BALCAO:
                raise HTTPException(
                    403,
                    "Atendente só pode criar pedido BALCAO",
                )

            if pedido_data.cliente_id:
                id_cliente = pedido_data.cliente_id
            else:
                id_cliente = None

        pedido = Pedido(
            id_unidade=pedido_data.id_unidade,
            id_usuario=id_cliente,
            canal_pedido=pedido_data.canal_pedido,
            status_pedido=StatusPedido.AGUARDANDO_PAGAMENTO,
            status_preparo=None,
            valor_total=valor_total,
        )

        try:
            pedido = self.pedido_repository.criar(db, pedido)

            for item in itens_processados:

                item_pedido = ItemPedido(
                    id_pedido=pedido.id,
                    id_produto=item["produto_id"],
                    quantidade=item["quantidade"],
                    preco_unitario=item["preco_unitario"],
                )

                self.item_repository.criar(db, item_pedido)

            db.commit()
            db.refresh(pedido)

            return pedido

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            db.rollback()
            logger.exception(e)

            raise HTTPException(
                500,
                "Erro interno ao criar pedido",
            )
    
    def confirmar_pedido(
        self,
        db: Session,
        pedido_id: int,
        usuario,
        usar_fidelidade: bool = False,
        pontos: int = 0
    ):

        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        if pedido.status_pedido != StatusPedido.AGUARDANDO_PAGAMENTO:
            raise HTTPException(400, "Pedido não pode ser confirmado")

        valor_final = Decimal(pedido.valor_total)
        desconto = Decimal("0")

        if usar_fidelidade and pontos > 0 and pedido.id_usuario:

            desconto, pontos_usados = self.fidelidade_service.aplicar_fidelidade_pedido(
                db=db,
                usuario_id=pedido.id_usuario,
                pedido_id=pedido.id,
                valor_pedido=valor_final,
                pontos_solicitados=pontos
            )

            valor_final -= Decimal(desconto)

        pedido.valor_total = float(valor_final)
        pedido.desconto_fidelidade = float(desconto)

        db.commit()
        db.refresh(pedido)

        return pedido
    
    def resumo_pedido_com_fidelidade(self, db, pedido_id, usuario):

        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        if not pedido.id_usuario:
            return {
                "pedido_id": pedido.id,
                "valor_total": pedido.valor_total,
                "saldo_pontos": 0,
                "desconto_possivel": 0,
                "pontos_maximos_usaveis": 0,
                "limite_percentual": 0.70
            }

        fidelidade = self.fidelidade_service.buscar_ou_criar(
            db,
            pedido.id_usuario
        )

        desconto, pontos_usados = self.fidelidade_service.calcular_desconto(
            Decimal(pedido.valor_total),
            fidelidade.saldo_pontos
        )

        return {
            "pedido_id": pedido.id,
            "valor_total": float(pedido.valor_total),
            "saldo_pontos": fidelidade.saldo_pontos,
            "desconto_possivel": float(desconto),
            "pontos_maximos_usaveis": pontos_usados,
            "limite_percentual": 0.70
        }

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

    def listar_pedidos(
        self,
        db: Session,
        usuario,
        canal: CanalPedido | None = None,
    ):

        if usuario.perfil == PerfilUsuario.CLIENTE:
            return self.pedido_repository.listar_por_usuario(
                db,
                usuario.id,
            )

        if usuario.perfil == PerfilUsuario.ATENDENTE:
            return self.pedido_repository.listar_por_unidade(
                db,
                usuario.id_unidade,
            )

        if usuario.perfil == PerfilUsuario.GERENTE:

            if canal:
                return self.pedido_repository.listar_por_canal(
                    db,
                    canal,
                )

            return self.pedido_repository.listar(db)

        return []

    def cancelar_pedido(self, db, pedido_id, usuario):

        pedido = self.pedido_repository.buscar_por_id(
            db,
            pedido_id,
        )

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        if pedido.status_pedido == StatusPedido.PAGO:
            raise HTTPException(
                400,
                "Pedido pago não pode ser cancelado",
            )

        pedido.status_pedido = StatusPedido.CANCELADO

        db.commit()

        return pedido

    def iniciar_preparo(self, db, pedido_id):

        pedido = self.pedido_repository.buscar_por_id(
            db,
            pedido_id,
        )

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        pedido.status_preparo = "EM_PREPARO"

        historico = HistoricoStatusPedido(
            id_pedido=pedido.id,
            status_anterior=pedido.status_preparo,
        status_novo="EM_PREPARO"
)

        self.historico_repository.criar(db, historico)

        db.commit()
        db.refresh(pedido)

        return pedido

    def marcar_pronto(self, db, pedido_id):

        pedido = self.pedido_repository.buscar_por_id(
            db,
            pedido_id,
        )

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        pedido.status_preparo = "PRONTO"

        historico = HistoricoStatusPedido(
            id_pedido=pedido.id,
            status_anterior=pedido.status_preparo,
            status_novo="PRONTO"
        )

        self.historico_repository.criar(db, historico)

        db.commit()
        db.refresh(pedido)

        return pedido

    def finalizar_pedido(self, db, pedido_id, usuario):

        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise HTTPException(404, "Pedido não encontrado")

        if pedido.status_preparo == "FINALIZADO":
            raise HTTPException(400, "Pedido já finalizado")

        self.estoque_service.baixar_estoque_por_pedido(db, pedido)

        pedido.status_preparo = "FINALIZADO"

        historico = HistoricoStatusPedido(
            id_pedido=pedido.id,
            status_anterior="PRONTO",
            status_novo="FINALIZADO"
        )

        self.historico_repository.criar(db, historico)

        db.commit()
        db.refresh(pedido)

        return pedido