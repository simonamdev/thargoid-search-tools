# Get the required system names
import csv
import json
import os
import time

import requests

start_time = time.time()

required_systems = []
with open('us_bodies.txt', 'r', encoding="latin-1") as us_bodies:
    for line in us_bodies:
        required_systems.append(line.strip().lower())
# print(required_systems)

system_count_required = len(required_systems)

# Find out how many of them are present in the system data

systems_file_path = os.path.join(os.path.dirname(__file__), 'systems.csv')

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

# Get their respective IDs
system_ids = {}

print('Retrieving System data')
for system in get_system_line():
    if system[2].lower() in required_systems:
        # print('{} found'.format(system[2]))
        system_ids[system[2]] = int(system[0])
        continue
    if len(list(system_ids.keys())) == system_count_required:
        break

# print(system_ids)
print('{}/{} IDs found'.format(len(list(system_ids.keys())), system_count_required))

missing_systems = [
    system for system in required_systems if system not in [
        found_system.lower() for found_system in system_ids.keys()
    ]
]

print('Missing systems: {}'.format(missing_systems))

print('Retrieving required planets')
required_planets = []
with open('planets.txt', 'r', encoding="latin-1") as us_planets:
    for line in us_planets:
        required_planets.append(line.strip().lower())

# append the planets to the system names. Order is preserved
required_planets = [
    {
        'system': data[0],
        'body': data[1]
    } for data in zip(required_systems, required_planets)
]
required_planet_names = ['{} {}'.format(planet['system'], planet['body']) for planet in required_planets]


bodies_file_path = os.path.join(os.path.dirname(__file__), 'bodies.jsonl')


def get_body_line():
    with open(bodies_file_path, 'r', encoding="latin-1") as big_file:
        for row in big_file:
            yield json.loads(row)

planet_data = []

print('Retrieving planet data')
for line in get_body_line():
    # Skip if not a planet
    if not line['group_name'] == 'Planet':
        continue
    # Skip if the system ID is not in our required system IDs
    # if not line['system_id'] in system_ids.values():
    #     continue
    # If the planet name matches, return it
    if line['name'].lower() in required_planet_names:
        planet_data.append(line)
    if len(planet_data) == system_count_required:
        break

# print(planet_data)
print('{}/{} Planets retrieved'.format(len(planet_data), system_count_required))

found_planet_names = [
    data['name'].lower() for data in planet_data
]
missing_planet_names = [
    planet['body'] for planet in required_planets if planet['body'] not in found_planet_names
]
print('Missing planets: {}'.format(missing_planet_names))

# filter out the unneeded data
required_keys = ['system', 'body', 'gravity', 'radius', 'rotational_period', 'surface_temperature', 'earth_masses', 'is_rotational_period_tidally_locked', 'distance_to_arrival']

print('Adapting planet data')
adapted_planet_data = []

for planet in planet_data:
    new_planet = {}
    for key, value in planet.items():
        # filter the required keys only
        if key in required_keys:
            new_planet[key] = value
        # add the new system/body key
    for system_name, system_id in system_ids.items():
        if planet['system_id'] == system_id:
            new_planet['system'] = system_name
            new_planet['body'] = planet['name'].replace('{} '.format(system_name), '')
    adapted_planet_data.append(new_planet)


# For each missing planet, get the data from EDSM instead
missing_planets = [planet for planet in required_planets if planet['body'].lower() in missing_planet_names]
missing_body_data = []
print('Retrieving following planets from EDSM: {}'.format(missing_planets))
for planet in missing_planets:
    url = 'https://www.edsm.net/api-system-v1/bodies'
    # url = 'https://www.edsm.net/api-system-v1/bodies?systemName=Sol'
    response = requests.get(url=url, params=[('systemName', planet['system'])])
    data = json.loads(response.text)
    print('{} Bodies present in {}'.format(len(data['bodies']), data['name']))
    for body in data['bodies']:
        full_planet_name = '{} {}'.format(planet['system'], planet['body'])
        if body['name'].lower() == full_planet_name.lower():
            print('{} found'.format(full_planet_name))
            missing_body_data.append(body)

print('Adapting missing planet data')
# we need to convert the EDSM keys to match the other key data
adapted_missing_body_data = []

for body in missing_body_data:
    # SUPER HACKY SPLIT UP OF SYSTEM AND BODY, SORRY :(
    system_name = ''
    body_name = ''
    for missing_planet in missing_planets:
        combined_name = '{} {}'.format(missing_planet['system'], missing_planet['body'])
        if combined_name.lower() == body['name'].lower():
            system_name = body['name'].replace(missing_planet['body'], '')
            body_name = body['name'].replace(missing_planet['system'], '')
            break
    adapted_missing_body_data.append(
        {
            'system': system_name,
            'body': body_name,
            'gravity': body['gravity'],
            'radius': body['radius'],
            'rotational_period': body['rotationalPeriod'],
            'surface_temperature': body['surfaceTemperature'],
            'earth_masses': body['earthMasses'],
            'is_rotational_period_tidally_locked': body['rotationalPeriodTidallyLocked'],
            'distance_to_arrival': body['distanceToArrival']
        }
    )
print('Adapted missing body data: {}'.format(adapted_missing_body_data))

# merge the lists
adapted_planet_data.extend(adapted_missing_body_data)

print('Dumping data to file')
with open('us_data.json', 'w') as output_file:
    output_file.write(json.dumps(adapted_planet_data))

end_time = time.time()
time = round((end_time - start_time) / 60, 2)
print('Time taken: {} minutes'.format(time))
