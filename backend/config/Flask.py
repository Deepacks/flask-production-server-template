from flask import Flask
from flask_jwt_extended import JWTManager


def configure_flask():
    from app_cfg import app_cfg
    app = Flask("FlaskTemplate")

    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = app_cfg["jwt"]["secret"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "Bearer"
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 60 * 60
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    jwt = JWTManager(app)

    # Configure db
    app.config["MONGODB_SETTINGS"] = {
        "host": app_cfg["mongo"]["host"],
    }

    return app
