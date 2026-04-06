from sqlalchemy.orm import Session
from src.domain.entities.pagamento import Pagamento


class PagamentoRepository:

    def criar(self, db: Session, pagamento: Pagamento):
        db.add(pagamento)
        db.commit()
        db.refresh(pagamento)
        return pagamento

    def buscar_por_id(self, db: Session, pagamento_id: int):
        return db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()

    def buscar_por_id_pedido(self, db: Session, pedido_id: int):
        return db.query(Pagamento).filter(Pagamento.pedido_id == pedido_id).first()
