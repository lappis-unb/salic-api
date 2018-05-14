import pytest
import re

from salic_api.salic_graphql.schema import schema
from .examples import INCENTIVADOR_RESPONSE

INCENTIVADORES_QUERY = """
    query {
            incentivadores {
            nome,
            municipio,
            UF,
            responsavel,
            cgccpf,
            total_doado,
            tipo_pessoa
        }
    }
"""


def check_query_response(query, expected):
    for key, value in query.items():
        assert value == expected[key]


@pytest.mark.usefixtures('db_data')
class TestGraphqlApi:
    def test_get_incentivadores(self):
        incentivadores = schema.execute(INCENTIVADORES_QUERY)

        check_query_response(incentivadores.data['incentivadores'][0],
                             INCENTIVADOR_RESPONSE)
