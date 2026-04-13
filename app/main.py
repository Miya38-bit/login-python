from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.config import get_session_secret
from app.routers import pages

app = FastAPI(title="login-python", description="セッション認証・ロール・権限の学習用")
app.add_middleware(
    SessionMiddleware,
    secret_key=get_session_secret(),
    max_age=14 * 24 * 60 * 60,
    same_site="lax",
)

app.include_router(pages.router)
