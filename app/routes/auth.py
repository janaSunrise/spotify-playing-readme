from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.config import settings
from app.exceptions import SpotifyAPIError
from app.lib.spotify import spotify_client
from app.templates import templates
from app.utils import create_or_update_user

auth_router = APIRouter(tags=["authentication"])


@auth_router.get("/login")
async def login():
    """Redirect to Spotify OAuth authorization."""
    auth_url = spotify_client.generate_auth_url(settings.spotify_scopes)
    return RedirectResponse(url=auth_url)


@auth_router.get("/callback")
async def callback(request: Request):
    """Handle Spotify OAuth callback."""
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="No authorization code found in callback")

    try:
        token = await spotify_client.generate_token(code)
        access_token = token["access_token"]
        user_id = (await spotify_client.get_user_info(access_token))["id"]
    except SpotifyAPIError as e:
        raise HTTPException(status_code=401, detail=f"Failed to authenticate with Spotify: {e!s}")
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid authentication response from Spotify")

    await create_or_update_user(user_id, token)

    return templates.TemplateResponse(
        request,
        "callback.html",
        {
            "id": user_id,
            "base_url": settings.base_url,
            "github_url": settings.github_url,
        },
    )
