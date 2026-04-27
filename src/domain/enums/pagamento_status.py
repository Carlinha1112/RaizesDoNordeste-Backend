import enum


class StatusPagamento(str, enum.Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    NEGADO = "NEGADO"