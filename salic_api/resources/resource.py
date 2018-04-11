import logging
import os

from flask import Response
from flask import current_app
from flask import request
from flask_cache import Cache
from flask_restful import Resource
from sqlalchemy.sql.functions import sum as sql_sum
from sqlalchemy import desc

from .query import filter_query, filter_query_like
from .serialization import serialize, listify_queryset
from ..utils import md5hash, MLStripper

log = logging.getLogger('salic-api')
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
APP_CONFIGURED = False

# Formats and mime types
VALID_FORMATS = {'json', 'xml', 'csv'}
JSON_MIME = 'application/json; charset=utf-8'
CSV_MIME = 'text/csv; charset=utf-8'
XML_MIME = 'application/xml; charset=utf-8'

# Mime map
ACCEPT_HEADERS = {
    'application/xml': 'xml',
    'text/csv': 'csv',
    'application/hal+json': 'json',
    'application/json': 'json',
}

# Headers
ACCESS_CONTROL_HEADERS = (
    "Content-Length, Content-Type, Date, Server, "
    "X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, "
    "Retry-After, "
    "X-Total-Count, "
    "Content-Disposition"
)


class SalicResource(Resource):
    """
    Base class for List and Detail resources.
    """

    # Basics
    resource_path = None
    query_class = None
    csv_columns = None
    request_args = {'format'}
    filter_likeable_fields = {}
    transform_args = {}

    # Pre-defined error messages
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

    def __init__(self, query_data=None):
        init_config()
        self.query_data = query_data
        self.url_args = {}
        self.args = {}

    #
    # Error factories
    #
    def internal_error(self, status_code=500):
        """
        Default 500 internal error.
        """
        log.info('invalid request (%s, code=13)' % status_code)
        return InvalidResult(self.INTERNAL_ERROR, status_code)

    def max_limit_paging_error(self, status_code=405):
        """
        Raised when paging limit is greater than maximum.
        """
        log.info('limit greater than maximum (%s, code=7)' % status_code)
        return InvalidResult(self.MAX_LIMIT_PAGING_ERROR, status_code)

    def resource_not_found_error(self):
        """
        Raised when requested object is not found on the databaser.
        """
        type_name = self.query_class.__name__[:-5]
        return InvalidResult({
            'message': '%r not found at %s' % (type_name, request.base_url),
            'message_code': 11
        }, 404)

    def invalid_request_args_error(self, valid_args, invalid_args):
        """
        Raised when user make a request with invalid arguments.
        """
        data = ', '.join(map(repr, valid_args))
        return InvalidResult({
            'message': 'invalid request arguments: {}. Possible args: ({})'.format(invalid_args,data),
            'message_code': 13,  # Is it?
        }, 500)

    def empty_query_error(self):
        """
        Raised when query return no value.
        """
        results = {
            'message': 'No object was found with your criteria',
            'message_code': 11
        }
        return InvalidResult(results, 404)

    def filter_query(self, query):
        """
        Filter query according to the filtering arguments.
        """
        self.transform_args_values()
        built_args = self.build_query_args()
        query_fields = self.query_class.labels_to_fields

        def validate_fields(fields_in):
            """
            Take the intersection between the fields requested and the
            query_fields. Do not keep the fields that already have a more
            complex filter on query.
            Eg. {name, email, etc} & {name} -> {name}
            """

            return (set(query_fields) & set(fields_in)) - set(self.query_class.fields_already_filtered)

        def map_to_column(filter_args):
            """
            Map each filter with a Column name and args value to the query
            Remove from the filter the columns that are a sum
            """
            return {query_fields[field]: built_args[field] for field in
                filter_args if type(query_fields[field]) is not sql_sum}

        filter_args = map_to_column(
            validate_fields(built_args.keys() - self.filter_likeable_fields)
        )

        filter_args_like = map_to_column(
            validate_fields(built_args.keys() & self.filter_likeable_fields)
        )

        query = filter_query(query, filter_args)
        query = filter_query_like(query, filter_args_like)

        return query

    def transform_args_values(self):
        """
        Transform args values from human readable to db values
        Eg. tipo_pessoa=fisica -> tipo_pessoa=1
        """
        for key in self.args.keys():
            if key in self.transform_args.keys():
                self.args[key] = self.transform_args[key][self.args[key]]

    #
    # HAL links
    #
    def apply_hal_data(self, result):
        """
        Insert HAL information on output data.

        HAL info usually comprises of a _links and a _embedded fields
        """
        raise NotImplementedError('must be implemented on subclass')

    def hal_links(self, result):
        """
        Return the link dictionary that is stored on '_links' field of a
        JSON+HAL response.
        """
        path = self.resource_path
        if path is None:
            return {}
        else:
            return {'self': self.url('/%s/' % path)}

    #
    # Utility functions
    #
    def url(self, *args, **kwargs):
        """
        Return a normalized URL for a path relative to the current resource.

        If path begins with a backslash, treat it as a absolute path relative
        to the API_ROOT_URL.
        """
        base = current_app.config['API_ROOT_URL'].rstrip("/")
        path = '/'.join(args).lstrip("/")
        if kwargs:
            query_args = '?'.join('%s=%s' % item for item in kwargs.items())
            path = '%s?%s' % (path, query_args)
        return '%s/%s' % (base, path.lstrip('/'))

    def filter_cgccpf(self, cgccpf, elements):
        """
        Given a cgc/cpf/cnpj, makes sure it return only elements with exact
        match. Used to correct the use of SQL LIKE statement
        """
        return [e for e in elements if e['cgcpf'] == cgccpf]

    def last_offset(self, n_records, limit):
        if n_records % limit == 0:
            return (n_records / limit - 1) * limit
        else:
            return n_records - (n_records % limit)

    def prepare_args(self, kwargs):
        """
        Inject all request arguments to the dictionary of arguments.
        """
        argset = set(request.args)
        query_fields = set(self.query_class.labels_to_fields)
        valid_args = self.request_args | query_fields

        if not valid_args.issuperset(argset):
            raise self.invalid_request_args_error(sorted(valid_args), sorted(argset-query_fields))
        args = {k: v for k, v in request.args.items()}
        return dict(kwargs, **args)

    #
    # Creating response
    #
    def get(self, **kwargs):
        """
        Default response to a GET request.
        """
        try:
            self.url_args.update(kwargs)
            self.args.update(self.prepare_args(kwargs))

            data = self.fetch_result()
            return self.render(data)

        # Expected errors
        except InvalidResult as error:
            if current_app.testing or DEBUG:
                raise
            return error.render(self)

        # Unexpected errors
        except Exception as ex:
            if current_app.testing or DEBUG:
                raise
            fmt = (type(self).__name__, type(ex).__name__, ex)
            log.error('%s: unhandled exception, %s: %s' % fmt)
            return self.internal_error().render(self)

    def fetch_result(self):
        """
        Happy path for obtaining a raw representation of the resulting object
        from the database.
        """
        raise NotImplementedError('must be implemented on a subclass')

    def query_db(self):
        """
        Return a query with all requested objects
        """
        if self.query_data is not None:
            return self.query_data

        if self.query_class is None:
            raise RuntimeError(
                'improperly configured (%s): please define the query_class for '
                'the current resource or implement the .query_db() '
                'method.' % type(self).__name__
            )

        query_args = self.build_query_args()
        data = self.query_data = self.query_class().query(**query_args)
        return data

    def build_query_args(self):
        """
        Return a dictionary with arguments to be passed to the query method of
        the query class.
        """
        unwanted_args = ('format', 'limit', 'offset', 'sort', 'order')
        args = dict(self.args)

        for arg in unwanted_args:
            args.pop(arg, None)

        return args

    def _csv_response(self, data, headers={}, status_code=200, raw=False):
        """
        Response for CSV content type

        Args:
            data:
                Raw data structure
            headers (dict):
                A mapping with extra headers for inclusion in the response.
            status_code (int):
                HTTP Response status code
            raw (bool):
                If True, do not serialize data to the desired format. Useful
                for testing.
        """
        if not raw:
            if isinstance(self,ListResource):
                columns = self.detail_resource_class.csv_columns
                data = data['_embedded'][self.embedding_field]
            else:
                columns = self.csv_columns

            if columns is None:
                class_name = type(self).__name__
                msg = 'resource %s must define a csv_columns attribute ' \
                    'in order to support CSV' % class_name
                raise RuntimeError(msg)
            data = serialize(data, 'csv', columns=columns)
            resource_path = request.path.split("/")

            if resource_path[len(resource_path) - 1] != "":
                resource_type = resource_path[len(resource_path) - 1]
            else:
                resource_type = resource_path[len(resource_path) - 2]

            args_hash = md5hash(format_args(request.args))
            fmt = (resource_type, args_hash)
            filename = "attachment; filename=salicapi-%s-%s.csv" % fmt
            headers["Content-Disposition"] = filename

        response = Response(data, content_type=CSV_MIME)

        return response

    def render(self, data, headers={}, status_code=200, raw=False):
        """
        Render response for given data.

        Args:
            data:
                Raw data structure
            headers (dict):
                A mapping with extra headers for inclusion in the response.
            status_code (int):
                HTTP Response status code
            raw (bool):
                If True, do not serialize data to the desired format. Useful
                for testing.
        """
        content_type = self.resolve_content()
        headers = {} if headers is None else headers

        if content_type is None:
            raise InvalidResult(self.INVALID_FORMAT, 405)

        if content_type == 'xml':
            if not raw:
                data = serialize(data, 'xml')
            response = Response(data, content_type=XML_MIME)

        elif content_type == 'csv':
            response = self._csv_response(data, headers, status_code, raw)
        else:
            if not raw:
                if status_code == 200:
                    if 'X-Total-Count' in headers:
                        total = headers['X-Total-Count']
                        self.args.setdefault('total', total)

                data = serialize(data, 'json')

            response = Response(data, content_type=JSON_MIME)

        headers['Access-Control-Expose-Headers'] = ACCESS_CONTROL_HEADERS
        response.headers.extend(headers)
        response.status_code = status_code
        real_ip = request.headers.get('X-Real-Ip') or ''
        log.info(' '.join(map(str, [request.path, real_ip, status_code,
                                    response.headers.get('Content-Length')])))
        return response

    def resolve_content(self):
        """
        Content Type resolution.
        """
        try:
            format = request.args['format']
            return format if format in VALID_FORMATS else None
        except KeyError:
            accept = request.headers.get('Accept', 'application/hal+json')
            json_values = ('application/hal+json', 'application/json', '*/*')
            if any(v in accept for v in json_values):
                return 'json'
            elif 'text/csv' in accept:
                return 'csv'
            elif 'application/xml' in accept:
                return 'xml'
            else:
                return None


class ListResource(SalicResource):
    """
    Base class for all Salic-API end points that return lists.
    """

    detail_resource_class = None
    embedding_field = None
    queryset_size = None
    has_pagination = True
    detail_resource = None
    detail_pk = None
    default_sort_field = None
    sort_fields = set()
    request_args = {'format', 'limit', 'offset', 'sort', 'order'}

    @property
    def _embedding_field(self):
        if self.embedding_field is None:
            if self.resource_path is not None and '/' not in self.resource_path:
                return self.resource_path
            else:
                raise RuntimeError(
                    'You must define the embedding_field class attribute for '
                    '%s.' % type(self).__name__
                )
        else:
            return self.embedding_field

    @property
    def limit(self):
        try:
            limit = int(self.args.get('limit', current_app.config['LIMIT_PAGING']))
        except ValueError as error:
            raise InvalidResult(self.INVALID_LIMIT_PAGING_ERROR, 500)
        return limit

    @property
    def offset(self):
        try:
            offset = int(self.args.get('offset', 0))
        except ValueError as error:
            raise InvalidResult(self.INVALID_OFFSET_PAGING_ERROR, 500)
        return offset

    @property
    def sort_field(self):
        return self.args.get('sort', None)

    @property
    def sort_order(self):
        return self.args.get('order', None)

    def __init__(self):
        self.queryset_size = 0
        if self.detail_resource_class is not None:
            self.detail_resource = self.detail_resource_class()
        super().__init__()

    def apply_hal_data(self, result):
        embedding_field = self._embedding_field
        items = result.pop(embedding_field)
        result['_embedded'] = {embedding_field: items}

        # Create pagination links
        if self.has_pagination:
            links = self.hal_pagination_links(items)
        else:
            links = self.hal_links(result)
        if links:
            result['_links'] = links

        return result

    def hal_pagination_links(self, results, limit=None, offset=None):
        """
        Create pagination links: self, first, last, next.
        """
        limit = int(self.limit)
        offset = int(self.offset)
        total = self.queryset_size
        base = self.url(self.resource_path)
        limit = current_app.config['LIMIT_PAGING'] if limit is None else limit
        offset = offset or 0
        pages = total // limit
        if limit > current_app.config['LIMIT_PAGING']:
            raise self.max_limit_paging_error()

        def link(offset):
            return '%s/?limit=%d&offset=%d' % (base, limit, offset)

        return {
            'self': link(offset),
            'next': link(offset + 1 if offset < pages else offset),
            'first': link(0),
            'last': link(pages),
        }

    def query_db(self):
        """
        Return a pair of (queryset, size) with a possibly truncated queryset of
        results and the number of elements in the complete queryset.
        """
        query = super().query_db()
        query = self.filter_query(query)
        query = self.sort_query(query)

        self.queryset_size = query.count()
        limited_query = query.limit(self.limit).offset(self.offset)
        return listify_queryset(limited_query)

    def sort_query(self, query):
        """
        Sort query according to sorting arguments.
        """

        if self.sort_field in self.sort_fields:
            field = self.sort_field
        else:
            field = self.default_sort_field

        if not field:
            return query

        field = self.query_class().labels_to_fields[field]

        if self.sort_order == 'desc':
            query = query.order_by(desc(field))
        else:
            query = query.order_by(field)
        return query

    def fetch_result(self):
        items = self.query_db()
        if len(items) == 0:
            raise self.empty_query_error()
        for item in items:
            self.prepare_item(item)

        result = {self._embedding_field: items}
        self.apply_hal_data(result)
        if self.has_pagination:
            result.update(total=self.queryset_size, count=len(items))
        return result

    def prepare_item(self, item):
        """
        Clean item inserted in the result list.
        """
        if self.detail_resource is None:
            return
        obj = self.prepared_detail_object(item)
        obj.apply_hal_data(item)
        obj.prepare_result(item)
        obj.remove_html(item)

    def prepared_detail_object(self, item):
        """
        Modify list of arguments to pass to a detail resource.
        """
        args = dict(self.args)
        args[self.detail_pk] = item[self.detail_pk]
        args.pop('limit', None)
        args.pop('offset', None)
        self.detail_resource.args = args
        return self.detail_resource

    def render(self, data, headers=None, **kwargs):
        if 'total' in data:
            headers = dict(headers or ())
            headers['X-Total-Count'] = data['total']
        return super().render(data, headers, **kwargs)


class DetailResource(SalicResource):
    """
    Base class for all end points that return dictionaries.
    """
    strip_html_fields = {}

    def apply_hal_data(self, result):
        links = self.hal_links(result)
        embedded = self.hal_embedded(result)
        if links:
            result['_links'] = links
        if embedded:
            result['_embedded'] = embedded
            link_map = self.hal_embedded_links(embedded)
            for name, links in link_map.items():
                for item in embedded[name]:
                    item['_links'] = dict(links)
        return result

    def hal_embedded(self, data):
        """
        Return a dictionary of embedded resources stored at the '_embedded'
        field of a JSON+HAL response.
        """
        return {}

    def hal_embedded_links(self, embedded):
        """
        Return a dictionary mapping each embedded list with its corresponding
        dictionary of links.

        This method does nothing and should be overridden on subclasses.
        """
        return {}

    def query_db(self):
        query = super().query_db()
        query = self.filter_query(query).limit(1)
        query = listify_queryset(query)
        if len(query) == 1:
            obj, = query
        else:
            raise self.resource_not_found_error()
        return obj

    def fetch_result(self):
        result = self.query_db()
        self.insert_related(result)
        self.apply_hal_data(result)
        self.prepare_result(result)
        self.remove_html(result)
        return result

    def remove_html(self, result):
        stripper = MLStripper()
        fields_to_strip = self.strip_html_fields & result.keys()

        for field in fields_to_strip:
            field_data = result.get(field, "")

            if not isinstance(field_data, str):
                continue  # Should only strip strings

            without_html = stripper.strip_tags(field_data)
            result[field] = without_html

    def insert_related(self, result):
        """
        Fetch all related and embedded data from other models and add it to the
        current result.

        The default implementation does nothing, but can be overridden in
        subclasses.
        """

    def prepare_result(self, result):
        """
        Clean result after insertion of related objects.

        The default implementation does nothing, but can be overridden in
        subclasses.
        """


def format_args(args: dict):
    return '&'.join('%s=%s' % item for item in args.items())


def on_request_start():
    content_type = request.headers.get('Accept', '')
    real_ip = request.headers.get('X-Real-Ip', '')
    args = format_args(request.args)
    log.info(' '.join([request.path, args, real_ip, content_type]))


def init_config():
    """
    Initial configuration for the current app. Triggered the first time a
    resource is initialized.
    """

    global APP_CONFIGURED

    if not APP_CONFIGURED:
        # Rate limiting setup
        if current_app.config['RATE_LIMITING_ACTIVE']:
            rate_limit = current_app.config['GLOBAL_RATE_LIMITS']
            log.info('Rate limiting active: %s' % rate_limit)
        else:
            log.info('Rate limiting is off')

        # Caching setup
        if current_app.config['CACHING_ACTIVE']:
            log.info('Caching is active')
        else:
            current_app.config['CACHE_TYPE'] = 'null'
            log.info('Caching is off')
            current_app.config['CACHE_NO_NULL_WARNING'] = True

        # Register the cache instance and binds it on to your app
        if getattr(current_app, 'cache', None) is None:
            current_app.cache = Cache(current_app)
            current_app.cache.clear()
            current_app.before_request(on_request_start)

        APP_CONFIGURED = True


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

