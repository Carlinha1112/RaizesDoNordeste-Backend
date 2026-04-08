from sqlalchemy.orm import Session

class FidelidadeService:

    PONTOS_POR_REAL = 1
    VALOR_POR_PONTO = 0.25
    LIMITE_DESCONTO = 0.70

    def __init__(self, fidelidade_repository, historico_repository):
        self.fidelidade_repository = fidelidade_repository
        self.historico_repository = historico_repository

    def buscar_fidelidade_usuario(self, db: Session, usuario_id: int):
        return self.fidelidade_repository.buscar_por_usuario(db, usuario_id)

    def calcular_pontos_por_valor(self, valor_pedido: float) -> int:
        return int(valor_pedido * self.PONTOS_POR_REAL)

    def calcular_desconto_por_pontos(self, pontos: int) -> float:
        return pontos * self.VALOR_POR_PONTO

    def aplicar_limite_desconto(self, valor_pedido: float, desconto: float):
        limite = valor_pedido * self.LIMITE_DESCONTO
        return min(desconto, limite)

    def calcular_desconto(self, valor_pedido: float, pontos_usados: int):
        desconto = self.calcular_desconto_por_pontos(pontos_usados)
        return self.aplicar_limite_desconto(valor_pedido, desconto)

    def adicionar_pontos(self, db: Session, usuario_id: int, valor_pedido: float):
        fidelidade = self.fidelidade_repository.buscar_por_usuario(db, usuario_id)

        if not fidelidade:
            raise Exception("Conta de fidelidade não encontrada")

        pontos = self.calcular_pontos_por_valor(valor_pedido)

        fidelidade.saldo_pontos += pontos

        self.historico_repository.registrar(
            db=db,
            usuario_id=usuario_id,
            pontos=pontos,
            tipo="CREDITO"
        )

        return fidelidade

    def debitar_pontos(self, db: Session, usuario_id: int, pontos: int):
        fidelidade = self.fidelidade_repository.buscar_por_usuario(db, usuario_id)

        if not fidelidade:
            raise Exception("Conta de fidelidade não encontrada")

        if fidelidade.saldo_pontos < pontos:
            raise Exception("Pontos insuficientes")

        fidelidade.saldo_pontos -= pontos

        self.historico_repository.registrar(
            db=db,
            usuario_id=usuario_id,
            pontos=pontos,
            tipo="DEBITO"
        )

        return fidelidade

    def consultar_pontos(self, db: Session, usuario_id: int):
        fidelidade = self.fidelidade_repository.buscar_por_usuario(db, usuario_id)
        return fidelidade.saldo_pontos if fidelidade else 0