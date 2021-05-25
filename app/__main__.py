from . import flask_app
from .config import DEBUG

if __name__ == "__main__":
    flask_app.run(debug=DEBUG)
