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

    def buscar_por_ingrediente(self, db: Session, ingrediente_id: int):
        return db.query(Estoque).filter(
            Estoque.id_ingrediente == ingrediente_id
        ).first()

    def listar(self, db: Session):
        return db.query(Estoque).all()

    def tem_estoque(self, db: Session, ingrediente_id: int, quantidade: float):
        estoque = self.buscar_por_ingrediente(db, ingrediente_id)
        return estoque is not None and estoque.quantidade_atual >= quantidade

    def debitar_estoque(self, db: Session, ingrediente_id: int, quantidade: float):
        estoque = self.buscar_por_ingrediente(db, ingrediente_id)

        if not estoque:
            raise Exception("Estoque não encontrado")

        if estoque.quantidade_atual < quantidade:
            raise Exception("Estoque insuficiente")

        estoque.quantidade_atual -= quantidade
        db.flush()
        return estoque

    def repor_estoque(self, db: Session, ingrediente_id: int, quantidade: float):
        estoque = self.buscar_por_ingrediente(db, ingrediente_id)

        if not estoque:
            raise Exception("Estoque não encontrado")

        estoque.quantidade_atual += quantidade
        db.flush()
        return estoque