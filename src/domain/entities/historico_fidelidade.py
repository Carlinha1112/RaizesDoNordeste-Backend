from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base
from datetime import datetime, timezone
import enum

class TipoMovimento(enum.Enum):
    DEBITO = "DEBITO"
    CREDITO = "CREDITO"

class Origem(enum.Enum):
    PEDIDO = "PEDIDO"
    CONVERSAO_PONTOS = "CONVERSAO_PONTOS"
    AJUSTE_MANUAL = "AJUSTE_MANUAL"

class HistoricoFidelidade(Base):
    __tablename__ = "historico_fidelidade"

    id = Column(Integer, primary_key=True, index=True)
    id_fidelidade = Column(Integer, ForeignKey("fidelidade.id"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    tipo_movimento = Column(Enum(TipoMovimento), nullable=False)
    pontos = Column(Integer, nullable=False)
    origem = Column(Enum(Origem), nullable=False)
    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    fidelidade = relationship("Fidelidade")
    usuario = relationship("Usuario")