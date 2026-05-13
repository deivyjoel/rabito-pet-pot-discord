from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.infrastructure.sql_alchemy.models.rabito import Base
from backend.infrastructure.repositories.models.rabito import RabitoRepository
from backend.application.backend_api import BackendAPI

# --- DB setup ---
# Establecemos el nombre de la base de datos
engine = create_engine('sqlite:///app.db', echo=False)
# Creamos todas las tablas
Base.metadata.create_all(engine)
# Creamos la fabrica de sesiones
Session = sessionmaker(bind=engine)
# Instanciamos una sesión
session = Session()

"""
Le damos una sesión a la clase RabitoRepository.
RabitoRepository tiene el CRUD hacia la tabla de sqlalchemy.
Además permite la trazabilidad de errores.
"""
rabito_repo = RabitoRepository(session)


"""
Creamos la clase BackendAPI para tener acceso a los metodos expuestos.
"""
bck_api = BackendAPI(
    rabito_repo = rabito_repo
)

"""
Creamos un Rabito con el USER_ID
"""

USER_ID = 12
rabito = bck_api.create_rabito(USER_ID, "juan")



# SIMULAMOS LOS 30 DIAS DE VIDA DEL RABITO
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


