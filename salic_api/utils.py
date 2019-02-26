import codecs
import logging
import time
import os
from contextlib import contextmanager
from hashlib import md5
from html.parser import HTMLParser

from Crypto import Random
from Crypto.Cipher import AES
from flask import current_app as app
from flask import Response

from .resources.query import Query

import simplejson

SECRET_KEY = ('1234' * 4).encode('ascii')
TESTING_IV = b'0123456789abcdef'
STATIC_IV = None

log = logging.getLogger('salic-api')


@contextmanager
def timer(action, verbose=True):
    """
    Log results for the time required to execute the given action.

    Used as a context manager:
    >>> with timer('foo'):
    ...     print('hello world!')
    """

    start = time.time()
    if verbose:
        log.debug('Start action: %r' % action)
    try:
        yield
    finally:
        msecs = (time.time() - start) * 1000
        if verbose:
            log.debug('Action completed in %f ms' % msecs)


def pc_quote(st):
    """
    Comenta string com sinais de '%'
    """
    return '%{}%'.format(st)


def url_key():
    return app.config['URL_KEY'].rjust(16).encode('ascii')


def encrypt(text):
    """
    Uses AES to encrypt text with a global secret key.

    It saves the initialization vector with the resulting message.
    """
    if text is None:
        log.debug("None text on encrypt")
        return ""

    if STATIC_IV is None:
        iv = Random.new().read(AES.block_size)
    else:
        iv = STATIC_IV

    cipher = AES.new(SECRET_KEY, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(text.encode('utf8'))
    return codecs.encode(msg, 'hex').decode('ascii')


def decrypt(text):
    """
    Uses AES to decrypt text with a global secret key.

    It extracts the initialization vector from the input message.
    """

    msg = codecs.decode(text.encode('ascii'), 'hex')
    iv = msg[:AES.block_size]

    if len(iv) != AES.block_size:
        return 'invalid'

    cipher = AES.new(SECRET_KEY, AES.MODE_CFB, iv)
    decoded = cipher.decrypt(msg[AES.block_size:])

    try:
        return decoded.decode('utf8')
    except Exception:
        return 'invalid'


def md5hash(text):
    return md5(text.encode('utf8')).hexdigest()


class MLStripper(HTMLParser):
    """
    Strip HTML from strings in Python
    Has some fixes to the stackoverflow version
    https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    """

    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, data):
        if not isinstance(self.fed, list):
            self.fed = []

        if isinstance(data, str):
            self.fed.append(data)
        else:
            log.debug(
                'MLStripper: data must be a str, but it is %s' % type(data))
            self.fed.append("")

    def get_data(self):
        return "".join(self.fed)

    def strip_tags(self, html):
        if not isinstance(html, str):
            return ""

        self.feed(html)
        data = self.get_data()
        self.fed = []

        return data

def get_sql_query(file_path):
    file = open(file_path, 'r')
    sql_query = file.read()
    file.close()
    return sql_query


def get_sql_results(file_path):
    query_result = Query().fetch(get_sql_query(file_path))
    json = simplejson.dumps(dict(query_result), use_decimal=True, sort_keys=True)
    response = Response(json, status=200, mimetype='application/json')

    return response
