import json
import sys
import requests
import numpy

import trilaterate

# Merope
center_merope = numpy.array([-78.59375, -149.625, -340.53125])
# Col 70 Sector FY-N C21-3
center_col70 = numpy.array([687.0625, -362.53125, -697.0625])


class DataRetriever:
    def __init__(self):
        self._cache = {}

    def get_possible_systems(self, coordinates, distances):
        center_origin = numpy.array(coordinates)
        possible_distances = (
            [distances[0], distances[1], distances[2]],
            [distances[0], distances[2], distances[1]],
            [distances[1], distances[0], distances[2]],
            [distances[1], distances[2], distances[0]],
            [distances[2], distances[1], distances[0]]
        )
        possible_coordinates = []
        for distance_list in possible_distances:
            print('Using distances: {}'.format(distance_list))
            try:
                answer = trilaterate.trilaterate(center_merope, center_col70, center_origin, distance_list[0], distance_list[1], distance_list[2])
                possible_coordinates.append(answer[0])
                possible_coordinates.append(answer[1])
            except Exception as e:
                print(e)
        possible_systems = []
        for coordinates in possible_coordinates:
            systems = self.get_closest_systems(coordinates[0], coordinates[1], coordinates[2], 5)
            possible_systems.extend(systems)
        return possible_systems

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
