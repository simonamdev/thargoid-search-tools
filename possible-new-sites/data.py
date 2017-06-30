import json
import sys
import requests


class DataRetriever:
    def __init__(self):
        self._cache = {}

    @staticmethod
    def generate_params(system_name, radii):
        return [
            [('systemName', system_name), ('radius', radius)] for radius in radii
        ]

    def ping_edsm(self, system_name, radii):
        # first check the mem cache
        key = (system_name, radii[0], radii[1], radii[2])
        if key in self._cache.keys():
            print('Retrieved data for: {} from cache'.format(system_name))
            return self._cache[key]
        responses = self.get_data(system_name=system_name, radii=radii)
        possible_sites = self.format_data(responses=responses, system_name=system_name)
        self.store_in_cache(system_name=system_name, radii=radii, results=possible_sites)
        return possible_sites

    def get_data(self, system_name, radii):
        url = 'https://www.edsm.net/api-v1/sphere-systems'
        params = self.generate_params(system_name, radii=radii)
        print('Pinging EDSM with following params: {}, {}'.format(system_name, radii))
        responses = []
        for param in params:
            # print('Pinging EDSM on parameters: {}'.format(param))
            responses.append(requests.get(url=url, params=param))
        return responses

    def format_data(self, system_name, responses):
        # flatten the responses
        possible_sites = set()
        for response in responses:
            site_data_set = json.loads(response.text)
            for site_data in site_data_set:
                # skip the site if it is the system we are in
                if site_data['name'] == system_name:
                    continue
                possible_sites.add(site_data['name'])
        return possible_sites

    def store_in_cache(self, system_name, radii, results):
        key = (system_name, radii[0], radii[1], radii[2])
        self._cache[key] = results
        size = round(sys.getsizeof(self._cache) / 1024, 2)
        print('Added results: {} to key: {}'.format(results, key))
        print('Cache has grown to: {}kB'.format(size))


if __name__ == '__main__':
    retriever = DataRetriever()
    sites = retriever.ping_edsm(system_name='HIP 15443', radii=[5.3, 2.5, 0.1])
    print(sites)
