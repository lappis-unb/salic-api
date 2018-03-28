from .test_utils import *

class TestFornecedor:
    def test_list_and_detail_fields(self):
        validates_list_and_detail('fornecedores')

    def test_fornecedor_produtos(self):
        # TODO check why there are some cgccpfs coming null
        salic, api = make_request('fornecedores')
        salic_products = salic['_embedded']['fornecedores'] \
        [0]['_links']['produtos']
        api_products = api['_embedded']['fornecedores'] \
        [0]['_links']['produtos']

        result_salic = requests.get(salic_products)
        salic_data = json.loads(result_salic.text)
        result_api = requests.get("http://localhost:5000/" + api_products)
        api_data = json.loads(result_api.text)

        validates_list_and_detail('produtos', salic_data, api_data)
