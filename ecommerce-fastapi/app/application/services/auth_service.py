from app.domain.entities.user import User
from app.application.services.user_service import UserService
from app.domain.exceptions import AuthenticationException, AuthorizationException, ValidationError
from app.infrastructure.security.jwt_handler import create_access_token, decode_access_token
from app.infrastructure.logging import get_logger, safe_extra

logger = get_logger(__name__)

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, email: str, password: str) -> dict:
        try:
            user = self.user_service.get_user_by_email(email)
            if not user:
                logger.info(
                    "Intento de login con email no registrado",
                    extra={"email": email, "ip": "unknown"}  # Podés agregar IP desde el request
                )
                raise AuthenticationException("Credenciales inválidas")
            
            if not user.is_active:
                logger.warning(
                    "Intento de login con usuario inactivo",
                    extra={"user_id": user.id, "email": email}
                )
                raise AuthenticationException("Usuario inactivo")
            
            if not self.user_service.verify_password(user, password):
                logger.warning(
                    "Intento de login con contraseña incorrecta",
                    extra={"email": email, "user_id": user.id}
                )
                raise AuthenticationException("Credenciales inválidas")
            
            # Login exitoso
            access_token = create_access_token(
                data={"sub": str(user.id), "role": user.role.value}
            )
            
            logger.info(
                "Login exitoso",
                extra=safe_extra({
                    "user_id": user.id,
                    "user_email": email,
                    "user_role": user.role.value,
                    "user_name": user.name
                })
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role.value
                }
            }
            
        except AuthenticationException:
            raise
        except Exception as e:
            logger.exception(
                "Error inesperado en login",
                extra={"email": email, "error_type": type(e).__name__}
            )
            raise

    def register(self, email: str, password: str, name: str, phone: str = None) -> User:
        try:
            user = self.user_service.create_user(email=email, password=password, name=name, phone=phone)
            logger.info(
                "Usuario registrado",
                extra=safe_extra({
                    "user_id": user.id,
                    "user_email": email,
                    "user_role": user.role.value,
                    "user_name": user.name
                })
            )
            
            return user
            
        except ValidationError as e:
            logger.warning(
                f"Error de validación en registro: {e}",
                extra={"email": email, "error": str(e)}
            )
            raise
        except Exception as e:
            logger.exception(
                "Error inesperado en registro",
                extra={"email": email, "error_type": type(e).__name__}
            )
            raise

    def get_current_user(self, token: str) -> User:
        payload = decode_access_token(token)
        if payload is None:
            raise AuthenticationException("Token inválido")
        user_id = int(payload.get("sub"))
        if not user_id:
            raise AuthenticationException("Token inválido")
        user = self.user_service.get_user(user_id)
        if not user.is_active:
            raise AuthorizationException("Usuario inactivo")
        return user