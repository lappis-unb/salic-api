import copy
import json

import pytest

from salic_api import fixtures as ex
from salic_api.fixtures import examples
from tests.examples import PROJETOS_AREAS, PROJETO_RESPONSE, \
    INCENTIVADOR_RESPONSE, FORNECEDOR_RESPONSE, PROPONENTE_RESPONSE, \
    PREPROJETO_RESPONSE, CAPTACOES_RESPONSE, PRODUTOS_RESPONSE


@pytest.mark.usefixtures('db_data')
class TestCoreUrls:
    valid_core_urls = [
        '/test',
        '/v1/fornecedores',
        '/v1/incentivadores',
        '/v1/proponentes'
    ]

    def test_core_url_examples(self, client):
        for url in self.valid_core_urls:
            assert client.get(url).status_code == 200, url


@pytest.mark.usefixtures('db_data')
class TestEndpoints:
    def test_projetos_areas(self, client):
        url = '/v1/projetos/areas'
        expected = PROJETOS_AREAS
        check_endpoint(client, url, expected)

    def test_projetos_detail(self, client):
        url = '/v1/projetos/20001234'
        expected = PROJETO_RESPONSE
        check_endpoint(client, url, expected)

    def test_projetos_list(self, client):
        url = '/v1/projetos/'
        expected = single_list(PROJETO_RESPONSE, 'projetos')
        check_endpoint(client, url, expected)

    def test_incentivadores_detail(self, client):
        url = '/v1/incentivadores/30313233343536373839616263646566e0797636'
        expected = INCENTIVADOR_RESPONSE
        check_endpoint(client, url, expected)

    def test_incentivadores_list(self, client):
        url = '/v1/incentivadores'
        expected = single_list(INCENTIVADOR_RESPONSE, 'incentivadores')
        check_endpoint(client, url, expected)

    def test_fornecedores_detail(self, client):
        url = '/v1/fornecedores/30313233343536373839616263646566e0797636'
        expected = FORNECEDOR_RESPONSE
        check_endpoint(client, url, expected)

    def test_fornecedores_list(self, client):
        url = '/v1/fornecedores/'
        expected = single_list(FORNECEDOR_RESPONSE, 'fornecedores')
        check_endpoint(client, url, expected)

    def test_preprojetos_detail(self, client):
        url = '/v1/propostas/1'
        expected = PREPROJETO_RESPONSE
        check_endpoint(client, url, expected)

    def _test_preprojetos_list(self, client):
        url = '/v1/propostas/'
        expected = single_list(PREPROJETO_RESPONSE, 'propostas')
        check_endpoint(client, url, expected)

    def test_proponentes_detail(self, client):
        url = '/v1/proponentes/30313233343536373839616263646566e0797636'
        expected = PROPONENTE_RESPONSE
        check_endpoint(client, url, expected)

    def test_proponentes_list(self, client):
        url = '/v1/proponentes/'
        expected = single_list(PROPONENTE_RESPONSE, 'proponentes')
        check_endpoint(client, url, expected)

    def test_projeto_captacoes_list(self, client):
        url = '/v1/projetos/20001234/captacoes'
        expected = CAPTACOES_RESPONSE
        check_endpoint(client, url, expected)

    def test_fornecedor_produtos(self, client):
        url = '/v1/fornecedores/30313233343536373839616263646566e0797636/produtos'
        expected = PRODUTOS_RESPONSE
        check_endpoint(client, url, expected)


class TestEndpointsIsolated:
    def test_fornecedores_detail(self, client):
        factories = [ex.tbcomprovantepagamento_example, ex.agentes_example,
                     ex.tbplanilhaaprovacao_example, ex.nomes_example,
                     ex.tbPlanilhaItens_example, ex.internet_example,
                     ex.tbcomprovantepagamentoxplanilhaaprovacao_example]

        with examples(factories):
            url = '/v1/fornecedores/30313233343536373839616263646566e0797636'
            expected = FORNECEDOR_RESPONSE
            check_endpoint(client, url, expected)


class TestEndpointPagination:
    def test_preprojetos_list_pagination(self, client):

        def get_data(limit, offset):
            url = '/v1/propostas/?limit=%s&offset=%s' % (limit, offset)
            data = client.get(url).get_data(as_text=True)
            return json.loads(data)

        def assert_pagination(total, count, fields):
            assert data.get('total') == total
            assert data.get('count') == count

            for k, v in fields.items():
                assert propostas[0][k] == v

        with examples([ex.mecanismo_example]):
            with examples([ex.pre_projeto_example], 4):

                data = get_data(2, 0)
                propostas = data.get('_embedded').get('propostas')
                assert_pagination(4, 2, {'id': 1})


                data = get_data(3, 3)
                propostas = data.get('_embedded').get('propostas')
                assert_pagination(4, 1, {'id': 4})


def check_endpoint(client, url, expected):
    """
    Tests if response from given url matches the expected object.
    """
    data = client.get(url).get_data(as_text=True)
    data = json.loads(data)
    expected = copy.deepcopy(expected)
    assert sorted(data) == sorted(expected)
    assert data['_links'] == expected['_links']
    for key, value in data.get('_embedded', {}).items():
        assert value == expected.get('_embedded', {})[key]
    assert data == expected


def single_list(item, embed_key, url=None, **kwargs):
    """
    Returns a paginated JSON response that contains a single item in the
    response.
    """
    item = copy.deepcopy(item)
    item.pop('_embedded', None)

    url = url or embed_key
    result = {
        'count': 1,
        '_embedded': {
            embed_key: [
                item,
            ]
        },
        '_links': {
            'self': 'v1/%s/?limit=100&offset=0' % url,
            'first': 'v1/%s/?limit=100&offset=0' % url,
            'last': 'v1/%s/?limit=100&offset=0' % url,
            'next': 'v1/%s/?limit=100&offset=0' % url,
        },
        'total': 1,
    }
    result.update(kwargs)
    return result
