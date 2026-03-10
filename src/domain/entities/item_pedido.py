from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class ItemPedido(Base):
    __tablename__ = "item_pedido"

    id = Column(Integer, primary_key=True, index=True)  
    id_pedido = Column(Integer, ForeignKey("pedido.id"), primary_key=True)
    id_produto = Column(Integer, ForeignKey("produto.id"), primary_key=True)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

    pedido = relationship("Pedido")
    produto = relationship("Produto")