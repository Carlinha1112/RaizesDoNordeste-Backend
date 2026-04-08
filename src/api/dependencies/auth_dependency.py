from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.usuario_repository import UsuarioRepository
from src.application.services.auth_service import AuthService

security = HTTPBearer()


def get_auth_service():
    return AuthService(UsuarioRepository())


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service)
):
    token = credentials.credentials

    usuario_id = service.verificar_token(token)

    if not usuario_id:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = service.usuario_repository.buscar_por_id(db, usuario_id)

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return usuario