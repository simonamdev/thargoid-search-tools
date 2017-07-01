import os

import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

map_image_path = os.path.join(os.path.dirname(__file__), 'map.png')
temp_image_path = os.path.join(os.path.dirname(__file__), 'temp.jpg')

im = Image.open(map_image_path)
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
im.save(temp_image_path)
text = pytesseract.image_to_string(Image.open(temp_image_path))
print(text)
