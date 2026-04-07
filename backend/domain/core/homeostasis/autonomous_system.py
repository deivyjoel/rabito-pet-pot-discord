from backend.domain.core.homeostasis.drives import Drives
from backend.domain.entities.rabito import Rabito
import math

class AutonomousSystem:
    def __init__(self):
        self.drives = Drives()
        #self.action = ActionSystem()
    
    def simulate(self, r: Rabito, hours: float):
        #1. Dinámica pasiva
        r.tick(hours)

        #2. Calcular drives
        drives = self.drives.compute(r)
            
        return drives
