from sqlalchemy import Column, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base
from datetime import datetime, timezone
import enum


class TipoMovimento(enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class MotivoMovimento(enum.Enum):
    PEDIDO = "PEDIDO"
    AJUSTE = "AJUSTE"
    REPOSICAO = "REPOSICAO"


class MovimentoEstoque(Base):
    __tablename__ = "movimento_estoque"

    id = Column(Integer, primary_key=True, index=True)

    id_estoque = Column(Integer, ForeignKey("estoque.id"), nullable=False)
    id_usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    id_unidade = Column(Integer, ForeignKey("unidade.id"), nullable=False)

    tipo = Column(Enum(TipoMovimento), nullable=False)
    quantidade = Column(Integer, nullable=False)
    motivo = Column(Enum(MotivoMovimento), nullable=True)

    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    estoque = relationship("Estoque")
    usuario = relationship("Usuario")
    unidade = relationship("Unidade")