from sqlalchemy.orm import Session
from src.infrastructure.repositories.usuario_repository import UsuarioRepository
from src.domain.entities.usuario import Usuario
from src.api.schemas.usuario_schema import UsuarioCreate


class UsuarioService:

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository


    def criar_usuario(self, db: Session, usuario_data: UsuarioCreate):
        existente = self.repository.buscar_por_email(db, usuario_data.email)
        if existente:
            raise Exception("Email já cadastrado")
        usuario = Usuario(
            nome=usuario_data.nome,
            data_nasc=usuario_data.data_nasc,
            email=usuario_data.email,
            telefone=usuario_data.telefone,
            perfil=usuario_data.perfil
        )
        usuario.senha_hash = usuario.hash_password(usuario_data.senha)
        return self.repository.criar(db, usuario)


    def buscar_usuario(self, db: Session, usuario_id: int):
        return self.repository.buscar_por_id(db, usuario_id)


    def listar_usuarios(self, db: Session):
        return self.repository.listar(db)


    def desativar_usuario(self, db: Session, usuario_id: int):
        usuario = self.repository.buscar_por_id(db, usuario_id)
        if not usuario:
            raise Exception("Usuário não encontrado")
        return self.repository.desativar(db, usuario)


    def autenticar_usuario(self, db: Session, email: str, senha: str):
        usuario = self.repository.buscar_por_email(db, email)
        if not usuario:
            raise Exception("Usuário não encontrado")
        if not usuario.verify_password(senha):
            raise Exception("Senha inválida")
        return usuario