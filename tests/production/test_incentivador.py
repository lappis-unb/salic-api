from test_utils import *


class TestIncentivador:
    def test_list_and_detail_fields(self):
        validates_list_and_detail('incentivadores')

    def test_incentivador_doacoes_fields(self):
        salic, api = make_request('incentivadores')
        salic_donations_link = salic['_embedded']['incentivadores'] \
        [0]['_links']['doacoes']
        api_donations_link = api['_embedded']['incentivadores'] \
        [0]['_links']['doacoes']

        result_salic = requests.get(salic_donations_link)
        salic_data = json.loads(result_salic.text)
        result_api = requests.get("http://localhost:5000/" + api_donations_link)
        api_data = json.loads(result_api.text)

        validates_list_and_detail('doacoes', salic_data, api_data)
