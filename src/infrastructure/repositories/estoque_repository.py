from sqlalchemy.orm import Session
from src.domain.entities.estoque import Estoque

class EstoqueRepository:

    def criar(self, db: Session, estoque: Estoque):
        db.add(estoque)
        db.commit()
        db.refresh(estoque)
        return estoque

    def buscar_por_id(self, db: Session, estoque_id: int):
        return db.query(Estoque).filter(Estoque.id == estoque_id).first()

    def buscar_por_produto_unidade(self, db: Session, produto_id: int, unidade: str):
        return db.query(Estoque).filter(Estoque.produto_id == produto_id, Estoque.unidade == unidade).first()

    def listar(self, db: Session):
        return db.query(Estoque).all()