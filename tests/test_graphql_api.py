import pytest

from salic_api.salic_graphql.schema import schema
from .examples import (INCENTIVADOR_RESPONSE, FORNECEDOR_RESPONSE,
                       PRODUTOS_RESPONSE, PROJETO_RESPONSE)


def check_query_response(query, expected):
    for key, value in query.items():
        assert value == expected[key]


@pytest.mark.usefixtures('db_data')
class TestGraphqlApi:
    def test_get_incentivadores(self):
        incentivadores = schema.execute(INCENTIVADORES_QUERY)

        check_query_response(incentivadores.data['incentivadores'][0],
                             INCENTIVADOR_RESPONSE)

    def test_get_fornecedores(self):
        fornecedores = schema.execute(FORNECEDORES_QUERY)

        check_query_response(fornecedores.data['fornecedores'][0],
                             FORNECEDOR_RESPONSE)

    def test_get_fornecedor_produtos(self):
        fornecedores_produtos = schema.execute(PRODUTOS_QUERY)

        check_query_response(
            fornecedores_produtos.data['fornecedores'][0]['produtos'][0],
            PRODUTOS_RESPONSE['_embedded']['produtos'][0])


INCENTIVADORES_QUERY = """
    query {
        incentivadores {
            nome
            municipio
            UF
            responsavel
            cgccpf
            total_doado
            tipo_pessoa
        }
    }
"""

FORNECEDORES_QUERY = """
    query {
        fornecedores {
            nome
            email
        }
    }
"""

PRODUTOS_QUERY = """
    query {
        fornecedores(limit: 1) {
            produtos {
                id_planilha_aprovacao
                justificativa
                data_pagamento
                nome
                cgccpf
                tipo_forma_pagamento
                data_aprovacao
                valor_pagamento
                id_arquivo,
                nr_comprovante
                nome_fornecedor
                id_comprovante_pagamento
                tipo_documento
                nr_documento_pagamento
                nm_arquivo
                PRONAC
            }
        }
    }
"""
