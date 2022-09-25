from __future__ import annotations

import random
from typing import Any

from flask import Blueprint, render_template, request
from flask.wrappers import Response
from memoization import cached

from ..lib.supabase import get_user
from ..models.song import Song
from ..utils.css import generate_bar
from ..utils.dtype import parse_boolean
from ..utils.spotify import get_song_info
from ..utils.themes import THEMES

blueprint = Blueprint(
    "image", __name__, template_folder="templates", url_prefix="/image"
)

# Constants for the spotify playing image endpoint
STATUS_MAPPING = {
    True: ["Vibing to", "Binging to", "Listening to", "Obsessed with"],
    False: ["Was listening to", "Previously binging to", "Was vibing to"],
}

PLAYING_CONFIG_MAPPING = {
    "simple": {"width": 350, "height": 140, "num_bar": 40},
    "wavy": {"width": 480, "height": 180, "num_bar": 90},
}


# Utility methods
@cached(ttl=5, max_size=128)
def make_spotify_playing_svg(song: Song, params: dict[str, Any]) -> str:
    theme = params["theme"]
    color_theme = params["color_theme"]
    bars_when_not_playing = params["bars_when_not_playing"]

    # Get the dimensions and display parameters.
    height = PLAYING_CONFIG_MAPPING[theme]["height"]
    width = PLAYING_CONFIG_MAPPING[theme]["width"]
    num_bar = PLAYING_CONFIG_MAPPING[theme]["num_bar"]

    if color_theme not in THEMES:
        color_theme = "none"

    # Generate the CSS bar
    content_bar = "".join(["<div class='bar'></div>" for _ in range(num_bar)])
    css_bar = generate_bar(num_bar)

    # Get the status text to be displayed
    if song.is_now_playing:
        status = random.choice(STATUS_MAPPING[True]) + ":"
    else:
        status = random.choice(STATUS_MAPPING[False]) + ":"
        if not bars_when_not_playing:
            content_bar = ""

    render_data = {
        # Basic SVG Metadata
        "height": height,
        "width": width,
        # Animated bars
        "content_bar": content_bar,
        "css_bar": css_bar,
        # Song-related info
        "status": status,
        "song": song,
        # Other metadata
        "show_animation": len(song.name) > 27,
        "display_cover": params["display_cover"],
        "hide_status": params["hide_status"],
        "colors": {
            "background": THEMES[color_theme].background_color,
            "title": THEMES[color_theme].title_color,
            "text": THEMES[color_theme].text_color,
        },
    }

    return render_template(f"image/spotify-playing.{theme}.html.j2", **render_data)


# App Routes
@blueprint.route("/spotify-playing/<user_id>")
def spotify_playing(user_id: str) -> Response:
    theme = request.args.get("theme", default="simple")
    color_theme = request.args.get("color_theme", default="none")

    display_cover = parse_boolean(request.args.get("display_cover", default="true"))
    bars_when_not_playing = parse_boolean(
        request.args.get("bars_when_not_playing", default="true")
    )
    hide_status = parse_boolean(request.args.get("hide_status", default="false"))

    # Get the user from the ID
    user = get_user(user_id)

    if not user:
        return Response(
            "No user found with the ID.", 404
        )  # TODO: Display the error SVG

    song = get_song_info(user_id)

    # Generate SVG and render it.
    params = {
        "theme": theme,
        "color_theme": color_theme,
        "display_cover": display_cover,
        "bars_when_not_playing": bars_when_not_playing,
        "hide_status": hide_status,
    }
    svg = make_spotify_playing_svg(song, params)

    response = Response(svg, mimetype="image/svg+xml")
    response.headers["Cache-Control"] = "s-maxage=1"

    return response


@blueprint.route("/top-tracks/<user_id>")
def top_tracks(user_id: str) -> Response:
    user = get_user(user_id)

    if not user:
        return Response(
            "No user found with the ID.", 404
        )  # TODO: Display the error SVG

    return Response("TODO: Top tracks")


@blueprint.route("/top-artists/<user_id>")
def top_artists(user_id: str) -> Response:
    user = get_user(user_id)

    if not user:
        return Response(
            "No user found with the ID.", 404
        )  # TODO: Display the error SVG

    return Response("TODO: Top artists")
