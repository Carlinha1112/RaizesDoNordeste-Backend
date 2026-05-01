from enum import Enum


class TipoMovimento(str, Enum):
    CREDITO = "CREDITO"
    DEBITO = "DEBITO"


class Origem(str, Enum):
    PEDIDO = "PEDIDO"
    AJUSTE = "AJUSTE"