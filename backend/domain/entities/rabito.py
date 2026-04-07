from dataclasses import dataclass, field
from datetime import datetime
from backend.domain.utils.utils import clamp
from backend.domain.entities.constans import (
    R_FATIGUE,
    SLEEP_THRESHOLD_FATIGUE, SLEEP_THRESHOLD_ENERGY,
    WAKE_THRESHOLD_FATIGUE, WAKE_THRESHOLD_ENERGY,
    ENERGY_DECAY_AWAKE, FATIGUE_GAIN_AWAKE, STIM_DECAY,
    FATIGUE_DECAY_ASLEEP, RESERVE_CONSUMED_PER_HOUR, RESERVE_EFFICIENCY,
    SleepState, CRITICAL_ENERGY
)


@dataclass
class Rabito:
    id: int
    user_id: int 
    name: str
    
    reserve: float
    energy: float
    fatigue: float
    stimulation: float
    bond: float

    created_at: datetime
    last_updated_at: datetime

    sleep_state: SleepState = SleepState.AWAKE

    def _clamp_all(self) -> None:
        self.energy = clamp(self.energy)
        self.fatigue = clamp(self.fatigue)
        self.stimulation = clamp(self.stimulation)
        self.bond = clamp(self.bond)
        self.reserve = clamp(self.reserve)

    def check_sleep_transition(self):
        if self.sleep_state == SleepState.AWAKE:
            if  self.fatigue > SLEEP_THRESHOLD_FATIGUE or \
                self.energy < SLEEP_THRESHOLD_ENERGY and \
                self.energy > CRITICAL_ENERGY:
                
                print("Duerme")
                self.sleep_state = SleepState.ASLEEP
                
        elif self.sleep_state == SleepState.ASLEEP:
            if  self.fatigue <= WAKE_THRESHOLD_FATIGUE and \
                self.energy > WAKE_THRESHOLD_ENERGY:

                self.sleep_state = SleepState.AWAKE

            elif self.reserve <= 0 and self.energy < CRITICAL_ENERGY:
                print("Despierta moribundo...")
                self.sleep_state = SleepState.AWAKE
    
    def _passive_decay(self, hours: float) -> None:
        self.energy -= ENERGY_DECAY_AWAKE * hours
        self.fatigue += FATIGUE_GAIN_AWAKE * hours
        self.stimulation -= STIM_DECAY * hours
        self._clamp_all()
    
    def passive_decay_without_reserve(self, hours: float) -> None:
        self.energy -= ENERGY_DECAY_AWAKE * hours * 0.3
        self.fatigue += FATIGUE_GAIN_AWAKE * hours
        self.stimulation -= STIM_DECAY * hours
        self._clamp_all()
    
    def convert_reserve_to_energy(self, hours: float) -> None:
        if self.reserve <= 0:
            self.sleep_state = SleepState.AWAKE
            return
        reserve_used = min(RESERVE_CONSUMED_PER_HOUR * hours, self.reserve)
        self.reserve -= reserve_used
        self.energy += reserve_used * RESERVE_EFFICIENCY
        self._clamp_all()

    def _sleep_update(self, hours: float) -> None:
        """Recuperación durante el sueño, financiada por reserva"""
        self.stimulation -= STIM_DECAY * hours

        if self.reserve <= 0:
            self._clamp_all()
            self.energy -= ENERGY_DECAY_AWAKE * hours * 3
            return
        self.fatigue -= min(FATIGUE_DECAY_ASLEEP * hours, max(0, self.fatigue - R_FATIGUE))

        self.convert_reserve_to_energy(hours)
    
    def tick(self, hours: float) -> None:
        """Actualiza el estado del Rabito por el paso del tiempo"""
        STEP = 1
        i = 0
        remaining = hours
        while remaining > 0:
            print("HORA:", i+1)
            step = min(STEP, remaining)
            self.check_sleep_transition()

            if self.sleep_state == SleepState.AWAKE:
                print("despierto...")
                print("atributos de la mascota: {}", {
                    "energy": round(self.energy, 3),
                    "fatigue": round(self.fatigue, 3),
                    "stimulation": round(self.stimulation, 3),
                    "bond": round(self.bond, 3),
                    "reserve": round(self.reserve, 3)
                })
                if self.reserve >= 0:
                    self._passive_decay(step)
                else:
                    self.passive_decay_without_reserve(step)
                
                if self.energy < CRITICAL_ENERGY and self.reserve > 0:
                    self.convert_reserve_to_energy(step)
                
            else:
                print("durmiendo...")
                print("atributos de la mascota: {}", {
                    "energy": round(self.energy, 3),
                    "fatigue": round(self.fatigue, 3),
                    "stimulation": round(self.stimulation, 3),
                    "bond": round(self.bond, 3),
                    "reserve": round(self.reserve, 3)
                })
                self._sleep_update(step)

            remaining -= step
            i+=1

