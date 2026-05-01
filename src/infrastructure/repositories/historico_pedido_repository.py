from sqlalchemy.orm import Session
from src.domain.entities.historico_status_pedido import HistoricoStatusPedido

class HistoricoPedidoRepository:

    def listar(
        self,
        db: Session,
        pedido_id=None,
        data_inicio=None,
        data_fim=None
    ):
        query = db.query(HistoricoStatusPedido)

        if pedido_id is not None:
            query = query.filter(HistoricoStatusPedido.id_pedido == pedido_id)

        if data_inicio is not None  :
            query = query.filter(HistoricoStatusPedido.data_hora >= data_inicio)

        if data_fim is not None:
            query = query.filter(HistoricoStatusPedido.data_hora <= data_fim)

        return query.all()
    
    def criar(self, db, historico):
        db.add(historico)
        return historico

    def listar_por_pedido(self, db, pedido_id):
        return db.query(HistoricoStatusPedido)\
            .filter(HistoricoStatusPedido.id_pedido == pedido_id)\
            .all()