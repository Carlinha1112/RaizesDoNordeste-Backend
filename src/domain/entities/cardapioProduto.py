from sqlalchemy import Column, Integer, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base


class CardapioProduto(Base):
    __tablename__ = "cardapio_produto"

    id_cardapio = Column(Integer, ForeignKey("cardapio.id"), primary_key=True)
    id_produto = Column(Integer, ForeignKey("produto.id"), primary_key=True)
    preco_venda = Column(Numeric(10, 2), nullable=False)
    ativo_no_cardapio = Column(Boolean, default=True)

    cardapio = relationship("Cardapio")
    produto = relationship("Produto")