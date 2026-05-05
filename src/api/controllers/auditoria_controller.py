from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dependencies.role_dependency import require_role
from src.domain.entities.usuario import PerfilUsuario

from src.infrastructure.database.database import get_db
from src.api.dependencies.auth_dependency import get_current_user
from src.infrastructure.repositories.auditoria_repository import AuditoriaRepository

router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoria"]
)

@router.get("/")
def listar_logs(
    db: Session = Depends(get_db),
    usuario=Depends(require_role(PerfilUsuario.GERENTE))
):
    repo = AuditoriaRepository()
    return repo.listar(db)