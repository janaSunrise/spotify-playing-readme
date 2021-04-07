from flask import Flask

from .login import login

flask_app = Flask(__name__)
flask_app.register_blueprint(login)
