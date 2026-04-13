from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean, DateTime, Enum
from src.infrastructure.database.database import Base
from datetime import datetime, timezone 
from sqlalchemy.orm import relationship
import enum
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PerfilUsuario(enum.Enum):
    GERENTE = "GERENTE"
    ATENDENTE = "ATENDENTE"
    CLIENTE = "CLIENTE"

class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    data_nasc = Column(Date, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    perfil = Column(Enum(PerfilUsuario), nullable=False)
    id_unidade = Column(Integer, ForeignKey("unidade.id"), nullable=True)
    data_cadastro = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ativo = Column(Boolean, default=True)

    unidade = relationship("Unidade")  

    def hash_password(self, senha: str) -> str:
        return pwd_context.hash(senha)
    def verify_password(self, senha: str) -> bool:  
        return pwd_context.verify(senha, self.senha_hash)