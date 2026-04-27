from pydantic import BaseModel

class PontosResponse(BaseModel):
    usuario_id: int
    pontos: int