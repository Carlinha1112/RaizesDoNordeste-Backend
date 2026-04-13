from sqlalchemy.orm import Session
from typing import List
from datetime import date

from src.domain.entities.pedido import Pedido, StatusPagamento
from src.domain.entities.item_pedido import ItemPedido

from src.api.schemas.pedido_schema import PedidoCreate, ItemPedidoCreate
from src.domain.entities.usuario import PerfilUsuario



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
        pedido_data,
        itens,
        pontos_utilizados,
        usuario
    ):
        usuario_id = usuario.id
        try:
            if not itens:
                raise Exception("Pedido não pode ser vazio")

            hoje = date.today()

            cardapio = self.cardapio_repository.buscar_cardapio_ativo(
                db, pedido_data.id_unidade, hoje
            )

            if not cardapio:
                raise Exception("Não existe cardápio ativo")

            valor_total = 0

            for item in itens:
                cardapio_produto = self.cardapio_produto_repository.buscar(
                    db, cardapio.id, item.produto_id
                )

                if not cardapio_produto or not cardapio_produto.ativo_no_cardapio:
                    raise Exception(f"Produto {item.produto_id} indisponível")

                ingredientes = self.produto_ingrediente_repository.listar_por_produto(
                    db, item.produto_id
                )

                for ing in ingredientes:
                    quantidade_necessaria = (
                        ing.quantidade_necessaria * item.quantidade
                    )

                    if not self.estoque_repository.tem_estoque(
                        db,
                        ing.id_ingrediente,
                        quantidade_necessaria
                    ):
                        raise Exception(
                            f"Estoque insuficiente para ingrediente {ing.id_ingrediente}"
                        )

                valor_total += cardapio_produto.preco_venda * item.quantidade

            desconto = 0

            if pontos_utilizados > 0:
                desconto = self.fidelidade_service.calcular_desconto(
                    valor_total,
                    pontos_utilizados
                )

                if desconto > valor_total * 0.7:
                    raise Exception("Desconto excede 70% do valor do pedido")

            valor_final = valor_total - desconto

            pedido = Pedido(
                id_unidade=pedido_data.id_unidade,
                id_usuario=usuario_id,
                canal_pedido=pedido_data.canal_pedido,
                status_pagamento=StatusPagamento.AGUARDANDO_PAGAMENTO,
                valor_total=valor_final
            )

            pedido_salvo = self.pedido_repository.criar(db, pedido)

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

    def buscar_pedido(self, db: Session, pedido_id: int, usuario):
        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise Exception("Pedido não encontrado")

        if usuario.perfil == PerfilUsuario.CLIENTE:
            if pedido.id_usuario != usuario.id:
                raise Exception("Acesso negado")

        if usuario.perfil == PerfilUsuario.ATENDENTE:
            if pedido.id_unidade != usuario.id_unidade:
                raise Exception("Acesso negado")

        return pedido

    def listar_pedidos(self, db: Session, usuario):

        if usuario.perfil == PerfilUsuario.CLIENTE:
            return self.pedido_repository.listar_por_usuario(db, usuario.id)

        if usuario.perfil == PerfilUsuario.ATENDENTE:
            return self.pedido_repository.listar_por_unidade(db, usuario.id_unidade)

        if usuario.perfil == PerfilUsuario.GERENTE:
            return self.pedido_repository.listar(db)

    def cancelar_pedido(self, db: Session, pedido_id: int, usuario):

        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            raise Exception("Pedido não encontrado")
        
        if usuario.perfil == PerfilUsuario.ATENDENTE:
            if pedido.id_unidade != usuario.id_unidade:
                raise Exception("Você não pode acessar pedidos de outra unidade")

        if usuario.perfil == PerfilUsuario.CLIENTE:
            if pedido.id_usuario != usuario.id:
                raise Exception("Você não pode cancelar este pedido")

        if pedido.status_pagamento == StatusPagamento.PAGO:
            raise Exception("Não é possível cancelar um pedido já pago")

        pedido.status_pagamento = StatusPagamento.CANCELADO

        db.commit()
        return pedido