from sqlalchemy.orm import Session
from src.domain.entities.fidelidade import Fidelidade


class FidelidadeRepository:

    def criar(self, db: Session, fidelidade: Fidelidade):
        db.add(fidelidade)
        db.flush()
        return fidelidade

    def buscar_por_id(self, db: Session, fidelidade_id: int):
        return db.query(Fidelidade).filter(
            Fidelidade.id == fidelidade_id
        ).first()

    def buscar_por_usuario(
        self,
        db: Session,
        usuario_id: int
    ):
        return db.query(Fidelidade).filter(
            Fidelidade.id_usuario == usuario_id
        ).first()

    def listar(self, db: Session):
        return db.query(Fidelidade).all()