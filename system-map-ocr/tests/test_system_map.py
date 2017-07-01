import os

from system_map_parser import SystemMapParser

map_image_path = os.path.join(os.path.dirname(__file__), 'files', 'map.png')


class TestSystemMapParts:
    parser = SystemMapParser(map_image_path)

    def test_system_name(self):
        results = self.parser.parse_system_map()
        assert 'upsilon aguari' == results['name'].lower()
        # assert 'upsilon aquarii' == results['name'].lower()
