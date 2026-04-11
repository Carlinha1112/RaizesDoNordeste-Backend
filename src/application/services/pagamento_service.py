import random
from sqlalchemy.orm import Session

from src.domain.entities.pagamento import Pagamento, Status, Metodo
from src.domain.entities.pedido import StatusPagamento


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

    def processar_pagamento(self, db: Session, pedido_id: int, metodo: Metodo):
        try:
            pedido = self.pedido_repository.buscar_por_id(db, pedido_id)

            if not pedido:
                raise Exception("Pedido não encontrado")

            if pedido.status_pagamento != StatusPagamento.AGUARDANDO_PAGAMENTO:
                raise Exception("Pedido não está aguardando pagamento")

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

            if aprovado:
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

            else:
                pedido.status_pagamento = StatusPagamento.AGUARDANDO_PAGAMENTO

            db.commit()
            return pagamento_salvo

        except Exception:
            db.rollback()
            raise