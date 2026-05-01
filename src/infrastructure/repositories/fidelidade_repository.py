from sqlalchemy.orm import Session
from src.domain.entities.fidelidade import Fidelidade
from src.domain.entities.historico_fidelidade import HistoricoFidelidade

class FidelidadeRepository:

    def criar(self, db: Session, fidelidade: Fidelidade):
        db.add(fidelidade)
        db.flush()
        return fidelidade

    def buscar_por_id(self, db: Session, fidelidade_id: int):
        return db.query(Fidelidade).filter(
            Fidelidade.id == fidelidade_id
        ).first()

    def buscar_por_usuario(
        self,
        db: Session,
        usuario_id: int
    ):
        return db.query(Fidelidade).filter(
            Fidelidade.id_usuario == usuario_id
        ).first()

    def listar(self, db: Session):
        return db.query(Fidelidade).all()
    
    def listar_historico(
        self,
        db: Session,
        usuario_id=None,
        data_inicio=None,
        data_fim=None
    ):
        query = db.query(HistoricoFidelidade)

        if usuario_id is not None:
            query = query.filter(HistoricoFidelidade.usuario_id == usuario_id)

        if data_inicio is not None:
            query = query.filter(HistoricoFidelidade.data_hora >= data_inicio)

        if data_fim is not None:
            query = query.filter(HistoricoFidelidade.data_hora <= data_fim)

        return query.all()