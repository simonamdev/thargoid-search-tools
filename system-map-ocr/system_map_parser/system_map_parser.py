import os

import pytesseract
from PIL import Image

# workaround for tessdata being on a different drive on windows
config_path = 'G:\Program Files (x86)\Tesseract-OCR\\tessdata'
config_args = '--tessdata-dir "{}"'.format(config_path)


class SystemMapParser:
    part_dimensions = {
        'name': {
            'x': 10,
            'y': 192,
            'w': 155,
            'h': 25
        }
    }

    def __init__(self, map_image_path):
        self._map_image_path = map_image_path
        print('Parsing map at: {}'.format(self._map_image_path))
        self._map_image = Image.open(map_image_path)

    def parse_system_map(self):
        # Generate part images
        self.__generate_part_images()
        # Parse part images and get results
        try:
            results = self.__extract_text_from_parts()
        finally:
            # Delete the temporary images
            self.__clean_up_temporary_images()
            pass
        return results

    def __extract_text_from_parts(self):
        results = {}
        for part, dimensions in self.part_dimensions.items():
            text = pytesseract.image_to_string(Image.open(self.__generate_part_path(part)), config=config_args)
            results[part] = text
        return results

    def __generate_part_images(self):
        for part, dimensions in self.part_dimensions.items():
            temp_image_path = self.__generate_part_path(part)
            part_image = self._map_image.crop(
                (
                    dimensions['x'],
                    dimensions['y'],
                    dimensions['w'] + dimensions['x'],
                    dimensions['h'] + dimensions['y']
                )
            )
            part_image.save(temp_image_path)

    def __clean_up_temporary_images(self):
        temporary_image_paths = self.__generate_temporary_image_paths()
        for path in temporary_image_paths:
            os.remove(path)

    def __generate_temporary_image_paths(self):
        return [self.__generate_part_path(part) for part in self.part_dimensions.keys()]

    @staticmethod
    def __generate_part_path(part_name):
        return os.path.join(os.path.dirname(__file__), '{}.png'.format(part_name))
