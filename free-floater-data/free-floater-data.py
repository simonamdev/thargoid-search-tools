import json

file_name = 'free-floater-systems.json'
file_path = 'G:\Dropbox\Personal\Projects\\thargoid-search-tools\\free-floater-data\\{}'.format(file_name)


class FreeFloaterDataParser:
    def __init__(self, path):
        self._path = path
        self._data = None

    def parse_file(self):
        with open(self._path, 'r') as data_file:
            self._data = json.loads(data_file.read())

    def get_data(self):
        return self._data

if __name__ == '__main__':
    parser = FreeFloaterDataParser(path=file_path)
    parser.parse_file()
    print(parser.get_data())
