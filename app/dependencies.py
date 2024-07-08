from fastapi import Depends, HTTPException, status

from app import schemas
from .auth import get_current_active_user
from .schemas import Role

def admin_only(current_user: schemas.UserResponse = Depends(get_current_active_user)):
    if current_user.role != Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user

def manager_only(current_user: schemas.UserResponse = Depends(get_current_active_user)):
    if current_user.role not in [Role.admin, Role.manager]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user

def user_only(current_user: schemas.UserResponse = Depends(get_current_active_user)):
    if current_user.role not in [Role.admin, Role.manager, Role.user]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user
