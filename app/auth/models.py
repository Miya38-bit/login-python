from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class Permission(str, Enum):
    MEMBER_DASHBOARD = "member:dashboard"
    PROFILE_EDIT = "profile:edit"
    ADMIN_PANEL = "admin:panel"
    REPORTS_VIEW = "reports:view"


ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.USER: frozenset(
        {
            Permission.MEMBER_DASHBOARD,
            Permission.PROFILE_EDIT,
        }
    ),
    Role.ADMIN: frozenset(
        {
            Permission.MEMBER_DASHBOARD,
            Permission.PROFILE_EDIT,
            Permission.ADMIN_PANEL,
            Permission.REPORTS_VIEW,
        }
    ),
}
