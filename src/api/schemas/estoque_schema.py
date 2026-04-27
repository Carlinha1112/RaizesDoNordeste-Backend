from pydantic import BaseModel
from decimal import Decimal


class EstoqueCreate(BaseModel):
    id_unidade: int
    id_ingrediente: int
    quantidade: Decimal


class EstoqueMovimento(BaseModel):
    quantidade: Decimal


class EstoqueAjuste(BaseModel):
    quantidade: Decimal


class EstoqueResponse(BaseModel):
    id: int
    id_unidade: int
    id_ingrediente: int
    quantidade: Decimal

    class Config:
        from_attributes = True