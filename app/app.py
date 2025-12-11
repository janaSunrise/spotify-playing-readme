from fastapi import FastAPI

from app.routes import auth_router, index_router, spotify_router

app = FastAPI(title="Spotify playing for README", redoc_url=None)

app.include_router(index_router)
app.include_router(auth_router)
app.include_router(spotify_router)
