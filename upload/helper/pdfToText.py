import pytesseract as tess
from PIL import Image

img = Image.open('check3.jpg')
text = tess.image_to_string(img)

word = "Internship"
if word.lower() in text.lower():
    print(word)
else:
    print("Word not found")