import copy
import json

import pytest

from salic_api import fixtures as ex
from salic_api.resources import InvalidResult
from salic_api.fixtures import examples, FACTORIES
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
                     ex.tbcomprovantepagamentoxplanilhaaprovacao_example,
                     ex.tbarquivo_example, ex.projeto_example, ex.pre_projeto_example]

        with examples(factories):
            url = '/v1/fornecedores/30313233343536373839616263646566e0797636'
            expected = FORNECEDOR_RESPONSE
            check_endpoint(client, url, expected)

class TestErrorResponses:
    def test_invalid_pronac(self, client):
        url = '/v1/projetos/abc'
        message = 'PRONAC must be an integer'
        check_error(client, url, message, 404)

    def test_pronac_not_found(self, client):
        url = '/v1/projetos/123'
        message = "'Projeto' not found at http://localhost/v1/projetos/123"
        check_error(client, url, message, 404)

    def test_invalid_argument(self, client):
        url = '/v1/propostas/?abc=1'
        message = (
            "invalid request arguments: "
            "['abc']. Possible args: ("
            "'acessibilidade', 'data_aceite', 'data_arquivamento', "
            "'data_inicio', 'data_termino', 'democratizacao', "
            "'especificacao_tecnica', 'estrategia_execucao', "
            "'etapa', 'ficha_tecnica', 'format', 'id', 'impacto_ambiental', "
            "'justificativa', 'limit', 'mecanismo', 'nome', 'objetivos', "
            "'offset', 'order', 'resumo', 'sinopse', 'sort')"
            )
        check_error(client, url, message, 500)

    def test_empty_result(self, client):
        with examples(FACTORIES):
            url = '/v1/projetos/?UF=abc'
            message = 'No object was found with your criteria'
            check_error(client, url, message, 404)

    def test_invalid_format(self, client):
        with examples(FACTORIES):
            url = '/v1/projetos/?format=invalid'
            message = 'invalid format'
            check_error(client, url, message, 405)

class TestEndpointPagination:
    def get_data(self, client, limit, offset):
        url = '/v1/propostas/?limit=%s&offset=%s' % (limit, offset)
        data = client.get(url).get_data(as_text=True)
        return json.loads(data)

    def assert_pagination(self, data, total, count, embedded_field, expected_embedded):
        assert data.get('total') == total
        assert data.get('count') == count

        embedded = data.get('_embedded').get(embedded_field)
        for k, v in expected_embedded.items():
            assert embedded[0][k] == v

    def test_preprojetos_list_pagination(self, client):
        with examples([ex.mecanismo_example]):
            with examples([ex.pre_projeto_example], 4):
                data = self.get_data(client, 2, 0)
                self.assert_pagination(data, 4, 2, 'propostas', {'id': 1})

                data = self.get_data(client, 3, 3)
                self.assert_pagination(data, 4, 1, 'propostas', {'id': 4})

    def test_pagination_error(self,client):
        with examples([ex.mecanismo_example]):
            with examples([ex.pre_projeto_example], 4):
                url = '/v1/propostas/?limit=200'
                message = 'Max limit paging exceeded'
                check_error(client, url, message, 405)

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

def check_error(client, url, message, status_code):
    with pytest.raises(InvalidResult) as e:
        client.get(url)
    assert e.value.args[0]['message'] == message
    assert e.value.args[1] == status_code

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
