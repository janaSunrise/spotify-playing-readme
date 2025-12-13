import random

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.exceptions import UserNotFoundError
from app.lib.spotify import spotify_client
from app.models.spotify import SpotifyItem
from app.models.spotify_api import (
    SpotifyEpisode,
    SpotifyTrack,
)
from app.utils import get_access_token, render_spotify_svg

spotify_router = APIRouter()


async def get_song_info(user_id: str) -> tuple[SpotifyItem, bool]:
    access_token = await get_access_token(user_id)
    data = await spotify_client.get_now_playing(access_token)

    if data is not None and data.item is not None:
        is_now_playing = data.is_playing
        currently_playing_type = data.currently_playing_type

        if currently_playing_type == "episode" and isinstance(data.item, SpotifyEpisode):
            return SpotifyItem.from_episode(data.item, is_now_playing=is_now_playing), is_now_playing
        if isinstance(data.item, SpotifyTrack):
            return SpotifyItem.from_track(data.item, is_now_playing=is_now_playing), is_now_playing

    recent_plays = await spotify_client.get_recently_played(access_token)
    if not recent_plays.items:
        raise HTTPException(status_code=404, detail="No recent plays found for user")

    song_data = random.choice(recent_plays.items).track
    return SpotifyItem.from_track(song_data, is_now_playing=False), False


@spotify_router.get("/spotify")
async def get_spotify_widget(
    user_id: str,
    image: bool = True,
    style: str = "default",
    color_theme: str = "light",
) -> Response:
    try:
        item, is_now_playing = await get_song_info(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail="User not found. Please authenticate first at /login",
        ) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch song info.") from e

    svg: str = await render_spotify_svg(
        item=item,
        is_now_playing=is_now_playing,
        needs_cover_image=image,
        style=style,
        color_theme=color_theme,
    )

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "s-maxage=1"},
    )
