import base64
from time import time

from fastapi import HTTPException
from markupsafe import escape

from app.exceptions import TokenRefreshError
from app.lib.spotify import spotify_client
from app.lib.supabase import supabase_client
from app.models.spotify import SpotifyItem
from app.models.spotify_api import SpotifyTokenResponse
from app.templates import templates
from app.theming import (
    MAX_TEXT_LENGTH,
    VISUALIZER_BAR_COUNT,
    WIDGET_HEIGHT,
    WIDGET_WIDTH,
    generate_visualizer_bars,
    generate_visualizer_css,
    get_colors,
    validate_card_style,
    validate_color_theme,
)


async def load_image_b64(url: str) -> str:
    if not url:
        return ""
    if image_content := await spotify_client.fetch_image(url):
        return base64.b64encode(image_content).decode("ascii")
    return ""


async def get_access_token(user_id: str) -> str:
    user = await supabase_client.get_user(user_id)

    if user.is_token_expired():
        try:
            new_token: SpotifyTokenResponse = await spotify_client.refresh_token(user.refresh_token)
            expired_time: int = int(time()) + new_token.expires_in

            await supabase_client.update_token(user_id, new_token.access_token, expired_time)
        except TokenRefreshError as exc:
            raise HTTPException(status_code=401, detail="Token refresh failed. Please login again.") from exc
        else:
            return new_token.access_token

    return user.access_token


async def render_spotify_svg(
    item: SpotifyItem,
    is_now_playing: bool,
    needs_cover_image: bool,
    style: str | None = None,
    color_theme: str | None = None,
) -> str:
    img = await load_image_b64(item.image_url) if item.image_url and needs_cover_image else ""
    artist_name = str(escape(item.artist))
    song_name = str(escape(item.name))

    card_style = validate_card_style(style)
    colors = get_colors(color_theme)
    is_dark_mode = validate_color_theme(color_theme) == "dark"

    content_bar = generate_visualizer_bars(VISUALIZER_BAR_COUNT) if is_now_playing else ""
    css_bar = generate_visualizer_css(VISUALIZER_BAR_COUNT) if is_now_playing else ""

    status = "Currently playing:" if is_now_playing else "Last listened to:"

    template_name = f"spotify.{card_style}.html.j2"
    rendered_data = {
        "width": WIDGET_WIDTH,
        "height": WIDGET_HEIGHT,
        "num_bar": VISUALIZER_BAR_COUNT,
        "content_bar": content_bar,
        "css_bar": css_bar,
        "status": status,
        "artist_name": artist_name,
        "song_name": song_name,
        "img": img,
        "is_now_playing": is_now_playing,
        "explicit": item.is_explicit,
        "show_animation": len(song_name) > MAX_TEXT_LENGTH or len(artist_name) > MAX_TEXT_LENGTH,
        "needs_cover_image": needs_cover_image,
        "bg_color": colors["bg"],
        "text_color": colors["text"],
        "accent_color": colors["accent"],
        "status_color": colors["status"],
        "is_dark_mode": is_dark_mode,
    }

    try:
        return templates.env.get_template(template_name).render(**rendered_data)
    except (KeyError, ValueError, TypeError):
        fallback_template = "spotify.default.html.j2"
        return templates.env.get_template(fallback_template).render(**rendered_data)
