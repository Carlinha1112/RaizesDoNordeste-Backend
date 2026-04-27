from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.api.schemas.fidelidade_schema import PontosResponse
from src.infrastructure.database.database import get_db

from src.application.services.fidelidade_service import FidelidadeService

from src.infrastructure.repositories.fidelidade_repository import FidelidadeRepository
from src.infrastructure.repositories.historico_fidelidade_repository import HistoricoFidelidadeRepository

from src.api.dependencies.role_dependency import require_role
from src.api.dependencies.auth_dependency import get_current_user

from src.domain.entities.usuario import PerfilUsuario


router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])


def get_fidelidade_service():
    return FidelidadeService(
        FidelidadeRepository(),
        HistoricoFidelidadeRepository()
    )


@router.get("/me", response_model=PontosResponse)
def consultar_meus_pontos(
    db: Session = Depends(get_db),
    usuario=Depends(get_current_user),
    service: FidelidadeService = Depends(get_fidelidade_service)
):
    pontos = service.consultar_pontos(db, usuario.id)
    return {"usuario_id": usuario.id, "pontos": pontos}


@router.get("/{usuario_id}", response_model=PontosResponse)
def consultar_pontos_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _usuario=Depends(require_role(PerfilUsuario.GERENTE)),
    service: FidelidadeService = Depends(get_fidelidade_service)
):
    pontos = service.consultar_pontos(db, usuario_id)
    return {"usuario_id": usuario_id, "pontos": pontos}