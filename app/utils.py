import base64
import random
from textwrap import dedent
from time import time

from fastapi import HTTPException
from markupsafe import escape

from app.exceptions import TokenRefreshError
from app.lib.spotify import spotify_client
from app.lib.supabase import supabase_client
from app.models.spotify import SpotifyItem
from app.models.spotify_api import SpotifyTokenResponse
from app.models.user import User
from app.templates import templates
from app.themes import get_theme_colors, get_theme_dimensions

STATUS_TEXTS: dict[bool, list[str]] = {
    True: ["Vibing to", "Binging to", "Listening to", "Obsessed with"],
    False: ["Was listening to", "Previously binging to", "Was vibing to"],
}


def generate_bar(bar_count: int = 75) -> str:
    css_bar: str = ""
    left: int = 1

    for i in range(1, bar_count + 1):
        anim: int = random.randint(300, 600)
        css_bar += dedent(f"""
        .bar:nth-child({i}) {{
            left: {left}px;
            animation-duration: {anim}ms;
        }}
        """)
        left += 4

    return css_bar


async def load_image_b64(url: str) -> str:
    if not url:
        return ""
    image_content: bytes = await spotify_client.fetch_image(url)
    if not image_content:
        return ""
    return base64.b64encode(image_content).decode("ascii")


async def get_access_token(user_id: str) -> str:
    user: User = await supabase_client.get_user(user_id)

    if user.is_token_expired():
        try:
            new_token: SpotifyTokenResponse = await spotify_client.refresh_token(user.refresh_token)
            expired_time: int = int(time()) + new_token.expires_in

            await supabase_client.update_token(user_id, new_token.access_token, expired_time)

            return new_token.access_token
        except TokenRefreshError as exc:
            raise HTTPException(status_code=401, detail="Token refresh failed. Please login again.") from exc

    return user.access_token


async def render_spotify_svg(
    item: SpotifyItem,
    theme: str,
    is_now_playing: bool,
    needs_cover_image: bool,
    bars_when_not_listening: bool,
    hide_status: bool,
    color_theme: str,
    title_color: str = "",
    text_color: str = "",
    bg_color: str = "",
) -> str:
    img: str = await load_image_b64(item.image_url) if item.image_url and needs_cover_image else ""
    artist_name: str = str(escape(item.artist))
    song_name: str = str(escape(item.name))

    dimensions = get_theme_dimensions(theme)
    width: int = dimensions["width"]
    height: int = dimensions["height"]
    num_bar: int = dimensions["num_bar"]

    colors = get_theme_colors(color_theme, title_color, text_color, bg_color)

    content_bar: str = "".join(["<div class='bar'></div>" for _ in range(num_bar)])
    css_bar: str = generate_bar(num_bar)

    title_text: str
    if is_now_playing:
        title_text = random.choice(STATUS_TEXTS[True]) + ":"
    else:
        title_text = random.choice(STATUS_TEXTS[False]) + ":"
        if not bars_when_not_listening:
            content_bar = ""

    template_name: str = f"spotify.{theme}.html.j2"
    rendered_data: dict[str, str | int | bool] = {
        "width": width,
        "height": height,
        "num_bar": num_bar,
        "content_bar": content_bar,
        "css_bar": css_bar,
        "status": title_text,
        "artist_name": artist_name,
        "song_name": song_name,
        "img": img,
        "is_now_playing": is_now_playing,
        "explicit": item.is_explicit,
        "show_animation": len(song_name) > 27,
        "needs_cover_image": needs_cover_image,
        "hide_status": hide_status,
        "bg_color": colors["bg_color"],
        "title_color": colors["title_color"],
        "text_color": colors["text_color"],
    }

    return templates.env.get_template(template_name).render(**rendered_data)
