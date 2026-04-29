from pydantic import BaseModel, EmailStr
from datetime import date
from enum import Enum


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

    class Config:
        from_attributes = True