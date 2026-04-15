import logging
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from fastapi import HTTPException

from src.domain.entities.pedido import Pedido, StatusPagamento
from src.domain.entities.item_pedido import ItemPedido

from src.api.schemas.pedido_schema import PedidoCreate, ItemPedidoCreate
from src.domain.entities.usuario import PerfilUsuario

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
            
            logger.info(f"Usuário {usuario_id} iniciando criação de pedido")

            if not itens:
                logger.warning("Tentativa de criar pedido vazio")
                raise HTTPException(status_code=400, detail="Pedido não pode ser vazio")

            hoje = date.today()

            cardapio = self.cardapio_repository.buscar_cardapio_ativo(
                db, pedido_data.id_unidade, hoje
            )

            if not cardapio:
                logger.warning(f"Sem cardápio ativo para unidade {pedido_data.id_unidade}")
                raise HTTPException(status_code=404, detail="Não existe cardápio ativo")

            valor_total = 0

            for item in itens:
                cardapio_produto = self.cardapio_produto_repository.buscar(
                    db, cardapio.id, item.produto_id
                )

                if not cardapio_produto:
                    raise HTTPException(status_code=404, detail="Produto não encontrado no cardápio")

                if not cardapio_produto.ativo_no_cardapio:
                    raise HTTPException(status_code=400, detail="Produto indisponível")

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
                        logger.warning(f"Estoque insuficiente para ingrediente {ing.id_ingrediente}")
                        raise HTTPException(status_code=400, detail=
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
                    logger.warning("Desconto excede limite permitido")
                    raise HTTPException(status_code=400, detail="Desconto excede 70% do valor do pedido")

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

            logger.info(f"Pedido {pedido_salvo.id} criado com sucesso")

            return pedido_salvo

        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao criar pedido: {str(e)}")
            raise

    def buscar_pedido(self, db: Session, pedido_id: int, usuario):
        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

        if not pedido:
            logger.warning(f"Pedido {pedido_id} não encontrado")
            raise HTTPException(status_code=404, detail="Pedido não encontrado")

        if usuario.perfil == PerfilUsuario.CLIENTE:
            if pedido.id_usuario != usuario.id:
                logger.warning(f"Cliente {usuario.id} tentou acessar pedido {pedido_id}")
                raise HTTPException(status_code=403, detail="Acesso negado")

        if usuario.perfil == PerfilUsuario.ATENDENTE:
            if pedido.id_unidade != usuario.id_unidade:
                logger.warning(f"Atendente {usuario.id} tentou acessar outra unidade")
                raise HTTPException(status_code=403, detail="Acesso negado")

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
            logger.warning(f"Tentativa de cancelar pedido inexistente {pedido_id}")
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
        if usuario.perfil == PerfilUsuario.ATENDENTE:
            if pedido.id_unidade != usuario.id_unidade:
                logger.warning("Atendente tentando cancelar pedido de outra unidade")
                raise HTTPException(status_code=403, detail="Você não pode acessar pedidos de outra unidade")

        if usuario.perfil == PerfilUsuario.CLIENTE:
            if pedido.id_usuario != usuario.id:
                logger.warning("Cliente tentando cancelar pedido de outro cliente")
                raise HTTPException(status_code=403, detail="Você não pode cancelar este pedido")

        if pedido.status_pagamento == StatusPagamento.PAGO:
            logger.warning(f"Tentativa de cancelar pedido pago {pedido_id}")
            raise HTTPException(status_code=400, detail="Não é possível cancelar um pedido já pago")

        pedido.status_pagamento = StatusPagamento.CANCELADO

        db.commit()

        logger.info(f"Pedido {pedido_id} cancelado com sucesso")

        return pedido