from sqlalchemy.orm import Session
from src.infrastructure.repositories.pedido_repository import PedidoRepository
from src.infrastructure.repositories.produto_repository import ProdutoRepository
from src.domain.entities.produto import Produto

class ProdutoService:

    def __init__(self):
        self.repository = ProdutoRepository()
        self.pedido_repository = PedidoRepository()


    def criar_produto(self, db: Session, produto: Produto):
        return self.repository.criar(db, produto)


    def buscar_produto(self, db: Session, produto_id: int):
        return self.repository.buscar_por_id(db, produto_id)


    def listar_produtos(self, db: Session):
        return self.repository.listar(db)
    
    
    def listar_produtos_por_unidade(self, db: Session, unidade_id: int):
        return self.repository.buscar_por_unidade(db, unidade_id)