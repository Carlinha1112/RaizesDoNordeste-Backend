from pydantic import BaseModel


class UnidadeCreate(BaseModel):
    nome: str
    cidade: str
    estado: str


class UnidadeResponse(BaseModel):
    id: int
    nome: str
    cidade: str
    estado: str
    ativo: bool

    class Config:
        from_attributes = True