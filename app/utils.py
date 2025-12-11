import base64
import random
from collections.abc import Callable
from textwrap import dedent
from time import time
from typing import Any

import httpx
from fastapi import HTTPException
from markupsafe import escape

from app.exceptions import TokenRefreshError
from app.lib import spotify_client, supabase_client
from app.models.user import User
from app.themes import THEMES


async def get_access_token(uid: str) -> str:
    user = await supabase_client.get_user(uid)

    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist. Please login first.")

    # Check if token is expired
    if user.is_token_expired():
        # Refresh the token
        try:
            new_token = await spotify_client.refresh_token(user.refresh_token)
            expired_time = int(time()) + new_token["expires_in"]

            # Update in database
            await supabase_client.update_token(uid, new_token["access_token"], expired_time)

            return new_token["access_token"]
        except TokenRefreshError as exc:
            raise HTTPException(status_code=401, detail="Token refresh failed. Please login again.") from exc

    return user.access_token


async def create_or_update_user(user_id: str, token_data: dict) -> User:
    user = User(
        id=user_id,
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        token_type=token_data.get("token_type", "Bearer"),
        expires_in=token_data.get("expires_in"),
        scope=token_data.get("scope"),
        expired_time=int(time()) + token_data.get("expires_in", 3600),
    )

    return await supabase_client.upsert_user(user)


def generate_bar(bar_count: int = 75) -> str:
    css_bar = ""
    left = 1

    for i in range(1, bar_count + 1):
        anim = random.randint(300, 600)
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
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
    return base64.b64encode(response.content).decode("ascii")


async def render_spotify_svg(
    item: dict[str, Any],
    theme: str,
    is_now_playing: bool,
    needs_cover_image: bool,
    bars_when_not_listening: bool,
    hide_status: bool,
    color_theme: str,
    title_color: str,
    text_color: str,
    bg_color: str,
    template_render: Callable[[str], str],
) -> str:
    """Render Spotify widget SVG using template."""
    currently_playing_type = item.get("currently_playing_type", "track")

    # Initialize variables
    img, artist_name, song_name = "", "", ""

    # Get the info
    if currently_playing_type == "track":
        images = item.get("album", {}).get("images", [])
        image_url = images[1]["url"] if len(images) > 1 else images[0]["url"] if images else ""
        img = await load_image_b64(image_url) if image_url and needs_cover_image else ""
        artist_name = item["artists"][0]["name"].replace("&", "&amp;")
        song_name = item["name"].replace("&", "&amp;")
    elif currently_playing_type == "episode":
        images = item.get("images", [])
        image_url = images[1]["url"] if len(images) > 1 else images[0]["url"] if images else ""
        img = await load_image_b64(image_url) if image_url and needs_cover_image else ""
        artist_name = item["show"]["publisher"].replace("&", "&amp;")
        song_name = item["name"].replace("&", "&amp;")

    # Mappings
    title_text_mapping = {
        True: ["Vibing to", "Binging to", "Listening to", "Obsessed with"],
        False: ["Was listening to", "Previously binging to", "Was vibing to"],
    }

    theme_mapping = {
        "plain": {
            "width": 350,
            "height": 140,
            "num_bar": 40,
        },
        "wavy": {
            "width": 480,
            "height": 175,
            "num_bar": 90,
        },
        None: {
            "width": 150,
            "height": 75,
            "num_bar": 15,
        },
    }

    is_explicit = item.get("explicit", False)
    height = theme_mapping[theme]["height"]
    width = theme_mapping[theme]["width"]
    num_bar = theme_mapping[theme]["num_bar"]

    # Theme mapping
    if color_theme not in THEMES:
        color_theme = "none"

    bg_color_final = THEMES[color_theme]["bg_color"]
    title_color_final = THEMES[color_theme]["title_color"]
    text_color_final = THEMES[color_theme]["text_color"]

    # Override with custom colors if provided
    if title_color:
        title_color_final = str(escape(title_color))
    if text_color:
        text_color_final = str(escape(text_color))
    if bg_color:
        bg_color_final = str(escape(bg_color))

    if not bg_color_final:
        bg_color_final = "white"

    # Default color matching
    if not title_color_final and not text_color_final:
        text_color_final, title_color_final = "#212122", "#212122"
    elif not title_color_final and text_color_final:
        title_color_final = text_color_final
    elif title_color_final and not text_color_final:
        text_color_final = title_color_final

    content_bar = "".join(["<div class='bar'></div>" for _ in range(num_bar)])
    css_bar = generate_bar(num_bar)

    if is_now_playing:
        title_text = random.choice(title_text_mapping[True]) + ":"
    else:
        title_text = random.choice(title_text_mapping[False]) + ":"
        if not bars_when_not_listening:
            content_bar = ""

    rendered_data = {
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
        "explicit": is_explicit,
        "show_animation": len(song_name) > 27,
        "needs_cover_image": needs_cover_image,
        "hide_status": hide_status,
        "bg_color": bg_color_final,
        "title_color": title_color_final,
        "text_color": text_color_final,
    }

    return template_render(f"spotify.{theme}.html.j2", **rendered_data)
