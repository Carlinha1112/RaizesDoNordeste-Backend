from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class ProdutoIngrediente(Base):
    __tablename__ = "produto_ingrediente"

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produto.id"))
    ingrediente_id = Column(Integer, ForeignKey("ingrediente.id"))
    quantidade = Column(Float)

    produto = relationship("Produto", back_populates="ingredientes")