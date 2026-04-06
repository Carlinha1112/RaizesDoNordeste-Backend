from sqlalchemy.orm import Session
from src.domain.entities.produto import Produto

class ProdutoRepository:

    def criar(self, db: Session, produto: Produto):
        db.add(produto)
        db.commit()
        db.refresh(produto)
        return produto

    def buscar_por_id(self, db: Session, produto_id: int):
        return db.query(Produto).filter(Produto.id == produto_id).first()

    def listar(self, db: Session):
        return db.query(Produto).all()

    def listar_ativos(self, db: Session):
        return db.query(Produto).filter(Produto.ativo == True).all()
    
    def desativar(self, db: Session, produto: Produto):
        produto.ativo = False
        db.commit()
        db.refresh(produto)
        return produto