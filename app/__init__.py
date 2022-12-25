from .app import app
from .routes import auth, dashboard, health, image, user

app.register_blueprint(auth.blueprint)
app.register_blueprint(dashboard.blueprint)
app.register_blueprint(health.blueprint)
app.register_blueprint(image.blueprint)
app.register_blueprint(user.blueprint)
