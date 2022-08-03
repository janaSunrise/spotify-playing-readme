from .config import Config
from .core.app import app

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
