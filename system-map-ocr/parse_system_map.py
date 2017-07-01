import os

import pytesseract
from PIL import Image

map_image_path = os.path.join(os.path.dirname(__file__), 'map.png')

map_image = Image.open(map_image_path)


def generate_part_path(part_name):
    return os.path.join(os.path.dirname(__file__), '{}.png'.format(part_name))

sizes = {
    'system_name': {
        'x': 10,
        'y': 192,
        'w': 155,
        'h': 25
    }
}

temporary_image_paths = [generate_part_path(part) for part in sizes.keys()]

# Generate part images
for part, dimensions in sizes.items():
    temp_image_path = generate_part_path(part)
    part_image = map_image.crop(
        (
            dimensions['x'],
            dimensions['y'],
            dimensions['w'] + dimensions['x'],
            dimensions['h'] + dimensions['y']
        )
    )
    part_image.save(temp_image_path)

results = {}

# Parse part images and save results
for part, dimensions in sizes.items():
    text = pytesseract.image_to_string(Image.open(generate_part_path(part)))
    results[part] = text
    print(text)

# Delete the temporary images
for path in temporary_image_paths:
    os.remove(path)
