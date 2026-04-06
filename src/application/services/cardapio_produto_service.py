from sqlalchemy.orm import Session

from src.infrastructure.repositories.cardapio_produto_repository import CardapioProdutoRepository
from src.domain.entities.cardapio_produto import CardapioProduto

from src.api.schemas.cardapio_produto_schema import (
    CardapioProdutoCreate,
    CardapioProdutoUpdate
)


class CardapioProdutoService:

    def __init__(self, repository: CardapioProdutoRepository):
        self.repository = repository


    def adicionar_produto(
        self,
        db: Session,
        cardapio_id: int,
        dados: CardapioProdutoCreate
    ):
        item = CardapioProduto(
            id_cardapio=cardapio_id,
            id_produto=dados.id_produto,
            preco_venda=dados.preco_venda,
            ativo_no_cardapio=True
        )
        return self.repository.adicionar_produto(db, item)


    def listar_produtos(self, db: Session, cardapio_id: int):
        return self.repository.listar_por_cardapio(db, cardapio_id)


    def atualizar_produto(
        self,
        db: Session,
        cardapio_id: int,
        produto_id: int,
        dados: CardapioProdutoUpdate
    ):
        item = self.repository.buscar(db, cardapio_id, produto_id)
        if not item:
            raise Exception("Produto não encontrado no cardápio")
        item.preco_venda = dados.preco_venda
        item.ativo_no_cardapio = dados.ativo_no_cardapio
        return self.repository.atualizar(db, item)