from flask import Flask
from supabase.client import create_client

from .config import Config
from .lib.spotify import Spotify

app = Flask(__name__)

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

spotify = Spotify(Config.SPOTIFY_CLIENT_ID, Config.SPOTIFY_CLIENT_SECRET)
