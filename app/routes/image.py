from __future__ import annotations

from typing import Any

from flask import Blueprint, request
from flask.wrappers import Response
from memoization import cached

from ..lib.supabase import get_user
from ..models.song import Song
from ..utils.song import get_song_info

blueprint = Blueprint(
    "image", __name__, template_folder="templates", url_prefix="/image"
)

# Constants for the image endpoint.
STATUS_MAPPING = {
    True: ["Vibing to", "Binging to", "Listening to", "Obsessed with"],
    False: ["Was listening to", "Previously binging to", "Was vibing to"],
}

THEME_DISPLAY_MAPPING = {
    "plain": {"width": 350, "height": 140, "num_bar": 40},
    "wavy": {"width": 480, "height": 175, "num_bar": 90},
    None: {"width": 150, "height": 75, "num_bar": 15},
}


# Utility methods for images
@cached(ttl=5, max_size=128)
def make_svg(song: Song, params: dict[str, Any]) -> None:
    ...  # TODO: Implement


# App Routes
@blueprint.route("/spotify-playing")
def spotify_playing() -> Response:
    user_id = request.args.get("id")

    theme = request.args.get("theme", default="simple")  # noqa: F841
    color_theme = request.args.get("color_theme", default="none")  # noqa: F841

    display_cover = (  # noqa: F841
        True if request.args.get("display_cover", default="true") == "true" else False
    )
    bars_when_not_playing = (  # noqa: F841
        True
        if request.args.get("bars_when_not_playing", default="true") == "true"
        else False
    )
    hide_status = (  # noqa: F841
        True if request.args.get("hide_status", default="true") == "true" else False
    )

    if not user_id:
        return Response("No user id passed.")

    user = get_user(user_id)

    if not user:
        return Response("No user found with the ID.")

    song = get_song_info(user_id)  # noqa: F841

    # TODO: Generate SVG and Render it.
    return Response("TODO.")
