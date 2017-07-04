# Needs API to be run separately
# TODO: Run the API automatically
import os

import requests

url = 'http://127.0.0.1:10000/v1/unknown-sites'

current_directory = os.path.dirname(__file__)
parent_of_current_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
systems_file = os.path.join(parent_of_current_directory, 'systems_required.txt')
planets_file = os.path.join(parent_of_current_directory, 'planets_required.txt')


required_sites_list = []


systems = []
planets = []
with open(systems_file, 'r') as system_file:
    for row in system_file:
        systems.append(row.strip().upper())


with open(planets_file, 'r') as planet_file:
    for row in planet_file:
        planets.append(row.strip().upper())


# sites = []
# for system, planet in zip(systems, planets):
#     sites.append('{} {}'.format(system, planet))
#
# print(sites)


class TestUnknownSiteAPI:
    def test_all_sites_return_200(self):#
        bad_responded = []
        for system, planet in zip(systems, planets):
            print('Requesting: {} {}'.format(system, planet))
            response = requests.get(url=url, params=[('system', system), ('body', planet)])
            if not response.status_code == 200:
                bad_responded.append((system, planet))
        print(bad_responded)
        error_percentage = (len(bad_responded) / len(systems)) * 100
        print('Error: {}/{} {}%'.format(len(bad_responded), len(systems), error_percentage))
        assert len(bad_responded) == 0
