from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.dependencies.role_dependency import require_role
from src.domain.entities.usuario import PerfilUsuario

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.ingrediente_repository import IngredienteRepository
from src.application.services.ingrediente_service import IngredienteService
from src.api.schemas.ingrediente_schema import IngredienteCreate, IngredienteResponse


router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


def get_service():
    return IngredienteService(IngredienteRepository())


@router.post("/", response_model=IngredienteResponse)
def criar_ingrediente(
    ingrediente: IngredienteCreate,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE)),
    service: IngredienteService = Depends(get_service)
):
    return service.criar_ingrediente(db, ingrediente)


@router.get("/", response_model=list[IngredienteResponse])
def listar_ingredientes(
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE, PerfilUsuario.ATENDENTE)),
    service: IngredienteService = Depends(get_service)
):
    return service.listar_ingredientes(db)


@router.get("/{ingrediente_id}", response_model=IngredienteResponse)
def buscar_ingrediente(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE, PerfilUsuario.ATENDENTE)),
    service: IngredienteService = Depends(get_service)
):
    return service.buscar_ingrediente(db, ingrediente_id)