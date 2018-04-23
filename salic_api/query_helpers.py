from flask import request, current_app
from sqlalchemy.sql.functions import sum as sql_sum
from sqlalchemy import desc
from .resources.query import filter_query, filter_query_like
from .resources.error_messages import invalid_request_args_error


def apply_filters(query, query_class, filter_likeable_fields, built_args, transform_args):
    """
    Filter query according to the filtering arguments.
    """
    built_args = transform_args_values(built_args, transform_args)
    query_fields = query_class.labels_to_fields

    def validate_fields(fields_in):
        """
        Take the intersection between the fields requested and the
        query_fields. Do not keep the fields that already have a more
        complex filter on query.
        Eg. {name, email, etc} & {name} -> {name}
        """

        return (set(query_fields) & set(fields_in)) - set(query_class.fields_already_filtered)

    def map_to_column(filter_args):
        """
        Map each filter with a Column name and args value to the query
        Remove from the filter the columns that are a sum
        """
        return {query_fields[field]: built_args[field] for field in
                filter_args if type(query_fields[field]) is not sql_sum}

    filter_args = map_to_column(
        validate_fields(built_args.keys() - filter_likeable_fields)
    )

    filter_args_like = map_to_column(
        validate_fields(built_args.keys() & filter_likeable_fields)
    )

    query = filter_query(query, filter_args)
    query = filter_query_like(query, filter_args_like)

    return query


def transform_args_values(args, transform_args):
    """
    Transform args values from human readable to db values
    Eg. tipo_pessoa=fisica -> tipo_pessoa=1
    """
    for key in args.keys():
        if key in transform_args.keys():
            args[key] = transform_args[key][args[key]]
    return args


def prepare_args(kwargs, fields_dict, request_args):
    """
    Inject all request arguments to the dictionary of arguments.
    """
    argset = set(request.args)
    query_fields = set(fields_dict)
    valid_args = request_args | query_fields

    if not valid_args.issuperset(argset):
        raise invalid_request_args_error(sorted(valid_args), sorted(argset - query_fields))
    args = {k: v for k, v in request.args.items()}
    return dict(kwargs, **args)


def sort_query(query, sort_field, sort_fields, sort_order, default_sort_field, fields_dict):
    """
    Sort query according to sorting arguments.
    """

    if sort_field in sort_fields:
        field = sort_field
    else:
        field = default_sort_field

    if not field:
        return query

    field = fields_dict[field]

    if sort_order == 'desc':
        query = query.order_by(desc(field))
    else:
        query = query.order_by(field)
    return query


def resolve(query_class, list_class, kwargs):
    query = query_class().query()
    query = apply_filters(
        query,
        query_class,
        list_class.filter_likeable_fields,
        kwargs,
        list_class.transform_args
    )
    query = sort_query(
        query,
        kwargs.get('sort'),
        list_class.sort_fields,
        kwargs.get('order','asc'),
        list_class.default_sort_field,
        query_class.labels_to_fields)

    query = query.limit(kwargs.get('limit',
        current_app.config['LIMIT_PAGING']))
    query = query.offset(kwargs.get('offset',0))

    return query
