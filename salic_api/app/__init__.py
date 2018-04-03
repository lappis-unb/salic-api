import os

from flask import Flask

from .rate_limiting import limiter

dirname = os.path.join
STATIC_URL_PATH = dirname(os.path.dirname(os.path.dirname(__file__)), 'static')


def create_app():
    from .urls import make_urls
    from .general_config import ENVIRONMENT

    app = Flask(__name__, static_url_path=STATIC_URL_PATH)
    app.config.from_pyfile(ENVIRONMENT)

    make_urls(app)
    return app
