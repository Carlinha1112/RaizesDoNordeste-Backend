from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    ativo = Column(Boolean, default=True)

    ingredientes = relationship(
        "ProdutoIngrediente",
        back_populates="produto",
        cascade="all, delete-orphan"
    )