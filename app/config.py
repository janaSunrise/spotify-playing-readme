import os

# Normal ENV Variables.
BASE_URL = os.getenv("BASE_URL")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")

# Firebase creds
FB_API_KEY = os.getenv("FB_API_KEY")
FB_DOMAIN = os.getenv("FB_DOMAIN")
FB_PROJECT_ID = os.getenv("FB_PROJECT_ID")
FB_STORAGE_BUCKET = os.getenv("FB_STORAGE_BUCKET")
FB_MESSAGING_ID = os.getenv("FB_MESSAGING_ID")
FB_DATABASE_URL = os.getenv("FB_DATABASE_URL")

# Spotify URL config
REDIRECT_URI = BASE_URL + "/callback"

SPOTIFY__BASE_URL = "https://api.spotify.com/v1/me"
SPOTIFY__AUTH_BASE = "https://accounts.spotify.com"

SPOTIFY__GENERATE_TOKEN = SPOTIFY__AUTH_BASE + "/api/token"
SPOTIFY__REFRESH_TOKEN = SPOTIFY__AUTH_BASE + "/api/token"

SPOTIFY__NOW_PLAYING = SPOTIFY__BASE_URL + "/player/currently-playing?additional_types=track,episode"
SPOTIFY__RECENTLY_PLAYED = SPOTIFY__BASE_URL + "/player/recently-played?limit=10"
SPOTIFY__USER_INFO = SPOTIFY__BASE_URL

# Auth URL Spotify
SPOTIFY__LOGIN = (
        f"{SPOTIFY__AUTH_BASE}/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code"
        f"&scope=user-read-currently-playing,user-read-recently-played&redirect_uri={REDIRECT_URI}"
)
