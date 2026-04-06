from sqlalchemy.orm import Session
from src.domain.entities.produto_ingrediente import ProdutoIngrediente


class ProdutoIngredienteRepository:

    def criar(self, db: Session, entity: ProdutoIngrediente):
        db.add(entity)
        db.flush()
        return entity


    def listar_por_produto(self, db: Session, produto_id: int):
        return db.query(ProdutoIngrediente).filter(
            ProdutoIngrediente.id_produto == produto_id
        ).all()


    def buscar(self, db: Session, produto_id: int, ingrediente_id: int):
        return db.query(ProdutoIngrediente).filter(
            ProdutoIngrediente.id_produto == produto_id,
            ProdutoIngrediente.id_ingrediente == ingrediente_id
        ).first()


    def remover_por_produto(self, db: Session, produto_id: int):
        db.query(ProdutoIngrediente).filter(
            ProdutoIngrediente.id_produto == produto_id
        ).delete()


    def atualizar_quantidade(
        self,
        db: Session,
        produto_id: int,
        ingrediente_id: int,
        nova_quantidade
    ):
        relacao = self.buscar(db, produto_id, ingrediente_id)
        if relacao:
            relacao.quantidade_necessaria = nova_quantidade
            db.flush()
        return relacao