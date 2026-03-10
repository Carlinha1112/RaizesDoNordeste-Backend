from sqlalchemy import Column, DateTime, Integer, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base
from datetime import datetime, timezone


class Fidelidade(Base):
    __tablename__ = "fidelidade"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    saldo_pontos = Column(Numeric(10, 2), default=0)
    aderiu = Column(Boolean, default=True) 
    data_adesao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    usuario = relationship("Usuario")
