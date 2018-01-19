import os

import pytest

from salic_api.app import create_app

DIRNAME = os.path.dirname(__file__)
os.environ['TESTING'] = 'true'


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    return app


@pytest.fixture
def example():
    return lambda x: os.path.join(DIRNAME, 'restapi', 'examples', x)