from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.produto_repository import ProdutoRepository
from src.application.services.produto_service import ProdutoService
from src.api.schemas.produto_schema import ProdutoCreate, ProdutoResponse
from src.infrastructure.repositories.produto_ingrediente_repository import ProdutoIngredienteRepository
from src.infrastructure.repositories.ingrediente_repository import IngredienteRepository
from src.api.dependencies.role_dependency import require_role
from src.domain.entities.usuario import PerfilUsuario

router = APIRouter(prefix="/produtos", tags=["Produtos"])


def get_service():
    return ProdutoService(
        ProdutoRepository(),
        ProdutoIngredienteRepository(),
        IngredienteRepository()
    )


@router.post("/", response_model=ProdutoResponse)
def criar_produto(
    produto: ProdutoCreate,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE)),
    service: ProdutoService = Depends(get_service),
):
    return service.criar_produto(db, produto)


@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE, PerfilUsuario.ATENDENTE)),
    service: ProdutoService = Depends(get_service)
):
    return service.listar_produtos(db)


@router.get("/ativos", response_model=list[ProdutoResponse])
def listar_produtos_ativos(
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE, PerfilUsuario.ATENDENTE)),
    service: ProdutoService = Depends(get_service)
):
    return service.listar_produtos_ativos(db)

@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE, PerfilUsuario.ATENDENTE)),
    service: ProdutoService = Depends(get_service)
):
    return service.buscar_produto(db, produto_id)

@router.patch("/{produto_id}/desativar")
def desativar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE)),
    service: ProdutoService = Depends(get_service)
):
    return service.desativar_produto(db, produto_id)