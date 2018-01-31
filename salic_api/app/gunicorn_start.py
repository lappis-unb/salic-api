from flask import Flask

from .rate_limiting import limiter


def create_app(config_file='development.cfg'):
    from .urls import make_urls
    from .general_config import ENVIRONMENT

    app = Flask(__name__)
    app.config.from_pyfile(ENVIRONMENT)

    make_urls(app)
    return app

app = create_app()