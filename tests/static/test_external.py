import pytest
import requests


@pytest.mark.slow
class TestSalicEntryPointsV1:
    def absolute_url(self, url):
        return 'http://api.salic.cultura.gov.br/v1/' + url.lstrip('/')

    def fetch_json(self, url):
        absolute_url = self.absolute_url(url)
        result = requests.get(absolute_url)
        print('URL:', absolute_url)
        assert result.status_code == 200
        return result.json()

    def check_has_links_and_embedded(self, json, url=None):
        assert '_links' in json
        assert isinstance(json['_links'], dict)
        if url is not None:
            assert json['_links']['self'] == url
        assert '_embedded' in json
        assert isinstance(json['_embedded'], dict)

    def check_is_in(self, data, list_of_objects):
        for obj in data:
            assert obj in list_of_objects

    #
    # Unit tests
    #
    def test_areas(self):
        data = self.fetch_json('projetos/areas/')
        self.check_has_links_and_embedded(data)
        self.check_is_in(Data.projetos_areas, data['_embedded']['areas'])

    def test_segmentos(self):
        data = self.fetch_json('projetos/segmentos/')
        self.check_has_links_and_embedded(data)
        self.check_is_in(Data.projetos_segmentos,
                         data['_embedded']['segmentos'])


class Data:
    """
    Expected JSON examples for selected entry points
    """

    projetos_areas = [
        {
            "codigo": "1",
            "_links": {
                "self": "http://api.salic.cultura.gov.br/v1/projetos/?area=1"
            },
            "nome": "Artes Cênicas"
        },
        {
            "codigo": "2",
            "_links": {
                "self": "http://api.salic.cultura.gov.br/v1/projetos/?area=2"
            },
            "nome": "Audiovisual"
        },
        {
            "codigo": "3",
            "_links": {
                "self": "http://api.salic.cultura.gov.br/v1/projetos/?area=3"
            },
            "nome": "Música"
        },
    ]

    projetos_segmentos = [
        {
            "codigo": "1A",
            "_links": {
                "self": "http://api.salic.cultura.gov.br/v1/projetos/?segmento=1A"
            },
            "nome": "Teatro de  bonecos e congêneres"
        },
        {
            "codigo": "1B",
            "_links": {
                "self": "http://api.salic.cultura.gov.br/v1/projetos/?segmento=1B"
            },
            "nome": "Desfile de  de escola de samba"
        },
        {
            "codigo": "1C",
            "_links": {
                "self": "http://api.salic.cultura.gov.br/v1/projetos/?segmento=1C"
            },
            "nome": "Desfile de bloco carnavalesco"
        },
    ]
