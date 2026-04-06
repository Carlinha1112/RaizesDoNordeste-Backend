from sqlalchemy.orm import Session
from src.domain.entities.cardapio_produto import CardapioProduto


class CardapioProdutoRepository:

    def adicionar_produto(self, db: Session, item: CardapioProduto):
        db.add(item)
        db.commit()
        db.refresh(item)
        return item


    def buscar(self, db: Session, cardapio_id: int, produto_id: int):
        return (
            db.query(CardapioProduto)
            .filter(
                CardapioProduto.id_cardapio == cardapio_id,
                CardapioProduto.id_produto == produto_id
            )
            .first()
        )


    def listar_por_cardapio(self, db: Session, cardapio_id: int):
        return (
            db.query(CardapioProduto)
            .filter(CardapioProduto.id_cardapio == cardapio_id)
            .all()
        )


    def atualizar(self, db: Session, item: CardapioProduto):
        db.commit()
        db.refresh(item)
        return item