from dataclasses import dataclass

import bcrypt

from app.auth.models import Role


@dataclass(frozen=True)
class UserRecord:
    username: str
    password_hash: str
    role: Role
    display_name: str


def _hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _seed() -> dict[str, UserRecord]:
    return {
        "alice": UserRecord(
            username="alice",
            password_hash=_hash_password("alicepass"),
            role=Role.USER,
            display_name="一般ユーザー Alice",
        ),
        "admin": UserRecord(
            username="admin",
            password_hash=_hash_password("adminpass"),
            role=Role.ADMIN,
            display_name="管理者",
        ),
    }


_USERS: dict[str, UserRecord] = _seed()


def get_by_username(username: str) -> UserRecord | None:
    return _USERS.get(username)


def verify_password(plain: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        plain.encode("utf-8"),
        password_hash.encode("utf-8"),
    )
