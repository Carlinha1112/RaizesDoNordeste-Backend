from sqlalchemy.orm import Session
from typing import List
from datetime import date

from src.domain.entities.pedido import Pedido, StatusPagamento
from src.domain.entities.item_pedido import ItemPedido

from src.api.schemas.pedido_schema import PedidoCreate, ItemPedidoCreate


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


    def criar_pedido(
        self,
        db: Session,
        pedido_data: PedidoCreate,
        itens: List[ItemPedidoCreate],
        pontos_utilizados: int,
        usuario_id: int   # 🔥 vem do JWT
    ):
        try:
            # ❗ E01 - Pedido vazio
            if not itens:
                raise Exception("Pedido não pode ser vazio")

            hoje = date.today()

            # 1️⃣ buscar cardápio ativo
            cardapio = self.cardapio_repository.buscar_cardapio_ativo(
                db, pedido_data.id_unidade, hoje
            )
            if not cardapio:
                raise Exception("Não existe cardápio ativo")

            valor_total = 0

            # 2️⃣ validar disponibilidade + estoque (ingredientes)
            for item in itens:
                cardapio_produto = self.cardapio_produto_repository.buscar(
                    db, cardapio.id, item.produto_id
                )

                if not cardapio_produto or not cardapio_produto.ativo_no_cardapio:
                    raise Exception(f"Produto {item.produto_id} indisponível")

                ingredientes = self.produto_ingrediente_repository.buscar_por_produto(
                    db, item.produto_id
                )

                for ing in ingredientes:
                    quantidade_necessaria = ing.quantidade * item.quantidade

                    if not self.estoque_repository.tem_estoque(
                        db, ing.ingrediente_id, quantidade_necessaria
                    ):
                        raise Exception(
                            f"Estoque insuficiente para ingrediente {ing.ingrediente_id}"
                        )

                valor_total += cardapio_produto.preco_venda * item.quantidade

            # 3️⃣ aplicar fidelidade (desconto)
            desconto = 0
            if pontos_utilizados > 0:
                desconto = self.fidelidade_service.calcular_desconto(
                    valor_total,
                    pontos_utilizados
                )

                # ❗ RN01 - máximo 70%
                if desconto > valor_total * 0.7:
                    raise Exception("Desconto excede 70% do valor do pedido")

            valor_final = valor_total - desconto

            # 4️⃣ criar pedido
            pedido = Pedido(
                id_unidade=pedido_data.id_unidade,
                id_usuario=usuario_id,   # 🔥 vem do token
                canal_pedido=pedido_data.canal_pedido,
                status_pagamento=StatusPagamento.AGUARDANDO_PAGAMENTO,
                valor_total=valor_final
            )

            pedido_salvo = self.pedido_repository.criar(db, pedido)

            # 5️⃣ criar itens
            for item in itens:
                cardapio_produto = self.cardapio_produto_repository.buscar(
                    db, cardapio.id, item.produto_id
                )

                item_entity = ItemPedido(
                    id_pedido=pedido_salvo.id,
                    id_produto=item.produto_id,
                    quantidade=item.quantidade,
                    preco_unitario=cardapio_produto.preco_venda
                )

                self.item_repository.criar(db, item_entity)

            # 6️⃣ debitar pontos (se usou)
            if pontos_utilizados > 0:
                self.fidelidade_service.debitar_pontos(
                    db,
                    usuario_id,
                    pontos_utilizados
                )

            db.commit()
            return pedido_salvo

        except Exception:
            db.rollback()
            raise