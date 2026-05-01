from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base
from datetime import datetime, timezone
import enum
from src.domain.enums.fidelidade_enum import TipoMovimento, Origem

class HistoricoFidelidade(Base):
    __tablename__ = "historico_fidelidade"

    id = Column(Integer, primary_key=True, index=True)
    id_fidelidade = Column(Integer, ForeignKey("fidelidade.id"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    id_pedido = Column(Integer, ForeignKey("pedido.id"), nullable=True)
    tipo_movimento = Column(Enum(TipoMovimento), nullable=False)
    pontos = Column(Integer, nullable=False)
    origem = Column(Enum(Origem), nullable=False)
    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    fidelidade = relationship("Fidelidade")
    usuario = relationship("Usuario")
    pedido = relationship("Pedido")