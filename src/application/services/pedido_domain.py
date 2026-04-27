from fastapi import HTTPException
from src.domain.enums.pedido_status import StatusPedido, StatusPreparo


class PedidoDomain:

    @staticmethod
    def pode_ser_pago(status: StatusPedido):
        return status == StatusPedido.AGUARDANDO_PAGAMENTO

    @staticmethod
    def marcar_como_pago(pedido):
        if pedido.status_pedido != StatusPedido.AGUARDANDO_PAGAMENTO:
            raise HTTPException(409, "Pedido não pode ser pago")

        pedido.status_pedido = StatusPedido.PAGO
        pedido.status_preparo = StatusPreparo.AGUARDANDO_PREPARO

    @staticmethod
    def iniciar_preparo(pedido):
        if pedido.status_pedido != StatusPedido.PAGO:
            raise HTTPException(409, "Pedido precisa estar pago")

        if pedido.status_preparo != StatusPreparo.AGUARDANDO_PREPARO:
            raise HTTPException(409, "Pedido não está aguardando preparo")

        pedido.status_preparo = StatusPreparo.EM_PREPARO

    @staticmethod
    def marcar_pronto(pedido):
        if pedido.status_preparo != StatusPreparo.EM_PREPARO:
            raise HTTPException(409, "Pedido não está em preparo")

        pedido.status_preparo = StatusPreparo.PRONTO

    @staticmethod
    def finalizar_pedido(pedido):
        if pedido.status_preparo != StatusPreparo.PRONTO:
            raise HTTPException(409, "Pedido não está pronto")

        pedido.status_preparo = StatusPreparo.FINALIZADO
        pedido.status_pedido = StatusPedido.FINALIZADO

    @staticmethod
    def cancelar(pedido):
        if pedido.status_pedido == StatusPedido.FINALIZADO:
            raise HTTPException(409, "Pedido já finalizado")

        pedido.status_pedido = StatusPedido.CANCELADO