from pydantic import BaseModel
from enum import Enum
from typing import List


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
    itens: List[ItemPedidoCreate]
    pontos_utilizados: int = 0


class PedidoResponse(BaseModel):

    id: int
    id_unidade: int
    id_usuario: int
    canal_pedido: CanalPedido
    valor_total: float

    class Config:
        from_attributes = True
