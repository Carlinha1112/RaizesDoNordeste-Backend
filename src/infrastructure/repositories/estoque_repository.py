from sqlalchemy.orm import Session
from src.domain.entities.estoque import Estoque


class EstoqueRepository:

    def criar(self, db: Session, estoque: Estoque):
        db.add(estoque)
        db.commit()
        db.refresh(estoque)
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

    def tem_estoque(
        self,
        db: Session,
        unidade_id: int,
        ingrediente_id: int,
        quantidade: float
    ):
        estoque = self.buscar_por_unidade_ingrediente(
            db,
            unidade_id,
            ingrediente_id
        )

        return estoque is not None and estoque.quantidade >= quantidade

    def debitar_estoque(
        self,
        db: Session,
        unidade_id: int,
        ingrediente_id: int,
        quantidade: float
    ):
        estoque = self.buscar_por_unidade_ingrediente(
            db,
            unidade_id,
            ingrediente_id
        )

        if not estoque:
            raise Exception("Estoque não encontrado")

        if estoque.quantidade < quantidade:
            raise Exception("Estoque insuficiente")

        estoque.quantidade -= quantidade
        db.flush()

        return estoque

    def repor_estoque(
        self,
        db: Session,
        unidade_id: int,
        ingrediente_id: int,
        quantidade: float
    ):
        estoque = self.buscar_por_unidade_ingrediente(
            db,
            unidade_id,
            ingrediente_id
        )

        if not estoque:
            raise Exception("Estoque não encontrado")

        estoque.quantidade += quantidade
        db.flush()

        return estoque