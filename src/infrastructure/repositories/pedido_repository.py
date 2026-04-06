from sqlalchemy.orm import Session
from src.domain.entities.pedido import Pedido, StatusPagamento, StatusPreparo


class PedidoRepository:

    def criar(self, db: Session, pedido: Pedido):
        db.add(pedido)
        db.flush()  # gera ID sem commit
        return pedido

    def buscar_por_id(self, db: Session, pedido_id: int):
        return db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def listar_por_unidade(self, db: Session, unidade_id: int):
        return db.query(Pedido).filter(Pedido.id_unidade == unidade_id).all()

    def listar_por_usuario(self, db: Session, usuario_id: int):
        return db.query(Pedido).filter(Pedido.id_usuario == usuario_id).all()
    
    def listar_por_status_preparo(self, db: Session, status: StatusPreparo):
        return db.query(Pedido).filter(
            Pedido.status_preparo == status,
            Pedido.status_pagamento == StatusPagamento.PAGO
        ).all()
    
    def listar_por_status_pagamento(self, db: Session, status: str):
        return db.query(Pedido).filter(Pedido.status_pagamento == status).all()

    def listar(self, db: Session):
        return db.query(Pedido).all()
    
    def atualizar(self, db: Session, pedido: Pedido):
        db.flush()
        return pedido
    