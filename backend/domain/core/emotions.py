from backend.domain.utils.utils import clamp

class Emotions:
    """
    No guarda emociones. No tiene memoria emocional.
    Solo calcula un mapa comprimido del estado interno actual.
    Es una función:
    Emoción = f(Drives, Estado)
    """
    def __init__(self, drives):
        self.d = drives

    def compute(self, rabito):
        """
        1. Calcula los drives actuales
        2. Los combina
        3. Devuelve un diccionario de valores 0-1
        """

        Dc = self.d.conservation(rabito)
        De = self.d.exploration(rabito)
        Da = self.d.affiliation(rabito)

        return {
            "frustration": clamp(De * Dc),
            "loneliness": clamp(Da), #Corregir
            "calm": clamp(1 - (Dc + De + Da) / 3), #Corregir
            "motivation": clamp(De * rabito.energy),

        }