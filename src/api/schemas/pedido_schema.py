from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

from src.domain.enums.pedido_status import (
    StatusPedido,
    StatusPreparo
)


class CanalPedido(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"


class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int


class PedidoCreate(BaseModel):
    id_unidade: int
    canal_pedido: CanalPedido
    cliente_id: Optional[int] = None
    itens: List[ItemPedidoCreate]
    pontos_utilizados: int = 0


class PedidoResponse(BaseModel):
    id: int
    id_unidade: int
    id_usuario: Optional[int] = None

    canal_pedido: str
    valor_total: float

    status_pedido: StatusPedido
    status_preparo: Optional[StatusPreparo] = None

    class Config:
        from_attributes = True