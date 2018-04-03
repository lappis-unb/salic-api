import csv
import datetime
import decimal
import io
import json
import logging

import dicttoxml


def listify_queryset(queryset):
    """
    Returns a fully serializable list of dictionaries
    """
    return list(map(convert_object, queryset))


def serialize(data, format, **kwargs):
    """
    Return a string of serialized data for the given output format.
    """
    if format == 'xml':
        return to_xml(data, **kwargs)
    elif format == 'json':
        return to_json(data, **kwargs)
    elif format == 'csv':
        return to_csv(data, **kwargs)
    else:
        raise ValueError('invalid format: %s' % format)


def convert_atom(x):
    """
    Convert atomic Python data type to JSON compatible value.
    """
    if isinstance(x, decimal.Decimal):
        return float(x)
    elif isinstance(x, datetime.date):
        return str(x)
    return x


def convert_object(x):
    """
    Convert an instance of a queryset to a JSON compatible value.
    """
    return dict(zip(x.keys(), map(convert_atom, x)))


def to_xml(data):
    return dicttoxml.dicttoxml(data)


def to_json(data):
    return json.dumps(data, ensure_ascii=False)


def to_csv(data, columns):
    if isinstance(data, dict):
        data = [data]

    file = io.StringIO()
    writer = csv.DictWriter(file, columns)
    writer.writeheader()
    for row in data:
        filtered_row = {key: row[key] for key in row if key in columns}
        writer.writerow(filtered_row)
    return file.getvalue()
