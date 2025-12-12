from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.lib import spotify, supabase
from app.routes.auth import auth_router
from app.routes.spotify import spotify_router
from app.templates import templates


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await supabase.supabase_client.initialize()
    yield
    await spotify.spotify_client.close()

MAX_AGE = 604_800  # 7 days in seconds


app: FastAPI = FastAPI(title="Spotify playing for README", redoc_url=None, lifespan=lifespan)

app.add_middleware(
    SessionMiddleware, secret_key=settings.session_secret_key, max_age=MAX_AGE,
)

app.include_router(auth_router)
app.include_router(spotify_router)


@app.get("/")
async def index(request: Request) -> Response:
    user_id = request.session.get("user_id")

    if user_id:
        return RedirectResponse(url="/customize", status_code=303)

    return templates.TemplateResponse(
        request,
        "index.html",
        {"github_url": settings.github_url},
    )
