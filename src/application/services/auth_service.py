from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.infrastructure.repositories.usuario_repository import UsuarioRepository

SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class AuthService:

    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def autenticar_usuario(self, db: Session, email: str, senha: str):
        usuario = self.usuario_repository.buscar_por_email(db, email)

        if not usuario or not usuario.verify_password(senha):
            return None

        return usuario

    def criar_token(self, usuario_id: int):
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "sub": str(usuario_id),
            "exp": expire
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return token

    def verificar_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            usuario_id = payload.get("sub")

            if usuario_id is None:
                return None

            return int(usuario_id)

        except JWTError:
            return None