"""
Este módulo contêm classes e funções responsáveis por estabelecer a conexão com
o banco de dados. O SALIC API possui conectores para SQLite (para testes) e
para o MS SQL Server. Futuramente, é possível criar conectores para outros
bancos como postgres ou MySQL.
"""

import logging
import urllib.error
import urllib.parse
import urllib.request

from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

log = logging.getLogger(__file__)

MEMORY_ENGINE = None
ENGINE_MAPPER = {}
register_engine = (lambda name: lambda f: ENGINE_MAPPER.setdefault(name, f))


class SqlConnector:
    """
    Represents a connection with the database.

    Args:
        driver (str):
            An optional string describing which database should be used.
            Valid values are: "sqlite", "memory", "pyodbc" (MS SQL Server),
            "postgres", "pymssql".
        app:
            Optional Flask app instance.
    """

    def __init__(self, driver=None, app=None):
        if app is None:
            app = current_app
        if driver is None:
            driver = app.config['SQL_DRIVER']

        # Start session
        self.engine = load_engine(driver=driver, app=app)
        session_class = sessionmaker(bind=self.engine)
        try:
            self.session = session_class()
            log.info('Connection Openned')
        except Exception:
            log.error('Can\'t create database session')
            raise

    def __del__(self):
        # Close session after query executes
        self.session.close()
        log.info('Database connection closed')


def get_session(driver=None, app=None):
    """
    Return a session for the current SQL connector.

    Accept the same arguments as :class:`salic_api.connector.SqlConnector`
    """
    return SqlConnector(driver=driver, app=app).session


def get_engine(driver=None, app=None):
    """
    Return the engine object for the current SQL connector.

    Accept the same arguments as :class:`salic_api.connector.SqlConnector`
    """
    return SqlConnector(driver=driver, app=app).engine


def load_engine(driver, app=None):
    """
    Return engine for the given driver and config mapping.

    Accept the same arguments as :class:`salic_api.connector.SqlConnector`
    """
    try:
        if driver == 'sqlite':
            engine = sqlite_engine({})
        elif driver == 'memory':
            engine = memory_engine({})
        else:
            if app is None:
                app = current_app
            config = app.config
            engine = ENGINE_MAPPER[driver](config)
    except KeyError:
        msg = 'Unknown SQL driver: %r' % driver
        log.error(msg)
        raise RuntimeError(msg)
    return engine


#
# Register SQL engines
#
@register_engine('sqlite')
def sqlite_engine(config):
    return create_engine('sqlite:///db.sqlite3')


@register_engine('memory')
def memory_engine(config):
    global MEMORY_ENGINE

    if MEMORY_ENGINE is None:
        MEMORY_ENGINE = create_engine('sqlite://')
    return MEMORY_ENGINE


@register_engine('pyodbc')
def pymssql_uri(config):
    quoted = urllib.parse.quote_plus(
        'DRIVER={FreeTDS};Server=%s;Database=%s;UID=%s;PWD=%s;'
        'TDS_Version=8.0;CHARSET=UTF8;Port=%s'
        % (current_app.config['DATABASE_HOST'],
           current_app.config['DATABASE_NAME'],
           current_app.config['DATABASE_USER'],
           current_app.config['DATABASE_PASSWORD'],
           current_app.config['DATABASE_PORT']))

    engine = create_engine(
        'mssql+pyodbc:///?odbc_connect={}'.format(quoted),
        connect_args={'convert_unicode': True})
    engine.dialect.identifier_preparer.initial_quote = ''
    engine.dialect.identifier_preparer.final_quote = ''

    return engine


@register_engine('postgres')
def postgres_engine(config):
    uri = "postgresql://{user}:{pasword}@{host}:{port}/{name}".format(
        user=config['DATABASE_USER'],
        password=config['DATABASE_PASSWORD'],
        host=config['DATABASE_HOST'],
        port=config['DATABASE_PORT'],
        name=config['DATABASE_NAME'],
    )
    return create_engine(uri)


@register_engine('pymssql')
def pymssql_engine(config):
    uri = "mssql+pymssql://{user}:{pasword}@{host}:{port}/{name}".format(
        user=config['DATABASE_USER'],
        password=config['DATABASE_PASSWORD'],
        host=config['DATABASE_HOST'],
        port=config['DATABASE_PORT'],
        name=config['DATABASE_NAME'],
    )
    return create_engine(uri)
