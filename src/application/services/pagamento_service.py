import random
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.domain.entities.pagamento import Pagamento, Status, Metodo
from src.domain.entities.pedido import StatusPagamento
from src.domain.entities.usuario import PerfilUsuario

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

    def processar_pagamento(self, db: Session, pedido_id: int, metodo: Metodo, usuario):
        try:
            logger.info(f"[PAGAMENTO] Usuário {usuario.id} iniciou pagamento do pedido {pedido_id}")

            pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

            if not pedido:
                logger.warning(f"[PAGAMENTO] Pedido {pedido_id} não encontrado")
                raise HTTPException(status_code=404, detail="Pedido não encontrado")

            if pedido.status_pagamento != StatusPagamento.AGUARDANDO_PAGAMENTO:
                logger.warning(f"[PAGAMENTO] Pedido {pedido_id} não está aguardando pagamento")
                raise HTTPException(status_code=409, detail="Pedido não está aguardando pagamento")

            # 🔒 Regras de autorização
            if usuario.perfil == PerfilUsuario.CLIENTE:
                if pedido.id_usuario != usuario.id:
                    logger.warning(f"[SEGURANÇA] Cliente {usuario.id} tentou pagar pedido de outro usuário")
                    raise HTTPException(status_code=403, detail="Você não pode pagar este pedido")

            if usuario.perfil == PerfilUsuario.ATENDENTE:
                if pedido.id_unidade != usuario.id_unidade:
                    logger.warning(f"[SEGURANÇA] Atendente {usuario.id} tentou acessar outra unidade")
                    raise HTTPException(status_code=403, detail="Você não pode pagar pedidos de outra unidade")

            # 💳 Simulação de pagamento
            if metodo == Metodo.PIX:
                aprovado = True
            else:
                aprovado = random.choice([True, False])

            status_pagamento = Status.APROVADO if aprovado else Status.NEGADO

            pagamento = Pagamento(
                id_pedido=pedido.id,
                metodo=metodo,
                status=status_pagamento,
                valor_pago=pedido.valor_total
            )

            pagamento_salvo = self.pagamento_repository.criar(db, pagamento)

            # ✅ Pagamento aprovado
            if aprovado:
                logger.info(f"[PAGAMENTO] Pedido {pedido.id} aprovado")

                pedido.status_pagamento = StatusPagamento.PAGO

                itens = pedido.itens

                for item in itens:
                    ingredientes = self.produto_ingrediente_repository.listar_por_produto(
                        db, item.id_produto
                    )

                    for ing in ingredientes:
                        quantidade = ing.quantidade_necessaria * item.quantidade

                        self.estoque_repository.debitar_estoque(
                            db, ing.id_ingrediente, quantidade
                        )

                self.fidelidade_service.adicionar_pontos(
                    db, pedido.id_usuario, pedido.valor_total
                )

            # ❌ Pagamento negado
            else:
                logger.warning(f"[PAGAMENTO] Pedido {pedido.id} NEGADO")

                pedido.status_pagamento = StatusPagamento.AGUARDANDO_PAGAMENTO

            db.commit()

            logger.info(f"[PAGAMENTO] Processamento finalizado para pedido {pedido.id}")

            return pagamento_salvo

        except Exception as e:
            db.rollback()
            logger.error(f"[ERRO] Falha ao processar pagamento do pedido {pedido_id}: {str(e)}")
            raise