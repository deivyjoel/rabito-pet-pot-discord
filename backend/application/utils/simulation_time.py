from datetime import datetime
from backend.domain.core.homeostasis.block_duration import estimate_duration
from backend.domain.entities.rabito import Rabito
from backend.domain.core.homeostasis.autonomous_system import AutonomousSystem

def _update_time(rabito: Rabito, autonomous_system=None) -> None:
    if autonomous_system is None:
        autonomous_system = AutonomousSystem()
    now = datetime.utcnow()
    remaining = (now - rabito.last_updated_at).total_seconds() / 3600

    while remaining > 0:
        drives = autonomous_system.drives.compute(rabito)
        action = autonomous_system.decision.choose_action(drives)

        duration = estimate_duration(rabito, action)

        step = min(duration, remaining)

        rabito.passive_decay(step)
        autonomous_system.action.apply(rabito, action, hours=step)
        remaining -= step
    rabito.last_updated_at = now
