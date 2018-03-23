import operator

from sqlalchemy import func

from ..connector import SqlConnector


class Query:
    """
    Base class for all query objects for the SALIC api.
    """

    session = property(lambda self: self.sql_connector.session)
    labels_to_fields = ()  # Override on child
    fields_already_filtered = {}

    @property
    def query_fields(self):
        return tuple(v.label(k) for k, v in self.labels_to_fields.items())

    def __init__(self):
        self.sql_connector = SqlConnector()

    def query(self, **kwargs):
        raise NotImplementedError('must be implemented on subclass')

    def all(self, **kwargs):
        return self.query(**kwargs).all()

    def fetch(self, query, binds=None):
        """
        Execute the given query and fetches all results.

        Args:
            query:
                An SQL query
            binds:
                An optional dictionary with binds from variable names to their
                corresponding values to be inserted into the query.
        """
        return self.execute_query(query, binds or {}).fetchall()

    def raw_query(self, *args, **kwargs):
        """
        Create a raw SQLAlchemy query object in the current session.
        """
        return self.session.query(*args, **kwargs)

    def execute_query(self, query, *args, **kwargs):
        """
        Execute an SQL query.
        """
        return self.session.execute(query, *args, **kwargs)

    def count(self, qs):
        """
        Return the number of elements on queryset.
        """
        count_q = qs.statement.with_only_columns([func.count()]).order_by(None)
        count = qs.session.execute(count_q).scalar()
        return count or 0

    def select_as(self, *args, **kwargs):
        """
        Apply all filters in the given dictionary.

        >>> q.select_as(                                     # doctest: +SKIP
        ...     ModelA, {'field_a': value_a, 'field_b': value_b},
        ...     ModelB, {'field_c': value_c})

        If a single model is present, the query can be simpler:

        >>> q.select_as(ModelA,                              # doctest: +SKIP
        ...                field_a=value_a,
        ...                field_b=value_b)
        """
        if kwargs:
            arg_list = _query_args(*args, kwargs)
        else:
            models = args[::2]
            mappings = args[1::2]
            arg_list = []
            for model, mapping in zip(models, mappings):
                arg_list.extend(_query_args(model, mapping))

        return self.raw_query(*arg_list)


def _query_args(model, mapping):
    assert isinstance(mapping, dict)

    arg_list = []
    for attr, label in mapping.items():
        arg_list.append(getattr(model, attr).label(label))
    return arg_list


def filter_query(query, filters, op=operator.eq):
    """
    Apply filter to query excluding null values.

    Args:
        query:
            A SQL query.
        filters:
            A list of tuples of fields to value associations or a mapping.
        op:
            An optional function used as an operator. If not given, it tests
            for equality. It can also use other functions, specially those on
            the operator module such as operator.gt, operator.lt, etc.

    Examples:
    >>> filter_query(query, {Model.Column1: value1, Model.Column1: value1})
    """
    if isinstance(filters, dict):
        filters = filters.items()
    for k, v in filters:
        if v is not None:
            query = query.filter(op(k, v))
    return query


def filter_query_like(query, data):
    if isinstance(data, dict):
        data = data.items()
    for k, v in data:
        if v is not None:
            query = query.filter(k.like('%{}%'.format(v)))
    return query
