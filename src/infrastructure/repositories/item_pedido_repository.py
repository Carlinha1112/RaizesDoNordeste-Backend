from sqlalchemy.orm import Session
from src.domain.entities.item_pedido import ItemPedido


class ItemPedidoRepository:

    def criar(self, db: Session, item: ItemPedido):
        db.add(item)
        db.flush()
        return item


    def listar_por_pedido(self, db: Session, pedido_id: int):
        return (
            db.query(ItemPedido)
            .filter(ItemPedido.pedido_id == pedido_id)
            .all()
        )


    def buscar_por_id(self, db: Session, item_id: int):
        return (
            db.query(ItemPedido)
            .filter(ItemPedido.id == item_id)
            .first()
        )