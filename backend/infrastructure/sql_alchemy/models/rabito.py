from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from backend.infrastructure.repositories.date_reference import get_utc_now
from backend.domain.entities.constans import R_ENERGY, R_FATIGUE, R_RESERVE, R_STIMULATION

R_BOND = 0.7

class Base(DeclarativeBase):
    pass


# Tabla principal pet
class RabitoModel(Base):
    __tablename__ = "rabito"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Estado fisiológico persistido
    reserve: Mapped[float] = mapped_column(Float, default=R_RESERVE)
    energy: Mapped[float] = mapped_column(Float, default=R_ENERGY)
    fatigue: Mapped[float] = mapped_column(Float, default=R_FATIGUE)
    stimulation: Mapped[float] = mapped_column(Float, default=R_STIMULATION)
    bond: Mapped[float] = mapped_column(Float, default=R_BOND)
    sleep_state: Mapped[str] = mapped_column(String(20), default="AWAKE")  # "AWAKE" o "ASLEEP"
    
    last_updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=get_utc_now)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now
    )

    events = relationship(
        "RabitoEventModel",
        back_populates="rabito",
        cascade="all, delete-orphan"
    )


class RabitoEventModel(Base):
    __tablename__ = "rabito_event"

    id: Mapped[int] = mapped_column(primary_key=True)
    rabito_id: Mapped[int] = mapped_column(
        ForeignKey("rabito.id"),
        nullable=False
    )

    type: Mapped[str] = mapped_column(String(50), nullable=False)
    # feed, play, interact, rest, explore, etc.

    value: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_utc_now
    )

    rabito = relationship("RabitoModel", back_populates="events")