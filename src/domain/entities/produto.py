from sqlalchemy import Column, Integer, String, Boolean
from infrastructure.database.database import Base

class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    ativo = Column(Boolean, default=True)

