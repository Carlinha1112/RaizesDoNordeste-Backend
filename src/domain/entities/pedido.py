from sqlalchemy import Column, DateTime, Integer, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base
from datetime import datetime, timezone
import enum

class CanalPedido(enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICK_UP"

class Status(enum.Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO PAGAMENTO"
    PAGO = "PAGO"
    EM_PREPARO = "EM PREPARO"
    PRONTO = "PRONTO"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"

class Pedido(Base):
    __tablename__ = "pedido"

    id = Column(Integer, primary_key=True, index=True)
    id_unidade = Column(Integer, ForeignKey("unidade.id"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    canal_pedido = Column(Enum(CanalPedido), nullable=False)
    status = Column(Enum(Status), nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    unidade = relationship("Unidade")
    usuario = relationship("Usuario")   