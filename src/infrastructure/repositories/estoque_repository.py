from sqlalchemy.orm import Session
from src.domain.entities.estoque import Estoque


class EstoqueRepository:

    def criar(self, db: Session, estoque: Estoque):
        db.add(estoque)
        db.flush()
        return estoque

    def buscar_por_id(self, db: Session, estoque_id: int):
        return db.query(Estoque).filter(
            Estoque.id == estoque_id
        ).first()

    def buscar_por_unidade_ingrediente(
        self,
        db: Session,
        unidade_id: int,
        ingrediente_id: int
    ):
        return db.query(Estoque).filter(
            Estoque.id_unidade == unidade_id,
            Estoque.id_ingrediente == ingrediente_id
        ).first()

    def listar(self, db: Session):
        return db.query(Estoque).all()

    def listar_por_unidade(self, db: Session, unidade_id: int):
        return db.query(Estoque).filter(
            Estoque.id_unidade == unidade_id
        ).all()