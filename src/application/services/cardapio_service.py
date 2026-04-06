from sqlalchemy.orm import Session
from datetime import date

from src.infrastructure.repositories.cardapio_repository import CardapioRepository
from src.domain.entities.cardapio import Cardapio
from src.api.schemas.cardapio_schema import CardapioCreate


class CardapioService:

    def __init__(self, cardapio_repository: CardapioRepository):
        self.repository = cardapio_repository


    def criar_cardapio(self, db: Session, dados: CardapioCreate):
        cardapio = Cardapio(
            id_unidade=dados.id_unidade,
            data_inicio=dados.data_inicio,
            data_fim=dados.data_fim
        )
        return self.repository.criar(db, cardapio)


    def buscar_cardapio(self, db: Session, cardapio_id: int):
        return self.repository.buscar_por_id(db, cardapio_id)


    def listar_cardapios(self, db: Session):
        return self.repository.listar(db)


    def listar_cardapios_ativos(self, db: Session):
        hoje = date.today()
        return self.repository.listar_ativos(db, hoje)  