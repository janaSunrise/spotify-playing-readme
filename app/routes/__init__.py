from .auth import auth_router
from .index import index_router
from .spotify import spotify_router

__all__ = ["auth_router", "index_router", "spotify_router"]
