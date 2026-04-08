from sqlalchemy.orm import Session
from src.domain.entities.historico_fidelidade import HistoricoFidelidade

class HistoricoFidelidadeRepository:

    def registrar(self, db: Session, usuario_id: int, pontos: int, tipo: str):
        historico = HistoricoFidelidade(
            id_usuario=usuario_id,
            pontos=pontos,
            tipo_movimento=tipo
        )
        db.add(historico)
        db.flush()
        return historico