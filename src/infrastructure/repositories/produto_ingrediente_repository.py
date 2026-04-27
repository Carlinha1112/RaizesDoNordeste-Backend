from sqlalchemy.orm import Session
from src.domain.entities.produto_ingrediente import ProdutoIngrediente


class ProdutoIngredienteRepository:

    def criar(self, db: Session, entity: ProdutoIngrediente):
        db.add(entity)
        db.flush()
        return entity

    def listar_por_produto(self, db: Session, produto_id: int):
        return db.query(ProdutoIngrediente).filter(
            ProdutoIngrediente.produto_id == produto_id
        ).all()

    def buscar(self, db: Session, produto_id: int, ingrediente_id: int):
        return db.query(ProdutoIngrediente).filter(
            ProdutoIngrediente.produto_id == produto_id,
            ProdutoIngrediente.ingrediente_id == ingrediente_id
        ).first()

    def remover_por_produto(self, db: Session, produto_id: int):
        db.query(ProdutoIngrediente).filter(
            ProdutoIngrediente.produto_id == produto_id
        ).delete(synchronize_session=False)

        db.flush()

    def atualizar_quantidade(
        self,
        db: Session,
        produto_id: int,
        ingrediente_id: int,
        nova_quantidade: float
    ):
        relacao = self.buscar(db, produto_id, ingrediente_id)

        if relacao:
            relacao.quantidade = nova_quantidade
            db.flush()

        return relacao