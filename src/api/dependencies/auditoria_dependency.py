from src.application.services.auditoria_service import AuditoriaService
from src.infrastructure.repositories.auditoria_repository import AuditoriaRepository


def get_auditoria_service():
    return AuditoriaService(
        AuditoriaRepository()
    )