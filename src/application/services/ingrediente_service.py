from sqlalchemy.orm import Session
from src.infrastructure.repositories.ingrediente_repository import IngredienteRepository
from src.domain.entities.ingrediente import Ingrediente


class IngredienteService:

    def __init__(self, repository: IngredienteRepository):
        self.repository = repository


    def criar_ingrediente(self, db: Session, data):
        ingrediente = Ingrediente(
            nome=data.nome,
            unidade_medida=data.unidade_medida
        )
        return self.repository.criar(db, ingrediente)


    def listar_ingredientes(self, db: Session):
        return self.repository.listar(db)


    def buscar_ingrediente(self, db: Session, ingrediente_id: int):
        return self.repository.buscar_por_id(db, ingrediente_id)