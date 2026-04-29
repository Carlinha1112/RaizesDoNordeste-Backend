from sqlalchemy.orm import Session
from fastapi import HTTPException
from decimal import Decimal

from src.domain.entities.estoque import Estoque
from src.domain.entities.usuario import PerfilUsuario

from src.infrastructure.repositories.estoque_repository import (
    EstoqueRepository
)


class EstoqueService:

    def __init__(self):
        self.repository = EstoqueRepository()

    def criar_ou_repor(
        self,
        db: Session,
        dados,
        usuario
    ):
        try:
            self._validar_permissao(usuario)

            item = self.repository.buscar_por_unidade_ingrediente(
                db,
                dados.id_unidade,
                dados.id_ingrediente
            )

            if item:
                item.quantidade += dados.quantidade
            else:
                item = Estoque(
                    id_unidade=dados.id_unidade,
                    id_ingrediente=dados.id_ingrediente,
                    quantidade=dados.quantidade
                )
                self.repository.criar(db, item)

            db.commit()
            db.refresh(item)

            return item

        except:
            db.rollback()
            raise

    def listar(self, db: Session):
        return self.repository.listar(db)

    def listar_por_unidade(
        self,
        db: Session,
        unidade_id: int
    ):
        return self.repository.listar_por_unidade(
            db,
            unidade_id
        )

    def entrada(
        self,
        db: Session,
        estoque_id: int,
        quantidade,
        usuario
    ):
        try:
            self._validar_permissao(usuario)

            item = self._buscar_item(db, estoque_id)

            item.quantidade += quantidade

            db.commit()
            db.refresh(item)

            return item

        except:
            db.rollback()
            raise

    def saida(
        self,
        db: Session,
        estoque_id: int,
        quantidade,
        usuario
    ):
        try:
            self._validar_permissao(usuario)

            item = self._buscar_item(db, estoque_id)

            if item.quantidade < quantidade:
                raise HTTPException(
                    400,
                    "Estoque insuficiente"
                )

            item.quantidade -= quantidade

            db.commit()
            db.refresh(item)

            return item

        except:
            db.rollback()
            raise

    def ajustar(
        self,
        db: Session,
        estoque_id: int,
        quantidade,
        usuario
    ):
        try:
            self._validar_permissao(usuario)

            item = self._buscar_item(db, estoque_id)

            item.quantidade = quantidade

            db.commit()
            db.refresh(item)

            return item

        except:
            db.rollback()
            raise

    def excluir(
        self,
        db: Session,
        estoque_id: int,
        usuario
    ):
        try:
            if usuario.perfil != PerfilUsuario.GERENTE:
                raise HTTPException(
                    403,
                    "Sem permissão"
                )

            item = self._buscar_item(db, estoque_id)

            db.delete(item)
            db.commit()

        except:
            db.rollback()
            raise

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
                    composicao.ingrediente_id,   # ou nome correto do campo
                    quantidade_total
                )
    
    def debitar_por_pedido( 
        self, 
        db: Session, 
        unidade_id: int, 
        ingrediente_id: int, 
        quantidade
    ): 
        item = self.repository.buscar_por_unidade_ingrediente( 
            db, 
            unidade_id, 
            ingrediente_id 
        ) 
        if not item: 
            raise HTTPException( 
                404, 
                "Ingrediente sem estoque" 
            ) 
        quantidade = Decimal(str(quantidade))
        if item.quantidade < quantidade: 
            raise HTTPException( 
                400, 
                "Estoque insuficiente" 
            ) 
        item.quantidade -= quantidade 
        db.flush() 

    def _buscar_item(self, db, estoque_id):
        item = self.repository.buscar_por_id(
            db,
            estoque_id
        )

        if not item:
            raise HTTPException(
                404,
                "Item não encontrado"
            )

        return item

    def _validar_permissao(self, usuario):
        if usuario.perfil not in [
            PerfilUsuario.GERENTE,
            PerfilUsuario.ATENDENTE
        ]:
            raise HTTPException(
                403,
                "Sem permissão"
            )