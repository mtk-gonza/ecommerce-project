from app.domain.entities.user import User
from app.application.services.user_service import UserService
from app.domain.exceptions import AuthenticationException, AuthorizationException
from app.infrastructure.security.jwt_handler import create_access_token, decode_access_token

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, email: str, password: str) -> dict:
        user = self.user_service.get_user_by_email(email)
        if not user:
            raise AuthenticationException("Credenciales inválidas")
        if not user.is_active:
            raise AuthenticationException("Usuario inactivo")
        if not self.user_service.verify_password(user, password):
            raise AuthenticationException("Credenciales inválidas")
        
        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role.value}
        )
        
        # ✅ Retornar solo los campos que UserInTokenSchema espera
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role.value  # .value para convertir Enum a string
            }
        }

    def register(self, email: str, password: str, name: str, phone: str = None) -> User:
        return self.user_service.create_user(email=email, password=password, name=name, phone=phone)

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