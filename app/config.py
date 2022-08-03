from typing import cast

from decouple import config


class Config:
    DEBUG = cast(bool, config("DEBUG", default=False, cast=bool))
    BASE_URL = cast(str, config("BASE_URL"))

    SPOTIFY_CLIENT_ID = cast(str, config("SPOTIFY_CLIENT_ID"))
    SPOTIFY_CLIENT_SECRET = cast(str, config("SPOTIFY_CLIENT_SECRET"))

    SUPABASE_URL = cast(str, config("SUPABASE_URL"))
    SUPABASE_KEY = cast(str, config("SUPABASE_KEY"))

    GITHUB_URL = "https://github.com/janaSunrise/spotify-playing-readme"


class SpotifyScopes:
    LISTENING_TO = [
        "user-read-currently-playing",
        "user-read-recently-played",
    ]

    TOP_TRACKS = ["user-top-read"]

    ALL_SCOPES = LISTENING_TO + TOP_TRACKS
