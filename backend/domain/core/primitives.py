from backend.domain.utils.utils import clamp

class Primitives:
    def __init__(self):
        # Rango [0,1]
        self.energy = 0.7
        self.fatigue = 0.2
        self.stimulation = 0.5
        self.bond = 0.6

        self.E_opt = 0.7
        self.S_opt = 0.5
        self.B_opt = 0.7
    
    def clamp_all(self):
        self.energy = clamp(self.energy)
        self.fatigue = clamp(self.fatigue)
        self.stimulation = clamp(self.stimulation)
        self.bond = clamp(self.bond)
        