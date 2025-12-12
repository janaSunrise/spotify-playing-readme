from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import Response

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


app: FastAPI = FastAPI(title="Spotify playing for README", redoc_url=None, lifespan=lifespan)

app.include_router(auth_router)
app.include_router(spotify_router)


@app.get("/")
async def index(request: Request) -> Response:
    return templates.TemplateResponse(
        request,
        "index.html",
        {"github_url": settings.github_url},
    )
