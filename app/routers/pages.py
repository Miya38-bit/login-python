from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth.deps import SessionUser, get_session_user, require_permission
from app.auth.models import Permission
from app.auth.users import get_by_username, verify_password

router = APIRouter()

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))


def _ctx(request: Request, user: SessionUser | None = None, **extra):
    return {"request": request, "user": user, **extra}


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = get_session_user(request)
    return templates.TemplateResponse("home.html", _ctx(request, user))


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    user = get_session_user(request)
    if user is not None:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", _ctx(request, None))


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(),
    password: str = Form(),
):
    rec = get_by_username(username.strip())
    if rec is None or not verify_password(password, rec.password_hash):
        return templates.TemplateResponse(
            "login.html",
            _ctx(request, None, error="ユーザー名またはパスワードが正しくありません"),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    request.session["user"] = rec.username
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/public", response_class=HTMLResponse)
async def page_public(request: Request):
    user = get_session_user(request)
    return templates.TemplateResponse("public.html", _ctx(request, user))


@router.get("/member", response_class=HTMLResponse)
async def page_member(
    request: Request,
    user: Annotated[SessionUser, Depends(require_permission(Permission.MEMBER_DASHBOARD))],
):
    return templates.TemplateResponse("member.html", _ctx(request, user))


@router.get("/reports", response_class=HTMLResponse)
async def page_reports(
    request: Request,
    user: Annotated[SessionUser, Depends(require_permission(Permission.REPORTS_VIEW))],
):
    return templates.TemplateResponse("reports.html", _ctx(request, user))


@router.get("/admin", response_class=HTMLResponse)
async def page_admin(
    request: Request,
    user: Annotated[SessionUser, Depends(require_permission(Permission.ADMIN_PANEL))],
):
    return templates.TemplateResponse("admin.html", _ctx(request, user))
