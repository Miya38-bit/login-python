from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.auth.models import ROLE_PERMISSIONS, Permission, Role
from app.auth.users import get_by_username


@dataclass(frozen=True)
class SessionUser:
    username: str
    role: Role
    display_name: str


def get_session_user(request: Request) -> SessionUser | None:
    username = request.session.get("user")
    if not username or not isinstance(username, str):
        return None
    rec = get_by_username(username)
    if rec is None:
        request.session.clear()
        return None
    return SessionUser(
        username=rec.username,
        role=rec.role,
        display_name=rec.display_name,
    )


def require_login(request: Request) -> SessionUser:
    user = get_session_user(request)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": "/login"},
        )
    return user


def require_permission(permission: Permission):
    def _dep(user: Annotated[SessionUser, Depends(require_login)]) -> SessionUser:
        allowed = ROLE_PERMISSIONS.get(user.role, frozenset())
        if permission not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="この権限ではアクセスできません",
            )
        return user

    return _dep
