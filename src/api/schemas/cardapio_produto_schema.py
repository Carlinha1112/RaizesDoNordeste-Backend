from pydantic import BaseModel
from decimal import Decimal


class CardapioProdutoCreate(BaseModel):
    id_produto: int
    preco_venda: Decimal


class CardapioProdutoUpdate(BaseModel):
    preco_venda: Decimal
    ativo_no_cardapio: bool


class CardapioProdutoResponse(BaseModel):
    id_cardapio: int
    id_produto: int
    preco_venda: Decimal
    ativo_no_cardapio: bool

    class Config:
        from_attributes = True