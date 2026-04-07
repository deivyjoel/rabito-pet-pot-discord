import random
from backend.domain.entities.constans import MAX_ATTR, MIN_ATTR, R_ENERGY

def clamp(x: float) -> float:
    return max(MIN_ATTR, min(MAX_ATTR, x))


def noise(scale=0.02):
    return random.uniform(-scale, scale)


def move_towards(current: float, target: float, max_change: float, available_energy: float):
    """
    Mueve 'current' hacia 'target' hasta max_change, pero limitada con la energía disponible

    Args:.

    
        current: valor actual del atributo
        target: valor objetivo (setpoint)
        max_change: cuánto podría cambiar normalmente en una unidad de tiepo
        available_energy: cuánta energía hay para gastar en este cambio
    Returns:
        nuevo valor del atributo
    
    """
    delta = target  - current
    if delta > 0:
        delta = min(delta, max_change)
    else:
        delta = max(delta, -max_change)

    # Limita el cambio a la energía disponible
    delta = max(min(delta, available_energy), -available_energy)
    return current + delta
