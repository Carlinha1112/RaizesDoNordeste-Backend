from sqlalchemy.orm import Session
from src.domain.entities.movimento_estoque import MovimentoEstoque
from src.domain.entities.movimento_estoque import TipoMovimento


class MovimentoRepository:

    def listar(
        self,
        db: Session,
        unidade_id=None,
        data_inicio=None,
        data_fim=None,
        tipo=None
    ):
        query = db.query(MovimentoEstoque)

        if unidade_id is not None:
            query = query.filter(MovimentoEstoque.id_unidade == unidade_id)

        if tipo is not None:
            query = query.filter(
            MovimentoEstoque.tipo == TipoMovimento(tipo)
            )

        if data_inicio is not None:
            query = query.filter(MovimentoEstoque.data_hora >= data_inicio)

        if data_fim is not None:
            query = query.filter(MovimentoEstoque.data_hora <= data_fim)

        return query.order_by(MovimentoEstoque.data_hora.desc()).all()