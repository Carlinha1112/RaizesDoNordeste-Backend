from sqlalchemy.orm import Session
from src.domain.entities.usuario import Usuario


class UsuarioRepository:

    def criar(self, db: Session, usuario: Usuario):
        db.add(usuario)
        db.flush()
        return usuario

    def buscar_por_id(self, db: Session, usuario_id: int):
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def buscar_por_email(self, db: Session, email: str):
        return db.query(Usuario).filter(Usuario.email == email).first()

    def listar(self, db: Session):
        return db.query(Usuario).all()
    
    def desativar(self, db: Session, usuario: Usuario):
        usuario.ativo = False
        db.flush()
        return usuario