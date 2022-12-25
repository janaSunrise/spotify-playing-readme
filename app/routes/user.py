from typing import cast

from flask import Blueprint, jsonify
from flask.wrappers import Response

from ..app import spotify
from ..lib.supabase import get_access_token
from ..models.song import Song
from ..models.top_artists import TopArtists
from ..models.top_tracks import TopTracks

blueprint = Blueprint("user", __name__, template_folder="templates", url_prefix="/user")


def song_to_json(song: Song) -> dict[str, str | bool]:
    return {
        "playing": song.is_now_playing,
        "name": song.name,
        "artist": song.artist,
        "album": song.album,
        "is_explicit": song.is_explicit,
        "currently_playing_type": song.currently_playing_type,
        "image_url": song.image_url,
    }


@blueprint.route("/currently-playing/<user_id>")
def currently_playing(user_id: str) -> Response:
    access_token = cast(str, get_access_token(user_id))
    now_playing = spotify.currently_playing(access_token)

    if not now_playing or now_playing["currently_playing_type"] == "ad":
        return jsonify({"playing": False})

    item = now_playing["item"]
    item["currently_playing_type"] = now_playing["currently_playing_type"]
    item["is_now_playing"] = now_playing["is_playing"]

    song = Song.from_json(item)

    return jsonify(song_to_json(song))


@blueprint.route("/recently-played/<user_id>")
def recently_played(user_id: str) -> Response:
    access_token = cast(str, get_access_token(user_id))
    recently_played = spotify.recently_played(access_token)

    songs = []
    for item in recently_played["items"]:
        item["track"]["currently_playing_type"] = "track"
        item["track"]["is_now_playing"] = False

        songs.append(Song.from_json(item["track"]))

    return jsonify([song_to_json(song) for song in songs])


@blueprint.route("/top-artists/<user_id>")
def top_artists(user_id: str) -> Response:
    access_token = cast(str, get_access_token(user_id))
    top_artists = spotify.top_artists(access_token)

    return jsonify(TopArtists.from_json(top_artists))


@blueprint.route("/top-tracks/<user_id>")
def top_tracks(user_id: str) -> Response:
    access_token = cast(str, get_access_token(user_id))
    top_tracks = spotify.top_tracks(access_token)

    return jsonify(TopTracks.from_json(top_tracks))
