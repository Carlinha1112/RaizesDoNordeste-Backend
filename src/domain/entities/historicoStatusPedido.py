from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from infrastructure.database.database import Base
from datetime import datetime, timezone
import enum

class Status(enum.Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO PAGAMENTO"
    PAGO = "PAGO"
    EM_PREPARO = "EM PREPARO"
    PRONTO = "PRONTO"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"

class HistoricoStatusPedido(Base):
    __tablename__ = "historico_status_pedido"

    id = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id"), nullable=False)
    status = Column(Enum(Status), nullable=False)
    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    pedido = relationship("Pedido")
   