import enum
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Enum, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from src.infrastructure.database.database import Base
from src.domain.enums.pedido_status import StatusPedido, StatusPreparo


class CanalPedido(str, enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"


class Pedido(Base):
    __tablename__ = "pedido"

    id = Column(Integer, primary_key=True, index=True)

    id_unidade = Column(Integer, ForeignKey("unidade.id"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=True)

    canal_pedido = Column(Enum(CanalPedido), nullable=False)

    status_pedido = Column(Enum(StatusPedido), nullable=False)
    status_preparo = Column(Enum(StatusPreparo), nullable=True)

    valor_total = Column(Numeric(10, 2), nullable=False)

    data_hora = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    unidade = relationship("Unidade")
    usuario = relationship("Usuario")
    itens = relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )
