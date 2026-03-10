from sqlalchemy import Column, Integer, String, Boolean
from infrastructure.database.database import Base

class Unidade(Base):
    __tablename__ = "unidade"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)

