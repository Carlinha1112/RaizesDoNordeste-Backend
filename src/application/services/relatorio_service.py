from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from src.domain.entities.usuario import PerfilUsuario


class RelatorioService:

    def __init__(
        self,
        movimento_repository,
        historico_pedido_repository,
        fidelidade_repository,
        historico_fidelidade_repository
    ):
        self.movimento_repository = movimento_repository
        self.historico_pedido_repository = historico_pedido_repository
        self.fidelidade_repository = fidelidade_repository
        self.historico_fidelidade_repository = historico_fidelidade_repository

    def _validar_gerente(self, usuario):
        if usuario.perfil != PerfilUsuario.GERENTE:
            raise HTTPException(403, "Acesso restrito ao gerente")

    def relatorio_estoque(
        self,
        db: Session,
        usuario,
        unidade_id: int | None = None,
        data_inicio: datetime | None = None,
        data_fim: datetime | None = None,
        tipo: str | None = None
    ):
        self._validar_gerente(usuario)

        movimentos = self.movimento_repository.listar(
            db=db,
            unidade_id=unidade_id,
            data_inicio=data_inicio,
            data_fim=data_fim,
            tipo=tipo
        )

        return [
            {
                "id": m.id,
                "unidade_id": m.id_unidade,
                "ingrediente_id": m.estoque.id_ingrediente,
                "tipo": m.tipo.value,
                "quantidade": m.quantidade,
                "motivo": m.motivo.value if m.motivo else None,
                "data": m.data_hora
            }
            for m in movimentos
        ]

    def relatorio_pedidos(
        self,
        db: Session,
        usuario,
        pedido_id: int | None = None,
        data_inicio: datetime | None = None,
        data_fim: datetime | None = None
    ):
        self._validar_gerente(usuario)

        historicos = self.historico_pedido_repository.listar(
            db=db,
            pedido_id=pedido_id,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        return [
            {
                "pedido_id": h.id_pedido,
                "status_anterior": h.status_anterior,
                "status_novo": h.status_novo,
                "data": h.data_hora
            }
            for h in historicos
        ]

    def relatorio_fidelidade_usuario(
        self,
        db,
        usuario_logado,
        usuario_id: int
    ):
        if (
            usuario_logado.id != usuario_id
            and usuario_logado.perfil != PerfilUsuario.GERENTE
        ):
            raise HTTPException(403, "Sem permissão")

        historicos = self.historico_fidelidade_repository.listar_por_usuario(
            db=db,
            usuario_id=usuario_id
        )

        historicos.sort(key=lambda h: h.data_hora)

        saldo = 0
        extrato = []

        for h in historicos:
            credito = 0
            debito = 0

            if h.tipo_movimento.value == "CREDITO":
                credito = h.pontos
                saldo += h.pontos
            else:
                debito = h.pontos
                saldo -= h.pontos

            extrato.append({
                "data": h.data_hora,
                "origem": h.origem.value,
                "pedido_id": h.id_pedido,
                "credito": credito,
                "debito": debito,
                "saldo": saldo
            })

        fidelidade = self.fidelidade_repository.buscar_por_usuario(
            db,
            usuario_id
        )

        return {
            "usuario_id": usuario_id,
            "data_cadastro": fidelidade.data_cadastro,
            "saldo_atual": fidelidade.saldo_pontos,
            "extrato": extrato
        }