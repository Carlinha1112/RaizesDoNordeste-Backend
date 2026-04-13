from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.infrastructure.database.database import get_db
from src.infrastructure.repositories.usuario_repository import UsuarioRepository

SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    usuario = UsuarioRepository().buscar_por_id(db, user_id)

    if not usuario:
        raise credentials_exception

    return usuario