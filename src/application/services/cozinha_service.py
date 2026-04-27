from sqlalchemy.orm import Session
from src.domain.entities.pedido import Pedido
from src.domain.enums.pedido_status import StatusPreparo
from src.infrastructure.repositories.pedido_repository import PedidoRepository

class CozinhaService:

    def __init__(self, pedido_repository):
        self.pedido_repository = pedido_repository


    def iniciar_preparo(self, db: Session, pedido_id: int):
        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)
        if not pedido:
            raise Exception("Pedido não encontrado")
        if pedido.status_pagamento != StatusPagamento.PAGO:
            raise Exception("Pedido ainda não foi pago")
        pedido.status_preparo = StatusPreparo.EM_PREPARO
        db.commit()
        return pedido  

    def marcar_pronto(self, db: Session, pedido_id: int):
        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)
        pedido.status_preparo = StatusPreparo.PRONTO
        db.commit()
        return pedido


    def finalizar_pedido(self, db: Session, pedido_id: int):
        pedido = self.pedido_repository.buscar_por_id(db, pedido_id)
        pedido.status_preparo = StatusPreparo.FINALIZADO
        db.commit()
        return pedido
    
    def listar_por_status_preparo(self, db: Session, status: StatusPreparo):
        return self.pedido_repository.listar_por_status_preparo(db, status)