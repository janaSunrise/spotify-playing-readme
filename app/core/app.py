from flask import Flask
from supabase.client import create_client

from ..config import Config

app = Flask(__name__)

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
