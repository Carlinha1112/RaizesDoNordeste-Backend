from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from src.infrastructure.database.database import get_db
from src.application.services.auth_service import AuthService
from src.infrastructure.repositories.usuario_repository import UsuarioRepository

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service():
    return AuthService(UsuarioRepository())


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    service: AuthService = Depends(get_auth_service)
):
    usuario = service.autenticar_usuario(
        db,
        form_data.username,   
        form_data.password
    )

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = service.gerar_token(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }