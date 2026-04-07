from log import logger
from pydantic import ValidationError
from functools import wraps
from backend.application.decorators.validator_types import validate_types
from backend.application.results.operation_result import OperationResult
from backend.infrastructure.repositories.errors import RepositoryError


def handle_usecase_errors(f):
    f_validated = validate_types(f)
    
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f_validated(*args, **kwargs)
        
        except ValidationError as e:
            errors = e.errors()
            campo = errors[0].get('loc', ('desconocido',))[-1] 
            detalle = errors[0].get('msg', 'Error de validación')
            
            msg = f"Dato inválido en '{campo}': {detalle}"
            return OperationResult(False, msg, None)
        except RepositoryError as e:
            logger.error(
                "Error de repositorio en use case",
                extra={
                    "usecase": f.__name__,
                    "error": str(e)
                }
            )
            return OperationResult(False, "Error de base de datos", None)
               
        except Exception as e:
            logger.exception(
                "Error inesperado en use case",
                extra={"usecase": f.__name__}
            )
            return OperationResult(False, "Ocurrió un error interno", None)
        
    return wrapper

