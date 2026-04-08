from pydantic import BaseModel
from typing import List


class ProdutoIngredienteCreate(BaseModel):
    ingrediente_id: int
    quantidade: float


class ProdutoIngredienteResponse(BaseModel):
    ingrediente_id: int
    quantidade: float

    class Config:
        from_attributes = True


class ProdutoCreate(BaseModel):
    nome: str
    descricao: str
    ingredientes: List[ProdutoIngredienteCreate]


class ProdutoResponse(BaseModel):
    id: int
    nome: str
    descricao: str
    ingredientes: List[ProdutoIngredienteResponse]

    class Config:
        from_attributes = True