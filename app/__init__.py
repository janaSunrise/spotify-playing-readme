from .app import app
from .routes import auth, dashboard, health

app.register_blueprint(auth.blueprint)
app.register_blueprint(dashboard.blueprint)
app.register_blueprint(health.blueprint)
