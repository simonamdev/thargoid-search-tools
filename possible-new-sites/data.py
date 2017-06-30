import json

import requests


class Data:
    def __init__(self, system_name, radii):
        self._system_name = system_name
        self._radii = radii

    def generate_params(self):
        return [
            [('systemName', self._system_name), ('radius', radius)] for radius in self._radii
        ]

    def ping_edsm(self):
        responses = self.get_data()
        possible_sites = self.format_data(responses=responses)
        return possible_sites

    def get_data(self):
        url = 'https://www.edsm.net/api-v1/sphere-systems'
        params = self.generate_params()
        responses = []
        for param in params:
            print('Pinging on parameters: {}'.format(param))
            responses.append(requests.get(url=url, params=param))
        return responses

    def format_data(self, responses):
        # flatten the responses
        possible_sites = set()
        for response in responses:
            site_data_set = json.loads(response.text)
            for site_data in site_data_set:
                # skip the site if it is the system we are in
                if site_data['name'] == self._system_name:
                    continue
                possible_sites.add(site_data['name'])
        return possible_sites


if __name__ == '__main__':
    data = Data('HIP 15443', [5.3, 2.5, 0.1])
    sites = data.ping_edsm()
    print(sites)
