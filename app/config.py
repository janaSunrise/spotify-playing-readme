from typing import cast

from decouple import config


class Config:
    DEBUG = cast(bool, config("DEBUG", default=False, cast=bool))
    BASE_URL = cast(str, config("BASE_URL"))

    SPOTIFY_CLIENT_ID = cast(str, config("SPOTIFY_CLIENT_ID"))
    SPOTIFY_CLIENT_SECRET = cast(str, config("SPOTIFY_CLIENT_SECRET"))
    SPOTIFY_SCOPES = [
        "user-read-currently-playing",
        "user-read-recently-played",
        "user-top-read",
    ]

    SUPABASE_URL = cast(str, config("SUPABASE_URL"))
    SUPABASE_KEY = cast(str, config("SUPABASE_KEY"))

    REDIRECT_URI = BASE_URL + "/dashboard"

    GITHUB_URL = "https://github.com/janaSunrise/spotify-playing-readme"
