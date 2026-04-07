from enum import Enum

# CONCEPTS
"""
1. Energia: Recurso general de acción
2. Reversa: Material potencial a energia
3. Fatiga: Acumulación de desgaste neurofisiologico
4. Estimulación: Nivel reciente de variabilidad y novedad en el entorno
"""
"""
Ciclo de sueño: 16h despierto -> 8h dormido
Muerte sin comida: día 10
Estimulación vacía: día 3 sin jugar
Energía colapsa: día 2 sin reserva
"""
# RANGOS
MIN_ATTR = 0.0
MAX_ATTR = 1.0

# SETPOINTS (estado óptimo futuro)
R_ENERGY = 0.75
R_FATIGUE = 0.25
R_STIMULATION = 0.55
R_RESERVE = 0.7


# Umbrales para dormir/despertar
SLEEP_THRESHOLD_FATIGUE = 0.75 # Si fatiga > esto -> se duerme
SLEEP_THRESHOLD_ENERGY = 0.20 # Si energy < esto  se duerme
WAKE_THRESHOLD_FATIGUE = 0.25 # Si fatiga < esto durmiendo  -> despierta
WAKE_THRESHOLD_ENERGY = 0.75 # Si energy > esto durmiendo -> despierta

CRITICAL_ENERGY = 0.15 # Cuando despierta moribundo

# ==========================
# TASAS BASE (sin genética)
# Después estas serán modificadas por genetics
# ==========================
# Despierto
ENERGY_DECAY_AWAKE = (R_ENERGY-SLEEP_THRESHOLD_ENERGY) / 16   # En 16 horas sin dormir, energía cae de óptimo a umbral de dormir
FATIGUE_GAIN_AWAKE = (SLEEP_THRESHOLD_FATIGUE - R_FATIGUE) / 16 # Si no durmiera, en 16h llegaría a umbral de dormir por fatiga
STIM_DECAY   = 1 / 72   # Se agota en 3 días


# Ciclo de fatiga y dormir (Ciclo circadiano)
FATIGUE_DECAY_ASLEEP = (SLEEP_THRESHOLD_FATIGUE - R_FATIGUE) / 8  # Durmiendo se recupera más rápido, en 8h estaría en nivel óptimo de fatiga

# Si energia: 
RESERVE_CONSUMED_PER_HOUR=  (R_RESERVE / 3) / 8  # 0.029 por hora
RESERVE_EFFICIENCY = 2.36

# ==========================
# ESTADOS
# ==========================
class SleepState(Enum):
    AWAKE  = "awake"
    ASLEEP = "asleep"