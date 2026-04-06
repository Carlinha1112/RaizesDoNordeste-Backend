from sqlalchemy.orm import Session
from src.infrastructure.repositories.unidade_repository import UnidadeRepository
from src.domain.entities.unidade import Unidade
from src.api.schemas.unidade_schema import UnidadeCreate


class UnidadeService:

    def __init__(self, unidade_repository: UnidadeRepository):
        self.unidade_repository = unidade_repository


    def criar_unidade(self, db: Session, unidade_data: UnidadeCreate):
        unidade = Unidade(
            nome=unidade_data.nome,
            cidade=unidade_data.cidade,
            estado=unidade_data.estado,
            ativo=True
        )

        return self.unidade_repository.criar(db, unidade)


    def buscar_unidade(self, db: Session, unidade_id: int):
        return self.unidade_repository.buscar_por_id(db, unidade_id)


    def listar_unidades(self, db: Session):
        return self.unidade_repository.listar(db)


    def listar_unidades_ativas(self, db: Session):
        return self.unidade_repository.listar_ativos(db)


    def desativar_unidade(self, db: Session, unidade_id: int):

        unidade = self.unidade_repository.buscar_por_id(db, unidade_id)

        if not unidade:
            raise Exception("Unidade não encontrada")

        return self.unidade_repository.desativar(db, unidade)