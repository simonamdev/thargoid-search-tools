import os

import pytesseract
from PIL import Image

map_image_path = os.path.join(os.path.dirname(__file__), 'map.png')
temp_image_path = os.path.join(os.path.dirname(__file__), 'temp.jpg')

img = Image.open(map_image_path)
width, height = img.size
x = 10
y = 725
cropped_img = img.crop(
    (
        x,
        y,
        363 + x,
        164 + y
    )
)
cropped_img.show()
cropped_img.save(temp_image_path)

text = pytesseract.image_to_string(Image.open(temp_image_path))
print(text)
