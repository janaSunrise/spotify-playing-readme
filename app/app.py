from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.lib import spotify, supabase
from app.routes.auth import auth_router
from app.routes.spotify import spotify_router
from app.templates import templates

MAX_AGE = 604_800  # 7 days in seconds


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    spotify.spotify_client.initialize()
    await supabase.supabase_client.initialize()
    yield
    await spotify.spotify_client.close()


app = FastAPI(title="Spotify playing for README", redoc_url=None, lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret_key,
    max_age=MAX_AGE,
)

app.include_router(auth_router)
app.include_router(spotify_router)


@app.get("/")
async def index(request: Request) -> Response:
    return templates.TemplateResponse(
        request,
        "index.html",
        {"github_url": settings.github_url},
    )
