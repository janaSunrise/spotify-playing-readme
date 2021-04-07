import os

BASE_URL = os.getenv("BASE_URL")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")

# Spotify URL config
SPOTIFY__GENERATE_TOKEN = "https://accounts.spotify.com/api/token"
SPOTIFY__REFRESH_TOKEN = "https://accounts.spotify.com/api/token"
REDIRECT_URI = BASE_URL + "/callback"

SPOTIFY__NOW_PLAYING = "https://api.spotify.com/v1/me/player/currently-playing?additional_types=track,episode"
SPOTIFY__RECENTLY_PLAYED = "https://api.spotify.com/v1/me/player/recently-played?limit=10"
SPOTIFY__USER_INFO = "https://api.spotify.com/v1/me"

# Auth URL Spotify
SPOTIFY__LOGIN = (
        f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code"
        f"&scope=user-read-currently-playing,user-read-recently-played&redirect_uri={REDIRECT_URI}"
)
