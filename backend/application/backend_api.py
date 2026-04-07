from backend.application.use_cases.rabito_cases import create_rabito, delete_rabito, get_rabito, feed_rabito, play_with_rabito, ver_dato_rabito, simular_horas
from backend.domain.core.homeostasis.autonomous_system import AutonomousSystem
from backend.infrastructure.repositories.models.rabito import RabitoRepository

class BackendAPI:
    def __init__(self, rabito_repo: RabitoRepository):
        self.rabito_repo = rabito_repo

    def create_rabito(self, user_id: int, name: str):
        return create_rabito(self.rabito_repo, user_id, name)

    def delete_rabito(self, rabito_id: int, user_id: int):
        return delete_rabito(self.rabito_repo, rabito_id, user_id)

    def get_rabito(self, user_id: int):
        return get_rabito(self.rabito_repo, user_id)

    def feed_rabito(self, user_id: int, amount: float = 0.2):
        return feed_rabito(self.rabito_repo, user_id, amount)

    def play_with_rabito(self, user_id: int):
        return play_with_rabito(self.rabito_repo, user_id)
    
    def ver_dato_rabito(self, user_id: int):
        return ver_dato_rabito(self.rabito_repo, user_id)
    
    def simular_horas(self, user_id: int, horas: float):
        return simular_horas(self.rabito_repo, user_id, horas, AutonomousSystem())
    

