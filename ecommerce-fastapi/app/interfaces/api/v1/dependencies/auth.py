from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.application.services.auth_service import AuthService
from app.domain.entities.user import User
from app.domain.exceptions import AuthenticationException, AuthorizationException
from .services import get_auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)) -> User:
    try:
        return auth_service.get_current_user(token)
    except AuthenticationException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    except AuthorizationException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no autorizado")

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Se requiere rol de administrador")
    return current_user