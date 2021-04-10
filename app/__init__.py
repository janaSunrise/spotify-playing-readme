import pyrebase
from flask import Flask

from .config import FB_API_KEY, FB_DOMAIN, FB_PROJECT_ID, FB_MESSAGING_ID, FB_STORAGE_BUCKET, FB_DATABASE_URL

config = {
    "apiKey": FB_API_KEY,
    "authDomain": FB_DOMAIN,
    "databaseURL": FB_DATABASE_URL,
    "projectId": FB_PROJECT_ID,
    "storageBucket": FB_STORAGE_BUCKET,
    "messagingSenderId": FB_MESSAGING_ID,
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

# -- Circular imports --
from .callback import callback
from .login import login
from .view import view

flask_app = Flask(__name__)
flask_app.register_blueprint(login)
flask_app.register_blueprint(callback)
flask_app.register_blueprint(view)
