from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.unidade_repository import UnidadeRepository
from src.application.services.unidade_service import UnidadeService
from src.api.schemas.unidade_schema import UnidadeCreate, UnidadeResponse
from src.api.dependencies.role_dependency import require_role
from src.domain.entities.usuario import PerfilUsuario

router = APIRouter(prefix="/unidades", tags=["Unidades"])


def get_unidade_service():
    return UnidadeService(UnidadeRepository())


@router.post("/", response_model=UnidadeResponse)
def criar_unidade(
    unidade: UnidadeCreate,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE)),
    service: UnidadeService = Depends(get_unidade_service)
):
    return service.criar_unidade(db, unidade)


@router.get("/", response_model=List[UnidadeResponse])
def listar_unidades(
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE, PerfilUsuario.ATENDENTE)),
    service: UnidadeService = Depends(get_unidade_service)
):
    return service.listar_unidades(db)


@router.get("/ativas", response_model=List[UnidadeResponse])
def listar_unidades_ativas(
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE, PerfilUsuario.ATENDENTE)),
    service: UnidadeService = Depends(get_unidade_service)
):
    return service.listar_unidades_ativas(db)


@router.get("/{unidade_id}", response_model=UnidadeResponse)
def buscar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE, PerfilUsuario.ATENDENTE)),
    service: UnidadeService = Depends(get_unidade_service)
):
    return service.buscar_unidade(db, unidade_id)


@router.patch("/{unidade_id}/desativar", response_model=UnidadeResponse)
def desativar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE)),
    service: UnidadeService = Depends(get_unidade_service)
):
    return service.desativar_unidade(db, unidade_id)