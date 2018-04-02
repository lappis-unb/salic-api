import pytest
import requests
import json


salic_url_base = "http://api.salic.cultura.gov.br/v1/"
api_url_base = "http://localhost:5000/v1/"


def make_request(endpoint):
    result_salic = requests.get(salic_url_base + endpoint)
    salic_data = json.loads(result_salic.text)

    result_api = requests.get(api_url_base + endpoint)
    api_data = json.loads(result_api.text)

    return salic_data, api_data

def check_fields(salic_data, api_data, specific_field=None):
    if specific_field is not None:
        salic_data = salic_data.get(specific_field)
        api_data = api_data.get(specific_field)

    for key in salic_data.keys():
        if key not in api_data:
            return False

    return True

def validates_list_and_detail(endpoint, salic_object=None, api_object=None):
    if salic_object and api_object:
        salic, api = salic_object, api_object
    else:
        salic, api = make_request(endpoint)

    assert check_fields(salic, api)
    assert check_fields(salic, api, '_embedded')
    assert check_fields(salic, api, '_links')
    assert check_fields(salic['_embedded'][endpoint][0],
                        api['_embedded'][endpoint][0])
    assert check_fields(salic['_embedded'][endpoint][0]["_links"],
                        api['_embedded'][endpoint][0]["_links"])