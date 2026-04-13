from sqlalchemy.orm import Session
from src.infrastructure.repositories.usuario_repository import UsuarioRepository
from src.domain.entities.usuario import Usuario
from src.api.schemas.usuario_schema import UsuarioCreate
from src.domain.entities.usuario import PerfilUsuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UsuarioService:

    def __init__(self, repository: UsuarioRepository):
        self.repository = repository


    def criar_usuario(self, db: Session, usuario: UsuarioCreate):

        if usuario.perfil == PerfilUsuario.ATENDENTE and not usuario.id_unidade:
            raise Exception("Atendente deve estar vinculado a uma unidade")

        usuario_entity = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            senha_hash="",  
            perfil=usuario.perfil,
            id_unidade=usuario.id_unidade
        )

        usuario_entity.senha_hash = usuario_entity.hash_password(usuario.senha)

        usuario_salvo = self.repository.criar(db, usuario_entity)

        db.commit()
        return usuario_salvo


    def buscar_usuario(self, db: Session, usuario_id: int):
        return self.repository.buscar_por_id(db, usuario_id)


    def listar_usuarios(self, db: Session):
        return self.repository.listar(db)


    def desativar_usuario(self, db: Session, usuario_id: int):
        usuario = self.repository.buscar_por_id(db, usuario_id)
        if not usuario:
            raise Exception("Usuário não encontrado")
        self.repository.desativar(db, usuario)
        db.commit()
        return usuario

