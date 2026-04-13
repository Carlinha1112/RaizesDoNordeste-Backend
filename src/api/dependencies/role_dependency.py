from fastapi import Depends, HTTPException
from src.domain.entities.usuario import PerfilUsuario
from src.api.dependencies.auth_dependency import get_current_user

def require_role(*roles: PerfilUsuario):
    def role_checker(usuario = Depends(get_current_user)):
        if usuario.perfil not in roles:
            raise HTTPException(
                status_code=403,
                detail="Acesso não autorizado"
            )
        return usuario
    return role_checker