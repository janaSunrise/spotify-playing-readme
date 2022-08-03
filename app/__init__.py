from .core.app import app
from .routes import health

app.register_blueprint(health.blueprint)
