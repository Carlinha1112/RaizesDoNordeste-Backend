from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base


class Cardapio(Base):
    __tablename__ = "cardapio"

    id = Column(Integer, primary_key=True, index=True)
    id_unidade = Column(Integer, ForeignKey("unidade.id"), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date)
    
    unidade = relationship("Unidade")
