from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.application.services.fidelidade_service import FidelidadeService
from src.infrastructure.repositories.fidelidade_repository import FidelidadeRepository
from src.infrastructure.repositories.historico_fidelidade_repository import HistoricoFidelidadeRepository

router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])

def get_fidelidade_service():
    return FidelidadeService(
        FidelidadeRepository(),
        HistoricoFidelidadeRepository()
    )

@router.get("/{usuario_id}")
def consultar_pontos(
    usuario_id: int,
    db: Session = Depends(get_db),
    service: FidelidadeService = Depends(get_fidelidade_service)
):
    pontos = service.consultar_pontos(db, usuario_id)
    return {"pontos": pontos}