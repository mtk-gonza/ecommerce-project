from fastapi import Depends, HTTPException, status
from app.interfaces.api.v1.dependencies.auth import get_current_user

def require_roles(allowed_roles: list):
    def role_checker(user = Depends(get_current_user)):
        user_roles = [role.name for role in user.roles]
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return user

    return role_checker