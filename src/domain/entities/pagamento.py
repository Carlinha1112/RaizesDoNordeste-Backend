from sqlalchemy import Column, DateTime, Integer, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from src.infrastructure.database.database import Base
from src.domain.enums.pagamento_status import StatusPagamento


class Metodo(enum.Enum):
    PIX = "PIX"
    CARTAO = "CARTAO"
    DINHEIRO = "DINHEIRO"


class Pagamento(Base):
    __tablename__ = "pagamento"

    id = Column(Integer, primary_key=True, index=True)

    id_pedido = Column(Integer, ForeignKey("pedido.id"), nullable=False)

    metodo = Column(Enum(Metodo), nullable=False)

    status = Column(Enum(StatusPagamento), nullable=False)

    valor_pago = Column(Numeric(10, 2), nullable=False)

    data_hora = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    pedido = relationship("Pedido")
