import logging


log = logging.getLogger('salic-api')

INTERNAL_ERROR = {
    'message': 'internal error',
    'code': 13,
}
INVALID_FORMAT = {
    'message': 'invalid format',
    'code': 55,
}
MAX_LIMIT_PAGING_ERROR = {
    'message': 'Max limit paging exceeded',
    'message_code': 7,
}
INVALID_LIMIT_PAGING_ERROR = {
    'message': 'limit must be an integer',
    'message_code': 7,
}
INVALID_OFFSET_PAGING_ERROR = {
    'message': 'limit must be an integer',
    'message_code': 7,
}
#
# Error factories
#
def internal_error(status_code=500):
    """
    Default 500 internal error.
    """
    log.info('invalid request (%s, code=13)' % status_code)
    return InvalidResult(INTERNAL_ERROR, status_code)

def max_limit_paging_error(status_code=405):
    """
    Raised when paging limit is greater than maximum.
    """
    log.info('limit greater than maximum (%s, code=7)' % status_code)
    return InvalidResult(MAX_LIMIT_PAGING_ERROR, status_code)

def resource_not_found_error(resource_name, base_url):
    """
    Raised when requested object is not found on the databaser.
    """
    return InvalidResult({
        'message': '%r not found at %s' % (resource_name, base_url),
        'message_code': 11
    }, 404)

def invalid_request_args_error(valid_args, invalid_args):
    """
    Raised when user make a request with invalid arguments.
    """
    data = ', '.join(map(repr, valid_args))
    return InvalidResult({
        'message': 'invalid request arguments: {}. Possible args: ({})'.format(invalid_args, data),
        'message_code': 13,  # Is it?
    }, 500)

def empty_query_error():
    """
    Raised when query return no value.
    """
    results = {
        'message': 'No object was found with your criteria',
        'message_code': 11
    }
    return InvalidResult(results, 404)

class InvalidResult(Exception):
    """
    Exception raised for invalid errors
    """

    def __init__(self, message, status_code=500):
        super().__init__(message, status_code)

    def render(self, resource):
        """
        Render error message using the supplied resource renderer.
        """
        payload, status_code = self.args
        return resource.render(payload, status_code=status_code)
