from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.discord_bot import create_bot
from backend.infrastructure.sql_alchemy.models.rabito import Base
from backend.infrastructure.repositories.models.rabito import RabitoRepository
from backend.application.backend_api import BackendAPI

# --- DB setup ---
engine = create_engine('sqlite:///app.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
rabito_repo = RabitoRepository(session)

bck_api = BackendAPI(
    rabito_repo = rabito_repo
)

USER_ID = 133
rabito = bck_api.create_rabito(USER_ID, "juan")



print("\nSimulando 30 días...\n")
print("Rabito - Estado nacimiento: ")
data = bck_api.ver_dato_rabito(USER_ID)
if not data:
    data = {}

print({
        "energy": round(data["energy"], 3),
        "fatigue": round(data["fatigue"], 3),
        "stimulation": round(data["stimulation"], 3),
        "bond": round(data["bond"], 3),
        "reserve": round(data["reserve"], 3)
})

for day in range(1):
    bck_api.simular_horas(USER_ID, 96)

    data = bck_api.ver_dato_rabito(USER_ID)
    if not data:
        break
    print(f"Día {day+1}")
    print({
        "energy": round(data["energy"], 3),
        "fatigue": round(data["fatigue"], 3),
        "stimulation": round(data["stimulation"], 3),
        "bond": round(data["bond"], 3),
        "reserve": round(data["reserve"], 3)
    })
    print()


