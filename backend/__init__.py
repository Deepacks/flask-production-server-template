import yaml
from flask_mongoengine import MongoEngine

from app_cfg import load_app_cfg
from backend.config.Flask import configure_flask
from backend.routes import add_routes_to_app

db = MongoEngine()


def make_app(config_file="./yamls/config.yaml"):

    with open(config_file, "r") as config:
        read_config = yaml.load(config, Loader=yaml.FullLoader)
        load_app_cfg(read_config)

    app = configure_flask()

    db.init_app(app)
    add_routes_to_app(app)

    return app
