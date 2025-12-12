import random

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.exceptions import UserNotFoundError
from app.lib.spotify import spotify_client
from app.models.spotify import SpotifyItem
from app.models.spotify_api import (
    SpotifyEpisode,
    SpotifyRecentlyPlayedResponse,
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

    recent_plays: SpotifyRecentlyPlayedResponse = await spotify_client.get_recently_played(access_token)
    if not recent_plays.items:
        raise HTTPException(status_code=404, detail="No recent plays found for user")

    song_data = random.choice(recent_plays.items).track
    return SpotifyItem.from_track(song_data, is_now_playing=False), False


@spotify_router.get("/spotify")
async def get_spotify_widget(
    id: str,  # noqa: A002
    theme: str = "plain",
    image: bool = True,
    bars_when_not_listening: bool = True,
    hide_status: bool = False,
    title_color: str = "",
    text_color: str = "",
    bg_color: str = "",
    color_theme: str = "none",
) -> Response:
    try:
        item, is_now_playing = await get_song_info(id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail="User not found. Please authenticate first at /login",
        ) from e
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch song info: {e!s}") from e

    svg: str = await render_spotify_svg(
        item=item,
        theme=theme,
        is_now_playing=is_now_playing,
        needs_cover_image=image,
        bars_when_not_listening=bars_when_not_listening,
        hide_status=hide_status,
        color_theme=color_theme,
        title_color=title_color,
        text_color=text_color,
        bg_color=bg_color,
    )

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "s-maxage=1"},
    )
