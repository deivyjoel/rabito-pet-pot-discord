import asyncio
from backend.application.utils.simulation_time import _update_time
from backend.infrastructure.repositories.models.rabito import RabitoRepository
from application.autonomous.event_producer import EventProducer
from backend.domain.core.agent import OntologicalAgent

CHECK_INTERVAL_SECONDS = 1000
async def rabito_autonomy_loop():
    """
    Loop autónomo del sistema.
    - Simula tiempo
    - Ejecuta agente
    - Persite eventos
    """
    while True:
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)
        rabito_repo = RabitoRepository() # type: ignore
        agent = OntologicalAgent()
        producer = EventProducer(agent) 
        rabitos = rabito_repo.get_all() # type: ignore

        for rabito in rabitos:
            _update_time(rabito)
            events = producer.produce(rabito)
            for event in events:
                rabito_repo.add_event(rabito.id, event["action"], 0.1) # type: ignore
            rabito_repo.save_state(rabito) # type: ignore
