import os

import pytest

import salic_api.utils
from salic_api.app import create_app
from salic_api.fixtures import make_tables, populate, clear_tables, fixture_for_pytest

salic_api.utils.STATIC_IV = salic_api.utils.TESTING_IV

DIRNAME = os.path.dirname(__file__)
os.environ['TESTING'] = 'true'


#
# Test fixtures
#
@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    app.config['SQL_DRIVER'] = 'memory'
    make_tables(app=app)
    return app


@pytest.yield_fixture
def db_data(app):
    try:
        populate(app=app)
        yield ()
    finally:
        clear_tables()


@pytest.fixture
def example():
    return lambda x: os.path.join(DIRNAME, 'restapi', 'examples', x)
