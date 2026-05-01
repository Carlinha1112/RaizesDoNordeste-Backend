from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal
from src.domain.entities.fidelidade import Fidelidade
from src.domain.enums.fidelidade_enum import (
    TipoMovimento,
    Origem
)



class FidelidadeService:

    PONTOS_POR_REAL = Decimal("1")
    VALOR_POR_PONTO = Decimal("0.10")
    LIMITE_DESCONTO = Decimal("0.70")

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
        valor_pedido: float,
        pedido_id: int | None = None
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
            origem=Origem.PEDIDO,
            pedido_id=pedido_id
        )

        return fidelidade

    def debitar_pontos(self, db, usuario_id: int, pontos: int):
        fidelidade = self.buscar_ou_criar(db, usuario_id)

        if fidelidade.saldo_pontos < pontos:
            raise HTTPException(400, "Pontos insuficientes")

        fidelidade.saldo_pontos -= pontos

        self.historico_repository.registrar(
            db=db,
            fidelidade_id=fidelidade.id,
            usuario_id=usuario_id,
            pontos=pontos,
            tipo=TipoMovimento.DEBITO,
            origem=Origem.AJUSTE
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
    
    def calcular_desconto(self, valor_pedido: float, pontos_disponiveis: int):

        valor_pedido = Decimal(str(valor_pedido))
        pontos_disponiveis = Decimal(pontos_disponiveis)

        desconto_teorico = pontos_disponiveis * self.VALOR_POR_PONTO

        limite = valor_pedido * self.LIMITE_DESCONTO

        desconto_aplicado = min(desconto_teorico, limite)

        pontos_usados = int(desconto_aplicado / self.VALOR_POR_PONTO)

        return float(desconto_aplicado), pontos_usados
    
    def aplicar_fidelidade_pedido(
        self,
        db: Session,
        usuario_id: int,
        pedido_id: int,
        valor_pedido: float,
        pontos_solicitados: int
    ):
        fidelidade = self.buscar_ou_criar(db, usuario_id)

        if pontos_solicitados <= 0:
            return 0, 0

        desconto, pontos_usados = self.calcular_desconto(
            valor_pedido,
            min(pontos_solicitados, fidelidade.saldo_pontos)
        )

        if pontos_usados > 0:
            self.debitar_pontos(
                db=db,
                usuario_id=usuario_id,
                pontos=pontos_usados
            )

            self.historico_repository.registrar(
                db=db,
                fidelidade_id=fidelidade.id,
                usuario_id=usuario_id,
                pontos=pontos_usados,
                tipo=TipoMovimento.DEBITO,
                origem=Origem.PEDIDO,
                pedido_id=pedido_id
            )

        return desconto, pontos_usados  