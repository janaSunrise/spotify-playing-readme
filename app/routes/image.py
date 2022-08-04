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
