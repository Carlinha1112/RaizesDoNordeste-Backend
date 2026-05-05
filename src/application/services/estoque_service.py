from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal

from src.domain.entities.estoque import Estoque
from src.domain.entities.usuario import PerfilUsuario
from src.domain.entities.usuario import Usuario
from src.domain.entities.movimento_estoque import (
    MovimentoEstoque,
    TipoMovimento,
    MotivoMovimento
)

from src.infrastructure.repositories.estoque_repository import (
    EstoqueRepository
)


class EstoqueService:

    def __init__(self, auditoria_service):
        self.repository = EstoqueRepository()
        self.auditoria_service = auditoria_service        

    def _validar_permissao(self, usuario):
        if usuario.perfil not in [
            PerfilUsuario.ATENDENTE,
            PerfilUsuario.GERENTE
        ]:
            raise HTTPException(
                status_code=403,
                detail="Sem permissão"
            )

    def criar(self, db: Session, dados, usuario):
        try:
            self._validar_permissao(usuario)

            item_existente = self.repository.buscar_por_unidade_ingrediente(
                db,
                dados.id_unidade,
                dados.id_ingrediente
            )

            if item_existente:
                raise HTTPException(400, "Item de estoque já existe")

            item = Estoque(
                id_unidade=dados.id_unidade,
                id_ingrediente=dados.id_ingrediente,
                quantidade=dados.quantidade
            )

            self.repository.criar(db, item)

            db.flush()

            self.auditoria_service.registrar(
                db=db,
                usuario_id=usuario.id,
                acao="CRIAR_ESTOQUE",
                entidade="Estoque",
                entidade_id=item.id,
                detalhes=f"Ingrediente {item.id_ingrediente} criado com {item.quantidade}"
        )

            db.commit()
            db.refresh(item)

            return item

        except:
            db.rollback()
            raise

    def listar(self, db: Session):
        return self.repository.listar(db)

    def listar_por_unidade(self, db: Session, unidade_id: int):
        return self.repository.listar_por_unidade(db, unidade_id)

    def entrada(self, db: Session, estoque_id: int, quantidade, usuario):
        try:
            self._validar_permissao(usuario)

            item = self._buscar_item(db, estoque_id)

            item.quantidade += quantidade

            self.auditoria_service.registrar(
                db=db,
                usuario_id=usuario.id,
                acao="ENTRADA_ESTOQUE",
                entidade="Estoque",
                entidade_id=item.id,
                detalhes=f"+{quantidade} unidades"
            )

            movimento = MovimentoEstoque(
                id_estoque=item.id,
                id_usuario=usuario.id,
                id_unidade=item.id_unidade,
                tipo=TipoMovimento.ENTRADA,
                quantidade=float(quantidade),
                motivo=MotivoMovimento.REPOSICAO    
            )

            db.add(movimento)

            db.commit()
            db.refresh(item)

            return item

        except:
            db.rollback()
            raise

    def saida(self, db: Session, estoque_id: int, quantidade, usuario):
        try:
            self._validar_permissao(usuario)

            item = self._buscar_item(db, estoque_id)

            if item.quantidade < quantidade:
                raise HTTPException(400, "Estoque insuficiente")

            item.quantidade -= quantidade

            self.auditoria_service.registrar(
                db=db,
                usuario_id=usuario.id,
                acao="SAIDA_ESTOQUE",
                entidade="Estoque",
                entidade_id=item.id,
                detalhes=f"-{quantidade} unidades"
        )

            movimento = MovimentoEstoque(
                id_estoque=item.id,
                id_usuario=usuario.id,
                id_unidade=item.id_unidade,
                tipo=TipoMovimento.SAIDA,
                quantidade=float(quantidade),
                motivo=MotivoMovimento.AJUSTE
            )

            db.add(movimento)

            db.commit()
            db.refresh(item)

            return item

        except:
            db.rollback()
            raise

    def ajustar(self, db: Session, estoque_id: int, quantidade, usuario):
        try:
            self._validar_permissao(usuario)

            item = self._buscar_item(db, estoque_id)

            quantidade_anterior = item.quantidade
            item.quantidade = quantidade

            self.auditoria_service.registrar(
                db=db,
                usuario_id=usuario.id,
                acao="AJUSTE_ESTOQUE",
                entidade="Estoque",
                entidade_id=item.id,
                detalhes=f"{quantidade_anterior} -> {quantidade}"
            )

            movimento = MovimentoEstoque(
                id_estoque=item.id,
                id_usuario=usuario.id,
                id_unidade=item.id_unidade,
                tipo=TipoMovimento.AJUSTE,
                quantidade=float(quantidade),
                motivo=MotivoMovimento.AJUSTE
            )

            db.add(movimento)

            db.commit()
            db.refresh(item)

            return item

        except:
            db.rollback()
            raise

    def excluir(self, db: Session, estoque_id: int, usuario):
        try:
            if usuario.perfil != PerfilUsuario.GERENTE:
                raise HTTPException(403, "Sem permissão")

            item = self._buscar_item(db, estoque_id)

            db.delete(item)
            db.commit()

        except:
            db.rollback()
            raise

    def buscar_estoque(self, db, id_unidade, ingrediente_id):
        return self.repository.buscar_por_unidade_ingrediente(
            db,
            id_unidade,
            ingrediente_id
        )

    def baixar_estoque_por_pedido(self, db, pedido):
        for item in pedido.itens:
            produto = item.produto

            for composicao in produto.ingredientes:
                quantidade_total = (
                    Decimal(str(composicao.quantidade))
                    * Decimal(str(item.quantidade))
                )

                self.debitar_por_pedido(
                    db,
                    pedido.id_unidade,
                    composicao.ingrediente_id,
                    quantidade_total
                )

    def debitar_por_pedido(self, db: Session, unidade_id: int, ingrediente_id: int, quantidade):
        item = self.repository.buscar_por_unidade_ingrediente(
            db,
            unidade_id,
            ingrediente_id
        )

        if not item:
            raise HTTPException(404, "Ingrediente sem estoque")

        quantidade = Decimal(str(quantidade))

        if item.quantidade < quantidade:
            raise HTTPException(400, "Estoque insuficiente")

        item.quantidade -= quantidade

        usuario_sistema = db.query(Usuario).filter(
            Usuario.email == "sistema@interno.com"
        ).first()

        if not usuario_sistema:
            raise HTTPException(500, "Usuário sistema não encontrado")  

        self.auditoria_service.registrar(
            db=db,
            usuario_id=usuario_sistema.id,
            acao="SAIDA_ESTOQUE_PEDIDO",
            entidade="Estoque",
            entidade_id=item.id,
            detalhes=f"-{quantidade} (pedido automático)"
        )

        movimento = MovimentoEstoque(
            id_estoque=item.id,
            id_usuario=usuario_sistema.id,
            id_unidade=unidade_id,
            tipo=TipoMovimento.SAIDA,
            quantidade=float(quantidade),
            motivo=MotivoMovimento.PEDIDO
        )

        db.add(movimento)

        db.flush()

    def _buscar_item(self, db, estoque_id):
        item = self.repository.buscar_por_id(db, estoque_id)

        if not item:
            raise HTTPException(404, "Item não encontrado")

        return item