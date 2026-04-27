import random
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.domain.entities.pagamento import Pagamento, Metodo
from src.domain.entities.usuario import PerfilUsuario
from src.domain.enums.pagamento_status import StatusPagamento
from src.application.services.pedido_domain import PedidoDomain

logger = logging.getLogger(__name__)


class PagamentoService:

    def __init__(
        self,
        pagamento_repository,
        pedido_repository,
        produto_ingrediente_repository,
        estoque_repository,
        fidelidade_service
    ):
        self.pagamento_repository = pagamento_repository
        self.pedido_repository = pedido_repository
        self.produto_ingrediente_repository = produto_ingrediente_repository
        self.estoque_repository = estoque_repository
        self.fidelidade_service = fidelidade_service

    # =====================================================
    # PROCESSAR PAGAMENTO
    # =====================================================
    def processar_pagamento(
        self,
        db: Session,
        pedido_id: int,
        metodo: Metodo,
        usuario
    ):

        pedido = self.pedido_repository.buscar_por_id(
            db,
            pedido_id
        )

        if not pedido:
            raise HTTPException(
                status_code=404,
                detail="Pedido não encontrado"
            )

        # ==========================================
        # SEGURANÇA
        # ==========================================
        if usuario.perfil == PerfilUsuario.CLIENTE:
            if pedido.id_usuario != usuario.id:
                raise HTTPException(
                    status_code=403,
                    detail="Você não pode pagar este pedido"
                )

        if usuario.perfil == PerfilUsuario.ATENDENTE:
            if pedido.id_unidade != usuario.id_unidade:
                raise HTTPException(
                    status_code=403,
                    detail="Você não pode pagar pedidos de outra unidade"
                )

        # ==========================================
        # VALIDA STATUS
        # ==========================================
        if not PedidoDomain.pode_ser_pago(
            pedido.status_pedido
        ):
            raise HTTPException(
                status_code=409,
                detail="Pedido não pode ser pago"
            )

        # ==========================================
        # REGRAS DE APROVAÇÃO
        # ==========================================
        # PIX sempre aprova
        # Dinheiro sempre aprova
        # Cartão pode negar aleatoriamente
        if metodo == Metodo.PIX:
            aprovado = True

        elif metodo == Metodo.DINHEIRO:
            aprovado = True

        elif metodo == Metodo.CARTAO:
            aprovado = random.choice(
                [True, True, True, False]
            )

        else:
            aprovado = False

        # ==========================================
        # CRIA REGISTRO PAGAMENTO
        # ==========================================
        pagamento = Pagamento(
            id_pedido=pedido.id,
            metodo=metodo,
            status=(
                StatusPagamento.APROVADO
                if aprovado
                else StatusPagamento.NEGADO
            ),
            valor_pago=pedido.valor_total
        )

        try:

            self.pagamento_repository.criar(
                db,
                pagamento
            )

            # ==================================
            # SE APROVADO
            # ==================================
            if aprovado:

                PedidoDomain.marcar_como_pago(
                    pedido
                )

                # só gera fidelidade se existir cliente
                if pedido.id_usuario:

                    self.fidelidade_service.adicionar_pontos(
                        db=db,
                        usuario_id=pedido.id_usuario,
                        valor_pedido=float(
                            pedido.valor_total
                        )
                    )

            db.commit()
            db.refresh(pagamento)

            return pagamento

        except HTTPException:
            db.rollback()
            raise

        except Exception as e:
            db.rollback()
            logger.exception(e)

            raise HTTPException(
                status_code=500,
                detail="Erro interno ao processar pagamento"
            )