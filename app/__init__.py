import base64
import json

import firebase_admin
from flask import Flask

from .config import FIREBASE_CONF

firebase_conf = json.loads(base64.b64decode(FIREBASE_CONF).decode("ascii"))
cred = firebase_admin.credentials.Certificate({
    "type": "service_account",
    "project_id": firebase_conf.get('project_id'),
    "private_key_id": firebase_conf.get('private_key_id'),
    "private_key": firebase_conf.get('private_key'),
    "client_email": firebase_conf.get('client_email'),
    "client_id": firebase_conf.get('client_id'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": firebase_conf.get('client_x509_cert_url')
})
firebase_admin.initialize_app(cred)

database = firebase_admin.firestore.client()

# -- Circular imports --
from .callback import callback
from .login import login
from .view import view

flask_app = Flask(__name__)
flask_app.register_blueprint(login)
flask_app.register_blueprint(callback)
flask_app.register_blueprint(view)
