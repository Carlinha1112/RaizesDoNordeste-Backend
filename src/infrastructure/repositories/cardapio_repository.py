from sqlalchemy.orm import Session
from src.domain.entities.cardapio import Cardapio
from datetime import date


class CardapioRepository:

    def criar(self, db: Session, cardapio: Cardapio):
        db.add(cardapio)
        db.commit()
        db.refresh(cardapio)
        return cardapio

    def buscar_por_id(self, db: Session, cardapio_id: int):
        return db.query(Cardapio).filter(Cardapio.id == cardapio_id).first()

    def buscar_por_unidade(self, db: Session, unidade_id: int):
        return db.query(Cardapio).filter(Cardapio.id_unidade == unidade_id).first()
    
    def buscar_cardapio_ativo(self, db: Session, unidade_id: int, data: date):
        return (
            db.query(Cardapio)
            .filter(
                Cardapio.id_unidade == unidade_id,
                Cardapio.data_inicio <= data,
                Cardapio.data_fim >= data
            )
            .first()
        )
    
    def listar(self, db: Session):
        return db.query(Cardapio).all()