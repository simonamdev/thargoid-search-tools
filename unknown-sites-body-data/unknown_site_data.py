import csv
import json
import os
import time
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--debug',
    dest='debug',
    action='store_true',
    default=False,
    help='Run in debug mode')
args = parser.parse_args()

# TODO: Add to argument parsing
bodies_required_path = 'us_bodies.txt'
planets_required_file_path = 'planets.txt'
data_directory = 'G:\Workspace\\thargoid-search\\'
systems_file_path = os.path.join(data_directory, 'systems.csv')
bodies_data_path = os.path.join(data_directory, 'bodies.jsonl')
output_file_path = os.path.join(data_directory, 'us_data.json')

start_time = time.time()

required_bodies = []
required_systems = []
print('Retrieving required systems')
with open(bodies_required_path, 'r', encoding='latin-1') as us_bodies:
    for line in us_bodies:
        required_systems.append(line.strip())

print('Retrieving required planets')
required_planets = []
with open(planets_required_file_path, 'r', encoding='latin-1') as us_planets:
    for line in us_planets:
        required_planets.append(line.strip())

print('Required system count: {}'.format(len(required_systems)))
print('Required planet count: {}'.format(len(required_planets)))

data = {}

for system, planet in zip(required_systems, required_planets):
    if system not in data.keys():
        data[system.upper()] = {
            'planets': []
        }
    data[system.upper()]['planets'].append(
        {
            'body': planet,
            'full_name': '{} {}'.format(system.upper(), planet.upper())
        }
    )

# Get the system ID for the required systems and include it in the dict
header_passed = False


def get_system_line():
    # skip the first line, which is the header
    with open(systems_file_path, newline='', encoding='utf-8') as big_file:
        reader = csv.reader(big_file)
        for row in reader:
            global header_passed
            if not header_passed:
                header_passed = True
                continue
            yield row

print('Retrieving System IDs')
lower_case_system_names = [sys.lower() for sys in required_systems]
for system in get_system_line():
    if system[2].lower() in lower_case_system_names:
        data[system[2].upper()]['id'] = int(system[0])

print('Determining missing systems')
missing_system_names = []
for system_name, system_data in data.items():
    if 'id' not in system_data.keys():
        missing_system_names.append(system_name)


print('Missing systems: Count: {} Names: {}'.format(len(missing_system_names), missing_system_names))


def get_body_line():
    with open(bodies_data_path, 'r', encoding='latin-1') as big_file:
        for row in big_file:
            yield json.loads(row)

required_planet_keys = ['system', 'body', 'gravity', 'radius', 'rotational_period', 'surface_temperature', 'earth_masses', 'is_rotational_period_tidally_locked', 'distance_to_arrival']

print('Retrieving planet data')
for line in get_body_line():
    # Skip if not a planet
    if not line['group_name'] == 'Planet':
        continue
    # for each of our bodies, check if the planet name matches
    for system_name, system_data in data.items():
        for planet in system_data['planets']:
            if planet['full_name'].lower() == line['name'].lower():
                # if the name matches, just dump all the body data into the large data structure
                # filter out the keys that aren't relevant
                adapted_data = {}
                for key, value in line.items():
                    if key in required_planet_keys:
                        adapted_data[key] = value
                planet['data'] = adapted_data
                break

planets_missing_data = []
print('Determining planets with missing data')
for system_name, system_data in data.items():
    for planet in system_data['planets']:
        if 'data' not in planet.keys():
            print('Planet without data: {}'.format(planet['full_name']))
            planets_missing_data.append(planet)

print('Planets missing data: {}'.format(len(planets_missing_data)))
print(planets_missing_data)


# For each missing planet, get the data from EDSM instead
print('Retrieving missing planet data from EDSM')
for planet in planets_missing_data:
    url = 'https://www.edsm.net/api-system-v1/bodies'  # ?systemName=Sol
    system_name = planet['full_name'].replace(' {}'.format(planet['body']), '')
    print('Making request for: {}'.format(system_name))
    response = requests.get(url=url, params=[('systemName', system_name)])
    edsm_data = json.loads(response.text)
    print('{} Bodies present in {}'.format(len(edsm_data['bodies']), edsm_data['name']))
    for body in edsm_data['bodies']:
        if body['name'].lower() == planet['full_name'].lower():
            print('{} found'.format(planet['full_name']))
            # adapt the data from EDSM
            adapted_data = {
                'system': system_name,
                'body': planet['body'],
                'gravity': body['gravity'],
                'radius': body['radius'],
                'rotational_period': body['rotationalPeriod'],
                'surface_temperature': body['surfaceTemperature'],
                'earth_masses': body['earthMasses'],
                'is_rotational_period_tidally_locked': body['rotationalPeriodTidallyLocked'],
                'distance_to_arrival': body['distanceToArrival']
            }
            planet['data'] = adapted_data

print('Final planet data count: {} / {}'.format(len(data), len(required_planets)))
print(data)

print('Writing data to file')
with open(output_file_path, 'w') as output_file:
    output_file.write(json.dumps(data))

end_time = time.time()
time = round((end_time - start_time) / 60, 2)
print('Time taken: {} minutes'.format(time))
