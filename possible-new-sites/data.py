import json
import sys
import requests


class DataRetriever:
    def __init__(self):
        self._cache = {}

    def get_closest_systems(self, x, y, z, radius=10):
        # first check the mem cache
        key = (x, y, z)
        if key in self._cache.keys():
            print('Retrieved data for: {} from cache'.format(key))
            return self._cache[key]
        systems = self.get_data_from_edsm(x=x, y=y, z=z, radius=radius)
        # flatten the list
        system_names = [system['name'] for system in systems]
        self.store_in_cache(key=key, result=system_names)
        return system_names

    def get_data_from_edsm(self, x, y, z, radius):
        url = 'https://www.edsm.net/api-v1/sphere-systems'
        print('Pinging EDSM with following params: [{}, {}, {}], R: {}'.format(
            x, y, z, radius
        ))
        response = requests.get(url=url, params=[('x', x), ('y', y), ('z', z), ('radius', round(radius, 2))])
        return json.loads(response.text)

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

    def store_in_cache(self, key, result):
        self._cache[key] = result
        size = round(sys.getsizeof(self._cache) / 1024, 2)
        print('Added results: {} to key: {}'.format(result, key))
        print('Cache has grown to: {}kB'.format(size))


if __name__ == '__main__':
    retriever = DataRetriever()
    sites = retriever.get_closest_systems(x=-90.75, y=-267.25, z=-309.625, radius=5)
    assert 1 == len(sites)
    assert 'Aries Dark Region FG-Y d18' == sites[0]
