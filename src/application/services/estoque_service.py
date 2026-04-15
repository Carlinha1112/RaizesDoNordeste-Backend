from sqlalchemy.orm import Session
from src.infrastructure.repositories.estoque_repository import EstoqueRepository
from fastapi import HTTPException


class EstoqueService:
    def __init__(self, estoque_repository: EstoqueRepository):
        self.estoque_repository = estoque_repository

    def verificar_estoque(
        self,
        db: Session,
        ingrediente_id: int,
        quantidade_necessaria: float
    ) -> bool:
        return self.estoque_repository.tem_estoque(
            db,
            ingrediente_id,
            quantidade_necessaria
        )

    def debitar_estoque(
        self,
        db: Session,
        ingrediente_id: int,
        quantidade: float
    ):
        if not self.estoque_repository.tem_estoque(db, ingrediente_id, quantidade):
            raise HTTPException(status_code=400, detail="Estoque insuficiente")

        return self.estoque_repository.debitar_estoque(
            db,
            ingrediente_id,
            quantidade
        )

    def repor_estoque(
        self,
        db: Session,
        ingrediente_id: int,
        quantidade: float
    ):
        return self.estoque_repository.repor_estoque(
            db,
            ingrediente_id,
            quantidade
        )