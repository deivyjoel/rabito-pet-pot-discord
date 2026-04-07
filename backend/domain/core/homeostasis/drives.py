from backend.domain.utils.utils import clamp
from backend.domain.core.primitives import Primitives 

class Drives:
    # Mide desviaciones del estado interno.
    """
    ¿Qué hacen cada método?
    1. Observan el estado actual
    2. Calcula distancia del equilibrio
    3. Amplifican por personalidad
    4. Devuelven un escalar entre 0 y 1
    """
    def conservation(self, rabito):
        #Este drive responde a: 'Necesito recuperar estabilidad fisiológica')
        return 1 - rabito.energy

    def exploration(self, rabito):
        # Si estimulación es muy baja, aburrimiento- Si es muy alta, saturación.
        return 1 - rabito.stimulation

    def affiliation(self, rabito):
        return 1 - rabito.bond
    
    def compute(self, rabito):
        return {
            "conservation": self.conservation(rabito),
            "exploration": self.exploration(rabito),
            "affiliation": self.affiliation(rabito)
        }
    

