# Get the required system names
import csv
import json
import os
import time

start_time = time.time()

required_systems = []
with open('us_bodies.txt', 'r') as us_bodies:
    for line in us_bodies:
        required_systems.append(line.strip().lower())
print(required_systems)

system_count_required = len(required_systems)

# Find out how many of them are present in the system data

systems_file_path = os.path.join(os.path.dirname(__file__), 'systems.csv')


def get_system_line():
    with open(systems_file_path, 'r') as big_file:
        reader = csv.reader(big_file)
        for row in reader:
            yield row

# Get their respective IDs

system_ids = {}

print('Retrieving System data')
header_passed = False
for system in get_system_line():
    # skip the first line, which is the header
    if not header_passed:
        header_passed = True
        continue
    if system[2].lower() in required_systems:
        # print('{} found'.format(system[2]))
        system_ids[system[2]] = int(system[0])
        continue
    if len(list(system_ids.keys())) == system_count_required:
        break

print(system_ids)
print('{}/{} IDs found'.format(len(list(system_ids.keys())), system_count_required))

missing_systems = [
    system for system in required_systems if system not in [
        found_system.lower() for found_system in system_ids.keys()
    ]
]

print('Missing systems: {}'.format(missing_systems))

print('Retrieving required planets')
required_planets = []
with open('planets.txt', 'r') as us_planets:
    for line in us_planets:
        required_planets.append(line.strip().lower())

# append the planets to the system names. Order is preserved
required_planets = ['{} {}'.format(data[0], data[1]) for data in zip(required_systems, required_planets)]


bodies_file_path = os.path.join(os.path.dirname(__file__), 'bodies.jsonl')


def get_body_line():
    with open(bodies_file_path, 'r') as big_file:
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
    if line['name'].lower() in required_planets:
        planet_data.append(line)
    if len(planet_data) == system_count_required:
        break

print(planet_data)
print('{}/{} Planets retrieved'.format(len(planet_data), system_count_required))


end_time = time.time()
time = round((end_time - start_time) / 60, 2)
print('Time taken: {} minutes'.format(time)
