from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class RabitoSummaryDTO:
    """DTO to transport rabito summary data."""
    name: str
    edad: float
    state: str
    last_interaction: datetime

