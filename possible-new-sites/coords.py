import os
import csv

big_file_path = os.path.join('G:\Downloads Folder\systems.csv')
# big_file_path = os.path.join(os.path.dirname(__file__), 'systems.csv')


def get_line():
    with open(big_file_path, 'r') as big_file:
        reader = csv.reader(big_file)
        for row in reader:
            yield row


def get_coordinates(system_name):
    i = 0
    for line in get_line():
        # skip the header
        if i == 0:
            i += 1
            continue
        system = line[2]
        if system_name == system:
            data = dict(system=system, x=float(line[3]), y=float(line[4]), z=float(line[5]))
            return data
    return None

if __name__ == '__main__':
    coords = get_coordinates('Synuefe ZK-X c17-7')
    print(coords)
