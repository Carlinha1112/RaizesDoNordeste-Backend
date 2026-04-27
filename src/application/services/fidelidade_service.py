from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.domain.entities.fidelidade import Fidelidade
from src.domain.entities.historico_fidelidade import (
    TipoMovimento,
    Origem
)



class FidelidadeService:

    PONTOS_POR_REAL = 1
    VALOR_POR_PONTO = 0.10
    LIMITE_DESCONTO = 0.70

    def __init__(self, fidelidade_repository, historico_repository):
        self.fidelidade_repository = fidelidade_repository
        self.historico_repository = historico_repository

    def buscar_ou_criar(
        self,
        db: Session,
        usuario_id: int
    ):
        fidelidade = self.fidelidade_repository.buscar_por_usuario(
            db,
            usuario_id
        )

        if fidelidade:
            return fidelidade

        nova = Fidelidade(
            id_usuario=usuario_id,
            saldo_pontos=0
        )

        return self.fidelidade_repository.criar(db, nova)

    def adicionar_pontos(
        self,
        db: Session,
        usuario_id: int,
        valor_pedido: float
    ):
        fidelidade = self.buscar_ou_criar(
            db,
            usuario_id
        )

        pontos = int(valor_pedido * self.PONTOS_POR_REAL)

        fidelidade.saldo_pontos += pontos

        self.historico_repository.registrar(
            db=db,
            fidelidade_id=fidelidade.id,
            usuario_id=usuario_id,
            pontos=pontos,
            tipo=TipoMovimento.CREDITO,
            origem=Origem.PEDIDO
        )

        return fidelidade

    def debitar_pontos(
        self,
        db: Session,
        usuario_id: int,
        pontos: int
    ):
        fidelidade = self.buscar_ou_criar(
            db,
            usuario_id
        )

        if fidelidade.saldo_pontos < pontos:
            raise HTTPException(
                400,
                "Pontos insuficientes"
            )

        fidelidade.saldo_pontos -= pontos

        self.historico_repository.registrar(
            db=db,
            fidelidade_id=fidelidade.id,
            usuario_id=usuario_id,
            pontos=pontos,
            tipo=TipoMovimento.DEBITO,
            origem=Origem.CONVERSAO_PONTOS
        )

        return fidelidade

    def consultar_pontos(
        self,
        db: Session,
        usuario_id: int
    ):
        fidelidade = self.buscar_ou_criar(
            db,
            usuario_id
        )

        return fidelidade.saldo_pontos