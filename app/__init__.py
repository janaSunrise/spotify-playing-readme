import base64
import json

import pyrebase
from flask import Flask

from .config import (
    FB_API_KEY,
    FB_DOMAIN,
    FB_PROJECT_ID,
    FB_MESSAGING_ID,
    FB_STORAGE_BUCKET,
    FB_DATABASE_URL,
    FB_SERVICE_ACCOUNT
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

# -- Circular imports --
from app import views

flask_app = Flask(__name__)

views_list = ("callback", "login", "view")
for view in views_list:
    flask_app.register_blueprint(getattr(views, view))
