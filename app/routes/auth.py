from time import time

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse, Response

from app.config import settings
from app.exceptions import SpotifyAPIError
from app.lib.spotify import spotify_client
from app.lib.supabase import supabase_client
from app.models.user import User
from app.templates import templates

auth_router = APIRouter()


@auth_router.get("/login")
async def login() -> RedirectResponse:
    auth_url = spotify_client.generate_auth_url(settings.spotify_scopes)
    return RedirectResponse(url=auth_url)


@auth_router.get("/callback")
async def callback(request: Request) -> Response:
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="No authorization code found in callback")

    try:
        token = await spotify_client.generate_token(code)
        access_token = token.access_token
        user_info = await spotify_client.get_user_info(access_token)
        user_id = user_info.id
    except SpotifyAPIError as e:
        raise HTTPException(status_code=401, detail="Failed to authenticate with Spotify") from e

    if not token.refresh_token:
        raise HTTPException(status_code=400, detail="refresh_token is required for user creation")

    user = User(
        id=user_id,
        access_token=token.access_token,
        refresh_token=token.refresh_token,
        token_type=token.token_type,
        expires_in=token.expires_in,
        scope=token.scope,
        expired_time=int(time()) + token.expires_in,
    )

    await supabase_client.upsert_user(user)

    # Store user_id in session
    request.session["user_id"] = user_id

    return RedirectResponse(url="/customize", status_code=303)


@auth_router.get("/customize")
async def customize(request: Request) -> Response:
    user_id = request.session.get("user_id")

    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        request,
        "customize.html",
        {
            "id": user_id,
            "base_url": settings.base_url,
            "github_url": settings.github_url,
        },
    )


@auth_router.get("/logout")
async def logout(request: Request) -> RedirectResponse:
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
