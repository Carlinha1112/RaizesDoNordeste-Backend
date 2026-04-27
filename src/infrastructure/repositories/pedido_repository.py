from sqlalchemy.orm import Session

from src.domain.entities.pedido import Pedido
from src.domain.enums.pedido_status import (
    StatusPedido,
    StatusPreparo
)


class PedidoRepository:

    # =====================================================
    # CREATE
    # =====================================================

    def criar(
        self,
        db: Session,
        pedido: Pedido
    ):
        db.add(pedido)
        db.flush()   # gera ID sem commit
        return pedido

    # =====================================================
    # READ
    # =====================================================

    def buscar_por_id(
        self,
        db: Session,
        pedido_id: int
    ):
        return db.query(Pedido).filter(
            Pedido.id == pedido_id
        ).first()

    def listar(
        self,
        db: Session
    ):
        return db.query(Pedido).all()

    def listar_por_usuario(
        self,
        db: Session,
        usuario_id: int
    ):
        return db.query(Pedido).filter(
            Pedido.id_usuario == usuario_id
        ).all()

    def listar_por_unidade(
        self,
        db: Session,
        unidade_id: int
    ):
        return db.query(Pedido).filter(
            Pedido.id_unidade == unidade_id
        ).all()

    def listar_por_canal(
        self,
        db: Session,
        canal
    ):
        return db.query(Pedido).filter(
            Pedido.canal_pedido == canal
        ).all()

    # =====================================================
    # PREPARO
    # =====================================================

    def listar_fila_preparo(
        self,
        db: Session,
        unidade_id: int | None = None
    ):

        query = db.query(Pedido).filter(
            Pedido.status_pedido == StatusPedido.PAGO,
            Pedido.status_preparo.in_(
                [
                    StatusPreparo.AGUARDANDO_PREPARO,
                    StatusPreparo.EM_PREPARO,
                    StatusPreparo.PRONTO
                ]
            )
        )

        if unidade_id:
            query = query.filter(
                Pedido.id_unidade == unidade_id
            )

        return query.order_by(
            Pedido.id.asc()
        ).all()

    def listar_por_status_preparo(
        self,
        db: Session,
        status: StatusPreparo
    ):
        return db.query(Pedido).filter(
            Pedido.status_pedido == StatusPedido.PAGO,
            Pedido.status_preparo == status
        ).all()

    # =====================================================
    # UPDATE
    # =====================================================

    def atualizar(
        self,
        db: Session,
        pedido: Pedido
    ):
        db.flush()
        return pedido