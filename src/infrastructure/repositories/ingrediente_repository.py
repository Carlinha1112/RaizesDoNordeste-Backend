from sqlalchemy.orm import Session
from src.domain.entities.ingrediente import Ingrediente


class IngredienteRepository:

    def criar(self, db: Session, ingrediente: Ingrediente):
        db.add(ingrediente)
        db.commit()
        db.refresh(ingrediente)
        return ingrediente

    def buscar_por_id(self, db: Session, ingrediente_id: int):
        return db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    
    def buscar_por_nome(self, db: Session, nome: str):
        return db.query(Ingrediente).filter(Ingrediente.nome == nome).first()

    def listar(self, db: Session):
        return db.query(Ingrediente).all()

