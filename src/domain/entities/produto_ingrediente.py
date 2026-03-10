from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class ProdutoIngrediente(Base):
    __tablename__ = "produtos_ingredientes"

    id_produto = Column(Integer, ForeignKey("produto.id"), primary_key=True)
    id_ingrediente = Column(Integer, ForeignKey("ingrediente.id"), primary_key=True)
    quantidade_necessaria = Column(Integer, nullable=False)   
    
    produto = relationship("Produto")
    ingrediente = relationship("Ingrediente")