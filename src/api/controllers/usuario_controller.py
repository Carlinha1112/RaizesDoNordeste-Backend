from src.api.dependencies.auth_dependency import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dependencies.role_dependency import require_role
from src.domain.entities.usuario import PerfilUsuario
from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.usuario_repository import UsuarioRepository
from src.application.services.usuario_service import UsuarioService
from src.api.schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

def get_usuario_service():
    return UsuarioService(UsuarioRepository())

@router.post("/", response_model=UsuarioResponse)
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db),
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.criar_usuario(db, usuario)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE)),
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.buscar_usuario(db, usuario_id)

@router.get("/")
def listar_usuarios(
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE)),
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.listar_usuarios(db)

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario = Depends(get_current_user),
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.atualizar_usuario(db, usuario_id, dados, usuario)

    
@router.patch("/{usuario_id}/desativar")
def desativar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(require_role(PerfilUsuario.GERENTE)),
    service: UsuarioService = Depends(get_usuario_service)
):
    return service.desativar_usuario(db, usuario_id)