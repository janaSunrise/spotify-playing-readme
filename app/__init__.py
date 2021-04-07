from flask import Flask

from .callback import callback
from .login import login

flask_app = Flask(__name__)
flask_app.register_blueprint(login)
flask_app.register_blueprint(callback)
