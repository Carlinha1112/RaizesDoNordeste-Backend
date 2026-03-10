from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True, index=True)
    id_unidade = Column(Integer, ForeignKey("unidade.id"), nullable=False)
    id_ingrediente = Column(Integer, ForeignKey("ingrediente.id"), nullable=False)
    quantidade_atual = Column(Integer, nullable=False)
    
    unidade = relationship("Unidade")
    ingrediente = relationship("Ingrediente")   