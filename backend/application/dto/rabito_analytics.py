from dataclasses import dataclass
from datetime import datetime

from backend.domain.models.health_status import HealthStatus

from backend.domain.models.health_status import HealthStatus

@dataclass(frozen=True)
class RabitoAnalyticsDTO:
    """DTO to transport rabito analytics data."""
    name: str
    edad: float
    health: str
    energy: float
    mood: float
    stress: float
    last_interaction: datetime

