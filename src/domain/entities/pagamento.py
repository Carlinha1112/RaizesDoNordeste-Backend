from sqlalchemy import Column, DateTime, Integer, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base
from datetime import datetime, timezone
import enum

class Metodo(enum.Enum):
    PIX = "PIX"
    CARTAO = "CARTAO"
    DINHEIRO = "DINHEIRO"

class Status(enum.Enum):
    APROVADO = "APROVADO"
    NEGADO = "NEGADO"

class Pagamento(Base):
    __tablename__ = "pagamento"

    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id"), nullable=False)
    metodo = Column(Enum(Metodo), nullable=False)
    status = Column(Enum(Status), nullable=False)
    valor_pago = Column(Numeric(10, 2), nullable=False)
    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    pedido = relationship("Pedido")
