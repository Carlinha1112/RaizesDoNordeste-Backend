from sqlalchemy import Column, Integer, String, DateTime
from src.infrastructure.database.database import Base
from datetime import datetime, timezone


class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=True)
    acao = Column(String, nullable=False)
    entidade = Column(String, nullable=False)
    entidade_id = Column(Integer, nullable=True)
    detalhes = Column(String, nullable=True)
    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))