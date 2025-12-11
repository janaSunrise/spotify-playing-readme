import random
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from app.lib.spotify import spotify_client
from app.models.requests import SpotifyWidgetParams
from app.templates import templates
from app.utils import get_access_token, render_spotify_svg

spotify_router = APIRouter(tags=["spotify"])


async def get_song_info(user_id: str) -> tuple[dict, bool]:
    """Get currently playing or recently played song for user."""
    access_token = await get_access_token(user_id)
    data = await spotify_client.get_now_playing(access_token)

    if data is not None and data != {}:
        song = data["item"]
        if not song.get("currently_playing_type"):
            song["currently_playing_type"] = data.get("currently_playing_type", "track")
        is_now_playing = data.get("is_playing", False)
        return song, is_now_playing

    # Fallback to recently played
    recent_plays = await spotify_client.get_recently_played(access_token)
    if not recent_plays.get("items"):
        raise HTTPException(status_code=404, detail="No recent plays found for user")

    size_recent_play = len(recent_plays["items"])
    idx = random.randint(0, size_recent_play - 1)
    song = recent_plays["items"][idx]["track"]
    song["currently_playing_type"] = "track"
    return song, False


@spotify_router.get("/spotify")
async def get_spotify_widget(
    id: Annotated[str, Query()],  # noqa: A002
    theme: Annotated[str, Query()] = "plain",
    image: Annotated[str, Query()] = "true",
    bars_when_not_listening: Annotated[str, Query()] = "true",
    hide_status: Annotated[str, Query()] = "false",
    title_color: Annotated[str, Query()] = "",
    text_color: Annotated[str, Query()] = "",
    bg_color: Annotated[str, Query()] = "",
    color_theme: Annotated[str, Query()] = "none",
):
    """Generate Spotify widget SVG."""
    params = SpotifyWidgetParams(
        id=id,
        theme=theme,
        image=image,
        bars_when_not_listening=bars_when_not_listening,
        hide_status=hide_status,
        title_color=title_color,
        text_color=text_color,
        bg_color=bg_color,
        color_theme=color_theme,
    )

    try:
        item, is_now_playing = await get_song_info(params.id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch song info: {e!s}")

    def template_render(template_name: str, **kwargs) -> str:
        """Helper to render template."""
        return templates.env.get_template(template_name).render(**kwargs)

    svg = await render_spotify_svg(
        item=item,
        theme=params.theme,
        is_now_playing=is_now_playing,
        needs_cover_image=params.needs_cover_image,
        bars_when_not_listening=params.bars_when_not_listening_flag,
        hide_status=params.hide_status_flag,
        color_theme=params.color_theme,
        title_color=params.title_color,
        text_color=params.text_color,
        bg_color=params.bg_color,
        template_render=template_render,
    )

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "s-maxage=1"},
    )
