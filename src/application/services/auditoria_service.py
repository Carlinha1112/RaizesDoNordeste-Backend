from src.domain.entities.auditoria import Auditoria


class AuditoriaService:

    def __init__(self, repository):
        self.repository = repository

    def registrar(
        self,
        db,
        usuario_id,
        acao,
        entidade,
        entidade_id=None,
        detalhes=None
    ):
        auditoria = Auditoria(
            usuario_id=usuario_id,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            detalhes=detalhes
        )

        self.repository.registrar(db, auditoria)