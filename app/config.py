import os
from functools import lru_cache


@lru_cache
def get_session_secret() -> str:
    return os.environ.get("SESSION_SECRET", "dev-only-change-with-env")
