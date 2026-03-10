from sqlalchemy import Column, Integer, String
from src.infrastructure.database.database import Base

class Ingrediente(Base):
    __tablename__ = "ingrediente"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    unidade_medida = Column(String)