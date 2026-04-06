from sqlalchemy.orm import Session
from src.domain.entities.unidade import Unidade


class UnidadeRepository:

    def criar(self, db: Session, unidade: Unidade):
        db.add(unidade)
        db.commit()
        db.refresh(unidade)
        return unidade

    def buscar_por_id(self, db: Session, unidade_id: int):
        return db.query(Unidade).filter(Unidade.id == unidade_id).first()

    def listar(self, db: Session):
        return db.query(Unidade).all()
    
    def listar_ativos(self, db: Session):
        return db.query(Unidade).filter(Unidade.ativo == True).all()

    def ativar(self, db: Session, unidade: Unidade):
        unidade.ativo = True
        db.commit()
        db.refresh(unidade)
        return unidade
    
    def desativar(self, db: Session, unidade: Unidade):
        unidade.ativo = False
        db.commit()
        db.refresh(unidade)
        return unidade