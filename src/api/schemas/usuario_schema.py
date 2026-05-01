from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from enum import Enum
from typing import Optional

class PerfilUsuario(str, Enum):
    GERENTE = "GERENTE"
    ATENDENTE = "ATENDENTE"
    CLIENTE = "CLIENTE"


class UsuarioCreate(BaseModel):
    nome: str
    data_nasc: date
    email: EmailStr
    telefone: str
    senha: str
    perfil: PerfilUsuario
    id_unidade: int | None = None
    consentimento: bool

class UsuarioUpdate(BaseModel): 
    nome: str | None = None
    telefone: str | None = None
    email: str | None = None
    senha: str | None = None

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    perfil: PerfilUsuario
    id_unidade: int | None = None
    ativo: bool
    consentimento: bool
    data_consentimento: Optional[datetime]
    versao_termos: Optional[str]    

    class Config:
        from_attributes = True