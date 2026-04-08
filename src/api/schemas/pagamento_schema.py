from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from enum import Enum

class MetodoPagamento(str, Enum):
    PIX = "PIX"
    CARTAO = "CARTAO"
    DINHEIRO = "DINHEIRO"

class StatusPagamento(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"

class PagamentoResponse(BaseModel):
    id: int
    id_pedido: int
    metodo: MetodoPagamento
    status: StatusPagamento
    valor_pago: Decimal
    data_hora: datetime

    class Config:
        from_attributes = True