from sqlalchemy import Column, Integer, ForeignKey, Numeric, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class CardapioProduto(Base):

    __tablename__ = "cardapio_produto"

    id = Column(Integer, primary_key=True, index=True)

    id_cardapio = Column(Integer, ForeignKey("cardapio.id"), nullable=False)
    id_produto = Column(Integer, ForeignKey("produto.id"), nullable=False)

    preco_venda = Column(Numeric(10, 2), nullable=False)
    ativo_no_cardapio = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("id_cardapio", "id_produto", name="uq_cardapio_produto"),
    )

    cardapio = relationship("Cardapio")
    produto = relationship("Produto")