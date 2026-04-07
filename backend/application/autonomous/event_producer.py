from backend.domain.core.agent import OntologicalAgent
from backend.domain.entities.rabito import Rabito

class EventProducer:

    def __init__(self, agent: OntologicalAgent):
        self.agent = agent

    def produce(self, rabito: Rabito) -> list[str]:
        """
        Evalúa el estado del rabito y genera eventos de dominio. No envía nada a Discord. Solo retorna eventos.
        """
        events = []
        # Ejecuta evaluación cognitiva
        agent_events = self.agent.step(rabito)

        if agent_events:
            events.extend(agent_events)
        return events