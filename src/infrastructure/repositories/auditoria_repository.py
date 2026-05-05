from src.domain.entities.auditoria import Auditoria

class AuditoriaRepository:

    def registrar(self, db, auditoria: Auditoria):
        db.add(auditoria)
        db.flush()
        return auditoria
    
    def listar(self, db):
        return db.query(Auditoria).all()