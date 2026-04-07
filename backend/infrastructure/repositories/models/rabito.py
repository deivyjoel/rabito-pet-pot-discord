from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete

from backend.domain.entities.constans import SleepState
from backend.infrastructure.sql_alchemy.models.rabito import RabitoModel, RabitoEventModel
from backend.infrastructure.repositories.errors import RepositoryError
from backend.domain.entities.rabito import Rabito
from enum import Enum


class RabitoRepository:
    def __init__(self, session):
        self.session = session

    # ==========================
    # Mapping
    # ==========================

    def _to_domain(self, model: RabitoModel) -> Rabito:
        return Rabito(
            id=model.id,
            user_id=model.user_id,
            name=model.name,
            reserve= model.reserve,
            energy=model.energy,
            fatigue=model.fatigue,
            stimulation=model.stimulation,
            bond=model.bond,
            created_at=model.created_at,
            sleep_state=SleepState(model.sleep_state.lower()),
            last_updated_at=model.last_updated_at
        )

    # ==========================
    # CRUD
    # ==========================

    def create(self, user_id: int, name: str) -> int:
        obj = RabitoModel(
            user_id=user_id,
            name=name
        )

        try:
            self.session.add(obj)
            self.session.commit()
            return obj.id

        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError("db_error") from e

    def delete(self, rabito_id: int, user_id: int) -> None:
        try:
            stmt = (
                delete(RabitoModel)
                .where(RabitoModel.id == rabito_id)
                .where(RabitoModel.user_id == user_id)
            )

            self.session.execute(stmt)
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError("db_error") from e

    def get_by_user_id(self, user_id: int) -> Rabito | None:
        obj = (
            self.session.query(RabitoModel)
            .filter_by(user_id=user_id)
            .first()
        )

        return self._to_domain(obj) if obj else None

    def save_state(self, rabito: Rabito) -> None:
        try:
            obj = self.session.get(RabitoModel, rabito.id)

            if not obj:
                return

            obj.energy = rabito.energy
            obj.reserve = rabito.reserve
            obj.fatigue = rabito.fatigue
            obj.stimulation = rabito.stimulation
            obj.bond = rabito.bond
            obj.last_updated_at = rabito.last_updated_at 
            obj.sleep_state = rabito.sleep_state.value 

            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError("db_error") from e

    # ==========================
    # Eventos
    # ==========================

    def add_event(
        self,
        rabito_id: int,
        event_type: str,
        value: float = 0.0
    ) -> None:

        event = RabitoEventModel(
            rabito_id=rabito_id,
            type=event_type,
            value=value
        )

        try:
            self.session.add(event)
            self.session.commit()

        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError("db_error") from e