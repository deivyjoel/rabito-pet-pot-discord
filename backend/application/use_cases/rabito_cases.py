from backend.application.results.operation_result import OperationResult
from backend.application.decorators.usecase_guard import handle_usecase_errors
#from backend.application.utils.simulation_time import _update_time
from backend.infrastructure.repositories.models.rabito import RabitoRepository
from backend.domain.core.homeostasis.autonomous_system import AutonomousSystem

# --- OPERATIONS ---
@handle_usecase_errors
def create_rabito(
    rabito_repo: RabitoRepository, 
    user_id: int, 
    name: str) -> OperationResult[int]:
    rabito_id = rabito_repo.create(user_id, name)
    return OperationResult(True, "Rabito creado correctamente", rabito_id)


@handle_usecase_errors
def delete_rabito(
    rabito_repo: RabitoRepository, 
    rabito_id: int, 
    user_id: int) -> OperationResult[None]:  
    rabito_repo.delete(rabito_id, user_id)
    return OperationResult(True, "Rabito eliminado correctamente", None)

@handle_usecase_errors
def get_rabito(
    rabito_repo: RabitoRepository, 
    user_id: int
    ) -> OperationResult:
    rabito = rabito_repo.get_by_user_id(user_id)
    if not rabito:
        return OperationResult(False, "No se encontró un Rabito para este usuario", None)
    return OperationResult(True, "Rabito obtenido correctamente", rabito)


@handle_usecase_errors
def feed_rabito(
    rabito_repo: RabitoRepository,
    user_id: int,
    amount: float = 0.2
) -> OperationResult[float]:

    rabito = rabito_repo.get_by_user_id(user_id)
    if not rabito:
        return OperationResult(False, "No se encontró un Rabito para este usuario", None)
    _update_time(rabito)
    rabito.feed(amount)
    rabito_repo.save_state(rabito)
    rabito_repo.add_event(rabito.id, "feed", amount)
    return OperationResult(True, "Rabito alimentado correctamente", 1.5)


@handle_usecase_errors
def play_with_rabito(
    rabito_repo: RabitoRepository,
    user_id: int,
) -> OperationResult[float]:

    rabito = rabito_repo.get_by_user_id(user_id)
    if not rabito:
        return OperationResult(False, "No se encontró un Rabito para este usuario", None)
    _update_time(rabito)
    rabito.play()
    rabito_repo.save_state(rabito)
    rabito_repo.add_event(rabito.id, "play", 0.1)
    return OperationResult(True, "Rabito jugó correctamente", 1.5)


@handle_usecase_errors
def interact_with_rabito(
    rabito_repo: RabitoRepository,
    user_id: int,
) -> OperationResult[float]:

    rabito = rabito_repo.get_by_user_id(user_id)
    if not rabito:
        return OperationResult(False, "No se encontró un Rabito para este usuario", None)
    _update_time(rabito)
    rabito.interact()
    rabito_repo.save_state(rabito)
    rabito_repo.add_event(rabito.id, "interact", 0.1)
    return OperationResult(True, "Rabito interactuó correctamente", 1.5)

@handle_usecase_errors
def ver_dato_rabito(
    rabito_repo: RabitoRepository,
    user_id: int,
):

    rabito = rabito_repo.get_by_user_id(user_id)
    """
    if not rabito:
        return OperationResult(False, "No se encontró un Rabito para este usuario", None)
    """
    if not rabito:
        return
    return {
        "energy": round(rabito.energy, 3),
        "fatigue": round(rabito.fatigue, 3),
        "stimulation": round(rabito.stimulation, 3),
        "bond": round(rabito.bond, 3),
        "reserve": round(rabito.reserve, 3)
    }

@handle_usecase_errors
def simular_horas(
    rabito_repo: RabitoRepository,
    user_id: int,
    horas: float,
    system_autonomus: AutonomousSystem
) -> OperationResult[float]:

    rabito = rabito_repo.get_by_user_id(user_id)
    if not rabito:
        return OperationResult(False, "No se encontró un Rabito para este usuario", None)
    system_autonomus.simulate(rabito, horas)
    rabito_repo.save_state(rabito)
    return OperationResult(True, f"Simulación de {horas} horas aplicada correctamente", 1.5)





