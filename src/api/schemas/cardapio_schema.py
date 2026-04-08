from pydantic import BaseModel
from datetime import date


class CardapioCreate(BaseModel):
    id_unidade: int
    data_inicio: date
    data_fim: date | None = None


class CardapioResponse(BaseModel):
    id: int
    id_unidade: int
    data_inicio: date
    data_fim: date | None

    class Config:
        from_attributes = True