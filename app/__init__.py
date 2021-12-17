import base64
import json

import pyrebase
from flask import Flask

from .config import (
    FB_API_KEY,
    FB_DATABASE_URL,
    FB_DOMAIN,
    FB_MESSAGING_ID,
    FB_PROJECT_ID,
    FB_SERVICE_ACCOUNT,
    FB_STORAGE_BUCKET
)

config = {
    "apiKey": FB_API_KEY,
    "authDomain": FB_DOMAIN,
    "databaseURL": FB_DATABASE_URL,
    "projectId": FB_PROJECT_ID,
    "storageBucket": FB_STORAGE_BUCKET,
    "messagingSenderId": FB_MESSAGING_ID,
    "serviceAccount": json.loads(base64.b64decode(FB_SERVICE_ACCOUNT).decode())
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

# Preventing circular imports
from app import views  # noqa: E402, F401, I100, I202

flask_app = Flask(__name__)

views_list = ("base", "auth", "view")
for view in views_list:
    flask_app.register_blueprint(getattr(views, view))
