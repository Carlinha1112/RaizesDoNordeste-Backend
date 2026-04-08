from sqlalchemy.orm import Session

from src.infrastructure.repositories.produto_repository import ProdutoRepository
from src.infrastructure.repositories.produto_ingrediente_repository import ProdutoIngredienteRepository
from src.infrastructure.repositories.ingrediente_repository import IngredienteRepository

from src.domain.entities.produto import Produto
from src.domain.entities.produto_ingrediente import ProdutoIngrediente

from src.api.schemas.produto_schema import ProdutoCreate


class ProdutoService:
    def __init__(
        self,
        produto_repository: ProdutoRepository,
        produto_ingrediente_repository: ProdutoIngredienteRepository,
        ingrediente_repository: IngredienteRepository
    ):
        self.produto_repository = produto_repository
        self.produto_ingrediente_repository = produto_ingrediente_repository
        self.ingrediente_repository = ingrediente_repository


    def criar_produto(self, db: Session, produto_data: ProdutoCreate):
        try:
            produto = Produto(
                nome=produto_data.nome,
                descricao=produto_data.descricao
            )
            produto_salvo = self.produto_repository.criar(db, produto)
            for item in produto_data.ingredientes:

                ingrediente = self.ingrediente_repository.buscar_por_id(
                    db,
                    item.ingrediente_id
                )
                if not ingrediente:
                    raise Exception(f"Ingrediente {item.ingrediente_id} não existe")
                relacao = ProdutoIngrediente(
                    id_produto=produto_salvo.id,
                    id_ingrediente=item.ingrediente_id,
                    quantidade_necessaria=item.quantidade
                )
                self.produto_ingrediente_repository.criar(db, relacao)
            db.commit()
            return produto_salvo
        except Exception:
            db.rollback()
            raise


    def buscar_produto(self, db: Session, produto_id: int):
        return self.produto_repository.buscar_por_id(db, produto_id)


    def listar_produtos(self, db: Session):
        return self.produto_repository.listar(db)


    def listar_produtos_ativos(self, db: Session):
        return self.produto_repository.listar_ativos(db)


    def desativar_produto(self, db: Session, produto_id: int):
        produto = self.produto_repository.buscar_por_id(db, produto_id)
        if not produto:
            raise Exception("Produto não encontrado")

        return self.produto_repository.desativar(db, produto)