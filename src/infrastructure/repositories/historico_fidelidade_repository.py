from sqlalchemy.orm import Session

from src.domain.entities.historico_fidelidade import (
    HistoricoFidelidade,
    TipoMovimento,
    Origem
)


class HistoricoFidelidadeRepository:

    def registrar(
        self,
        db: Session,
        fidelidade_id: int,
        usuario_id: int,
        pontos: int,
        tipo: TipoMovimento,
        origem: Origem,
        pedido_id: int | None = None
    ):
        historico = HistoricoFidelidade(
            id_fidelidade=fidelidade_id,
            id_usuario=usuario_id,
            id_pedido=pedido_id,
            pontos=pontos,
            tipo_movimento=tipo,
            origem=origem
        )

        db.add(historico)
        db.flush()

        return historico

    def listar_por_usuario(
        self,
        db: Session,
        usuario_id: int
    ):
        return db.query(
            HistoricoFidelidade
        ).filter(
            HistoricoFidelidade.id_usuario == usuario_id
        ).all()