import json
import sys

import requests

sys.path.append('../')
from utils.Timer import Timer

import logging

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

base_address = 'vm-debian:8000'
base_version = 'alpha'

uris = [
    '/projetos/',
]

content_types = [
    "application/json",
    "application/xml"
]


def print_result(response):
    print
    json.dumps(response.json(), indent=4, sort_keys=True)


def call_maker(path, headers={}):
    try:
        response = requests.get(path, headers=headers)
        return response
    except Exception as e:
        print
        str(e)


uri = uris[0]
total_seconds = 0
num_calls = 30
lowest = float('inf')
fastest = 0

for i in range(num_calls):
    print
    "Call # %d" % (i + 1)
    path = 'http://' + base_address + '/' + base_version + uri
    with Timer() as t:
        call_maker(path)
    print
    "Time elapsed : %f" % t.secs
    lowest = t.secs if t.secs < lowest else lowest
    fastest = t.secs if t.secs > fastest else fastest
    total_seconds += t.secs

print
"\n\n\nSeconds total: %f average : %f fastest %f lowest %f" % (
total_seconds, float(total_seconds) / num_calls, lowest, fastest)


# for call in calls:
# 	call.start()
