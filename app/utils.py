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
from app.templates import templates

VALID_THEMES = {"default", "apple"}
MAX_TEXT_LENGTH = 30
COLOR_THEMES = {
    "light": {
        "bg": "#ffffff",
        "text": "#1e293b",
        "accent": "#3b82f6",
        "status": "#64748b",
    },
    "dark": {
        "bg": "#1c1c1e",
        "text": "#f5f5f7",
        "accent": "#0a84ff",
        "status": "#98989d",
    },
    "purple": {
        "bg": "#faf5ff",
        "text": "#4c1d95",
        "accent": "#a855f7",
        "status": "#7c3aed",
    },
    "blue": {
        "bg": "#eff6ff",
        "text": "#1e40af",
        "accent": "#3b82f6",
        "status": "#3b82f6",
    },
    "green": {
        "bg": "#f0fdf4",
        "text": "#166534",
        "accent": "#22c55e",
        "status": "#16a34a",
    },
    "orange": {
        "bg": "#fff7ed",
        "text": "#9a3412",
        "accent": "#f97316",
        "status": "#ea580c",
    },
    "slate": {
        "bg": "#f8fafc",
        "text": "#0f172a",
        "accent": "#475569",
        "status": "#64748b",
    },
}

VALID_COLOR_THEMES = set(COLOR_THEMES.keys())


def validate_theme(theme: str | None) -> str:
    if not theme:
        return "default"
    normalized = theme.lower().strip()
    return normalized if normalized in VALID_THEMES else "default"


def validate_color_theme(color_theme: str | None) -> str:
    if not color_theme:
        return "light"
    normalized = color_theme.lower().strip()
    return normalized if normalized in VALID_COLOR_THEMES else "light"


def get_color_theme(color_theme: str | None) -> dict[str, str]:
    validated = validate_color_theme(color_theme)
    return COLOR_THEMES[validated]


def generate_bar(bar_count: int = 40) -> str:
    css_bar: str = ""

    for i in range(1, bar_count + 1):
        anim = random.randint(400, 800)
        delay = random.randint(0, 400)
        css_bar += dedent(f"""
        .bar:nth-child({i}) {{
            animation-duration: {anim}ms;
            animation-delay: -{delay}ms;
        }}
        """)

    return css_bar


async def load_image_b64(url: str) -> str:
    if not url:
        return ""
    image_content = await spotify_client.fetch_image(url)
    if not image_content:
        return ""
    return base64.b64encode(image_content).decode("ascii")


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
    theme: str | None = None,
    color_theme: str | None = None,
) -> str:
    img = await load_image_b64(item.image_url) if item.image_url and needs_cover_image else ""
    artist_name = str(escape(item.artist))
    song_name = str(escape(item.name))

    validated_theme = validate_theme(theme)
    colors = get_color_theme(color_theme)
    is_dark_mode = validate_color_theme(color_theme) == "dark"

    # Need to change these values to std.
    width = 350
    height = 140
    num_bar = 40

    content_bar = "".join(["<div class='bar'></div>" for _ in range(num_bar)]) if is_now_playing else ""
    css_bar = generate_bar(num_bar) if is_now_playing else ""

    status = "Currently playing:" if is_now_playing else "Last listened to:"

    template_name = f"spotify.{validated_theme}.html.j2"
    rendered_data = {
        "width": width,
        "height": height,
        "num_bar": num_bar,
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
