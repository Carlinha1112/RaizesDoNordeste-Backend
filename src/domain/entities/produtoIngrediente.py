from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base


class ProdutoIngrediente(Base):
    __tablename__ = "produtos_ingredientes"

    id_produto = Column(Integer, ForeignKey("produtos.id"), primary_key=True)
    id_ingrediente = Column(Integer, ForeignKey("ingredientes.id"), primary_key=True)
    quantidade_necessaria = Column(Integer, nullable=False)   
    
    produto = relationship("Produto")
    ingrediente = relationship("Ingrediente")